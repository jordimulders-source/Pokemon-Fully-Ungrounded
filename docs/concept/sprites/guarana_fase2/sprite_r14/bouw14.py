# Guarana fase 2, r14 (start r13). Jordi: "nu zijn een hoop van de vruchten te rechthoekig. En ik realiseer me nu dat het helemaal niet ten koste
# van de sprite gaat als de vruchttrossen gewoon wat groter maken ... overlappen is toch niet erg, zolang ze elkaar maar niet overlappen"
# + "ja en er moet iets ruimte tussen zitten, desnoods schuif je de linker maar iets naar links".
# Liaan/blad/takken/lussen/ranken = r13. De drie trossen worden opnieuw opgebouwd uit de vruchten van het model (positie, maat, open/dicht,
# volgorde voor/achter), vergroot om de takpunt, als ronde vruchten in fase 1-stijl (buitenlijn lijnrood linksboven / zwart rechtsonder,
# naden lijnrood, hooglicht linksboven, schaduwsikkel rechtsonder) met het fase 1-oog. Vanuit guarana_fase2/: python3 sprite_r14/bouw14.py
import sys; sys.path.insert(0,'sprite_r9'); import numpy as np; from PIL import Image; from gemeen2 import opslaan; from hulp import *
K,L,S,M,H=1,2,3,4,5; W,G=10,11; GROEN=(6,7,8,9); ROOD=(2,3,4,5)
def m2s(u,v): return u*0.06881-2.875, v*0.06881-8.24       # modelpixel (1024) -> r13-spritecoordinaat (zelfde ijking als r9-r13)
# open oogvruchten minstens 36 breed (9 px), zodat het fase 1-oog (7 breed) erin past: F, u, q iets breder dan in het model
# vrucht: (naam, cx, cy, rx, ry, soort, pupil) in modelpixels; volgorde = achter -> voor. soort: d=dicht, p=dicht peer, o=open oog,
# h=half dicht oog, k=klein/gedeeltelijk oog. pupil: c midden, l links, ll linksonder, d onder, lb linksboven
TROSSEN={
 'L':dict(anker=(240,440),vr=[
   ('G',217,635,33,35,'d',None),('E',170,598,36,34,'d',None),('C',318,522,30,37,'k','l'),('H',268,682,28,40,'p',None),
   ('A',178,505,38,45,'h','l'),('B (L2)',263,490,38,45,'o','c'),('D',258,575,38,42,'o','ll'),('F',302,612,36,38,'o','d')]),
 'M':dict(anker=(460,295),vr=[
   ('g',422,528,24,33,'p',None),('h',480,495,30,37,'p',None),('f',382,478,33,28,'d',None),('M2',378,415,27,22,'h','l'),
   ('c',380,372,30,30,'d',None),('d',432,437,38,35,'d',None),('a (H1)',432,342,38,44,'h','ll'),('b (M1)',520,337,40,37,'o','ll'),
   ('e',507,423,37,40,'o','l')]),
 'R':dict(anker=(790,435),vr=[
   ('r (R1)',692,510,28,35,'k','l'),('t',842,570,38,38,'d',None),('w',757,667,33,43,'p',None),('v',792,632,28,38,'p',None),
   ('p (RT)',748,472,38,38,'o','ll'),('q (R2)',836,482,38,40,'o','c'),('s',757,565,38,40,'o','l'),('u (R5)',707,605,36,37,'o','ll')]),
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
# ogen: witmasker (rij -> kolommen), schil = N4-ring (rond), lijnrood linksboven, zwart rechtsonder (fase 1)
WIT={'groot':[(1,3),(0,4),(0,4),(1,3)],'norm':[(1,2),(0,3),(0,3),(1,2)],'klein':[(0,1),(0,2),(1,2)]}
PUP={('groot','c'):[(2,1),(3,1),(2,2),(3,2)],('groot','l'):[(0,1),(1,1),(0,2),(1,2)],('groot','ll'):[(1,2),(2,2),(1,3),(2,3)],('groot','lm'):[(1,1),(2,1),(1,2),(2,2)],
     ('groot','d'):[(2,2),(3,2),(2,3),(3,3)],
     ('norm','c'):[(1,1),(2,1),(1,2),(2,2)],('norm','l'):[(0,1),(1,1),(0,2),(1,2)],('norm','ll'):[(0,2),(1,2),(1,3)],
     ('norm','d'):[(1,2),(2,2)],('klein','l'):[(0,1),(1,2)]}
def oog(maat,pup,half=False):
    w={(x,y) for y,(a,b) in enumerate(WIT[maat]) for x in range(a,b+1)}
    if half: w={(x,y) for (x,y) in w if y>=2}     # bovenste 2 rijen wit worden ooglid (vruchthuid)
    cx=sum(x for x,y in w)/len(w); cy=sum(y for x,y in w)/len(w)
    if half: cy-=1
    d={}
    for (x,y) in w:
        for ddy,ddx in N4:
            p=(x+ddx,y+ddy)
            if p in w or p in d: continue
            ex,ey=p[0]-cx,p[1]-cy
            d[p]=L if ((ex<=0 and ey<=0.5) or (ey<0 and ex<=1)) else K
    for p in w: d[p]=W
    pp=PUP[(maat,pup)]
    if half: pp=[(x,y) for (x,y) in [(a,b+1) for a,b in pp] if (x,y) in w][:3] or [min(w)]
    for p in pp:
        if p in w: d[p]=K
    return d,cx,cy
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
            pix[p]=S if u+v>0.9 else L     # naad: lijnrood; aan de schaduwkant (rechtsonder) schaduwtint

        else:
            # sikkel: de pixel rechts/onder/rechtsonder is de rand van de eigen (volledige) vrucht
            binnenrand=any(randvan(f,(x+ddx,y+ddy)) for ddy,ddx in ((1,0),(0,1),(1,1)))
            if binnenrand and u+v>0.55: pix[p]=S
            elif (u+0.36)**2+(v+0.40)**2<0.14: pix[p]=H
            else: pix[p]=M
    # ogen
    for i,f in enumerate(vr):
        if f['soort'] not in 'ohk': continue
        maat={'o':'groot' if f['pup']!='c' else 'norm','h':'groot' if f['rx']*2>=8.6 else 'norm','k':'klein'}[f['soort']]
        d,ex,ey=oog(maat,f['pup'],half=f['soort']=='h')
        ox=round(f['cx']-ex-0.5); oy=round(f['cy']-ey-0.5-(0.4 if f['soort']=='o' else 0))
        if f['soort']=='k': ox=round(f['cx']-ex-0.5)
        for (x,y),c in d.items():
            q=(x+ox,y+oy)
            if q in f["F"] and q in lab: pix[q]=c     # oog ligt bovenop (de opengebarsten vrucht steekt naar voren), binnen de eigen vruchtvorm
    return pix,lab
INSTEL={'L':(1.05,1.6,-5,0),'M':(1.05,1.6,0,0),'R':(1.3,1.6,0,0)}   # sp, sr, dx, dy per tros
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
if __name__=='__main__':
    o,o0,oud,info=maak()
    nieuw=np.zeros((64,64),bool)
    for n in info:
        for (x,y) in info[n][1]:
            if ok(y,x): nieuw[y,x]=True
    blijft=oud&~nieuw
    print('oud trospixel niet afgedekt:',int(blijft.sum()),list(zip(*np.where(blijft)))[:40])
    opslaan(o,'sprite_r14/guarana2_r14.png'); open('sprite_r14/normal.pal','w').write(open('sprite_r13/normal.pal').read())
