import os,glob
import xlwt
from Global import (TF_IDF, tf_idf, bigram, bi_tf_idf, sozgebolu)
from tqdm import tqdm
from time import monotonic, sleep
from datetime import timedelta
papka_korpus = os.path.dirname(os.path.abspath(__file__))
papka_train = os.path.join(papka_korpus, "testtrain/")

#TF_IDF jaily aqparat
print(TF_IDF.__doc__)

#----------------------------------------------------------------------------------------------------

#excelge daindyq
wb = xlwt.Workbook()
xlwt.add_palette_colour("kerek", 0x21)
wb.set_colour_RGB(0x21, 204, 255, 255)
style0 = xlwt.easyxf("pattern: pattern solid, fore_color Lime; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; font: name Times New Roman, bold on; align: horiz center;")
style1 = xlwt.easyxf("pattern: pattern solid, fore_color kerek; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; font: name Times New Roman; ")
style2 = xlwt.easyxf("pattern: pattern solid, fore_color yellow; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; font: name Times New Roman;")
style3 = xlwt.easyxf("pattern: pattern solid, fore_color red; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin; font: name Times New Roman;")



#textter
files = glob.glob(os.path.join(os.path.join(papka_korpus, "testouttexts/"), '*.gt'))
length = len(files)
pbar = tqdm(files)
start_time = monotonic()
for fail in pbar:
    filename = fail[fail.rfind("/")+1:]
    pbar.set_description(f"Жасалуда {str(filename)}")
    with open(fail, 'r', encoding="utf-8") as f:
        txt = f.read()

        #failda berilgen matinnen tek sozderdi wygaryp beredi
        soz = sozgebolu(txt)

        #TF_IDF klasssyndagy konstruktordy qoldanyluy
        TfIdf = tf_idf(text = soz, papka_train = papka_train)

        #esepteuler
        tf = TfIdf.tf_esepteu()
        idf = TfIdf.idf_esepteu()
        tfidf = TfIdf.tf_idf_esepteu()

        #bigram klasssyndagy konstruktordy qoldanyluy
        bi = bigram(text = txt, papka_korpus = papka_korpus)
        text = [bi.newlemm, bi.lastlemm]

        #bigram TF_IDF klasssyndagy konstruktordy qoldanyluy
        BiTfIdf = bi_tf_idf(text = text, papka_train = papka_train)

        bi_tf = BiTfIdf.bi_tf_esepteu()
        bi_idf = BiTfIdf.bi_idf_esepteu()
        bi_tfidf = BiTfIdf.bi_tf_idf_esepteu()

        ws = wb.add_sheet(filename[:filename.rfind(".")], cell_overwrite_ok = True)
        ws.write_merge(0, 0, 0, 1, "TF", style0)
        ws.write_merge(0, 0, 2, 3, "IDF", style0)
        ws.write_merge(0, 0, 4, 5, "TF-IDF",style0)

        i = 1
        j = 0
        ws.col(j).width = 5300
        ws.col(j+1).width = 5300
        for x in tf:
            ws.write(i, j, str(x), style1)
            ws.write(i, j+1, str(tf[x]), style1)
            i += 1
        for x in bi_tf:
            ws.write(i, j, str(x), style1)
            ws.write(i, j+1, str(bi_tf[x]), style1)
            i += 1
            
        i = 1
        j = 2
        ws.col(j).width = 5300
        ws.col(j+1).width = 5300
        for x in idf:
            ws.write(i, j, str(x), style1)
            ws.write(i, j+1, str(idf[x]), style1)
            i += 1
        for x in bi_idf:
            ws.write(i, j, str(x), style1)
            ws.write(i, j+1, str(bi_idf[x]), style1)
            i += 1

        i = 1
        j = 4
        ws.col(j).width = 5300
        ws.col(j+1).width = 5300
        for x in tfidf:
            ws.write(i, j, str(x), style1)
            ws.write(i, j+1, str(tfidf[x]), style1)
            i += 1
        for x in bi_tfidf:
            ws.write(i, j, str(x), style1)
            ws.write(i, j+1, str(bi_tfidf[x]), style1)
            i += 1
wb.save(os.path.join(papka_korpus, "keywords.xls"))
end_time = monotonic()
timedel = end_time - start_time 
print("Аяқталды! Барлығы {0} құжат. Жұмсалған уақыт: {1}".format(length, timedelta(seconds=timedel)))