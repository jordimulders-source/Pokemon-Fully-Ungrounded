# Hulpfuncties kleurronde: laden, opslaan, bewijs, vel.
from PIL import Image
import numpy as np, os
HIER=os.path.dirname(os.path.abspath(__file__))
TEMPEL=os.path.abspath(os.path.join(HIER,'..','..'))
AF=os.path.join(TEMPEL,'af','tempel.png')
def laad(p=AF):
    im=Image.open(p); return np.array(im), im.getpalette()[:48]
def bewaar(a,pal,p):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(pal+[0]*(768-len(pal)))
    im.info['transparency']=0; im.save(p,transparency=0)
def rgb(a,pal):
    P=np.array(pal).reshape(-1,3); return P[a]
OGEN=[(13,38,16,42),(22,38,25,42)]
def deurmasker(a0):
    m=np.zeros(a0.shape,bool)
    m[a0==12]=True
    # zwarte onderrand binnen de deuropening
    for y in range(48,60):
        for x in range(16,24):
            if a0[y,x]==1: m[y,x]=True
    return m
def bewijs(a,pal,a0,pal0):
    out=[]
    alpha=((a!=0)!=(a0!=0)).sum(); out.append('alpha diff: %d'%alpha)
    R,R0=rgb(a,pal),rgb(a0,pal0)
    for (x0,y0,x1,y1) in OGEN:
        d=(R[y0:y1+1,x0:x1+1]!=R0[y0:y1+1,x0:x1+1]).any(2).sum(); out.append('oog x%d-%d y%d-%d diff: %d'%(x0,x1,y0,y1,d))
    m=deurmasker(a0); d=((R!=R0).any(2)&m).sum(); out.append('deurgat (%d px) diff: %d'%(m.sum(),d))
    out.append('kleuren gebruikt (incl. transparant): %d'%len(np.unique(a)))
    out.append('pixels veranderd t.o.v. af: %d'%(R!=R0).any(2).sum())
    return '\n'.join(out)
def vel(a,pal,a0,pal0,model,p):
    from PIL import ImageDraw
    def rgba(a,pal):
        R=rgb(a,pal).astype('uint8'); A=np.where(a==0,0,255).astype('uint8')
        return Image.fromarray(np.dstack([R,A]),'RGBA')
    k,o=rgba(a,pal),rgba(a0,pal0)
    m=Image.open(model).convert('RGB').resize((512,512),Image.LANCZOS)
    W=Image.new('RGB',(512*3+40,512+20+12*30+20),(236,236,236))
    for i,im in enumerate([k,o]):
        bg=Image.new('RGB',(512,512),(255,255,255)); big=im.resize((512,512),Image.NEAREST); bg.paste(big,(0,0),big); W.paste(bg,(10+i*522,10))
    W.paste(m,(10+2*522,10))
    # stuk op 12x: stenen rechts-midden
    crop=k.crop((26,26,56,56)).resize((360,360),Image.NEAREST); bg=Image.new('RGB',(360,360),(255,255,255)); bg.paste(crop,(0,0),crop); W.paste(bg,(10,532))
    crop=k.crop((2,30,32,60)).resize((360,360),Image.NEAREST); bg=Image.new('RGB',(360,360),(255,255,255)); bg.paste(crop,(0,0),crop); W.paste(bg,(380,532))
    for j,c in enumerate([(255,255,255),(40,40,48),(152,208,160)]):
        bg=Image.new('RGB',(64,64),c); bg.paste(k,(0,0),k); W.paste(bg,(760+j*74,532))
        bg=Image.new('RGB',(64,64),c); bg.paste(o,(0,0),o); W.paste(bg,(760+j*74,606))
    d=ImageDraw.Draw(W); d.text((760,690),'boven: nieuw 1x, onder: af 1x',fill=(0,0,0))
    W.save(p)
