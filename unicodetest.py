from unidecode import unidecode
from unicodedata import name
import ftfy

for i in range(33, 65535):
    if i > 0xEFFFF:
        continue  # Characters in Private Use Area and above are ignored
    if 0xD800 <= i <= 0xDFFF:
        continue
    h = hex(i)
    u = chr(i)
    f = ftfy.fix_text(u, normalization="NFKC")
    a = unidecode(u)
    if a != "[?]" and len(u) != 0 and len(a) != 0 and len(f) != 0:
        new_char = ""
        if u != f:
            for c in list(f):
                new_char += "{}, ".format(ord(c))
            new_char = new_char[:-2]
        else:
            new_char = "Same"
        try:
            txt = name(u).lower()
            # print(txt)
            if 'mark' in txt:
                print(
                    f"dec={i} hex={h} unicode_chr={u} ftfy_chr(s)={f} ftfy_dec={new_char}\n", 
                    f"ascii_chr={a} uni_len={len(u)} ascii_len={len(a)} unicode_name={name(u)}"
                )
        except ValueError:
            pass
