import re, os
papka_korpus = os.path.dirname(os.path.abspath(__file__))
#stopwordtar
f = open(os.path.join(papka_korpus,"MorfAnaliz/stopw.txt"), 'r', encoding="utf-8")
stxt = list(f.readlines())
for i in range(len(stxt)):
    l = "" 
    for j in range(len(stxt[i])):
        if stxt[i][j] != '\n':
            l += stxt[i][j]
    stxt[i] = l

def sozgebolu(text):
    tag = re.findall(r'[<]+\w+[>]+', text)
    sozder = re.split(r'[<]+\w+[>]+', text)
    try:
        if sozder[0][0] == '\ufeff':
            sozder[0] = sozder[0][1:]
    except IndexError:
        pass
    for i in range(len(sozder)):
        sozder[i] = str(sozder[i]).lower()
        new = ""
        for j in sozder[i]:
            if j in "abcdefghigklmnopqrstuvwxyzаәбвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщьыъіэюя1234567890- ":
                new += j
        sozder[i] = new
    if sozder[len(sozder)-1] == '':
        del sozder[len(sozder)-1]
    #stopwordtard alyp tastau
    n = len(sozder)
    i = 0
    while i < n:
        for j in stxt:
            if sozder[i] == j or len(sozder[i]) < 2:
                try:
                    del sozder[i]
                    del tag[i]
                except IndexError:
                    pass
                n -= 1
                i -= 0 if i == 0 else 1
                break
        i += 1
    return [sozder, tag]