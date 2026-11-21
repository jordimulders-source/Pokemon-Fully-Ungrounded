# Klassen per natieve modelpixel van het Altaria-model (geen tekenen: alleen indelen van modelkleuren).
# 0 achtergrond (bijna-wit, verbonden met de rand) | 1 K zwart/donkerste navy | 2 wolk (blauwgrijs/teal, ook snavel en wang)
# 3 violet (kop, hals, kuif) | 4 static (cyaanwit) | 5 lavendelwit (kuiflichtjes, oogglans)
import numpy as np; from PIL import Image
NAMEN=['bg','K','wolk','violet','static','lavwit']
def klassen(path="gereedschap/natief.png",LS=203):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    licht=a.min(2)>=215
    bg=np.zeros(L.shape,bool); H,W=L.shape; st=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
    for y,x in st: bg[y,x]=licht[y,x]
    st=[p for p in st if bg[p]]
    while st:
        y,x=st.pop()
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and licht[yy,xx] and not bg[yy,xx]: bg[yy,xx]=True; st.append((yy,xx))
    # ingesloten wit (tussen kop en kuifstrengen) is ook achtergrond: puur wit (min>=240), buiten de kop
    wit=a.min(2)>=240; wit[45:65,68:101]=False; bg|=wit
    c=np.zeros(L.shape,int); f=~bg
    c[f]=2
    c[f&(B-G>=45)]=3
    hl=f&(L>=LS)
    c[hl&(G-R>=18)]=4
    c[hl&(G-R<18)]=5
    c[f&(L<30)]=1
    # kuif: de donkere randpixels van de strengen hebben een blauwgrijze tint (vallen anders in 'wolk'); binnen 2 px van violet, boven de vleugels -> violet
    v=(c==3)|(c==5); dil=v.copy()
    for dy in (-2,-1,0,1,2):
        for dx in (-2,-1,0,1,2): dil|=np.roll(np.roll(v,dy,0),dx,1)
    kuif=np.zeros(L.shape,bool); kuif[:44,88:]=True
    c[kuif&dil&(c==2)]=3
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '')
    Image.fromarray(np.array([(255,255,255),(0,0,0),(70,110,140),(100,90,220),(0,255,255),(255,120,255)],'uint8')[c]).resize((796,796),Image.NEAREST).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/4e735dd6-f6a1-5c3e-ad61-ba772ef1cd53/scratchpad/klassen.png')

def statisch(a,c,L):
    """Static-lijntjes in het model: cyaanwitte pixels (L>=203) + dunne lichte lijntjes (1-2 natieve px breed, beide kanten >=35 donkerder,
    cyaan: G-R>=25, L>=135). Kop/snavel/wang (natief x68-100, y45-64) niet (daar is het snavel- en wanglicht). Stukjes < 3 natieve px weg."""
    import numpy as np
    R,G,B=a[...,0],a[...,1],a[...,2]
    cand=(c!=0)&(L>=135)&(G-R>=25)&(c!=3)&(c!=5)
    thin=np.zeros(L.shape,bool)
    for y,x in zip(*np.where(cand)):
        l=L[y,x]
        for dy,dx in ((0,1),(1,0),(1,1),(1,-1)):
            if L[y-dy,x-dx]<=l-35 and L[y+dy,x+dx]<=l-35: thin[y,x]=True
            if (dy,dx) in ((0,1),(1,0)):
                if L[y-dy,x-dx]<=l-35 and L[y+2*dy,x+2*dx]<=l-35 and L[y+dy,x+dx]>=l-25: thin[y,x]=True
                if L[y+dy,x+dx]<=l-35 and L[y-2*dy,x-2*dx]<=l-35 and L[y-dy,x-dx]>=l-25: thin[y,x]=True
    s=(c==4)|thin
    s[45:65,68:101]=False
    from gemeen import label
    lab,n=label(s,acht=True)
    for i in range(1,n+1):
        if (lab==i).sum()<3: s[lab==i]=False
    return s
