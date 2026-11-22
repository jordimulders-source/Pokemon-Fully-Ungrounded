# Gedeelde hulpjes: palet, model op spriteschaal, opslaan als geindexeerde PNG.
import numpy as np; from PIL import Image
S=35/60; X0,Y0,U0,V0=21,14,26,19; PHX=PHY=0.5
MODEL='../referenties/gemini_gekozen_oddish.png'
# index: 0 transp, 1 zwart, 2-5 turquoise (selout, schaduw, midden, licht), 6-9 kelp (selout, schaduw, midden, licht), 10-11 rood, 12 glans oog
PAL=[(152,208,160),(16,16,16),(44,99,85),(66,138,122),(98,180,150),(160,210,186),(86,66,12),(142,124,24),(184,162,54),(218,198,120),(122,34,30),(206,72,62),(248,218,200)]
def model_op_schaal():
    m=Image.open(MODEL).convert('RGB'); k=10.24/S
    ox=10.25+10.24*(U0-PHX)-X0*k; oy=10.25+10.24*(V0-PHY)-Y0*k
    big=Image.new('RGB',(2048,2048),'white'); big.paste(m,(512,512))
    return big.crop((int(ox+512),int(oy+512),int(ox+512+64*k),int(oy+512+64*k))).resize((64,64),Image.BOX)
def rgb(o,bg=None):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg if bg else PAL[0]
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
def label(mask,acht=True):
    # verbonden componenten (zonder scipy)
    lab=np.zeros(mask.shape,int); n=0
    nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] if acht else [(-1,0),(1,0),(0,-1),(0,1)]
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n
        while st:
            cy,cx=st.pop()
            for dy,dx in nb:
                yy,xx=cy+dy,cx+dx
                if 0<=yy<mask.shape[0] and 0<=xx<mask.shape[1] and mask[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
    return lab,n
