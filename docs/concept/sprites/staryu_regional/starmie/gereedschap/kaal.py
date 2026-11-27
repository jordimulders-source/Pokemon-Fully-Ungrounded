# kaal.py: kale samenstelling (geen reparaties).
#  voorste ster = oppervlakgewogen reductie van het model (natief raster, alleen binnen de voorste-stermasker);
#  achterste punten = Gen 3-Starmie, punten van set B (zie gen3.py), pixel voor pixel, Gen 3-tint -> koektint.
import sys; sys.path.insert(0,'gereedschap'); from gemeen import *
KT=[(100,2),(118,3),(150,4),(185,5),(999,6)]      # koek: gemiddelde modelhelderheid -> tint
PT=[(138,8),(185,9),(999,10)]                     # paars glazuur/juweel
HG={'rood':12,'groen':13,'blauw':14,'geel':15}
G3MAP={1:5,2:4,3:3,4:2,14:1}                      # Gen 3 paars (licht..donker, zwart) -> koek
def tint(tab,L):
    for t,k in tab:
        if L<t: return k
def voorste():
    a=natief(); vm=voor_mask(a); K=np.empty((99,99),object)
    for v in range(99):
        for u in range(99): K[v,u]=klasse(a[v,u]) if vm[v,u] else None
    o=np.zeros((64,64),int); fm=np.zeros((64,64),bool)
    for Y in range(64):
        for X in range(64):
            fr={}; Ls={}; tw=0
            for u,v,w in overlap(X,Y):
                k=K[v,u]
                if k is None: continue
                tw+=w; fr[k]=fr.get(k,0)+w; Ls.setdefault(k,[]).append((w,a[v,u].mean()))
            if tw<0.5: continue
            fm[Y,X]=True
            f={k:x/tw for k,x in fr.items()}
            if f.get('zwart',0)>=0.3: o[Y,X]=1; continue
            h=max(HG,key=lambda k:f.get(k,0))
            if f.get(h,0)>=0.3: o[Y,X]=HG[h]; continue
            if f.get('wit',0)>=0.35: o[Y,X]=11; continue
            if f.get('plijn',0)>=0.3: o[Y,X]=7; continue
            k='paars' if f.get('paars',0)+f.get('plijn',0)+f.get('wit',0)*0.5>=f.get('koek',0)+f.get('zwart',0) else 'koek'
            src=Ls.get(k) or Ls.get('plijn') or Ls.get('zwart') or [(1,60)]
            L=sum(w*l for w,l in src)/sum(w for w,l in src)
            o[Y,X]=tint(PT if k=='paars' else KT,L)
    return o,fm
def achterste(fm):
    g,pal=laad_g3(); o=np.zeros((64,64),int); extra=[]
    for y,x in zip(*np.where(g>0)):
        if fm[y,x] or punt_van(x,y) not in SETB: continue
        if g[y,x] in G3MAP: o[y,x]=G3MAP[g[y,x]]
        else: extra.append((x,y))
    # Gen 3-goudpixels in een set B-sector (de gouden kernpunt lag over de achterste punt): tint van de
    # dichtstbijzijnde paarse pixel van dezelfde punt
    for x,y in extra:
        best=None
        for yy,xx in zip(*np.where(o>0)):
            if punt_van(xx,yy)!=punt_van(x,y): continue
            d=(xx-x)**2+(yy-y)**2
            if best is None or d<best[0]: best=(d,o[yy,xx])
        o[y,x]=best[1]
    return o,extra
def kaal():
    f,fm=voorste(); b,extra=achterste(fm)
    o=np.where(fm,f,b); return o,fm,extra
if __name__=='__main__':
    o,fm,extra=kaal(); opslaan(o,sys.argv[1] if len(sys.argv)>1 else 'sprite_r1/kaal.png')
    print('voor',fm.sum(),'achter',((o>0)&~fm).sum(),'goud->koek',extra); toon(o)
