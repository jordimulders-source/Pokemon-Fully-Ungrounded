# r6: alleen het OOG, op r5 115% (../r5/sprite_115_geel.png; het oude oog wordt vervangen, de rest is bevroren).
# Bronoog: Seviper Gen 3 (graphics/pokemon/seviper/anim_front_gba.png, frame 1, x16-22 y16-20): fel, schuin, amandelvorm,
# opgaand naar rechts zoals het modeloog (binnenhoek linksonder bij de snuit, buitenhoek rechtsboven). Pixel voor pixel
# overgenomen, alleen verschoven (DX,DY) naar de plek van het modeloog, en in onze kleuren:
#   Seviper zwart/donker (13, 10) -> leden 2 (het donkerbruin van de modelleden); pupil (18,18),(19,18) -> 1 (bijna-zwart)
#   Seviper lichtrood 7 -> binnenkant licht, roodschaduw 8 -> binnenkant schaduw; wit 1 (glans) -> 5 (lichtste creme) of binnenkant.
# Pixels van het oude oog (r5) die buiten het nieuwe oog vallen, krijgen hun r5-kale-reductie zonder oogregel (kop5 met OOG=crème),
# d.w.z. wat het model daar heeft (lid -> 2 blijft 2, oogwit -> crème).
import json, numpy as np; from PIL import Image
PAL=json.load(open('palet.json'))
sv=np.asarray(Image.open('../../../../../../graphics/pokemon/seviper/anim_front_gba.png')).astype(int)
DX,DY=-6,4
r5=np.asarray(Image.open('../r5/sprite_115_geel.png')).astype(int)
k5=np.load('../r5/kop5_115_13.npy').astype(int)
PUPIL={(18,18),(19,18)}
bron={}
for y in range(16,21):
    for x in range(16,23):
        v=sv[y,x]
        if v in (13,10): bron[(x,y)]='pupil' if (x,y) in PUPIL else 'lid'
        elif v==7: bron[(x,y)]='licht'
        elif v==8: bron[(x,y)]='schaduw'
        elif v==1: bron[(x,y)]='glans'
# alleen het oog zelf: de Seviper-huid rond het oog (geel/paars) hoort er niet bij
VAR={'geel':{'licht':13,'schaduw':14},'goud':{'licht':14,'schaduw':14}}
OUD=[(x,y) for y in range(18,25) for x in range(9,17) if r5[y,x]==13]   # oude oogbinnenkant (variant geel)
def maak(kleur,glans):
    a=r5.copy()
    for (x,y) in OUD: a[y,x]=5 if (x,y) not in [(p[0]+DX,p[1]+DY) for p in bron] else a[y,x]
    for (x,y),t in bron.items():
        X,Y=x+DX,y+DY
        if t=='lid': a[Y,X]=2
        elif t=='pupil': a[Y,X]=1
        elif t=='glans': a[Y,X]=5 if glans else VAR[kleur]['licht']
        else: a[Y,X]=VAR[kleur][t]
    return a
if __name__=='__main__':
    HX='.123456789ABCDEF'
    print('bronoog Seviper x16-22 y16-20:')
    for y in range(16,21): print(''.join({'lid':'L','pupil':'P','licht':'o','schaduw':'s','glans':'w'}.get(bron.get((x,y)),'.') for x in range(16,23)))
    for kleur in VAR:
        for glans in (1,0):
            a=maak(kleur,glans); n='sprite_%s%s.png'%(kleur,'_glans' if glans else '')
            im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save(n,transparency=0)
            print(n,'diff t.o.v. r5:',int((a!=r5).sum()))
    a=maak('geel',1)
    for y in range(16,27): print('%2d'%y,''.join(HX[v] for v in r5[y,4:20]),'  ',''.join(HX[v] for v in a[y,4:20]))
