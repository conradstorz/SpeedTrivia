# -*- coding: utf-8 -*-
"""Take a file named 'new_team_names.txt' and fold into the file 'Team_names.txt'.
    Incoming names are cleaned, stripped, finalized with a '.\n' and compared to
    existing team names looking for exact duplicates.
"""
import re
import pprint
import unicodedata

existing_names = []
new_name_submissions = []


def normalize(txt):
    txt = txt.strip()
    if txt == '': return ''    
    # ensure string ends with a '.'
    if txt[-1] != '.':
        txt = txt + '.'
    # unicode normalized attempts to change visible unicode to ascii
    uniclean = unicodedata.normalize(u'NFKD', txt).encode('ascii', 'ignore').decode('utf8')        
    # Regex attempts to remove any characters that are not visible.
    subd = re.sub('[^!-~]+',' ',uniclean).strip()
    return subd


with open('Team_names.txt', 'r') as en:
    existing_names = en.readlines()



existing_names = [normalize(name) for name in existing_names]


#print(existing_names)



with open('new_team_names.txt', 'r', encoding='utf8') as nn:
    new_name_submissions = nn.readlines()


new_name_submissions = [normalize(name) for name in new_name_submissions]
# remove blank lines
new_name_submissions = [name for name in new_name_submissions if name != '']


new_name_submissions.sort()

pprint.pprint(new_name_submissions)

dups = [name for name in new_name_submissions if name in existing_names]
unique_names = [name for name in new_name_submissions if name not in existing_names]

dups.sort()

#print(dups)

print(f'Original list has {len(existing_names)} names.')
print(f'New names list has {len(new_name_submissions)} names.')
print(f'There were {len(dups)} duplicates and {len(unique_names)} unique names.')

existing_names += unique_names
existing_names.sort()

unique_names = list(set(existing_names))
unique_names.sort()

#pprint.pprint(existing_names)

lowered_names = [name.lower() for name in existing_names]

dduped = [name for name in existing_names if name.lower() not in lowered_names]

print(f'{len(unique_names)} unique names remain.')

#pprint.pprint(unique_names)

#pprint.pprint(lowered_names)
