# proef.py: GEEN nieuwe sprite, alleen een proef van de keurder om de reparatielijst te toetsen (proef_A.png = alleen bek,
# proef_alles.png = bek + silhouet + randen + palet). De maker voert de reparaties zelf uit en meldt de afwijkingen.
import numpy as np; from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
src=Image.open(B+'sprite_r9/pitahaya2_r9A.png'); a0=np.array(src).astype(int); pal0=src.getpalette()
N='.KdrpPgGhHwWsv'; I={c:i for i,c in enumerate(N)}
def zet(a,lst,doel,oud=None):
    for x,y in lst:
        if oud: assert N[a[y,x]] in oud,(x,y,N[a[y,x]])
        a[y,x]=I[doel]
A=a0.copy()
# A: bek
zet(A,[(18,44),(19,44),(18,45),(19,45),(20,45),(18,46),(19,46),(20,46),(18,47)],'p','P')   # mondhoek achter: geen lichtste roze
zet(A,[(17,45)],'r','p')                                                                   # binnenlijn onder de bovenlip doorlopend (model r)
zet(A,[(16,48),(16,49),(17,49),(15,50),(16,50),(15,51)],'p','P')                           # verre lip: basis i.p.v. licht
zet(A,[(9,54),(10,54),(11,54)],'r','pP')                                                   # onderkant kaak = schaduw
zet(A,[(9,53),(10,53)],'P','p')                                                            # licht op de voorste lipbocht (model P)
zet(A,[(8,48),(8,49)],'r','d')                                                             # lipcontour één tint
def save(a,naam,pal=pal0):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(pal); im.save(naam,transparency=0)
save(A,'proef_A.png')
# B: silhouet naar het model
Z=A.copy()
zet(Z,[(61,48),(61,49),(61,50),(61,51)],'K','.')        # staart rechts: modelbolling (dekking 2,3,3,2 van 9)
zet(Z,[(60,48),(60,49),(60,50),(60,51)],'g','K')        # oude lijn wordt schaduwrand
zet(Z,[(18,34),(19,34),(20,34)],'.','rd')              # kopbovenkant: modeldekking 6,6,6 -> zadel 1 px lager tussen wenkbrauw en nekschub
zet(Z,[(18,35),(19,35),(20,35)],'d','p')                  # nieuwe bovenrand = selout
zet(Z,[(12,58)],'K','g')                                  # meest linkse poot: teenlijn 1|2 uit het model (natief 4/9 zwart) tot de onderrand
zet(Z,[(12,59),(15,59)],'.','K')                          # inkeping tussen de tenen onder de modelteenlijnen (12,58) en (15,58)
zet(Z,[(12,56)],'g','.')                                  # bolling op de bovenkant van teen 1 (modeldekking 2/9; diagonaal geen 1-1-1 meer)
# C: randen in vlaktint -> selout
zet(Z,[(25,32),(26,32),(25,33),(27,33),(32,33),(49,38),(48,39),(51,43),(52,43),(57,43),(58,44),(12,57),(10,58),(29,59),(28,60)],'g','G')
zet(Z,[(31,34),(38,34)],'d','p')
zet(Z,[(10,34),(11,34),(17,34),(9,35)],'d','r')
save(Z,'proef_alles_oudpalet.png')
pal=list(pal0)
nieuw={2:(0x68,0x18,0x38),5:(0xf8,0xa0,0xc8),6:(0x30,0x58,0x30),7:(0x4f,0x80,0x40),8:(0x78,0xa8,0x50),9:(0xb0,0xd0,0x68)}
for i,c in nieuw.items(): pal[3*i:3*i+3]=c
save(Z,'proef_alles.png',pal)
print('diff A',(A!=a0).sum(),'diff alles',(Z!=a0).sum())
