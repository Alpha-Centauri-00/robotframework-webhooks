import toml
import requests
from os import path
from enum import IntEnum
from datetime import datetime
from robot.errors import VariableError
from robot.libraries.BuiltIn import BuiltIn
from robot.utils.error import get_error_message


__version__ = "1.0.6"

bi = BuiltIn()
muting_keywords = [
    "Run Keyword And Ignore Error",
    "Run Keyword And Expect Error",
    "Run Keyword And Return Status",
    "Run Keyword And Warn On Failure",
    "Wait Until Keyword Succeeds",
]

class Kind(IntEnum):
    Suite = 0
    Test = 1
    Keyword = 2

class StackElement:
    def __init__(self, file, source, lineno, name, args=None, kind: Kind = Kind.Keyword):
        self.file = file
        self.source = source
        self.lineno = lineno
        self.name = name
        self.args = args or []
        self.kind = kind

    def resolve_args(self):
        for arg in self.args:
            try:
                resolved = bi.replace_variables(arg)
                if resolved != arg:
                    yield str(arg), f"{resolved} ({type(resolved).__name__})"
            except VariableError:
                yield str(arg), "<Unable to define variable value>"

class webhooks:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.StackTrace = []
        self.SuiteTrace = []
        self.new_error = True
        self.errormessage = []
        self.mutings = []
        self.lib_files = {}
        self.data_json = {}
        self.date = None
                
        self.config = toml.load("robot.toml")

    def start_suite(self, name, attrs):
        self.SuiteTrace.append(attrs["source"])

    def library_import(self, name, attrs):
        self.lib_files[name] = attrs.get("source")

    def resource_import(self, name, attrs):
        self.lib_files[name] = attrs.get("source")
    
    def start_test(self, name, attrs):
        
        self.date = datetime.strptime(attrs["starttime"], "%Y%m%d %H:%M:%S.%f").strftime("%d-%m-%Y")
        self.StackTrace = [
            StackElement(
                self.SuiteTrace[-1],
                self.SuiteTrace[-1],
                attrs["lineno"],
                name,
                kind=Kind.Test,
            )
        ]
        self.errormessage = []
    
    def start_keyword(self, name, attrs):
        source = attrs.get("source", self.StackTrace[-1].file if self.StackTrace else self.SuiteTrace[-1])
        file = self.lib_files.get(attrs.get("libname"), source)

        self.StackTrace.append(
            StackElement(
                file,
                self.fix_source(source),
                attrs.get("lineno", None),
                attrs["kwname"],
                attrs["args"],
            )
        )
        if attrs["kwname"] in muting_keywords:
            self.mutings.append(attrs["kwname"])
        self.new_error = True

    def fix_source(self, source):
        if source and path.isdir(source) and path.isfile(path.join(source, "__init__.robot")):
            return path.join(source, "__init__.robot")
        else:
            return source

    def end_keyword(self, name, attrs):
        if self.mutings and attrs["kwname"] == self.mutings[-1]:
            self.mutings.pop()
        if attrs["status"] == "FAIL" and self.new_error and not self.mutings:
            self.errormessage.append(get_error_message())
            self._send_teams()  # Ensure the message is sent immediately on failure
        self.StackTrace.pop()
        self.new_error = False

    def _send_teams(self):
        profile_image = self.config['variables'].get('profileImage', "")
        webhook_url = self.config['variables'].get('webhook_url', "")
        if not webhook_url:
            print("No webhook URL configured.")
            return
        self.data_json = {
            "title": "Robot Framework Test Failed",
            "description": "Error Message:\n" + "\n".join(self.errormessage),
            "creator": {
                "name": "Robot Framework",
                "profileImage": profile_image
            },
            "Status": "FAIL",
            "viewUrl": "https://adaptivecards.io",
            "properties": [
                {"key": "Suite: ", "value": self.SuiteTrace[-1] if self.SuiteTrace else "Unknown"},
                {"key": "Name: ", "value": self.StackTrace[0].name if self.StackTrace else "Unknown"},
                {"key": "Date: ", "value": f"{self.date}"}                
            ]
        }

        try:
            response = requests.post(webhook_url, json=self._create_card_payload())
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"Error: {error}")

    def _create_card_payload(self) -> dict:
        # Initialize the payload structure
        self.formatted_Card_Payload = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.2",
                        # Define the main body of the card
                        "body": [
                            # Title Section
                            {
                                "type": "TextBlock",
                                "size": "Medium",
                                "weight": "Bolder",
                                "text": self.data_json["title"],
                                "wrap": True
                            },
                            # Creator and Status Section
                            {
                                "type": "ColumnSet",
                                "columns": [
                                    {
                                        "type": "Column",
                                        "width": "auto",
                                        "items": [
                                            {
                                                "type": "Image",
                                                "url": self.data_json["creator"]["profileImage"],
                                                "size": "Medium",  # Adjusted to "Medium" for a larger image
                                                "style": "Person"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "Column",
                                        "width": "stretch",
                                        "items": [
                                            {
                                                "type": "TextBlock",
                                                "text": self.data_json["creator"]["name"],
                                                "weight": "Bolder",
                                                "wrap": True
                                            },
                                            {
                                                "type": "ColumnSet",
                                                "columns": [
                                                    {
                                                        "type": "Column",
                                                        "width": "auto",
                                                        "items": [
                                                            {
                                                                "type": "TextBlock",
                                                                "text": "Status:",
                                                                "weight": "Bolder",
                                                                "wrap": True,
                                                                "spacing": "Small"  # Reduced spacing
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "type": "Column",
                                                        "width": "auto",
                                                        "items": [
                                                            {
                                                                "type": "TextBlock",
                                                                "text": "FAIL",
                                                                "color": "default",
                                                                "weight": "Bolder",
                                                                "wrap": True,
                                                                "size": "Medium",
                                                                "spacing": "None"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            # Facts Section
                            {
                                "type": "FactSet",
                                "facts": [
                                    {"title": fact["key"] + ":", "value": fact["value"]}
                                    for fact in self.data_json["properties"]
                                ]
                            },
                            # Error Message Section with Border
                            {
                                "type": "Container",
                                "style": "attention",  # Sets a red background
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "Error Message:",
                                        "weight": "Bolder",
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": self.data_json["description"],
                                        "wrap": True,
                                        "spacing": "Small"
                                    }
                                ],
                                "bleed": True,
                                "separator": True,
                                "spacing": "Medium",
                                "padding": {
                                    "top": "small",
                                    "bottom": "small",
                                    "left": "small",
                                    "right": "small"
                                }
                            }
                        ]
                    }
                }
            ]
        }
        # Return the final payload
        return self.formatted_Card_Payload


