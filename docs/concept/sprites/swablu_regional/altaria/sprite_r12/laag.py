# laag.py: bepaalt de laag kop+hals in r11A (gedeeld door bouw.py)
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import label
im=Image.open('sprite_r11/altaria_r11A.png'); o=np.array(im).astype(int); PALI=im.getpalette()
PU,WS,WN,WD,WT,WC,ST,VS,VD,VM,VL,VH,LW=range(1,14)
sys.path.insert(0,'sprite_r11'); import importlib.util
spec=importlib.util.spec_from_file_location('b11','sprite_r11/bouw.py'); b11=importlib.util.module_from_spec(spec); spec.loader.exec_module(b11)
_,KOP,_=b11.bouw(*b11.VAR['A'])                        # kop A precies zoals in r11 gelegd (incl. snuit/pluis, ogen, kinrand)
# hals: violette pixels onder de kop (Y>=30), samenhangend met de kop
vio=np.isin(o,[VS,VD,VM,VL,VH])
lab,n=label(vio|KOP,acht=False)
ids=set(lab[KOP])-{0}
HALS=np.isin(lab,list(ids))&vio&~KOP
HALS[:30]=False
# halsrand links: wolk-selout direct links van de hals (de randlijn van de hals), zolang het selout blijft
RAND=np.zeros_like(HALS)
for Y,X in zip(*np.where(HALS)):
    x=X-1
    while o[Y,x]==WS and not KOP[Y,x]: RAND[Y,x]=True; x-=1
LAAG=KOP|HALS|RAND
# kuif (bevroren in r11): violet boven de kop (Y<=17) en de streng rechts over de vleugel (Y<=21, X>=34)
KUIF=np.zeros_like(LAAG)
for Y,X in zip(*np.where(vio|(o==LW))):
    if (Y<=17 or (Y<=21 and X>=34)) and not KOP[Y,X]: KUIF[Y,X]=True
