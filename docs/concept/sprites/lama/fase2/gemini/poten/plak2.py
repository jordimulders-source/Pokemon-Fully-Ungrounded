# r4 + vier poten uit r12, per poot uitgeknipt (polygoon, zonder buikhaar), geschaald,
# omgekleurd (nabij licht, ver donker) en per poot aangesloten onder de wol van r4.
from PIL import Image, ImageDraw; import numpy as np
a=np.array(Image.open('r4/r4_prompt_v4.png').convert('RGB')).astype(int)
B=Image.open('r12/r12_lama_foto.png').convert('RGB'); b=np.array(B).astype(int)
O=a.copy(); S=0.93
white=lambda p: p.sum()>=700
def wool(p): r,g,bb=p; return r>120 and g>70 and r-bb>45 and g>bb+15 and not (r>110 and g<80)
# 1. r4-poten weg
for y in range(820,1024):
    for x in range(195,505):
        p=a[y,x]
        if y>=905 or not wool(p): O[y,x]=255
O[824:,560:705]=255; O[824:,745:845]=255
# 2. poten uit r12: polygoon, bovenkant (top) -> aansluitpunt in r4 (doel), ver = donker
POTEN=[ # naam, polygoon r12, top r12, doel r4, ver
 ('nabij voor',[(320,595),(405,595),(380,640),(340,680),(300,740),(298,772),(232,776),(238,755),(280,690),(300,640)],(362,595),(335,850),False,1.0),
 ('ver voor',[(468,588),(527,588),(522,640),(537,700),(538,768),(480,772),(484,700),(489,650)],(497,588),(432,812),True,1.0),
 ('nabij achter',[(716,636),(806,636),(764,690),(724,722),(704,768),(656,772),(662,750),(698,700),(718,670)],(761,636),(645,800),False,1.38),
 ('ver achter',[(798,556),(884,556),(932,608),(947,680),(958,742),(952,762),(916,764),(912,700),(888,652),(852,612),(822,640)],(841,556),(772,806),True,1.0),
]
licht=(np.array([60,34,22]),np.array([178,120,74]),np.array([228,174,118]))
donker=(np.array([52,30,20]),np.array([128,80,50]),np.array([170,115,72]))
def kleur(p,ramp):
    d,m,l=ramp; L=(0.3*p[0]+0.59*p[1]+0.11*p[2])/255
    if L<0.22: return d
    t=min(1,(L-0.22)/0.6)
    return m+(l-m)*(t-0.5)*2 if t>0.5 else d+(m-d)*(0.35+0.65*t*2)
gezet=np.zeros((1024,1024),int)
# verre poten eerst (achter), nabije eroverheen
for naam,poly,top,doel,ver,sy in sorted(POTEN,key=lambda q: not q[4]):
    mk=Image.new('L',B.size,0); ImageDraw.Draw(mk).polygon(poly,fill=255); mk=np.array(mk)>0
    ys,xs=np.nonzero(mk)
    for y,x in zip(ys,xs):
        p=b[y,x]
        if white(p): continue
        X=int(round(doel[0]+(x-top[0])*S)); Y=int(round(doel[1]+(y-top[1])*S*sy))
        c=kleur(p,donker if ver else licht)
        for yy in range(Y,Y+1+int(sy)):
            for xx in (X,X+1):
                if 0<=xx<1024 and 0<=yy<1024 and (white(O[yy,xx]) or (not ver and gezet[yy,xx]==2)):
                    O[yy,xx]=c; gezet[yy,xx]=2 if ver else 1
Image.fromarray(O.clip(0,255).astype('uint8')).save('poten/r4_poten_r12.png')
# 3. gaatjes tussen wol en nabije voorpoot dichten (wit met boven én onder iets), daarna omlijnen
O2=O.copy(); vul=np.zeros((1024,1024),bool)
for x in range(285,405):
    for y in range(815,885):
        if white(O[y,x]) and any(not white(O[y-k,x]) for k in range(1,25)) and any(not white(O[y+k,x]) for k in range(1,25)):
            O2[y,x]=licht[1]; vul[y,x]=True
for y,x in zip(*np.nonzero(vul)):
    if any(white(O2[y+dy,x+dx]) for dy,dx in ((0,1),(0,-1),(1,0),(-1,0))): O2[y,x]=licht[0]
Image.fromarray(O2.clip(0,255).astype('uint8')).save('poten/r4_poten_r12.png')
