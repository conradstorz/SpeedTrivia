import os
import sys
from cryptocode import encrypt, decrypt

data = sys.argv[1]
password = sys.argv[2]

cyphertext = encrypt(data, password)

print(cyphertext)


myDecryptedMessage = decrypt(cyphertext, password)

print(myDecryptedMessage)
