# Eindkeuring Ledian-evo (27 nov): omlijningsronde volgens Dragonfly Cave op rood_c (Jordi's keuze).
# Alleen indexwijzigingen op een vaste lijst pixels; vorm/alpha, rood c, perzik, ogen, mond, stippen, ruitje,
# gewrichten en vleugelband ongemoeid (bewezen met asserts). Draaien vanuit deze map.
import numpy as np
from PIL import Image
SRC='../sprite_r2/rood_c.png'
im=Image.open(SRC); a=np.array(im); s=a.copy()
pal=im.getpalette()[:16*3]
ZWART,GRIJS2,SEL,SCH=1,2,7,8
GEELBASIS=13; pal[GEELBASIS*3:GEELBASIS*3+3]=[164,123,0]   # a47b00 = Ledians eigen donkerste geel (normal_gba.pal idx 9)
W={}   # (x,y): (nieuw, zone, reden)
def put(pts,new,zone,why,old):
    for x,y in pts:
        assert a[y,x] in old, ((x,y),a[y,x],old)
        W[(x,y)]=(new,zone,why)
# 1. Outline base aan de lichtkant (zwart -> eigen donkerste tint)
put([(6,18),(7,20),(8,21)],SEL,'hoofd: linkerpunt','buitenlijn lichtkant zwart -> selout',{1})
put([(32,14)],SEL,'hoofd: rechterpunt boven','zwart tussen selout op de bovenrand -> selout',{1})
put([(51,51),(54,52),(55,53)],SEL,'voorste been bovenrand','zwart tussen selout op de bovenrand -> selout (om-en-om weg)',{1})
put([(6,22),(7,22),(8,22),(6,23),(6,24),(6,25),(7,26)],SEL,'hoofd: verre gezichtshelft','donkergrijze buitenlijn van een rood onderdeel -> selout',{2})
put([(12,32)],SEL,'hoofd: kaak linksonder','grijze pixel op de rode lichtkantrand -> selout',{3})
put([(53,59),(53,60),(44,60)],GEELBASIS,'voeten','buitenlijn lichtkant zwart -> donkerste geel (a47b00)',{1})
# 2. Outline shadow: selout aan de schaduwkant (rechts/onder, tegen transparant) -> zwart
put([(62,21),(62,22)],ZWART,'vleugelpunt rechts','selout aan de schaduwkant -> zwart',{7})
put([(46,40),(44,42),(44,43),(44,44)],ZWART,'rechterarm (naar onderste vuist)','selout aan de schaduwkant -> zwart',{7})
put([(15,33),(13,33)],ZWART,'hoofd: kaak onder','onderrand: selout/grijs tussen zwart -> zwart',{7,3})
# 3. Binnenlijnen (vorm over vorm, 1 px) niet zwart -> selout van het voorste onderdeel
# GETEST EN TERUGGEDRAAID: binnenlijnen hoofd/arm (33,28)-(34,31) en arm/vleugel (44,29)-(41,32) naar selout.
# Aan beide kanten ligt schaduwrood c51810; selout 831c10 verschilt maar 18 helderheid -> hoofd, arm en vleugel
# smelten tot een vlek (vel_binnenlijn_test.png). Gen 3-Ledian houdt hier ook zwart (arm over romp, rijen 33-35 'fff').
TEST_BINNEN=[(33,28),(34,29),(34,30),(34,31),(44,29),(43,30),(42,31),(41,32)]
# 4. Outline highlights (schaduwtint binnen de lijn op de meest belichte randen)
put([(20,8),(19,9),(18,10)],SCH,'hoofd: bovenhelling','outline highlight',{7})
put([(10,15),(11,15)],SCH,'hoofd: linkerpunt boven','outline highlight',{7})
put([(57,20),(58,20)],SCH,'vleugel bovenrand','outline highlight',{7})
for (x,y),(n,_,_) in W.items(): s[y,x]=n
# bewijs
assert ((a==0)==(s==0)).all(); sil=int(((a==0)!=(s==0)).sum())
diff=int((a!=s).sum()); assert diff==len(W)
used=sorted(set(s.flatten().tolist())); assert len(used)-1<=15 and s.shape==(64,64)
def save(arr,fn,S=1):
    o=Image.fromarray(arr.astype('uint8'),'P'); o.putpalette(pal+[0]*(768-len(pal)))
    if S>1: o=o.resize((64*S,64*S),Image.NEAREST)
    o.save(fn,transparency=0)
save(s,'ledian_evo_ek.png'); save(s,'ledian_evo_ek_8x.png',8)
if __name__=='__main__':
    from collections import Counter
    print('silhouetdiff',sil,'gewijzigd',diff,'kleuren (zonder transparant)',len(used)-1,used)
    print('zwart',int((a==1).sum()),'->',int((s==1).sum()))
    for z,c in Counter(v[1] for v in W.values()).items(): print(' ',z,c)
