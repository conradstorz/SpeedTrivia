import os
os.system("setx bar hello2")
print(f'Env var "bar": {os.system("set bar")}')
password = os.environ.get('bar')
print(f'Password is:{password}')
print('VScode must be re-started to access changed environment.')
