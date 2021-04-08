import os
import sys
from cryptocode import encrypt, decrypt

cyphertext = sys.argv[1]
password = sys.argv[2]

myDecryptedMessage = decrypt(cyphertext, password)

print(myDecryptedMessage)

cyphertext = encrypt(myDecryptedMessage, password)

print(cyphertext)
