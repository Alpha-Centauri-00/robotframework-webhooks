from enum import IntEnum
from os import path

from robot.errors import VariableError
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import cut_long_message
import pymsteams

# After you added an Incoming Webhook App in your Channel, you'll get a new URL and 
# it should replace it in here!
Web_Hook = "PASTE YOUR URL IN HERE"


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
            text = "\n".join(self._create_stacktrace_text())
            myTeamsMessage = pymsteams.connectorcard(Web_Hook)
            myTeamsMessage.title("Robot Framework Results:")

            myTeamsMessage.text("text")

            myTeamsMessage.color("#eb0c33")
            section1 = pymsteams.cardsection()
            section1.text(text)
            myTeamsMessage.addSection(section1)
                        
            myTeamsMessage.send()
            print("\n".join(self._create_stacktrace_text()))

        self.StackTrace.pop()
        self.new_error = False

    def _create_stacktrace_text(self) -> str:
        error_text = [f"  "]
        error_text += ["  Traceback (most recent call last):\n"]
        call: StackElement
        for index, call in enumerate(self.StackTrace):
            if call.kind >= Kind.Test:
                kind = "  Test case Name:" if call.kind == Kind.Test else ""
                path = f"{call.source}"
                error_text += [
                    f'    {kind}  {call.name}  {"    ".join(call.args or [])}'
                ]
        error_text += [f"      File  {path}"]
        error_text += [f'{"_" * 78}']
        return error_text
