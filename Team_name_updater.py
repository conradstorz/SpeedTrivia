# -*- coding: utf-8 -*-
"""Take a file named 'new_team_names.txt' and fold into the file 'Team_names.txt'.
    Incoming names are cleaned, stripped, finalized with a '.\n' and compared to
    existing team names looking for exact duplicates.

"""
import pprint
import ftfy

existing_names = []
new_name_submissions = []


def normalize(txt):
    txt = txt.strip()
    if txt == "":
        return ""
    # ensure string ends with a '.'
    if txt[-1] != ".":
        txt = txt + "."
    # attempt to change 'FANCY' quotes and such to ascii
    subd = ftfy.fix_text(txt, normalization="NFKC")
    return subd


with open("Team_names.txt", "r") as en:
    existing_names = en.readlines()

existing_names = [normalize(name) for name in existing_names]


# print(existing_names)


with open("new_team_names.txt", "r", encoding="utf8") as nn:
    new_name_submissions = nn.readlines()


new_name_submissions = [normalize(name) for name in new_name_submissions]
# remove blank lines
new_name_submissions = [name for name in new_name_submissions if name != ""]


new_name_submissions.sort()

# pprint.pprint(new_name_submissions)

dups = [name for name in new_name_submissions if name in existing_names]  # This does not account for capitalization variance
unique_names = [name for name in new_name_submissions if name not in existing_names]

# print(dups.sort())

print(f"Original list has {len(existing_names)} names.")
print(f"New names list has {len(new_name_submissions)} names.")
print(f"There were {len(dups)} duplicates and {len(unique_names)} unique names.")

existing_names += unique_names
existing_names.sort()

unique_names = list(set(existing_names))  # This does not account for capitalization variance
unique_names.sort()

print(f"{len(existing_names)} unique names remain.")

pprint.pprint(unique_names)

print(f'{len(unique_names)} names.')