# Guarana fase 2, r16 (start r15): zie onderaan (__main__): alleen omcirkelde vruchten rond + kijkrichting; rest = r15.
# Kop van r15:
# Guarana fase 2, r15 (start r14). Jordi: "nu weer geen enkel oog dat de goede kant op kijkt, blijven in rondjes gaan. de tros rechts is ook geen geheel meer"
# + "er moeten tenminste een paar ogen naar linksonder kijken zoals in fase 1" / "heb ik toch al gezegd"
# + "de vormen van links en midden zijn verder oke, al heeft links onderin een heel verlept stukje fruit ipv recht en is midden op plekken iets te hard belijnd".
# Wijzigingen t.o.v. r14: (1) ogen: 4 ogen = fase 1-oog pixel voor pixel (OOG_F1A/OOG_F1B), de rest volgens SPEC-regel 5/6; (2) rechtertros
# compacter (sp 1,3 -> 1,1), zelfde vruchtmaat; (3) linkertros: vrucht G (linksonder) volledig rond voor E; (4) binnenlijnen: dubbele/zwarte
# lijnen tussen vruchten binnen een tros -> 1 px lijnrood. Vanuit guarana_fase2/: python3 sprite_r15/bouw15.py
import sys; sys.path.insert(0,'sprite_r9'); import numpy as np; from PIL import Image; from gemeen2 import opslaan; from hulp import *
K,L,S,M,H=1,2,3,4,5; W,G=10,11; GROEN=(6,7,8,9); ROOD=(2,3,4,5)
def m2s(u,v): return u*0.06881-2.875, v*0.06881-8.24       # modelpixel (1024) -> r13-spritecoordinaat (zelfde ijking als r9-r13)
# r15: H (onderste vrucht linkertros, was een spitse peer die verlept oogde) is een volle ronde vrucht; G staat nu voor E (was een sikkel achter E)
# open oogvruchten minstens 36 breed (9 px), zodat het fase 1-oog (7 breed) erin past: F, u, q iets breder dan in het model
# vrucht: (naam, cx, cy, rx, ry, soort, pupil) in modelpixels; volgorde = achter -> voor. soort: d=dicht, p=dicht peer, o=open oog,
# h=half dicht oog, k=klein/gedeeltelijk oog. pupil: c midden, l links, ll linksonder, d onder, lb linksboven
TROSSEN={
 'L':dict(anker=(240,440),vr=[
   ('E',170,598,36,34,'d',None),('G',217,635,33,35,'d',None),('C',318,522,30,37,'k','KL14'),('H',268,676,37,37,'d',None),
   ('A',178,505,38,45,'h','HALF7'),('B (L2)',263,490,38,45,'o','MIDDEN'),('D',258,575,38,42,'o','F1A'),('F',302,612,36,38,'o','D14')]),
 'M':dict(anker=(460,295),vr=[
   ('f',382,478,33,28,'d',None),('M2',378,415,27,22,'h','HALF6'),
   ('c',380,372,30,30,'d',None),('d',432,437,38,35,'d',None),('g',422,528,37,37,'d',None),('h',480,495,37,37,'d',None),
   ('a (H1)',432,342,38,44,'h','HALF7'),('b (M1)',520,337,40,37,'o','F1B'),('e',507,423,37,40,'o','L14')]),
 'R':dict(anker=(790,435),vr=[
   ('r (R1)',692,510,28,35,'k','KL14'),('t',842,570,38,38,'d',None),
   ('p (RT)',748,472,38,38,'o','F1A'),('q (R2)',836,482,38,40,'o','MIDDEN'),('s',757,565,38,40,'o','L14'),('u (R5)',707,605,36,37,'o','F1B'),
   ('v',792,632,37,37,'d',None),('w',757,667,37,37,'d',None)]),
}
def vorm(cx,cy,rx,ry,peer):
    cx=np.floor(cx)+0.5; cy=np.floor(cy)+0.5     # midden op een pixelmidden: oneven breedte, symmetrisch rond (3-5-7-9-9-9-7-5-3)
    s=set()
    for y in range(int(cy-ry-2),int(cy+ry+3)):
        for x in range(int(cx-rx-2),int(cx+rx+3)):
            u=(x+.5-cx)/rx; v=(y+.5-cy)/ry
            if peer and v>0: u=u/(1-0.38*v)
            if u*u+v*v<=1.0: s.add((x,y))     # iets ruitachtiger dan een ellips: kortere platte toppen/zijkanten
    return s
