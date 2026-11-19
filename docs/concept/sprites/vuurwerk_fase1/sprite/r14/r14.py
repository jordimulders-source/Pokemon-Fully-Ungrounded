# r14 = r12 B + (2) streeppatroon van de huls doorgetrokken tot onder de kegel + (1) palet naar fase 3 + schaduwsikkel in het rode deel.
import sys; sys.path.insert(0,'../r10'); from txt import CH
import numpy as np; from PIL import Image
S=Image.open('../r12/B.png'); a=np.array(S); old=np.array(S.getpalette()[:48]).reshape(16,3)
CH2=CH[:7]+'r'+CH[8:]; I={c:i for i,c in enumerate(CH2)}
A=a.copy(); LOG=[]
# ---- 2. vuurpijlpatroon: de strepen lopen diagonaal (index u=rij+kol); onder de handjes rij 20-22: l op u 44-45, M vanaf u 46.
#     Zelfde volgorde naar boven: M 36-39 | Y 40-42 | l 43-45 | M 46-49. Rechterkant van de huls (kol 28-29) in schaduwtint
#     zoals eronder (Y->p, l->t). Pixels die aan een roze handje grenzen ook in schaduwtint (anders vloeit de streep in de vingertop).
def kleur(u):
    if 40<=u<=42: return 'Y'
    if 43<=u<=45: return 'l'
    return 'M'
SH={'Y':'p','l':'t','M':'s'}
hand=lambda r,c: CH2[a[r,c]] in 'lms' and not (24<=c<=29 and 14<=r<=19 and CH2[a[r,c]]=='k')
for r in range(14,20):
    for c in range(24,30):
        if CH2[a[r,c]]!='k': continue
        v=kleur(r+c)
        nb=[(r+dy,c+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
        if c>=28 or v=='l': v=SH[v]   # roze streep onder kegel/handjes in schaduwtint (slagschaduw; anders vloeit hij in de roze vingers)
        A[r,c]=I[v]; LOG.append(('streep',r,c,'k',v))
# ---- schaduwsikkel rood deel: rode vlakpixels die rechts/rechtsonder aan de buitenlijn grenzen -> donkerrood (nieuwe index, zie palet)
red=[]
for r in range(38,63):
    for c in range(64):
        if CH2[A[r,c]]=='r' and CH2[A[r,c-1]]=='r' and (CH2[A[r,c+1]]=='#' or CH2[A[r+1,c+1]]=='#') : red.append((r,c))  # alleen waar het rood >=2 px breed is
# ---- 1. palet. Samengevoegd: E (oogzwart) -> '#' (36,11,16 vs 45,18,28), t (mauve) -> s. Vrij: indexen 2 en 11 voor fase-3-tinten.
P={ '#':(45,18,28),   # fase 3 buitenlijn
    'd':(173,38,92),  # fase 3 roze selout/schaduw (p)
    's':(205,58,122), # tussenschaduw roze (tussen fase 3 p en m; stap ~25-30 luma)
    'm':(236,86,158), # fase 3 roze
    'l':(246,130,170),# fase 3 lichtroze
    'r':(225,58,73),  # fase 3 rood
    'M':(208,38,154), # magenta streep pijl (blijft, geen fase-3-equivalent)
    'p':(205,150,55), # fase 3 oker
    'Y':(250,222,105),# fase 3 geel
    'c':(250,234,196),# fase 3 creme
    'k':(240,208,162),# fase 3 lichte peach
    'b':(222,160,115),# fase 3 peach (lichte lijn kop/ring)
}
NEW={'E':'#','t':'s'}
for ch,to in NEW.items(): A[A==I[ch]]=I[to]
DR,SA=I['E'],I['t']   # vrijgekomen indexen hergebruikt: 2 = donkerrood, 11 = zalm
for r,c in red: A[r,c]=DR
# rood deel: lichtkant roze -> zalm, selout d -> donkerrood (rij >= 38, rechts van de pijl of onder de opening)
def roodzone(r,c): return (r>=38 and c>=30) or r>=44
for r in range(64):
    for c in range(64):
        if roodzone(r,c):
            if A[r,c]==I['l']: A[r,c]=SA
            elif A[r,c]==I['d'] and c>=31: A[r,c]=DR   # selout rechts/binnenlijnen in het rood donkerrood; lichtkant (links) houdt roze selout
pal=[0,0,0]*16
for ch,rgb in P.items(): pal[I[ch]*3:I[ch]*3+3]=rgb
pal[DR*3:DR*3+3]=(150,29,49); pal[SA*3:SA*3+3]=(250,128,128)
pal[I['w']*3:I['w']*3+3]=(255,255,255)  # glans blijft wit (creme viel weg tegen het creme gezicht)
im=Image.fromarray(A,'P'); im.putpalette(pal); im.save('sprite.png',transparency=0)
for l in LOG: print(l)
print('sikkel rood',len(red))
