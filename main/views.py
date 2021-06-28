from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.generic import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import get_language
from .models import Corpora, Genres
from .apps import toGenres, toResult, toModal, toNLPjson, optimizeAbstract, generateID
from CorporaD.execute import *
from CorporaD.CorporaDB import corporaDB
from CorporaD.Global.summa import summarizer
from CorporaD.Global import bigram, sozgebolu
import time, os, re, json
from opencorpora.settings import BASE_DIR

temp_folder = BASE_DIR/'static/main/tmp'
remjs = os.path.join(temp_folder, "remove.js")
nlpjson = os.path.join(temp_folder, "nlp.json")
start = float(0)
end   = float(0)

genres_lang = {'kk':'kz', 'ru':'rus', 'en':'en'}


@require_GET
def index(request):
    til = get_language()
    current_genres_column = genres_lang.get(til, 'kz')
    start = time.monotonic()
    if os.path.exists(remjs):
        os.remove(remjs)
    if os.path.exists(nlpjson):
        os.remove(nlpjson) 
    context = {}
    CPI = 5
    genres = Genres.objects.all().order_by(current_genres_column)
    toGenres(genres, lang=til)
    context['genres'] = genres
    context['check_kk'] = True if til == 'kk' else False
    context['check_ru'] = True if til == 'ru' else False
    context['check_en'] = True if til == 'en' else False
    if request.is_ajax or request.method == 'GET':
        if request.GET.get('source', None):
            source = request.GET.get('source', None)
            context['source'] = source
            if request.GET.get('filters', None):
                filters = request.GET.get('filters', None)
                if filters != 'all' or filters != '':
                    context['filters'] = filters
                    filterSid = {}
                    if(filters.find(',')):
                        filters = str(filters).split(',')
                        for genre in filters:
                            p = Genres.objects.filter(Q(kz=genre) | Q(rus=genre) | Q(en=genre))
                            if p:
                                filterSid[str(p[0].pk)] = genre
                    else:
                        p = Genres.objects.filter(Q(kz=filters) | Q(rus=filters) | Q(en=filters))
                        if p:
                            filterSid[str(p[0].pk)] = filters
                    context['filterSid'] = filterSid
                    start = time.monotonic()
                    corp = Corpora.objects.raw("SELECT * FROM corpora WHERE MATCH(title,text,annotation,keywords) AGAINST ('%s' IN IN BOOLEAN MODE) and genre_id in(%s)"%(source,",".join(filterSid.keys())))
                    end = time.monotonic()
                else:
                    start = time.monotonic()
                    corp = Corpora.objects.raw("SELECT * FROM corpora WHERE MATCH(title,text,annotation,keywords) AGAINST ('%s' IN IN BOOLEAN MODE)"%source)
                    end = time.monotonic()
            
            corp = Corpora.objects.raw("SELECT * FROM corpora WHERE MATCH(title,text,annotation,keywords) AGAINST ('%s' IN BOOLEAN MODE)"%source)
            if len(corp) == 0:
                context['results'] = None
                return render(request, 'main/index.html', context)
            elif len(corp) < CPI:
                CPI = len(corp)
            else:
                context['countitem'] = len(corp)
                paginator = Paginator(corp, CPI)
                if 'page' in request.GET:
                    page_num = request.GET['page']
                else:
                    page_num = 1
                page = paginator.get_page(page_num)
                context['page_obj'] = page
                if page.object_list:
                    cid         = generateID(CPI)
                    title       = [obj.title for obj in page.object_list]
                    text        = [obj.text for obj in page.object_list]
                    lemmas      = [obj.lemmas for obj in page.object_list]
                    morphanaliz = [obj.morphanaliz for obj in page.object_list]
                    keywords    = [obj.keywords for obj in page.object_list]
                    annotation  = [obj.annotation for obj in page.object_list]
                    url         = [obj.url for obj in page.object_list]
                    context['results']   = toResult(CPI= CPI, cid= cid, text=text, title= title, keywords= keywords, annotation= annotation, url= url, lang= til)
                    toNLPjson(CPI= CPI, cid= cid, title= title, text= text, lemmas= lemmas, morphanaliz= morphanaliz, annotation= annotation)
            end = time.monotonic()
            context['dttime'] = round(end-start, 5)
            context['null'] = False
            return render(request, 'main/index.html', context)
        context['null'] = True
        return render(request, 'main/index.html', context)
    return render(request, 'main/index.html', context)