def tros(naam,sp,sr,dx=0,dy=0):
    # sp = schaal van de posities om de takpunt (anker), sr = schaal van de vruchten zelf; dx,dy = verschuiving van de hele tros
    T=TROSSEN[naam]; ax,ay=m2s(*T['anker']); out=[]
    for n,cx,cy,rx,ry,soort,pup in T['vr']:
        x,y=m2s(cx,cy); x=ax+(x-ax)*sp+dx; y=ay+(y-ay)*sp+dy; a,b=rx*0.06881*sr,ry*0.06881*sr
        x=np.floor(x)+0.5; y=np.floor(y)+0.5
        out.append(dict(n=n,cx=x,cy=y,rx=a,ry=b,soort=soort,pup=pup,F=vorm(x,y,a,b,soort=='p')))
    return out
# ogen als sjablonen (rij voor rij). F1A/F1B = fase 1-oog pixel voor pixel gekopieerd uit guarana/af/guarana.png:
# F1A = bovenste oog (x16-22, y17-23), F1B = onderste oog (x14-20, y27-33); wit, pupil en schil exact (schil daar lijnrood links/boven, zwart rechts/onder).
# De andere ogen volgens SPEC-regel 5/6 (schil lijnrood rondom). W wit, K zwart (pupil of fase 1-schil), L lijnrood, '.' = vrucht blijft.
OOG={
 'F1A':[".LLLL..",".LWWWK.","LWWWWWK","LWPPWWK","LWPPWWK",".KWWWK.","..KKK.."],
 'F1B':["..LLL..",".LWWWK.","LWWWWWK","LWPPWWK","LWPPWWK","KKWWWK.",".LKKK.."],
 'MIDDEN':["..LL..",".LWWL.","LWPPWL","LWPPWL",".LWWL.","..LL.."],                 # L2/R2: pupil 2x2 precies in het midden van wit 2-4-4-2
 'O45':["..LL..",".LWWL.","LWWWWL","LWPPWL","LWPPWL",".LWWL.","..LL.."],                 # 0 links, 1/2 onder
 'O54':["..LLL..",".LWWWL.","LWPPWWL","LWPPWWL",".LWWWL.","..LLL.."],                    # 1/2 links, 0 onder
 'ORO':["..LL..",".LWWL.","LWWWWL","LWWPPL",".LWPL.","..LL.."],                       # andere kant: rechtsonder (klein oog, past tussen RT en R5)
 'KL_L':["..LL..",".LWWL.","LPWWWL",".LWWL.","..LL.."],                                   # klein, andere kant: links
 'KL_R':["..LL..",".LWWL.","LWWWPL",".LWWL.","..LL.."],                                   # klein, andere kant: rechts
 'L14':["..LLL..",".LWWWL.","LPPWWWL","LPPWWWL",".LWWWL.","..LLL.."],                 # r16: pupilplek r14 ('groot','l'), schil r15
 'D14':["..LLL..",".LWWWL.","LWWWWWL","LWWPPWL",".LWPPL.","..LLL.."],                 # r16: pupilplek r14 ('groot','d')
 'KL14':[".LL..","LWWL.","LPPWL",".LWWL","..LL."],                                    # r16: klein oog r14-vorm, pupil links (niet linksonder: alleen a-d kijken driekwart)
 'HALF7':["..LLL..",".LMMML.","LPPWWWL",".LWWWL.","..LLL.."],                       # half dicht: gebogen lid van vruchthuid (M), pupil links tegen het lid
 'HALF6':["..LL..",".LMML.","LPPWWL",".LWWL.","..LL.."],
}
# P = pupil (zwart)
CH={'L':2,'K':1,'W':10,'M':4,'P':1}
def stempel(naam,cx,cy,half=False):
    T=OOG[naam]; h,w=len(T),len(T[0])
    ox=int(np.floor(cx))-(w-1)//2; oy=int(np.floor(cy))-((h-1)//2 if not half else 1)
    return {(ox+i,oy+j):CH[c] for j,r in enumerate(T) for i,c in enumerate(r) if c!='.'},(ox,oy)
def pupilplek(naam,d):
    T=OOG[naam]; h,w=len(T),len(T[0]); xs=[x for x,y in d]; ys=[y for x,y in d]
    ox,oy=min(xs)-min(i for r in T for i,c in enumerate(r) if c!='.'),min(ys)
    return {(ox+i,oy+j) for j,r in enumerate(T) for i,c in enumerate(r) if c=='P'},{(ox+i,oy+j) for j,r in enumerate(T) for i,c in enumerate(r) if c in 'WP'}
