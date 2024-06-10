from src.machine.Rotor import Rotor
from src.machine.Reflector import Reflector
from src.machine.Enigma import Enigma
from src.machine.Enigma import EnigmaInvalidArgumentException

enigma = Enigma(Rotor(1, "I", 1), Rotor(2, "II", 1), Rotor(3, "III", 1))
#print(enigma.input_chr("A", False))
#print(enigma.input_chr("J", False))
#print(enigma.input_chr("A"), enigma.input_chr("B"))
#print(enigma.encrypt_wrapper("Z Z"))
#enigma.reset()
#print(enigma.input_str("YSV"))
#print(enigma.input_chr("N"), enigma.input_chr("W"))
#enigma.reset()
#time, length, beta_code, alpha_code, call_sign, message = enigma.decrypt_wrapper("2113 - 8 - EEE LGD - LLAWL YSV")
#print(beta_code)
#print(alpha_code)
#print(message)
print(enigma)
#print(enigma.input_str("HELLO", False))
#print(enigma.input_str("KCCIH"))
