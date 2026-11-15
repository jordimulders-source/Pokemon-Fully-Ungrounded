# p7: keuring p6 (MOET 1-4 + MAG staart), alleen kleur/schaduw/lijnen binnen de bestaande vormen.
import numpy as np
from PIL import Image
P6=np.array(Image.open('../p6/welp_p6.png')); R=np.array(Image.open('../r11/welp_r11.png')); B=np.load('../p1/basis.npy')
PAL=Image.open('../r11/welp_r11.png').getpalette(); LIJN=np.isin(R,[1,2])
a=P6.copy(); fout=[]
def zet(x,y,v):
    if LIJN[y,x] or a[y,x]==0: fout.append((x,y)); return
    a[y,x]=v
# 1 tong/poot: geen perzik direct onder de tonggrens
zet(12,42,5); zet(13,42,5)
# 2+3 rugband: hele band + krul terug naar bruin; gap tegen de rugrand bovenste helft 4, onderste 3
for y in range(31,43):
    for x in range(31 if y<=37 else 37,45):
        if a[y,x] in (6,7,8): zet(x,y,int(B[y,x]) if B[y,x] in (3,4,5) else 4)
for x,y in [(33,32),(34,33),(35,34),(36,35)]: zet(x,y,4)
for x,y in [(37,36),(38,37),(40,38),(41,39),(41,42)]: zet(x,y,3)
for x,y in [(39,39),(39,40),(39,41),(38,40),(38,41)]: zet(x,y,4)   # bruin hart van de krul
RUG={(31,32):7,(32,32):8,(31,33):7,(32,33):8,(33,33):8,(32,34):7,(33,34):8,(34,34):8,(33,35):7,(34,35):8,(35,35):8,(35,36):7,(36,36):8,
     (36,37):7,(37,37):8,(37,38):7,(38,38):8,              # band 1 px van de rand, 8 boven / 7 schaduwkant
     (39,38):8,(39,39):8,(40,39):8,(40,40):8,(41,40):7,(40,41):7,(41,41):7,(40,42):7,(39,42):7,(38,42):7,(38,41):8}  # band boven 3 px breed (vlam), naar de krul 2 px; ronde open krul, hart (39,40-41),(38,40) bruin
for (x,y),v in RUG.items(): zet(x,y,v)
for x,y in [(38,39),(38,40),(39,40),(39,41)]: zet(x,y,4)
# 4 voorhoofd: band terug naar bruin, dan één golvende strook (2 px, 8 boven / 7 onder), links omkrullend, los van de bovenrand
for y in range(20,26):
    for x in range(12,25):
        if not LIJN[y,x] and a[y,x]!=0: a[y,x]=B[y,x]
KOL={14:21,15:22,16:23,17:23,18:22,19:21,20:21,21:21}      # bovenste rij van de strook per kolom (dal x16-17, bult x19-21)
for x,y0 in KOL.items(): zet(x,y0,8); zet(x,y0+1,7)
for (x,y),v in {(13,21):8,(12,21):8,(12,22):8,(12,23):7,(22,22):7}.items(): zet(x,y,v)  # krul links, uitloop rechts
# MAG staart: ring 1 px breder
zet(55,52,9); zet(54,54,8); zet(52,53,7)
im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PAL); im.save('welp_p7.png',transparency=0)
q=Image.open('welp_p7.png').convert('RGBA'); bg=Image.new('RGBA',q.size,(255,255,255,255)); bg.alpha_composite(q)
bg.resize((512,512),Image.NEAREST).save('welp_p7_8x.png')
if fout: print('overgeslagen (lijn/leeg):',fout)