def randvan(f,q): return q in f['F'] and any((q[0]+b,q[1]+a) not in f['F'] for a,b in N4)
def bouw_tros(vr):
    lab={}
    for i,f in enumerate(vr):
        for p in f['F']: lab[p]=i
    pix={}
    for p,i in lab.items():
        f=vr[i]; x,y=p; u=(x+.5-f['cx'])/f['rx']; v=(y+.5-f['cy'])/f['ry']
        rand=[(ddy,ddx) for ddy,ddx in N4 if (x+ddx,y+ddy) not in f['F']]
        buiten=[q for q in rand if (x+q[1],y+q[0]) not in lab]
        achter=[q for q in rand if (x+q[1],y+q[0]) in lab]      # buur hoort bij een andere (achterliggende) vrucht
        if buiten:
            pix[p]=K if (u+v>0.15 or any(q in ((1,0),(0,1)) for q in buiten) and u+v>-0.5) else L
        elif achter:
            pix[p]=S if u+v>0.6 else L     # naad: lijnrood; aan de schaduwkant (rechtsonder) schaduwtint

        else:
            # sikkel: de pixel rechts/onder/rechtsonder is de rand van de eigen (volledige) vrucht
            binnenrand=any(randvan(f,(x+ddx,y+ddy)) for ddy,ddx in ((1,0),(0,1),(1,1)))
            if binnenrand and u+v>0.35: pix[p]=S
            elif (u+0.36)**2+(v+0.40)**2<0.14: pix[p]=H
            else: pix[p]=M
    # binnenlijnen: zwart binnen de tros -> lijnrood; twee lijnpixels van verschillende vruchten naast elkaar (dubbele naad) -> de achterste wordt vrucht
    binnen=lambda q: all((q[0]+b,q[1]+a) in lab for a,b in N4)
    for q,c in list(pix.items()):
        if c==K and binnen(q): pix[q]=L
    for q,c in list(pix.items()):
        if c!=L or not binnen(q): continue
        i=lab[q]
        for a,b in N4:
            r=(q[0]+b,q[1]+a); j=lab.get(r)
            if j is not None and j!=i and pix.get(r)==L and binnen(r):
                k,z=(q,i) if i<j else (r,j)      # achterste (lagere index) wordt vrucht
                f=vr[z]; u=(k[0]+.5-f['cx'])/f['rx']; v=(k[1]+.5-f['cy'])/f['ry']
                pix[k]=S if u+v>0.55 else M
    # ogen bovenop (de opengebarsten vrucht steekt naar voren), binnen de eigen vruchtvorm. Plek: midden van de vrucht; overlapt of raakt
    # het oog een ander oog (dikke dubbele lijn), dan max. 1 px opschuiven binnen de vrucht. Een paar rondes, zodat elk oog met alle andere rekening houdt.
    ogen=[i for i,f in enumerate(vr) if f['soort'] in 'ohk']
    plek={i:(0,0) for i in ogen}
    def st(i,dd): f=vr[i]; return stempel(f['pup'],f['cx']+dd[0],f['cy']+dd[1],half=f['soort']=='h')[0]
    for ronde in range(4):
        for i in ogen:
            f=vr[i]; ander=set().union(*[set(st(j,plek[j])) for j in ogen if j!=i])
            keus=None
            for dd in ((0,0),(0,1),(1,0),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)):
                d=st(i,dd); uit=len(d)-sum(q in f['F'] for q in d)
                over=sum(q in ander for q in d); raakt=sum(any((q[0]+b,q[1]+a) in ander for a,b in N4) for q in d)
                sc=(uit>(1 if f['soort']=='h' else 0), over, raakt, abs(dd[0])+abs(dd[1]))
                if keus is None or sc<keus[0]: keus=(sc,dd)
            plek[i]=keus[1]
    for i in ogen:
        if vr[i]['n'] in OOGPLEK_R15: plek[i]=OOGPLEK_R15[vr[i]['n']]   # r16: elk oog op dezelfde plek als in r15
    oogpix=set()
    for i in ogen:
        f=vr[i]; d=st(i,plek[i]); f['oog']=d; f['oogverschuiving']=plek[i]
        for q,c in d.items():
            if q in f['F']: pix[q]=c; oogpix.add(q)
    # geen dubbele lijn langs een oog: lijnrood van een andere vrucht dat direct tegen de oogschil ligt wordt vrucht
    for q,c in list(pix.items()):
        if c!=L or q in oogpix or not binnen(q): continue
        if any((q[0]+b,q[1]+a) in oogpix and pix[(q[0]+b,q[1]+a)] in (L,K) for a,b in N4):
            f=vr[lab[q]]; u=(q[0]+.5-f['cx'])/f['rx']; v=(q[1]+.5-f['cy'])/f['ry']
            pix[q]=S if u+v>0.55 else M
    return pix,lab
