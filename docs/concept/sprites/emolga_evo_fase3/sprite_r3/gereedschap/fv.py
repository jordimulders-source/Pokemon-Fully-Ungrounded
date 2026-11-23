# Gedeelde hulpjes fruitvampier (Emolga-lijn fase 3). Model = Gemini r6 met lijf +25% horizontaal (om x=530), kop/oren/voeten gelijk.
# Natief raster komt uit r6 zelf (natief.py: pitch 10,244/10,240, fase 9,05/9,20 -> 99x99). Elke modelpixel (1024) krijgt de klasse
# van de natieve r6-cel waar hij vandaan komt: identiek (kop, oren, voeten) of via de per rij gemeten rek (rek.py, lijf).
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/'
G=D+'sprite_r1/gereedschap/'
NATIEF=G+'natief_r6.png'
PX,PY=10.244,10.240; FX,FY=9.05+0.5,9.20+0.5     # celgrens = fase+0,5
CX,REK=530,1.25
# klassen (k-means op de natieve voorgrond)
KL='.KDEGyYLMQNOBCW'
MODELKLEUR=[(255,255,255),(8,8,8),(31,31,30),(51,50,42),(58,59,59),(134,123,48),(207,185,59),(242,221,86),
            (66,76,86),(87,101,115),(109,128,148),(149,160,169),(192,199,208),(217,221,224),(239,243,245)]
def klassen_natief(path=NATIEF):
    a=np.asarray(Image.open(path).convert('RGB')).astype(float)
    licht=a.min(2)>=250
    lab,n=label(licht,acht=False)
    buiten=set(lab[0,:])|set(lab[-1,:])|set(lab[:,0])|set(lab[:,-1])
    bg=np.isin(lab,list(buiten))&licht
    bg|=licht   # ingesloten puur wit (>=250) is in r6 alleen de kier tussen de poten (natief x50-51, y5-8): achtergrond
    pal=np.array(MODELKLEUR[1:],float)
    d=((a[:,:,None,:]-pal[None,None])**2).sum(-1)
    c=d.argmin(-1)+1; c[bg]=0
    # antialiasrand: een lichte cel (staalblauw/wit, klassen 9-14) die aan de achtergrond grenst en geen lichte buur heeft
    # (alleen donker eromheen) is een randmengsel van zwarte lijn en witte achtergrond -> achtergrond.
    licht2=np.isin(c,range(9,15)); n=c.copy(); weg=[]
    for v_,u_ in zip(*np.where(licht2)):
        nb=[c[v_+dv,u_+du] for dv,du in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=v_+dv<c.shape[0] and 0<=u_+du<c.shape[1]]
        if 0 in nb and not any(9<=k<=14 for k in nb): n[v_,u_]=0; weg.append((u_,v_))
    klassen_natief.weg=weg
    return a,n
def label(mask,acht=True):
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
def box(e,r):
    # vensterom (2r+1)^2 via integraalbeeld
    p=np.pad(e,r,mode='edge'); I=np.pad(p.cumsum(0).cumsum(1),((1,0),(1,0))); k=2*r+1
    return I[k:,k:]-I[:-k,k:]-I[k:,:-k]+I[:-k,:-k]
REK=np.load(G+'rek.npy') if __import__('os').path.exists(G+'rek.npy') else None
def bronx():
    # r6-bron-x per modelpixel volgens de per rij gemeten rek (rek.py)
    xx=np.arange(1024)[None,:].astype(float)
    s=REK[:,0:1]; c=REK[:,1:2]
    return c+(xx-c)/s
def regio():
    # True = gerekt lijf, False = identiek (kop/oren/voeten). Per modelpixel de kleinste fout (11x11 venster).
    m=np.asarray(Image.open(D+'model/model.png').convert('RGB')).astype(int)
    r=np.asarray(Image.open(D+'gemini/r6.png').convert('RGB')).astype(int)
    src=np.clip(np.round(bronx()).astype(int),0,1023); yy=np.arange(1024)[:,None].repeat(1024,1)
    eid=np.abs(m-r).sum(2).astype(float); est=np.abs(m-r[yy,src]).sum(2).astype(float)
    eid=box(eid,5); est=box(est,5)
    reg=est<eid
    reg[REK[:,0]==1]=False
    return reg
def klassenkaart():
    a,c=klassen_natief(); reg=regio()
    yy,xx=np.mgrid[0:1024,0:1024].astype(float)
    xs=np.where(reg,bronx(),xx)
    u=np.clip(np.floor((xs-FX)/PX).astype(int),0,98); v=np.clip(np.floor((yy-FY)/PY).astype(int),0,98)
    return c[v,u],reg
def toon(o,ch=KL,y0=0,y1=None,x0=0,x1=None):
    y1=y1 or o.shape[0]; x1=x1 or o.shape[1]
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(ch[v] for v in o[y,x0:x1]))
def rgbk(o,bg=(255,255,255),kleuren=None):
    kleuren=kleuren or MODELKLEUR
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg
    for k in range(1,len(kleuren)): img[o==k]=kleuren[k]
    return Image.fromarray(img)
