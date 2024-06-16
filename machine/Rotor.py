import json
from src.supply.PathsManager import PathsManager


class RotorException(Exception):
    pass


class RotorInvalidArgumentException(RotorException):
    def __init__(self, msg: str, argument_given, argument_expected):
        super().__init__(msg)
        self.argument_given = argument_given
        self.argument_expected = argument_expected


class RotorInvalidFileException(RotorException):
    def __init__(self, msg: str, path: str):
        super().__init__(msg)
        self.path = path


class Rotor:
    def __init__(self, position: int, kind: str, ringposition: int):
        """
        This method initialises a new Rotor-Object and sets its base values.
        It also validates the params and raises RotorInvalidArgumentExceptions.
        :param position:
        :param kind:
        :param ringposition:
        """
        with open(PathsManager().getPath(PathsManager.SUPER_ID.index("Rotor"), PathsManager.ID.index("Rotor.json")),
                  "r") as js:
            f = json.load(js)
        self._types = f["kinds"]
        del f

        # Argument validation
        if not (1 <= ringposition <= 26) or not isinstance(ringposition, int):
            raise RotorInvalidArgumentException("Ringposition needs to be an integer in the range 1 <= n <= 26!",
                                                ringposition, range(1, 27))
        if kind not in (self._types.keys()):
            raise RotorInvalidArgumentException("Types needs to be a roman letter between I and VII. use i for I."
                                                " use v for V.", kind, self._types)
        if position not in [1, 2, 3]:
            raise RotorInvalidArgumentException("Position needs to be in the list of 1, 2, 3.", position,
                                                [1, 2, 3])

        # Set basic attributes
        self._position = position
        self._type = kind
        self._ringposition = ringposition
        self._turn = 0
        self._table = {int(k): v for k, v in self._types[kind].items()}
        self._inverse_table = {v: int(k) for k, v in self._types[kind].items()}
        self._input = [position, kind, ringposition]

    def _increase_clear(self, clear: int) -> int:
        """
        This method increases clear text, which is represented as an int with the range 1 <= n <= 26, based on the
        self._turn and self._position.
        :param clear:
        :return increased clear:
        """
        t = 0
        if self._position == 1:
            t = self._turn % 26
        elif self._position == 2:
            t = self._turn // 25
            t = t % 26
        elif self._position == 3:
            t = self._turn // (25 * 25)
            t = t % 26
        clear += t
        if clear > 26:
            clear -= 26
        if clear == 0:
            clear = 1
        return clear

    def _decrease_encoded(self, encoded: int) -> int:
        """
        This method decreases encoded text, which is represented as an int with the range 1 <= n <= 26, based on the
        self._turn and self._position.
        :param encoded:
        :return increased clear:
        """
        t = 0
        if self._position == 1:
            t = self._turn % 26
        elif self._position == 2:
            t = self._turn // 25
            t = t % 26
        elif self._position == 3:
            t = self._turn // (25 * 25)
            t = t % 26
        encoded -= t
        if encoded < 0:
            encoded = 26 + encoded
        if encoded == 0:
            encoded = 26
        return encoded

    def copy(self):
        """
        This method allows for a copy of the object.
        :return:
        """
        return Rotor(self._input[0], self._input[1], self._input[2])

    def permutate(self, clear: int) -> int:
        """
        This method encodes clear text which is represented as an int with the range 1 <= n <= 26, based on the in
        __init__ set rotor specifications.
        It also validates the params and raises RotorInvalidArgumentExceptions.
        :param clear:
        :return encodedTxt:
        """
        # Argument validation
        if not (1 <= clear <= 26):
            raise RotorInvalidArgumentException("The clear text must be an integer in the range 1 <= n <= 26!",
                                                clear, range(1, 27))

        # increase clear based on turns
        clear = self._increase_clear(clear)

        # uses the self._table corresponding to the rotor kind to encode clear
        encodedTxt = self._table[clear]
        encodedTxt = self._decrease_encoded(encodedTxt)
        return encodedTxt

    def inverse_permutate(self, clear: int) -> int:
        """
        This method encodes clear text which is represented as an int with the range 1 <= n <= 26, based on the in
        __init__ set rotor specifications. However, unlike permutate this method uses self_inverse_table.
        It also validates the params and raises RotorInvalidArgumentExceptions.
        :param clear:
        :return encodedTxt:
        """
        # Argument validation
        if not (1 <= clear <= 26):
            raise RotorInvalidArgumentException("The clear text must be an integer in the range 1 <= n <= 26!",
                                                clear, range(1, 27))

        # increase clear based on turns
        clear = self._increase_clear(clear)

        # uses the self._inverse_table corresponding to the rotor kind to encode clear
        encodedTxt = self._inverse_table[clear]
        encodedTxt = self._decrease_encoded(encodedTxt)
        return encodedTxt

    def next_turn(self):
        """
        This method increases self._turn
        :return:
        """
        self._turn += 1

    def set_turn(self, turn: int):
        self._turn = turn

    def get_position(self):
        return self._position

    def __str__(self):
        return f"position: {self._position}; kind: {self._type}; ringposition: {self._ringposition}; turn: {self._turn}"
