import os
import glob
from CorporaDB import corporaDB
from subprocess import PIPE, run
import collections, re, math

papka_korpus = os.path.dirname(__file__)
class EditedApertium_DB():
    def __init__(self, text, apertium):
        self.text = text
        self.apertium = apertium
        np = []
        unknown = []
        soilemder = self.soilemgebolu(self.text)
        self.txttest = str(self.apertium)
        testtxt = re.findall(r"\*\w+\$", self.txttest)
        testtxt = "".join(testtxt)
        testtxt = re.findall(r"\w+", testtxt)
        for soilem in soilemder:
            sozder = self.sozgebolu(soilem)
            for i in range(1,len(sozder)):
                if str(sozder[i][0]).isupper() and sozder[i] in testtxt:
                    np.append(str(sozder[i]))
                elif sozder[i] in testtxt:
                    unknown.append(str(sozder[i]))
        for w in np:
            self.txttest = re.sub(r'\*'+w, w+'<np>', self.txttest)
        for w in unknown:
            self.txttest = re.sub(r'\*'+w, w+'<unknown>', self.txttest)
    def sub(self, newtext):
        newtext = re.sub(r'[.]+([.]|[,]|[!]|[?])+', '. ', newtext)
        newtext = re.sub(r'[,]+([.]|[,]|[!]|[?])+', ', ', newtext)
        newtext = re.sub(r'[?]+([.]|[,]|[!]|[?])+', '? ', newtext)
        newtext = re.sub(r'[!]+([.]|[,]|[!]|[?])+', '! ', newtext)
        newtext = re.sub(r'[.]+', '. ', newtext)
        newtext = re.sub(r'[,]+', ', ', newtext)
        newtext = re.sub(r'[?]+', '? ', newtext)
        newtext = re.sub(r'[!]+', '! ', newtext)
        newtext = re.sub(r'[ ]+\.', '.', newtext)
        newtext = re.sub(r'[ ]+\,', ',', newtext)
        newtext = re.sub(r'[ ]+\?', '?', newtext)
        newtext = re.sub(r'[ ]+\!', '!', newtext)
        newtext = re.sub(r'[" "]+', ' ', newtext)
        return newtext
    def soilemgebolu(self, text):
        res = re.split(r"[.]|[?]|[!]", text)
        if res[len(res)-1] == '':
            del res[len(res)-1]
        return res

    def sozgebolu(self, text):
        return re.findall(r"\w+", text)
    def __str__(self):
        return self.txttest

class outtexts_DB():
    def __init__(self, aptext):
        txtmas = re.findall(r"[\w+|\w|\s|(\w\-\w)]+[<]+\w+[>]|[,|\.|\?|!]+[<]+\w+[>]|[«]+[<]+\w+[>]|[»]+[<]+\w+[>]|[\"]+[<]+\w+[>]|[\"]+[<]+\w+[>]|[\']+[<]+\w+[>]|[\']+[<]+\w+[>]|\n|\n+|[ ]+|[\"]+[<]+\w+[>]|.{1}[<]+lquot+[>]|.{1}[<]+rquot+[>]", aptext)
        self.newtext = ""
        for i in txtmas:
            self.newtext += str(i).replace("^","").replace("<cm>","").replace("<sent>","").replace("<lquot>","").replace("<rquot>","").replace("е<cop>", "")
        self.newtext = re.sub(r'[.]+([.]|[,]|[!]|[?])+', '. ', self.newtext)
        self.newtext = re.sub(r'[,]+([.]|[,]|[!]|[?])+', ', ', self.newtext)
        self.newtext = re.sub(r'[?]+([.]|[,]|[!]|[?])+', '? ', self.newtext)
        self.newtext = re.sub(r'[!]+([.]|[,]|[!]|[?])+', '! ', self.newtext)
        self.newtext = re.sub(r'[.]+', '. ', self.newtext)
        self.newtext = re.sub(r'[,]+', ', ', self.newtext)
        self.newtext = re.sub(r'[?]+', '? ', self.newtext)
        self.newtext = re.sub(r'[!]+', '! ', self.newtext)
        self.newtext = re.sub(r'[ ]+\.', '.', self.newtext)
        self.newtext = re.sub(r'[ ]+\,', ',', self.newtext)
        self.newtext = re.sub(r'[ ]+\?', '?', self.newtext)
        self.newtext = re.sub(r'[ ]+\!', '!', self.newtext)
        self.newtext = re.sub(r'[" "]+', ' ', self.newtext)
    def __str__(self):
        return self.newtext
class train_DB():
    def sozgebolu(self, text):
        sozder = re.split(r'[<]+\w+[>]+', text)
        for i in range(len(sozder)):
            sozder[i] = str(sozder[i]).lower()
            new = ""
            for j in sozder[i]:
                if j in "abcdefghigklmnopqrstuvwxyzаәбвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщьыъіэюя1234567890- ":
                    new += j
            sozder[i] = new
        if sozder[len(sozder)-1] == '':
            del sozder[len(sozder)-1]
        return sozder
    def __init__(self, outtexts):
        f = open(os.path.join(os.path.dirname(__file__), "Global/MorfAnaliz/stopw.txt"), 'r', encoding="utf-8")
        self.stxt = list(f.readlines())
        for i in range(len(self.stxt)):
            l = "" 
            for j in range(len(self.stxt[i])):
                if self.stxt[i][j] != '\n':
                    l += self.stxt[i][j]
            self.stxt[i] = l
        txt = outtexts
        soz = self.sozgebolu(txt)
        n = len(soz)
        i = 0
        while i < n:
            for j in self.stxt:
                if soz[i] == j:
                    soz.remove(j)
                    n -= 1
                    i -= 0 if i == 0 else 1
                    break
            i += 1
        self.sozd = " ".join(soz)
    def __str__(self):
        return self.sozd


ob = corporaDB()
start_with = 0
count = 25
lencorp = int(ob.Count_corpora()[0]['sany'])
while start_with < lencorp:
    mylist = ob.SelectsText(start_with = start_with, count_def = count)
    start_with += 25
    for i in range(len(mylist)):
        with open(os.path.join(papka_korpus,'tmp/text.tmp'),'w',encoding="utf-8") as f:
            f.write(mylist[i]['text'])
        os.system('''cd $HOME/sources/apertium-kaz-rus\ncat "{0}" | apertium -n -d. kaz-rus-tagger > "{1}"'''.format(os.path.join(papka_korpus,'tmp/text.tmp'), os.path.join(papka_korpus,'tmp/app.tmp')))
        apertium = open(os.path.join(papka_korpus,'tmp/app.tmp'),'r',encoding="utf-8").read()
        editedapertium = str(EditedApertium_DB(text = mylist[i]['text'], apertium = apertium))
        editedapertium = re.sub(r"'", "''", editedapertium)
        outtexts = str(outtexts_DB(aptext = editedapertium))
        outtexts = re.sub(r"'", "''", outtexts)
        train = str(train_DB(outtexts=outtexts))
        train = re.sub(r"'", "''", train)
        ob.KESTENI_JANARTU(bagan_aty='morphanaliz', bagan_mani=str(editedapertium), bagan_id=int(mylist[i]['id']))
        ob.KESTENI_JANARTU(bagan_aty='outtext', bagan_mani=str(outtexts), bagan_id=int(mylist[i]['id']))
        ob.KESTENI_JANARTU(bagan_aty='lemmas', bagan_mani=str(train), bagan_id=int(mylist[i]['id']))
    if start_with + count > lencorp:
        count = lencorp - start_with
    
    print(f"Qazirge {start_with + count} matin daiyn!")