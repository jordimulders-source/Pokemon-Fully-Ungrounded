# mat.npy -> P1 (Sigilyph-kleuren) en P2 (ons palet). Max 16 kleuren incl. transparant.
import numpy as np; from PIL import Image
o=np.load('mat.npy'); H,W=o.shape
BASIS={'.':(0,0,0),'K':(16,14,22),'1':(30,28,44),'2':(48,46,70),'3':(76,74,108),'g':(128,126,166),
       'L':(246,236,202),'M':(228,208,158),'D':(186,156,104),'S':(126,94,54),
       'B':(80,120,200),'b':(44,66,140),'R':(214,66,58),'r':(140,36,40),'W':(248,248,248),'w':(184,184,206)}
# P1: Sigilyph: zwarte grond (koptinten), wit, grijs, groen, blauw oogmidden; kraag = ons 'geel' (creme)
P1={'k':'K','z':'3','Z':'2','x':'1','C':'3','E':'B','G':'G','H':'H','y':'L','Y':'M','u':'D'}
P1kleur=dict(BASIS); P1kleur['G']=(56,160,72); P1kleur['H']=(40,104,56)
# P2: zelfde patroon in ons palet: creme grond, wit, grijsblauw, blauw (groen->blauw), oogmidden blauw, kraag rood
P2={'k':'S','z':'L','Z':'M','x':'D','C':'w','E':'B','G':'B','H':'b','y':'R','Y':'R','u':'r'}
def maak(naam,mp,kleur,extra=None):
    r=np.vectorize(lambda c: mp.get(c,c))(o)
    if extra: r=extra(r)
    if 'r' not in kleur or naam.endswith('P1.png'):
        r[r=='r']='K'   # P1: geen plek voor donkerrood; selout van de rode streep wordt lijn
    keys=['.']+sorted(set(r.ravel())-{'.'}); assert len(keys)<=16,(naam,keys,len(keys))
    full=np.zeros((64,64),'uint8'); x0=(64-W)//2; y0=64-H
    for j in range(H):
        for i in range(W): full[y0+j,x0+i]=keys.index(r[j,i])
    im=Image.fromarray(full,'P'); flat=[v for k in keys for v in kleur[k]]; im.putpalette(flat+[0]*(768-len(flat))); im.save(naam,transparency=0)
    print(naam,len(keys),'kleuren')
def p2lijn(r):
    # P2: lijnen in het bedekte deel zoals in r4: schaduwkant zwart; alleen lichtkant/binnenlijn selout
    r4=np.array([list(l.rstrip('\n')[3:]) for l in open('../sprite_r4/rollen_hand.txt') if l.strip()])
    m=(o=='k')
    r[m & (r4=='K')]='K'
    return r
maak('astro_P1.png',P1,P1kleur)
maak('astro_P2.png',P2,BASIS,p2lijn)
