import json
from src.supply.PathsManager import PathsManager


class ReflectorException(Exception):
    pass


class ReflectorInvalidArgumentException(ReflectorException):
    def __init__(self, msg: str, argument_given, argument_expected):
        super().__init__(msg)
        self.argument_given = argument_given
        self.argument_expected = argument_expected


class Reflector:
    def __init__(self, kind: str):
        # Argument validation
        kind = kind.upper()
        if kind not in ["B", "C"]:
            raise ReflectorInvalidArgumentException("The kind of the reflector has to be in the list ['B', 'C']",
                                                    kind, ["B", "C"])

        # set self._table with data from a json
        with open(PathsManager().getPath(PathsManager.SUPER_ID.index("Reflector"),
                                         PathsManager.ID.index("Reflector.json"))) as js:
            self._table = json.load(js)["kinds"][kind]

    def permutate(self, clear: int) -> int:
        # Argument validation
        if not (1 <= clear <= 26):
            raise ReflectorInvalidArgumentException("The clear text must be an integer in the range 1 <= n <= 26!",
                                                    clear, range(1, 27))

        # uses the self._table corresponding to the reflector kind to encode clear
        encodedTxt = self._table[clear]
        return encodedTxt
