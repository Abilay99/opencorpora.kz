import re
import os,glob
papka_korpus = os.path.dirname(os.path.abspath(__file__))
papka_outtexts = os.path.join(papka_korpus, "testouttexts/")
papka_train = os.path.join(papka_korpus, "testtrain/")
from tqdm import tqdm
from time import monotonic, sleep
from datetime import timedelta
from .Global import sozgebolu

files = glob.glob(os.path.join(papka_outtexts, "*.gt"))
length = len(files)
pbar = tqdm(files)
start_time = monotonic()
for fail in pbar:
    filename = fail[fail.rfind("/")+1:]
    pbar.set_description(f"Жасалуда {str(filename)}")
    with open(fail, 'r', encoding="utf-8") as f:
        inddot = filename.rfind(".")
        f2 = open(os.path.join(papka_train, filename[:inddot]+".tr"), 'w', encoding="utf-8")
        txt = f.read()
        soz = sozgebolu(txt)
        sozd = " ".join(soz[0])
        f2.write(str(sozd))
        f2.close()
end_time = monotonic()
timedel = end_time - start_time 

print("Аяқталды! Барлығы {0} құжат. Жұмсалған уақыт: {1}".format(length, timedelta(seconds=timedel)))