def _plek_r15():
    # oogverschuivingen precies zoals r15 (sprite_r15/bouw15.py) ze koos
    import bouw15 as V; d={}
    for n in 'LMR':
        vr=V.tros(n,*V.INSTEL[n]); V.bouw_tros(vr); d.update({f['n']:f['oogverschuiving'] for f in vr if 'oog' in f})
    return d
OOGPLEK_R15={}
INSTEL={'L':(1.05,1.6,-5,0),'M':(1.05,1.6,0,0),'R':(1.1,1.6,0,0)}   # sp, sr, dx, dy per tros
def oude_tros(o):
    # rood/wit/grijs van r13 + zwart dat alleen aan tros grenst (geen groen in de 8-buurt)
    m=np.isin(o,ROOD+(W,G))
    for y,x in zip(*np.where(o==K)):
        nb=[o[y+a,x+b] for a,b in N8 if ok(y+a,x+b)]
        if any(v in ROOD+(W,G) for v in nb) and not any(v in GROEN for v in nb): m[y,x]=True
    return m
def maak(src='sprite_r13/guarana2_r13.png',instel=INSTEL):
    o=np.array(Image.open(src)).astype(int); o0=o.copy()
    oud=oude_tros(o0); o[oud]=0
    alle={}; info={}
    for n,(sp,sr,dx,dy) in instel.items():
        vr=tros(n,sp,sr,dx,dy); pix,lab=bouw_tros(vr); info[n]=(vr,pix)
        for p,c in pix.items(): alle[p]=(n,c)
    for (x,y),(n,c) in alle.items():
        if ok(y,x): o[y,x]=c
    # oude trospixels die niet afgedekt zijn: achtergrond (zo ontstaat de ruimte tussen de trossen), behalve gaatjes die
    # rondom dicht zitten (alle 4 buren gevuld): die worden naad (lijnrood) tussen rood, of donkerste groen tussen groen
    gat=[(x,y) for y,x in zip(*np.where(oud)) if o[y,x]==0]
    for _ in range(3):
        for (x,y) in gat:
            if o[y,x]: continue
            nb=[o[y+a,x+b] for a,b in N4 if ok(y+a,x+b)]
            if sum(v!=0 for v in nb)>=4:
                o[y,x]=L if sum(v in ROOD for v in nb)>=sum(v in GROEN for v in nb) else 6
    return o,o0,oud,info
if __name__=='__main__' or True:
    pass
if True:
    if not OOGPLEK_R15: sys.path.insert(0,'sprite_r15'); OOGPLEK_R15.update(_plek_r15())
if __name__=='__main__':
    # r16: r15 blijft, alleen in de zones wordt de nieuwe opbouw overgenomen:
    #  - omcirkeld (sprite_r15/jordi_niet_rond.png): middelste tros onderste vruchten g en h, rechtertros onderste vruchten v en w -> rond, voor de rest
    #  - ogen waarvan de kijkrichting terug moet naar r14: F, e, s, C, R1 (stempel r15 + stempel r16)
    import bouw15 as V
    o,o0,oud,info=maak()
    r15=np.array(Image.open('sprite_r15/guarana2_r15.png')).astype(int)
    zone=set()
    for n,namen in (('M',('g','h')),('R',('v','w'))):
        for mod in (V,sys.modules[__name__]):
            for f in mod.tros(n,*mod.INSTEL[n]):
                if f['n'] in namen: zone|=f['F']
    oog_anders={'L':('C','F'),'M':('e',),'R':('r (R1)','s')}
    for n,namen in oog_anders.items():
        for mod in (V,sys.modules[__name__]):
            vr=mod.tros(n,*mod.INSTEL[n]); mod.bouw_tros(vr)
            for f in vr:
                if f['n'] in namen: zone|=set(f['oog'])
    zone|={(x+b,y+a) for (x,y) in zone for a in (-1,0,1) for b in (-1,0,1)}   # 1 px rand, voor de buitenlijn
    uit=r15.copy()
    for (x,y) in zone:
        if ok(y,x): uit[y,x]=o[y,x]
    Z=np.zeros((64,64),bool)
    for (x,y) in zone:
        if ok(y,x): Z[y,x]=True
    print('zone',int(Z.sum()),'px; anders dan r15 binnen zone',int(((uit!=r15)&Z).sum()),'buiten zone',int(((uit!=r15)&~Z).sum()))
    np.save('sprite_r16/zone.npy',Z)
    opslaan(uit,'sprite_r16/guarana2_r16.png'); open('sprite_r16/normal.pal','w').write(open('sprite_r15/normal.pal').read())
