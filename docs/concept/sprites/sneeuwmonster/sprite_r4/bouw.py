# Sneeuwmonster r4 = r3_ogen (a1, glans linksboven) + twee keurderreparaties (sprite_r2/KEURING.md); ogen niet aangeraakt.
#  1 kin: modeltinten terug (zoals r1), 4 -> 5 op de lijst hieronder; schaduw rij 30-31 blijft. Elk pixel gecontroleerd: model L >= 236.
#  2 pluklijntjes taps zoals het model: (31,14) (33,14) (28,17) 2 -> 3.
# Dezelfde twee reparaties op alle oogvarianten van r3_ogen -> r4_oog_<variant>_<glans>.png (complete sprites).
# Gebruik: cd sneeuwmonster && python3 sprite_r4/bouw.py
import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
U='sprite_r4/'
KIN=[(22,27),(23,27),(33,27),(34,27)]+[(x,28) for x in range(23,27)]+[(x,28) for x in range(29,34)]+[(x,29) for x in range(25,33)]
PLUK=[(31,14),(33,14),(28,17)]
M=np.asarray(Image.open(MODEL).convert('RGB')).astype(float); LM=M@[.299,.587,.114]
fr=lambda X,ph,o0,u0: int(round(ph+0.5+10.24*((X-o0)/S+u0)))
def modelL(X,Y):
    r=np.s_[fr(Y,9.25,Y0,V0)+1:fr(Y+1,9.25,Y0,V0)-1,fr(X,9.05,X0,U0)+1:fr(X+1,9.05,X0,U0)-1]; return LM[r].mean()
def repareer(o):
    o=o.copy()
    for X,Y in KIN:
        assert o[Y,X]==4, (X,Y,o[Y,X]); o[Y,X]=5
    for X,Y in PLUK:
        assert o[Y,X]==2, (X,Y,o[Y,X]); o[Y,X]=3
    return o
if __name__=='__main__':
    print('model L per kinpixel:',[(X,Y,int(modelL(X,Y))) for X,Y in KIN]); assert all(modelL(X,Y)>=236 for X,Y in KIN)
    print('model L pluklijntjes:',[(X,Y,int(modelL(X,Y))) for X,Y in PLUK])
    r3=np.asarray(Image.open('sprite_r3_ogen/sneeuwmonster_r3.png')).astype(int)
    r4=repareer(r3); opslaan(r4,U+'sneeuwmonster_r4.png')
    d=[(int(x),int(y),CH[r3[y,x]]+'>'+CH[r4[y,x]]) for y,x in zip(*np.where(r3!=r4))]
    print('diff r4 t.o.v. r3: %d px'%len(d), d); assert set((x,y) for x,y,_ in d)==set(KIN+PLUK)
    for lv in ('a','a1','b','c'):
        for gl in ('lb','onder'):
            b=np.asarray(Image.open('sprite_r3_ogen/oog_R_%s_%s.png'%(lv,gl))).astype(int); opslaan(repareer(b),U+'r4_oog_%s_%s.png'%(lv,gl))
    toon(r4,24,33,18,42)
    # ---------- vel: r4 8x | model 8x / kin-close-up 12x r3 (voor) | r4 (na) | model / 1x ----------
    def rgbo(o,bg=(255,255,255)):
        img=np.zeros((64,64,3),'uint8'); img[:]=bg
        for k in range(1,len(PAL)): img[o==k]=PAL[k]
        return Image.fromarray(img)
    MI=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+10.24*u
    def mcrop(x0,y0,x1,y1,z):
        u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
        return MI.crop((int(f(u0,9.05)),int(f(v0,9.25)),int(f(u1,9.05)),int(f(v1,9.25)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
    def grid(a,z):
        dr=ImageDraw.Draw(a)
        for x in range(0,a.width,z): dr.line([(x,0),(x,a.height)],fill=(225,225,225))
        for y in range(0,a.height,z): dr.line([(0,y),(a.width,y)],fill=(225,225,225))
        return a
    B=(14,8,50,56); W8=(B[2]-B[0])*8; H8=(B[3]-B[1])*8
    K=(19,10,42,34); z=12; wk=(K[2]-K[0])*z; hk=(K[3]-K[1])*z
    V=Image.new('RGB',(max(2*W8+10,3*(wk+10)),H8+20+hk+30+90),'white'); dr=ImageDraw.Draw(V)
    dr.text((2,2),'r4 8x',fill=(200,0,0)); dr.text((W8+12,2),'model 8x',fill=(200,0,0))
    V.paste(rgbo(r4).crop(B).resize((W8,H8),Image.NEAREST),(0,16)); V.paste(mcrop(*B,8),(W8+10,16))
    y=H8+24
    for i,(t,a) in enumerate((('voor (r3)',grid(rgbo(r3).crop(K).resize((wk,hk),Image.NEAREST),z)),('na (r4)',grid(rgbo(r4).crop(K).resize((wk,hk),Image.NEAREST),z)),('model',mcrop(*K,z)))):
        dr.text((i*(wk+10)+2,y),t,fill=(200,0,0)); V.paste(a,(i*(wk+10),y+14))
    y+=hk+24; x=0
    for bg in [(255,255,255),(248,248,232),(40,48,56),(24,24,24)]: V.paste(rgbo(r4,bg),(x,y)); x+=72
    V.save(U+'vel.png'); print(U+'vel.png',V.size)
