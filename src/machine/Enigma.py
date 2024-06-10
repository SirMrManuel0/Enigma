from datetime import datetime
import random
import string
from typing import Tuple

from src.machine.Rotor import Rotor
from src.machine.Reflector import Reflector


class EnigmaException(Exception):
    pass


class EnigmaInvalidArgumentException(EnigmaException):
    def __init__(self, msg: str, argument_given, argument_expected):
        super().__init__(msg)
        self.argument_given = argument_given
        self.argument_expected = argument_expected


class EnigmaDataCorruptionException(EnigmaException):
    def __init__(self, msg: str, data_given, data_expected):
        super().__init__(msg)
        self.data_given = data_given
        self.data_expected = data_expected


class Enigma:
    def __init__(self,
                 rotor1: Rotor, rotor2: Rotor, rotor3: Rotor,
                 reflector: Reflector = Reflector("B"),
                 plugboard: dict = {}):
        """
        This method initialises a new Enigma-Object and sets its base values.
        It also validates the params and raises EnigmaInvalidArgumentException.
        The plugboard must fulfill {k: v, v: k}; k and v must be integer in the range 1 <= n <= 26
        rotor1 must be at position = 1
        rotor2 must be at position = 2
        rotor3 must be at position = 3
        :param rotor1:
        :param rotor2:
        :param rotor3:
        :param reflector:
        :param plugboard:
        """

        # Argument validation
        if rotor1 is None:
            raise EnigmaInvalidArgumentException("rotor1 cannot be None",
                                                 rotor1, Rotor(1, "I", 1))
        if rotor2 is None:
            raise EnigmaInvalidArgumentException("rotor2 cannot be None",
                                                 rotor2, Rotor(2, "I", 1))
        if rotor3 is None:
            raise EnigmaInvalidArgumentException("rotor3 cannot be None",
                                                 rotor3, Rotor(3, "I", 1))
        if reflector is None:
            raise EnigmaInvalidArgumentException("reflector cannot be None",
                                                 reflector, Reflector("B"))
        if plugboard is None:
            raise EnigmaInvalidArgumentException("plugboard cannot be None",
                                                 plugboard, {})

        if rotor1.get_position() != 1:
            raise EnigmaInvalidArgumentException("rotor1 needs to be at position 1!", rotor1,
                                                 Rotor(1, "I", 1))
        if rotor2.get_position() != 2:
            raise EnigmaInvalidArgumentException("rotor2 needs to be at position 2!", rotor1,
                                                 Rotor(2, "I", 1))
        if rotor3.get_position() != 3:
            raise EnigmaInvalidArgumentException("rotor3 needs to be at position 3!", rotor1,
                                                 Rotor(3, "I", 1))

        # make sure plugboard:
        # fulfills {k: v, v: k}
        # consists of integers only
        # all integer are in the range 1 <= n <= 26
        plugCopy = {}
        for k, v in plugboard.items():
            plugCopy[k] = v
            plugCopy[v] = k
            if not isinstance(k, int) or not (1 <= k <= 26):
                raise EnigmaInvalidArgumentException("All keys in the plugboard must be integer"
                                                     " in the range 1 <= k <= 26!", k, range(1, 27))
            if not isinstance(v, int) or not (1 <= v <= 26):
                raise EnigmaInvalidArgumentException("All values in the plugboard must be integer"
                                                     " in the range 1 <= v <= 26!", v, range(1, 27))

        for k, v in plugCopy.items():
            if plugCopy[v] != k:
                raise EnigmaInvalidArgumentException("The plugboard must fulfill {k: v, v: k}",
                                                     {k: v, v: plugCopy[v]}, {k: v, v: k})

        # set self._ values
        self._rotor1 = rotor1
        self._rotor2 = rotor2
        self._rotor3 = rotor3
        self._reflector = reflector
        self._plugboard = plugCopy
        self._table = {
            "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10, "K": 11, "L": 12, "M": 13,
            "N": 14, "O": 15, "P": 16, "Q": 17, "R": 18, "S": 19, "T": 20, "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25,
            "Z": 26
        }
        self._inverse_table = {
            1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M",
            14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V", 23: "W", 24: "X", 25: "Y",
            26: "Z"
        }
        self._code = None

    def reset(self):
        """
        This method puts the rotors back to their original states.
        :return:
        """
        self._rotor1.set_turn(0)
        self._rotor2.set_turn(0)
        self._rotor3.set_turn(0)

    def input_chr(self, character: str, continuos: bool = True) -> str:
        """
        This method encrypts or decrypts a char represented as a str.
        The character must be an english uppercase letter.
        It also validates the params and raises EnigmaInvalidArgumentException.
        :param character:
        :param continuos:
        :return:
        """
        # Argument validation
        if len(character) != 1:
            raise EnigmaInvalidArgumentException("character is expected to be of len 1!", character, "A")
        if character not in self._table.keys():
            raise EnigmaInvalidArgumentException("character is expected to be a english uppercase letter!",
                                                 character, self._table.keys())

        if character in self._plugboard.keys():
            character = self._plugboard[character]

        encrypted = self._table[character]
        encrypted = self._rotor1.permutate(encrypted)
        encrypted = self._rotor2.permutate(encrypted)
        encrypted = self._rotor3.permutate(encrypted)
        encrypted = self._reflector.permutate(encrypted)
        encrypted = self._rotor3.inverse_permutate(encrypted)
        encrypted = self._rotor2.inverse_permutate(encrypted)
        encrypted = self._rotor1.inverse_permutate(encrypted)
        encrypted = self._inverse_table[encrypted]

        if encrypted in self._plugboard.keys():
            encrypted = self._plugboard[encrypted]

        if continuos:
            self._rotor1.next_turn()
            self._rotor2.next_turn()
            self._rotor3.next_turn()
        return encrypted

    def input_str(self, message: str, continuos: bool = True) -> str:
        """
        This method encrypts or decrypts a string.
        The string must consist of english uppercase letters only.
        It also validates the params and raises EnigmaInvalidArgumentException.
        :param message:
        :param continuos:
        :return:
        """
        # Argument validation
        if len(message) == 0:
            raise EnigmaInvalidArgumentException("The string must have a length!", message, "A")
        if any([True for c in message if c not in self._table.keys()]):
            raise EnigmaInvalidArgumentException("The string must consist of only english uppercase letters!",
                                                 message, "AAA")

        # put each character into input_chr
        output = ""
        for c in message:
            output += self.input_chr(c)
        if not continuos:
            self.reset()
            if self._code is not None:
                self.set_code(self._code)
        return output

    def set_code(self, code: list[int]):
        """
        This method sets the code for the enigma.
        It also validates the params and raises EnigmaInvalidArgumentException.
        :param code:
        :return:
        """
        # Argument validation
        if len(code) != 3 or any([True for n in code if not isinstance(n, int)]):
            raise EnigmaInvalidArgumentException("The code must be a list of three integer!", code,
                                                 [1, 1, 1])
        for i, v in enumerate(code):
            if not (1 <= v <= 26):
                raise EnigmaInvalidArgumentException("All elements in the code must be in the range 1 <= n <= 26! The "
                                                     "element at the index " + str(i) + " was not!", code[i],
                                                     range(1, 27))

        # set the turns of the rotors based on the code
        self._code = code.copy()
        self._rotor1.set_turn(code[2] - 1)
        self._rotor2.set_turn((code[1] - 1) * 26)
        self._rotor3.set_turn((code[0] - 1) * 26 * 26)

    def encrypt_wrapper(self, message: str, hide_code: list[int] = [5, 5, 5]) -> str:
        """
        This method encrypts a message according to the regulation, which applied to the german army in WW2.
        It also validates params and raises EnigmaInvalidArgumentException.
        The message can only consist of english uppercase letters and space ' '.
        All numbers must be written out. (e.g. 4 -> four)
        The hide_code is a secondary code, which is used to encrypt the original code. default is [5, 5, 5]
        :param message:
        :param hide_code:
        :return encrypted_message:
        """
        message = message.replace(",", "")
        message = message.replace(".", "")
        message = message.replace(";", "")
        message = message.replace(":", "")
        message = message.replace("'", "")
        message = message.replace('"', "")

        # Argument validation
        if any([True for c in message if c not in self._table.keys() and c != " "]):
            raise EnigmaInvalidArgumentException("The string can only consist of english upper case letters or ' '",
                                                 message, self._table.keys())
        if len(hide_code) != 3 or any([True for n in hide_code if not isinstance(n, int)]):
            raise EnigmaInvalidArgumentException("The code must be a list of three integer!", hide_code,
                                                 [1, 1, 1])
        for i, v in enumerate(hide_code):
            if not (1 <= v <= 26):
                raise EnigmaInvalidArgumentException("All elements in the code must be in the range 1 <= n <= 26! The "
                                                     "element at the index " + str(i) + " was not!", hide_code[i],
                                                     range(1, 27))

        # change string according to the regulation for the german army in WW2
        # replace ' ' with X
        message = [c for c in message]
        for i, c in enumerate(message):
            if c == " ":
                message[i] = "X"
        s = "".join(message)

        # replace CH with Q
        while s.find("CH") >= 0:
            i = s.find("CH")
            message[i] = "Q"
            message.pop(i + 1)
            s = "".join(message)

        # replace CK with Q
        while s.find("CK") >= 0:
            i = s.find("CK")
            message[i] = "Q"
            message.pop(i + 1)
            s = "".join(message)

        # encrypt
        message = self.input_str(s)

        # get the time and set it into the right format HHMM
        now = datetime.now()
        current_time = now.strftime("%H%M")

        # create a code to hide the real code
        alpha_code = ["A", "A", "A"]
        if self._code is not None:
            alpha_code = [self._inverse_table[c] for c in self._code]
        beta_code = [self._inverse_table[c] for c in hide_code]
        self.reset()
        self.set_code(hide_code)
        temp = []
        for c in alpha_code:
            temp.append(self.input_chr(c))
        alpha_code = temp.copy()
        del temp

        # add 5 random letters | regulation usually say the last three of these need to be a call sign, but ... I don't
        # create the call signs so for me these are just 5 random letters
        random_letters = ''.join(random.choices(string.ascii_uppercase, k=5))

        body = random_letters + message
        header = f"{current_time} - {len(body)} - {"".join(beta_code)} {"".join(alpha_code)} - "

        # create groups of 5
        body = ' '.join([body[i:i + 5] for i in range(0, len(body), 5)])

        # add header and body
        body = header + body

        return body

    def decrypt_wrapper(self, message: str) -> tuple[str, str, str, str, str, str]:
        """
        This method decrypts a message according to the regulation, which applied to the german army in WW2.
        It also validates params and raises EnigmaInvalidArgumentException and EnigmaDataCorruptionException.
        The message should be from encrypt_wrapper to be safe. You can also obviously replicate the format, but that is
        not recommended.
        :param message:
        :return:
        """
        # Argument valdation
        if len(message) < 26:
            raise EnigmaInvalidArgumentException("Only messages which were encrypted adhering to the regulations from "
                                                 "encrypt_wrapper can be decrypted with this method!",
                                                 message, "2044 - 8 - EEE OVN - KRHAG YSV")

        if any([True for c in message[22:] if c not in self._table.keys() and c != " "]):
            raise EnigmaInvalidArgumentException("All characters after the encryption header must be either a "
                                                 "whitespace ' ' or an english uppercase letter!",
                                                 message, self._table.keys())

        # splitting header from the message
        message = message.split(" ")
        time = message[0]
        length = message[2]
        beta_code = message[4]
        alpha_code = message[5]
        call_sign = message[7][2:]
        for i in range(8):
            message.pop(0)

        message = "".join(message)

        # validating codes and setting alpha code to self._code
        if any([True for c in beta_code if c not in self._table.keys()]):
            raise EnigmaDataCorruptionException("The beta code is corrupted! Only uppercase english letters were "
                                                "expected!", beta_code, self._table.keys())

        if any([True for c in alpha_code if c not in self._table.keys()]):
            raise EnigmaDataCorruptionException("The alpha code is corrupted! Only uppercase english letters were "
                                                "expected!", alpha_code, self._table.keys())

        beta_code = [self._table[c] for c in beta_code]

        self.reset()
        self.set_code(beta_code)
        temp = []
        for c in alpha_code:
            temp.append(self.input_chr(c))
        alpha_code = temp.copy()
        del temp
        alpha_code = [self._table[c] for c in alpha_code]

        self.reset()
        self.set_code(alpha_code)
        message = self.input_str(message)

        self.reset()

        if len(message) + len(call_sign) + 2 != int(length):
            raise EnigmaDataCorruptionException("The length of the message and call sign does not match the"
                                                " expected length! Part of the message got lost!",
                                                {"len(message)": len(message), "len(call_sign)": len(call_sign)},
                                                length)

        beta_code = str("".join([self._inverse_table[c] for c in beta_code]))
        alpha_code = str("".join([self._inverse_table[c] for c in alpha_code]))

        return time, length, beta_code, alpha_code, call_sign, message

    def __str__(self):
        return f"Rotor 1: {self._rotor1}\nRotor 2: {self._rotor2}\nRotor 3: {self._rotor3}\nReflector: {self._reflector}\n" \
               f"code: {self._code}\nplugboard: {self._plugboard}"