@require_POST
def ressumma(request):
    if request.is_ajax and request.method == 'POST':
        if request.POST.get('id', None) and request.POST.get('type', None):
            changeid = request.POST['id']
            types = request.POST['type']
            data = {}
            with open(nlpjson) as f:
                myjson = json.load(f)
            try:
                res = myjson[changeid]
            except KeyError:
                render(request, 'main/index.html')
            data['id'] = changeid
            response = ""
            annotation = res['annotation']
            mydict = {
                'kk': ' Жабу.',
                'en': ' Close.',
                'ru': ' Закрыть.',
                'kk1': 'ары қарай оқу',
                'en1': 'read more',
                'ru1': 'читать далее'
            }
            if types == 'show':
                a = str(annotation) if str(annotation).endswith('.') else str(annotation) + ".\t"
                response = a + '<a id="' + changeid + '" onclick="getsumma(this);" class="hidesumma">'+mydict[get_language()]+'</a>'
            else:
                if ('' or '\n' or ' ' or None) != annotation :
                    obj = optimizeAbstract(annotation)
                else:
                    obj = optimizeAbstract(res['text'])
                response = obj.shortAbstract +'<a id="'+ changeid +'" onclick="getsumma(this);" class="showsumma">'+mydict[get_language()+'1']+'</a>'
            data['summa'] = response
            return JsonResponse(data=data)
    return render(request, 'main/index.html')



@require_POST
def handlerpost(request):
    if request.method == 'POST':
        if request.POST.get('id', None):
            changeid = request.POST.get('id')
            data = {}
            with open(nlpjson) as f:
                myjson = json.load(f)
            res = myjson[changeid]
            data['token'] = toModal(res['token'])
            data['lemmas'] = toModal(res['lemmas'])
            data['morphanaliz'] = toModal(res['morphanaliz'])
            data['id'] = changeid
            return JsonResponse(data=data)
    return render(request, 'main/index.html')

@require_POST
def download(request):
    if request.is_ajax and request.method == 'POST':
        if request.POST.get('id', None) and request.POST.get('type', None):
            changeid = request.POST.get('id')
            types = request.POST.get('type', None)
            data = {}
            with open(nlpjson) as f:
                myjson = json.load(f)
            res = myjson[changeid]
            data['title'] = res['title']
            data['fileval'] = res[types]
            return JsonResponse(data=data)
    return render(request, 'main/index.html')

@require_POST
def execpost(request):
    context = {}
    if request.POST.get('text', None) and request.POST.get('text') != '' and request.POST.get('text') != '\n':
        input_val = request.POST['text']
        keywords = ""
        annotation = ""
        lemmatization = ""
        morphanaliz = ""
        #connect db
        ob = corporaDB()
        lencorp = int(ob.Count_corpora()[0]['sany'])

        with open(os.path.join(BASE_DIR,'CorporaD/tmp/text.tmp'),'w',encoding="utf-8") as f:
            f.write(input_val)
        os.system('''cd $HOME/sources/apertium-kaz-rus\ncat "{0}" | apertium -n -d. kaz-rus-tagger > "{1}"'''.format(os.path.join(BASE_DIR,'CorporaD/tmp/text.tmp'), os.path.join(BASE_DIR,'CorporaD/tmp/app.tmp')))
        text = open(os.path.join(papka_korpus,'tmp/text.tmp'),'r',encoding="utf8").read()
        apertium = open(os.path.join(papka_korpus,'tmp/app.tmp'),'r',encoding="utf-8").read()
        morphanaliz = str(EditedApertium_DB(text = text, apertium = apertium))
        outtexts = str(outtexts_DB(aptext = str(morphanaliz)))
        lemmatization = str(train_DB(outtexts=str(outtexts)))
        annotation = summarizer.summarize(text, language="kazakh")
        soz = sozgebolu(outtexts)
        
        #TF_IDF klasssyndagy konstruktordy qoldanyluy
        TfIdf = tf_idf(text = soz, len_corp = lencorp, objectCorporaDB = ob, length_keywords=5)
        #esepteuler
        tf = TfIdf.tf_esepteu()
        idf = TfIdf.idf_esepteu()
        tfidf = TfIdf.tf_idf_esepteu()
        
        #bigram klasssyndagy konstruktordy qoldanyluy
        bi = bigram(text = str(outtexts))
        bi_text = [bi.newlemm, bi.lastlemm]

        #bigram TF_IDF klasssyndagy konstruktordy qoldanyluy
        BiTfIdf = bi_tf_idf(text = bi_text, len_corp = lencorp, objectCorporaDB = ob, length_keywords=5)
        bi_tf = BiTfIdf.bi_tf_esepteu()
        bi_idf = BiTfIdf.bi_idf_esepteu()
        bi_tfidf = BiTfIdf.bi_tf_idf_esepteu()
        spis = []
        for x in tfidf:
            spis.append(str(x))
        for x in bi_tfidf:
            spis.append(str(x))
        
        keywords = ", ".join(spis)

        context['keywords'] = toModal(keywords)
        context['annotation'] = toModal(annotation)
        context['lemma'] = toModal(lemmatization)
        context['morph'] = toModal(morphanaliz)
        context['text'] = input_val
    return JsonResponse(context)

@require_GET
def execute(request):
    return render(request, 'main/execute.html')

@require_GET
def about(request):
    return render(request, 'main/about.html')

@require_GET
def privacy(request):
    return render(request, 'main/privacy.html')

