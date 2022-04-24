from JackTokenizer import JackTokenizer
tokens_from_line = []
stringy = ""
# cur_line = 'constructor "do" else.{ int -char~'
cur_line = "Class Bar {"
for c in cur_line:
    if "//" in stringy:
        break
    if c != ' ':
        stringy += c
    if c in JackTokenizer.SYMBOL or c in JackTokenizer.KEYWORDS:
        if stringy[:-1] != "":
            tokens_from_line.append(stringy[:-1])
        tokens_from_line.append(c)
        stringy = ""
    elif c == ' ':
        if stringy == "":
            continue
        tokens_from_line.append(stringy)
        stringy = ""
if stringy:
    tokens_from_line.append(stringy)
print(tokens_from_line)