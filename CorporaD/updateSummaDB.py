from CorporaDB import corporaDB
from Global import summarizer
from time import monotonic
from datetime import timedelta
import re
ob = corporaDB()

utechka = ob.SelectEmptyMorph()

start_time = monotonic()
for i in range(len(utechka)):
    text = utechka[i]['text']
    text = re.sub(r"\.", ". ", text)
    text = re.sub(r"\;", "; ", text)
    text = re.sub(r"\?", "? ", text)
    text = re.sub(r"\!", "! ", text)
    annotation = summarizer.summarize(text, language="kazakh")
    annotation = re.sub(r"'","''",annotation)
    text = re.sub(r"'","''",text)
    if len(text)>10 and len(annotation)>10:
        ob.KESTENI_JANARTU(bagan_aty='annotation', bagan_mani=annotation, bagan_id=int(utechka[i]['id']))
        ob.KESTENI_JANARTU(bagan_aty='text', bagan_mani=text, bagan_id=int(utechka[i]['id']))
end_time = monotonic()

print("Аяқталды! Барлығы {0} құжат. Жұмсалған уақыт: {1}".format(len(utechka), timedelta(seconds=end_time - start_time))) 