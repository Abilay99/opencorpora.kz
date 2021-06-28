import os, re
import collections,  math
from .Global import sozgebolu
papka_korpus = os.path.dirname(__file__)

#region Kerek
class EditedApertium_DB(object):
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
     
#------------------------------------------------------------------------------------------

class outtexts_DB(object):
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
     
#------------------------------------------------------------------------------------------

class train_DB(object):
    def __init__(self, outtexts):
        soz = sozgebolu(outtexts)
        self.sozd = " ".join(soz[0])
    def __str__(self):
        return self.sozd
     
#------------------------------------------------------------------------------------------

class tf_idf(object):
    def __init__(self, text, len_corp, objectCorporaDB, length_keywords = 15):
        self.__tf = collections.Counter(text[0])
        for i in range(len(text[0])):
            if len(str(text[0][i])) < 2:
                del self.__tf[text[0][i]]
        self.__idf = {}
        self.__tf_idf = {}
        self.__len_text = len(text[0])
        self.__len_corp = float(len_corp)
        self.__length_keywords = length_keywords
        self.__obj = objectCorporaDB
        for i in range(len(text[1])):
            if str(text[1][i]) != str('<n>') and str(text[1][i]) != str('<np>'):
                del self.__tf[text[0][i]]

    #===tf===
    def tf_esepteu(self):
        for i in self.__tf:
            self.__tf[i] =  self.__tf[i] / float(self.__len_text)

        new_tf = dict()
        kol = 0
        sort = sorted(self.__tf, key=self.__tf.get, reverse=True)
        for w in sort:
            new_tf[w] = self.__tf[w]
            kol += 1
            if kol == self.__length_keywords:
                break
        return new_tf
        #{w:self.__tf[w] for w in sorted(self.__tf, key=self.__tf.get, reverse=True)}
    #===idf===
    def idf_esepteu(self):
        nf = self.__len_corp
        for i in self.__tf:
            res = self.__obj.for_count_lemmas(phrase=str(i))
            nft = float(res[0]['sany'])
            try:
                self.__idf[i] = math.log(nf/nft, 10)
            except ZeroDivisionError:
                self.__idf[i] = math.log(nf/1.0, 10)
        new_idf = dict()
        kol = 0
        sort = sorted(self.__idf, key=self.__idf.get, reverse=True)
        for w in sort:
            new_idf[w] = self.__idf[w]
            kol += 1
            if kol == self.__length_keywords:
                break
        return new_idf
        #{w:self.__idf[w] for w in sorted(self.__idf, key=self.__idf.get, reverse=True)}
    
    #===tf_idf===
    def tf_idf_esepteu(self):
        for i in self.__tf:
            self.__tf_idf[i] = self.__idf[i]*self.__tf[i]
        new_tf_idf = dict()
        kol = 0
        sort = sorted(self.__tf_idf, key=self.__tf_idf.get, reverse=True)
        for w in sort:
            new_tf_idf[w] = self.__tf_idf[w]
            kol += 1
            if kol == self.__length_keywords:
                break
        return new_tf_idf
        #{w:self.__tf_idf[w] for w in sorted(self.__tf_idf, key=self.__tf_idf.get, reverse=True)}
     
#------------------------------------------------------------------------------------------

class bi_tf_idf(object):
    def __init__(self, text, len_corp, objectCorporaDB, length_keywords = 15):
        self.__bi_tf = collections.Counter(text[0])
        for i in range(len(text[0])):
            if len(str(text[0][i])) < 2:
                del self.__tf[text[0][i]]
        self.__bi_idf = {}
        self.__bi_tf_idf = {}
        self.__len_text = len(text[1])
        self.__len_corp = float(len_corp)
        self.__length_keywords = length_keywords
        self.__obj = objectCorporaDB

    #===tf===
    def bi_tf_esepteu(self):
        for i in self.__bi_tf:
            self.__bi_tf[i] =  self.__bi_tf[i] / float(self.__len_text)
        
        new_bi_tf = dict()
        kol = 0
        sort = sorted(self.__bi_tf, key=self.__bi_tf.get, reverse=True)
        for w in sort:
            new_bi_tf[w] = self.__bi_tf[w]
            kol += 1
            if kol == self.__length_keywords:
                break
        return new_bi_tf
        #{w:self.__bi_tf[w] for w in sorted(self.__bi_tf, key=self.__bi_tf.get, reverse=True)}
    
    #===idf===
    def bi_idf_esepteu(self):
        nf = self.__len_corp
        for i in self.__bi_tf:
            res = self.__obj.for_count_lemmas(phrase=str(i))
            nft = float(res[0]['sany'])
            try:
                self.__bi_idf[i] = math.log(nf/nft, 10)
            except ZeroDivisionError:
                self.__bi_idf[i] = math.log(nf/1.0, 10)

        new_bi_idf = dict()
        kol = 0
        sort = sorted(self.__bi_idf, key=self.__bi_idf.get, reverse=True)
        for w in sort:
            new_bi_idf[w] = self.__bi_idf[w]
            kol += 1
            if kol == self.__length_keywords:
                break
        return new_bi_idf
        #{w:self.__bi_idf[w] for w in sorted(self.__bi_idf, key=self.__bi_idf.get, reverse=True)}
    
    #===tf_idf===
    def bi_tf_idf_esepteu(self):
        for i in self.__bi_tf:
            self.__bi_tf_idf[i] = self.__bi_idf[i]*self.__bi_tf[i]
        new_bi_tf_idf = dict()
        kol = 0
        sort = sorted(self.__bi_tf_idf, key=self.__bi_tf_idf.get, reverse=True)
        for w in sort:
            new_bi_tf_idf[w] = self.__bi_tf_idf[w]
            kol += 1
            if kol == self.__length_keywords:
                break
        return new_bi_tf_idf
        #{w:self.__bi_tf_idf[w] for w in sorted(self.__bi_tf_idf, key=self.__bi_tf_idf.get, reverse=True)}
       
#-------------------------------------------------------------------------------------------------
#endregion Kerek
