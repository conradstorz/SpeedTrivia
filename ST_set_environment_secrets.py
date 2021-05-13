"""Decrypt tokens and secrets with user supplied password then inject values into environment.
"""

import os
import sys
from cryptocode import decrypt

# Find these values at https://twilio.com/user/account
# Encrypt with ST_encrypt_data.py using a secure password and place result here.
# Running ST_set_environment_secrets.py will set environment variables to original value with user provided correct password.
encrypted_account_sid = "vWFFuntfUAPQe/FTupv1OXV8AXWG5AaG8fzQp2ecunL7HA==*lmK4CGQhJTdlnZIJiVFmvQ==*DBCDTrmMz+oWPxgizpVkAA==*kaO0xIle1JPlQFS8syKmwQ=="
encrypted_auth_token = "LJ0ctrM7RN1N7JS2tIm5hvfVX+F85RQmb8pXpyxYE+g=*Z5nguaX60YPaM7zs2r//Ew==*EMZDFrrPZfZsWVoehWZEug==*33yCyWvj08vvbYliZcAVuQ=="

if len(sys.argv) > 1:
    password = sys.argv[1]
else:
    print('Password required on commandline.')
    sys.exit(1)
    
ACCOUNT_SID = decrypt(encrypted_account_sid, password)
AUTH_TOKEN = decrypt(encrypted_auth_token, password)

os.system(f"setx ACCOUNT_SID {ACCOUNT_SID}")
os.system(f"setx AUTH_TOKEN {AUTH_TOKEN}")

print('VScode must be re-started to access changed environment.')
print('Program end.')
