from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from random import randint
import re, tldextract, os, json
from nltk.tokenize import sent_tokenize, word_tokenize
from opencorpora.settings import BASE_DIR

temp_folder = BASE_DIR/'static/main/tmp'
remjs = os.path.join(temp_folder, "remove.js")
nlpjson = os.path.join(temp_folder, "nlp.json")
class MainConfig(AppConfig):
    name = 'main'
    verbose_name = _('Main')


def generateID(n):
    up = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    low = up.lower()
    numeric = "".join([str(w) for w in range(10)])
    chars = up + low + numeric
    length = len(chars)
    arr = []
    j = 0
    while j < n:
        result = ''
        for i in range(5):
            index = randint(0, length-1)
            result += chars[index]
        if result in arr:
            j -= 1
        else:
            result += '_'
            arr.append(result)
        j += 1   
    return arr

class optimizeTitle():
    shortTitle = ''
    title = ''
    def __init__(self, title):
        self.title = title
        title = re.sub(r'[\s|\s+]',' ', title)
        title = re.sub(r'[\n|\n+]',' ', title)
        arr = title.split(' ')
        title = ''
        length = len(arr)
        if length > 6:
            for i in range(6):
                title += arr[i] + ' '
                if len(title) > 60:
                    break
            title = title[:len(title) - 1] + '...'
        else:
            title += ' '.join(arr)
            if not title.endswith('.'):
                title += '.'
        self.shortTitle = title

class optimizeUrl():
    url = ''
    shortUrl = ''
    domain = ''
    schema = None
    def __init__(self, url):
        self.url = url
        if len(url) > 60:
            self.shortUrl = url[:60] + '...'
        else:
            self.shortUrl = url
        
        link = re.match(r'(\w+://)', url)
        if link:
            self.schema = link.group(1)

        parsed = tldextract.extract(url)
        if parsed:
            parsed = ".".join([i for i in parsed if i])
            self.domain = parsed

def toNormal(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\n|\n+]', ' ', text)
    return text

def toModal(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\&', '&amp;', text)
    text = re.sub(r'\'', '&#39;', text)
    text = re.sub(r'\"', '&quot;', text)
    text = re.sub(r'[\n|\n+]', '<br>', text)
    text = re.sub(r'<', '&lt;', text)
    text = re.sub(r'>', '&gt;', text)
    return text

def tokenization(text):
    return " ".join(re.findall(r'\w+',text))

class optimizeAbstract():
    abstract = ''
    shortAbstract = ''
    def __init__(self, annotation):
        self.abstract = annotation
        if len(self.abstract) < 150:
            self.shortAbstract = self.abstract
        else:
            sozder = word_tokenize(annotation)
            abss = ''
            if len(sozder) > 20:
                for i in range(20):
                    abss += sozder[i] + ' '
                    if len(abss) > 130:
                        break
                abss = abss[:len(abss)-1]
            else:
                abss += ' '.join(sozder)
            if not abss.endswith('.'):
                abss += '...'
            else:
                abss += '..'
            self.shortAbstract = abss

def toKeywords(keywords):
    kk = []
    keywords = keywords.split(', ')
    kk.extend(keywords[:3])
    kk.extend(keywords[16:18])
    return kk

def toGenres(genres, lang='kk'):
    with open(remjs, 'w', encoding="utf-8") as f:
        nl = '\n'
        tab = '\t'
        so = '{'
        sc = '}'
        tr = "'"
        for genre in genres:
            janr = genre.kz
            if lang == 'ru':
                janr = genre.rus
            elif lang == 'en':
                janr = genre.en
            f.write(f'{nl}$("div#{genre.pk}").click(function(){so}{nl}{tab}$(this).css({so}display : "none"{sc});{nl}{tab}selectedshtml = $.grep(selectedshtml, function(value){so}{nl}{tab*2}return value != "{janr}";{nl}{tab}{sc});{nl}{tab}$({tr}option[value="{genre.pk}"]{tr}).attr({tr}disabled{tr}, false);{nl}{sc});')

def toResult(CPI, cid, text, title, keywords, annotation, url, lang='kk'):
    taqyryby = []
    kilttiksozder = []
    mazmuny = []
    silteme = []
    for i in range(CPI):
        taqyryby.append(optimizeTitle(title[i]))
        kilttiksozder.append(toKeywords(keywords[i]))
        if annotation[i] != '' or annotation[i] != '\n' or annotation[i] != ' ' or annotation[i] != None:
            mazmuny.append(optimizeAbstract(annotation[i]))
        else:
            mazmuny.append(optimizeAbstract(text[i]))
        silteme.append(optimizeUrl(url[i]))
    
    
    for i in range(CPI):
        htmlkw = "<p>"
        for w in kilttiksozder[i]:
            htmlkw += "<span>" + w + "</span>|"
        htmlkw = htmlkw[:len(htmlkw)-1]+'</p>'
        kilttiksozder[i] = htmlkw
    html = ""
    mydict = {
        'kk': 'ары қарай оқу',
        'en': 'read more',
        'ru': 'читать далее'
    }
    for i in range(CPI):
        schema = silteme[i].schema if silteme[i].schema else "https://"
        nextsum = "" if mazmuny[i].shortAbstract == mazmuny[i].abstract else str('<a id="'+cid[i]+'" onclick="getsumma(this);" class="showsumma">'+mydict[lang]+'</a>')
        html += "<div class=\"result\">\n\r\t<a target=\"_blank\" href=\""+silteme[i].url+"\">"+toNormal(taqyryby[i].shortTitle)+"</a>\n\r\t<br>\n\r\t<p>"+silteme[i].shortUrl+"</p>\n\r\t<a href=\""+schema+silteme[i].domain+"\">"+silteme[i].domain+"</a>\n\r\t<p id=\""+cid[i]+"\" onclick=\"sendforgetid(this);\" data-toggle=\"modal\">"+toNormal(mazmuny[i].shortAbstract)+nextsum+"</p>\n\r\t"+kilttiksozder[i]+"\n\r</div>"
    return html

def toNLPjson(CPI, cid, title, text, lemmas, morphanaliz, annotation):
    with open(nlpjson, 'w') as f :
        myjson = {}
        for i in range(CPI):
            myjson[cid[i]] = {
                'title': title[i],
                'token': tokenization(text[i]),
                'lemmas': lemmas[i],
                'morphanaliz': morphanaliz[i],
                'annotation': annotation[i],
                'text': text[i]
                }
        json.dump(myjson, f, indent=4)