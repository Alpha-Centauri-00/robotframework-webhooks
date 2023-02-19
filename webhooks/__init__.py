from enum import IntEnum
from os import path
from slack_sdk.webhook import WebhookClient
from robot.errors import VariableError
from robot.libraries.BuiltIn import BuiltIn
import pymsteams
from robot.utils.error import get_error_message


__version__ = "0.1.1"


data = {
    "url": "Your Channel webhook url (Slack or MS-Teams)",
    
    "title":"Robot Framework Results: ",

    "icon":"https://upload.wikimedia.org/wikipedia/commons/e/e4/Robot-framework-logo.png?20180323153902",

    "fail":"<span  style='background-color: #ce3e01; color: #fff;border-radius: 3px;font-family: Helvetica, sans-serif;font-weight: bold;padding:2px 5px;'>FAIL</span>",

    "doco": "Documentation",

    "docu_info": "This is Documentation infos!!",

    "button_name": "e.g. github",

    "button_link":"https://github.com/"
    }


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
    def __init__(
        self, file, source, lineno, name, args=None, kind: Kind = Kind.Keyword
    ):
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
        self.errormessage = ""
        self.mutings = []
        self.lib_files = {}

    def start_suite(self, name, attrs):
        self.SuiteTrace.append(attrs["source"])

    def library_import(self, name, attrs):
        self.lib_files[name] = attrs.get("source")

    def resource_import(self, name, attrs):
        self.lib_files[name] = attrs.get("source")

    def start_test(self, name, attrs):
        self.StackTrace = [
            StackElement(
                self.SuiteTrace[-1],
                self.SuiteTrace[-1],
                attrs["lineno"],
                name,
                kind=Kind.Test,
            )
        ]

    def start_keyword(self, name, attrs):
        source = attrs.get(
            "source",
            self.StackTrace[-1].file if self.StackTrace else self.SuiteTrace[-1],
        )
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
        if (
            source
            and path.isdir(source)
            and path.isfile(path.join(source, "__init__.robot"))
        ):
            return path.join(source, "__init__.robot")
        else:
            return source

    def end_keyword(self, name, attrs):
        if self.mutings and attrs["kwname"] == self.mutings[-1]:
            self.mutings.pop()
        if attrs["status"] == "FAIL" and self.new_error and not self.mutings:
            error_text = "\n".join(self._create_stacktrace_text())
            if "slack" in data["url"]:
                self._send_slack(error_text=error_text)
            else:
                self._send_teams(error_text=error_text)
        self.StackTrace.pop()
        self.new_error = False


    def _send_slack(self,error_text):
        webhook = WebhookClient(data["url"])
        _path = self._get_testPath()
        
        response = webhook.send(
            text="fallback",
            blocks=[
            
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f">{data['title']}"
                        }
                    },
                    {
                        "type": "section",
                        "block_id": "section567",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"```{error_text}```"
                        },
                    
                        "accessory": {
                            "type": "image",
                            "image_url": f"{data['icon']}",
                            "alt_text": "Haunted hotel image"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Path: {_path}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Documentation: {data['docu_info']}",
                            
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{'-'*105}",
                            
                        }
                    }
                ]
        )


    def _send_teams(self,error_text):
        myTeamsMessage = pymsteams.connectorcard(data["url"])
        myTeamsMessage.title(data["title"])
        myTeamsMessage.text(data["fail"])

        myTeamsMessage.color("#eb0c33")
        section1 = pymsteams.cardsection()
        section1.activityImage(data["icon"])
        section1.activityText(f'<div  style="border: 1px solid #eb0c33; padding: 12px;font-weight:bold";>{error_text}</div>')
        _path = self._get_testPath()
        section1.addFact("Path: ", f"{_path}")
        section1.addFact(data["doco"], data["docu_info"])
        section1.linkButton(data["button_name"],data["button_link"])
        myTeamsMessage.addSection(section1)
        myTeamsMessage.send()


    def _create_stacktrace_text(self) -> str:      
        error_text = [f""]
        error_text += [f"Traceback (most recent call last):"]
        call: StackElement
        for index, call in enumerate(self.StackTrace):
            if call.kind >= Kind.Test:
                error_text += [f"{call.name} {call.args}"]

        new_list = [string.replace("[]","") for string in error_text]

        orig_error = [string.strip() for string in new_list if string.strip() != '']
        add_new_line = [string + '\n' for string in orig_error]
        final_error = [string.replace("'"," ") for string in add_new_line]
        
        adding_error_message = "Error is: " + get_error_message()

        final_error.append(adding_error_message)
        return final_error


    def _get_testPath(self) -> str:
        path_text = "  "
        call: StackElement
        for index, call in enumerate(self.StackTrace):
            if call.kind >= Kind.Test:
                
                path = f"{call.source}"
        path_text += path
        return path_text
