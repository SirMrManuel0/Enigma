import json
from supply.PathsManager import PathsManager


class ReflectorException(Exception):
    pass


class ReflectorInvalidArgumentException(ReflectorException):
    def __init__(self, msg: str, argument_given, argument_expected):
        super().__init__(msg)
        self.argument_given = argument_given
        self.argument_expected = argument_expected


class Reflector:
    def __init__(self, kind: str):
        """
        This method initialises a new Reflector-Object and sets its base values.
        It also validates the params and raises ReflectorInvalidArgumentException.
        :param kind:
        """
        # Argument validation
        kind = kind.upper()
        if kind not in ["B", "C"]:
            raise ReflectorInvalidArgumentException("The kind of the reflector has to be in the list ['B', 'C']",
                                                    kind, ["B", "C"])

        # set self._table with data from a json
        with open(PathsManager().getPath(PathsManager.SUPER_ID.index("Reflector"),
                                         PathsManager.ID.index("Reflector.json"))) as js:
            self._table = json.load(js)["kinds"][kind]
        self._table = {int(k): v for k, v in self._table.items()}
        self._type = kind

    def permutate(self, clear: int) -> int:
        """
        This method encodes clear text which is represented as an int with the range 1 <= n <= 26, based on the in
        __init__ set reflector specifications.
        It also validates the params and raises ReflectorInvalidArgumentException.
        :param clear:
        :return:
        """
        # Argument validation
        if not (1 <= clear <= 26):
            raise ReflectorInvalidArgumentException("The clear text must be an integer in the range 1 <= n <= 26!",
                                                    clear, range(1, 27))

        # uses the self._table corresponding to the reflector kind to encode clear
        encodedTxt = self._table[clear]
        return encodedTxt

    def __str__(self):
        return f"kind: {self._type}"
