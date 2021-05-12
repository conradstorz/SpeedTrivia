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
unique_existing_names_set = list(set(existing_names))  # This does not account for capitalization variance
unique_existing_names_set.sort()  # list is un-sorted after converting to a set
# lowercase all existing names for deduplication of new names
lower_existing_names = [name.lower() for name in existing_names]


with open("new_team_names.txt", "r", encoding="utf8") as nn:
    new_name_submissions = nn.readlines()
new_name_submissions = [normalize(name) for name in new_name_submissions]
# remove blank lines
new_name_submissions = [name for name in new_name_submissions if name != ""]
new_name_submissions.sort()
dups_in_existing_names = [name for name in new_name_submissions if name.lower() in lower_existing_names]
unique_from_existing_names = [name for name in new_name_submissions if name.lower() not in lower_existing_names]


combined_names = existing_names + unique_from_existing_names
combined_names.sort()
# lowercase all existing names for deduplication of new names
lower_combined_names = [name.lower() for name in combined_names]
# use set to de-duplicate
combined_lower_unique_names = list(set(lower_combined_names))
combined_lower_unique_names.sort()  # list is un-sorted after converting to a set
# Now recover the names with original capitalization intact
combined_unique_names = [name for name in combined_names if name.lower() in combined_lower_unique_names]
# Now I have re-introduced the duplicates so remove them again
all_unique_names = list(set(combined_unique_names))
all_unique_names.sort()  # list is un-sorted after converting to a set


pprint.pprint(all_unique_names)

print(f"Original list has {len(existing_names)} names.")
print(f"New names list has {len(new_name_submissions)} names.")
print(f"There were {len(dups_in_existing_names)} duplicates and {len(unique_from_existing_names)} unique names.")
print(f'{len(combined_unique_names)} names after comparing lowercase versions.')
print(f"{len(all_unique_names)} unique names when combined.")


with open("Cobined_Team_names.txt", "w") as cn:
    for name in all_unique_names:
        cn.write(name + '\n')

print(f'File written.')
