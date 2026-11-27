# r8: klauwen 1-op-1 uit echte Gen 3-vogelsprites (anim_front_gba.png), per klauw als geheel verplaatst (geen per-teen-
# verschuiving), omgekleurd naar C (karmijn 10/9/8, klauwpunt ivoor 7/14, lijn 1), op de modelplek van onze voeten
# (enkel links (26,49), rechts (35,49)), als voorste vorm met gesloten omlijning tegen de staart.
# Oude voetpixels die de nieuwe klauw niet bedekt: boven de staart (X>=26) loopt de staartveer van rij 53 omhoog door
# (zelfde kolom), links ervan wordt het achtergrond. Buiten de klauwzone (X 16-41, Y 48-57) pixeldiff 0 met r7 (assert).
import numpy as np; from PIL import Image, ImageDraw
G='../../../../../graphics/pokemon/'
PAL=[(152,208,160),(26,16,20),(124,76,18),(196,148,53),(229,184,79),(246,214,124),(206,188,180),(244,240,234),
 (128,28,42),(166,48,63),(208,99,104),(186,82,38),(222,118,50),(50,41,52),(204,192,148),(92,80,96)]
def opslaan(o,pad):
    im=Image.new('P',(64,64)); flat=[x for c in PAL for x in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.putdata([int(v) for v in o.ravel()]); im.save(pad,transparency=0)
def bron(n):
    a=np.array(Image.open(G+n+'/anim_front_gba.png'))[:64]
    pal=[tuple(int(v) for v in l.split()) for l in open(G+n+'/normal_gba.pal').read().split('\n')[3:19]]
    return a,pal
# per soort: kleurmap bronindex -> ons palet, en twee klauwen: (x0,y0,x1,y1) bronvak (incl.), bron-enkel (x,y), doel-enkel
VAR={
 'fearow':({5:1,7:10,8:9,13:8,4:1,3:7},
           [((16,57,24,63),(20,57),(26,49)), ((27,57,35,63),(31,57),(35,49))]),
 'zapdos':({5:1,8:10,9:9,10:8,4:1,2:7,1:7,3:14},
           [((19,50,23,54),(22,50),(26,49)), ((19,50,23,54),(22,50),(35,49))]),
 'noctowl':({13:1,7:9,5:10,9:8,1:7,12:14,3:10,4:10,15:1},
           [((20,56,29,59),(24,56),(26,49)), ((29,57,38,60),(33,57),(35,49))]),
}
r7=np.array(Image.open('../sprite_r7/sprite.png')).astype(int)
OUD=np.zeros((64,64),bool); OUD[49:53,21:39]=True; OUD&=r7>0
OUD[49:51,27:31]=False      # witte dijveren (r7) horen niet bij de voet
Z=np.zeros((64,64),bool); Z[48:58,16:42]=True
uit={}
for soort,(km,klauwen) in VAR.items():
    a,pal=bron(soort); o=r7.copy(); nieuw=np.zeros((64,64),bool); bronvakken=[]
    for (x0,y0,x1,y1),(ax,ay),(dx_,dy_) in klauwen:
        sx,sy=dx_-ax,dy_-ay; bronvakken.append((x0,y0,x1,y1))
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                k=a[y,x]
                if k==0 or k not in km: continue
                Y,X=y+sy,x+sx
                if 0<=Y<64 and 0<=X<64: o[Y,X]=km[k]; nieuw[Y,X]=True
    # niet bedekte oude voetpixels
    for Y,X in zip(*np.where(OUD&~nieuw)):
        o[Y,X]=r7[53,X] if X>=26 and r7[53,X]>0 else 0
    # gesloten omlijning tegen de staart (buren van de klauw die staart zijn)
    for Y,X in zip(*np.where(nieuw)):
        if o[Y,X]==1: continue
        for dy,dx in ((1,0),(0,1),(0,-1),(-1,0)):
            YY,XX=Y+dy,X+dx
            if 0<=YY<64 and 0<=XX<64 and not nieuw[YY,XX] and o[YY,XX] not in (0,1) and YY>=51 and not (o[YY,XX] in (6,7) and YY<=50):
                o[YY,XX]=1
    # losse pixels (geen 8-buur) weg
    for Y,X in zip(*np.where(Z&(o>0))):
        if all(not(0<=Y+a_<64 and 0<=X+b<64) or o[Y+a_,X+b]==0 for a_ in (-1,0,1) for b in (-1,0,1) if a_ or b): o[Y,X]=0
    assert not ((o!=r7)&~Z).any()
    uit[soort]=(o,bronvakken,a,pal); opslaan(o,'sprite_%s.png'%soort); np.save('sprite_%s.npy'%soort,o)
    print(soort,'px anders dan r7:',int((o!=r7).sum()),'klauwpixels uit bron:',int(nieuw.sum()),'kleuren',len(set(o.ravel()))-1)
def rgb(o,bg=(240,240,236)):
    x=np.array(PAL,'uint8')[o]; x[o==0]=bg; return Image.fromarray(x)
V=Image.new('RGB',(1640,3*350+10),'white'); d=ImageDraw.Draw(V)
for i,(soort,(o,vakken,a,pal)) in enumerate(uit.items()):
    y=i*350; d.text((2,y),soort+': bronklauwen 16x (origineel) | onze klauwen 16x | geheel 5x | 1x/2x',fill=(0,0,0)); x=0
    srgb=np.array(pal,'uint8')[a]; srgb[a==0]=(240,240,236)
    for (x0,y0,x1,y1) in vakken[:2]:
        im=Image.fromarray(srgb[y0-1:y1+2,x0-1:x1+2]).resize(((x1-x0+3)*16,(y1-y0+3)*16),Image.NEAREST); V.paste(im,(x,y+14)); x+=im.width+8
    im=rgb(o).crop((16,45,42,58)).resize((26*16,13*16),Image.NEAREST); V.paste(im,(x+10,y+14)); d.text((x+12,y+2),'onze klauwen 16x',fill=(0,0,0))
    V.paste(rgb(o).resize((320,320),Image.NEAREST),(x+450,y+14)); xx=x+790
    for bg in ((240,240,236),(40,40,56)):
        for s in (1,2): V.paste(rgb(o,bg).resize((64*s,64*s),Image.NEAREST),(xx,y+14)); xx+=64*s+8
V.save('vel.png')
