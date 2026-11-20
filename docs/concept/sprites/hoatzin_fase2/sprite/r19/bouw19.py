# r19 = r18 + (1) neklijn doorlopend + (2) poten los van elkaar + (3) rechterpoot-tenen/klauwen per pixel uit het model.
# Meetwaarden (achtergrond/9, donker/9, grijs-L/10 per spritepixel): ../r18/meetpoot.txt en meet_rechts.txt.
import numpy as np; from PIL import Image
im18=Image.open('../r18/hoatzin.png'); r18=np.array(im18); out=r18.copy(); log=[]
def zet(x,y,v,w):
    assert r18[y,x] not in (11,12,13,8,9,10), ('bevroren',x,y)
    if out[y,x]!=v: log.append((w,x,y,int(out[y,x]),v)); out[y,x]=v
# (1) neklijn: precies 1 lijnpixel per rij, 8-verbonden, direct links van de lichte vleugelrand.
LIJN={23:27,24:27,25:27,26:27,27:26,28:25,29:25,30:24,31:23,32:23,33:23,34:23,35:24,36:25,37:26,38:26,39:27,40:26}
for y,xl in LIJN.items():
    xs=[x for x in range(xl+1,40) if r18[y,x]==5]; xe=xs[0]
    for x in range(xl-2,xe):
        if x==xl: zet(x,y,1,'neklijn')
        elif x>xl and r18[y,x]>0: zet(x,y,4,'vleugelrand')                     # lichte strook tussen lijn en vleugel
        elif y>=27 and out[y,x] in (1,2): zet(x,y,3,'nek naast lijn') # nek: geen tweede donkere pixel tegen de lijn
for y in range(23,41):                                               # controle: 1 lijnpixel in het grensvenster, verbonden
    xl=LIJN[y]; assert [x for x in range(xl-2,xl+3) if out[y,x]==1]==[xl] or y<27, (y,[x for x in range(xl-2,xl+3) if out[y,x]==1])
    if y>23: assert abs(LIJN[y]-LIJN[y-1])<=1
# (2) poten los: de buitenlijn van de voorste (rechter)poot loopt over y56 door tot x25 (model: donker op (25,57)/(28,56));
#     de verre hiel (25-27,56) wordt die lijn, zodat de verre teen (y55) en de voorste voet (y57) gescheiden zijn.
for x in (25,26,27): zet(x,56,1,'scheiding')
# (3) rechterpoot (voorste), per pixel uit het model
for x in range(26,37): zet(x,57,14,'voet y57 grijs')                # model y57 x26-36 grijs (L 80-100), r18 had lijnstukjes
zet(34,57,15,'voet y57 licht')                                      # model L>=100
zet(37,57,1,'klauw rechts')                                         # model (37,57) 2/9 bg 7/9 donker: kleine klauw
for x in (34,35): zet(x,56,14,'rechter teen y56')                   # model grijs (L 80, 100); r18 zwart blok
zet(36,56,1,'teenpunt omlijning')
for x in (35,36): zet(x,58,1,'onderlijn rechter teen')              # model donker 6/9, r18 had 2
zet(37,58,0,'weg (model achtergrond)'); zet(35,59,0,'weg (model achtergrond)'); zet(36,59,0,'weg (model achtergrond)')
for x in range(25,32): zet(x,58,14,'voet y58 grijs')                # model y58 x25-31 grijs; r18 streepjes 1
zet(32,58,1,'rand')
# linker teen van de voorste voet: schuin omlaag naar links, 1 grijze pixel breed met lijn, klauw (24,61)
zet(24,59,1,'teen lijn'); zet(25,59,14,'teen'); zet(26,59,1,'teen onderlijn'); zet(27,59,1,'teen onderlijn')
zet(24,60,14,'teenpunt'); zet(25,60,1,'teen lijn'); zet(24,61,1,'klauw')
# teen recht omlaag x29-31: lijn | grijs | lijn, klauw klein
for y in (59,60,61): zet(29,y,1,'teen lijn'); zet(30,y,14,'teen'); zet(31,y,1,'teen lijn')
zet(29,62,1,'teen lijn'); zet(30,62,14,'teen'); zet(29,63,1,'klauw'); zet(30,63,0,'weg (model achtergrond 4/9, klauw 1 px)')
im=Image.fromarray(out.astype('uint8'),'P'); im.putpalette(im18.getpalette()); im.save('hoatzin.png',transparency=0)
im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png'); open('normal.pal','w').write(open('../r18/normal.pal').read())
np.save('r19.npy',out); np.save('vorm.npy',out)   # vorm + lijnposities; kleur19.py kleurt hierop
from collections import Counter
d=out!=r18; al=(out>0)!=(r18>0)
NEK=np.zeros((64,64),bool); NEK[22:42,14:38]=True; POOT=np.zeros((64,64),bool); POOT[50:64,14:42]=True
print('anders dan r18',d.sum(),'nek',(d&NEK).sum(),'poten',(d&POOT).sum(),'buiten',(d&~NEK&~POOT).sum(),'| alpha',al.sum(),'buiten poten',(al&~POOT).sum())
print(Counter(l[0] for l in log))
for y in range(22,42): print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in out[y,14:37]),'  ',''.join('.' if v==0 else '%x'%v for v in r18[y,14:37]))
for y in range(50,64): print('%2d '%y+''.join('.' if v==0 else '%x'%v for v in out[y,14:42]),'  ',''.join('.' if v==0 else '%x'%v for v in r18[y,14:42]))