def reduceer(c,dx=-16,drempel=0.45,nk=15):
    # 1024-klassenkaart -> 64x64: spritepixel (X,Y) = modelblok x in [16X-dx', ...) met dx = verschuiving in modelpixels.
    # meerderheidsklasse (geen mengtinten); silhouet = bedekking >= drempel.
    s=np.zeros((1024,1024+32),int); s[:,16+dx if dx>-16 else 0:][:, :0]=0
    p=np.zeros((1024,1024+64),int); p[:,32-dx:32-dx+1024]=c       # verschuif: modelx -> px = x+32-dx
    p=p[:,32:32+1024]                                                 # sprite X = (x-dx)//16
    b=p.reshape(64,16,64,16).transpose(0,2,1,3).reshape(64,64,256)
    cov=np.stack([(b==k).mean(-1) for k in range(nk)],-1)
    fg=1-cov[...,0]; w=cov.copy(); w[...,0]=0
    o=w.argmax(-1); o[fg<drempel]=0
    return o,cov
def reduceer2(c,dx=16,drempel=0.45,kprio=0.30,nk=15,prio=(1,)):
    # zoals reduceer, maar lijnklassen (prio, standaard K) winnen vanaf bedekking kprio: 1-px modellijnen blijven staan.
    o,cov=reduceer(c,dx,drempel,nk)
    for k in prio:
        m=(o>0)&(cov[...,k]>=kprio); o[m]=k
    return o,cov
# Samengevoegde klassen (technisch: geen mengtinten): E(antialias zwart/geel)->D, Q->M, O->N, C->B.
# Nieuwe nummering: 0 . | 1 K | 2 D | 3 G | 4 y | 5 Y | 6 L | 7 M | 8 N | 9 B | 10 W
KL2='.KDGyYLMNBW'
SAMEN={0:0,1:1,2:2,3:2,4:3,5:4,6:5,7:6,8:7,9:7,10:8,11:8,12:9,13:9,14:10}
KLEUR2=[(255,255,255),(8,8,8),(31,31,30),(58,59,59),(134,123,48),(207,185,59),(242,221,86),(70,82,96),(120,138,156),(200,206,214),(239,243,245)]
def samen(c):
    lut=np.array([SAMEN[i] for i in range(15)]); return lut[c]
GROEPEN=[(1,2,3),(4,5,6),(7,8),(9,10)]   # donker K/D/G | geel | masker | wit  (klassen KL2)
def reduceer3(c,dx=16,drempel=0.45,kprio=0.35):
    # eerst de kleurgroep met de grootste bedekking (zwart en donker tellen samen), dan de klasse binnen die groep;
    # K wint binnen de donkere groep vanaf kprio (1-px modellijnen).
    o,cov=reduceer(c,dx,drempel,11)
    fg=o>0
    gs=np.stack([cov[...,list(g)].sum(-1) for g in GROEPEN],-1); gi=gs.argmax(-1)
    n=np.zeros_like(o)
    for i,g in enumerate(GROEPEN):
        sub=cov[...,list(g)]; k=np.array(g)[sub.argmax(-1)]
        if i==0: k=np.where(cov[...,1]>=kprio,1,k)
        n=np.where(gi==i,k,n)
    n[~fg]=0
    return n,cov
def modelblokken(dx=16):
    # model.png per spritepixel (16x16-blok, zelfde verschuiving als reduceer): (64,64,256,3)
    m=np.asarray(Image.open(D+'model/model.png').convert('RGB')).astype(int)
    p=np.full((1024,1024+64,3),255); p[:,32-dx:32-dx+1024]=m; p=p[:,32:32+1024]
    return p.reshape(64,16,64,16,3).transpose(0,2,1,3,4).reshape(64,64,256,3)
def silhouet(dx=16,drempel=0.5):
    # silhouet rechtstreeks uit model.png: spritepixel is figuur als < 50% van zijn 16x16-blok achtergrond (min(RGB) >= 245) is.
    # Uitzondering: de kier tussen de poten valt onder 50% en wordt als reparatie gezet (bouw1).
    return (modelblokken(dx).min(-1)>=245).mean(-1)<drempel
def reduceer4(c,dx=16,kprio=0.35):
    # silhouet uit het model, kleurklasse uit de natieve klassenkaart (groep eerst, reduceer3)
    o,cov=reduceer3(c,dx,0.0,kprio)
    fg=silhouet(dx); o[~fg]=0
    leeg=fg&(cov[...,1:].sum(-1)<1e-9)
    for y,x in zip(*np.where(leeg)):
        nb=[o[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if 0<=yy<64 and 0<=xx<64 and o[yy,xx]>0]
        o[y,x]=max(set(nb),key=nb.count) if nb else 1
    return o,cov
