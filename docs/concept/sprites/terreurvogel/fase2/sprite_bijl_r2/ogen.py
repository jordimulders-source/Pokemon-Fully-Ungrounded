# Oogvarianten A/B/C op r2: oog pixel voor pixel uit een Gen 3-sprite, omgekleurd naar het palet. Bouwt vanaf terreurvogel_bijl_r2.png.
import numpy as np; from PIL import Image, ImageDraw
R2=Image.open('terreurvogel_bijl_r2.png'); B=np.array(R2).astype(int); PAL=R2.getpalette()[:48]
OUD=[(29,16),(29,17),(29,18),(30,16),(30,17),(30,18),(31,16),(31,17),(31,18)]   # oude oogpixels (x>=16); x=15 en rij 32 = snavelwortel, blijven
BRON={ # naam: (soort, [(x,y) bronpixels], kleurmap bronindex->onze index, verschuiving)
 'A':('pidgeot',[(13,23),(14,23),(15,23),(12,24),(13,24),(14,24),(15,24),(11,25),(12,25),(13,25),(14,25),(15,25),(11,26),(12,26),(13,26),(14,26),(15,26),(11,27),(12,27),(13,27)],
      {14:9,15:1,1:2,2:10,8:10},(4,5)),
 'B':('spearow',[(25,22),(26,22),(22,23),(23,23),(24,23),(25,23),(26,23),(23,24),(24,24),(25,24),(26,24),(24,25),(25,25)],
      {15:1,1:2,9:9,8:10},(-8,7)),
 'C':('dodrio',[(27,20),(28,20),(26,21),(27,21),(26,22),(27,22),(25,23),(26,23)],
      {15:2,14:1,4:9},(-10,8)),
}
def bron(soort):
    a=np.array(Image.open('../../../../../../graphics/pokemon/%s/anim_front_gba.png'%soort))[:64]
    pal=[int(v) for l in open('../../../../../../graphics/pokemon/%s/normal_gba.pal'%soort).read().split('\n')[3:19] for v in l.split()]
    return a,pal
res={}
for k,(soort,px,cm,(dx,dy)) in BRON.items():
    S=B.copy()
    for y,x in OUD: S[y,x]=11                     # oude oog weg: kopkleur (tan), vlak eromheen
    a,_=bron(soort); n=0
    for x,y in px:
        v=int(a[y,x]); S[y+dy,x+dx]=cm[v]; n+=1
    assert ((S>0)==(B>0)).all(), 'silhouet veranderd'
    im=Image.fromarray(S.astype('uint8'),'P'); im.putpalette(PAL+[0]*(768-48)); im.save('oog_%s.png'%k,transparency=0)
    diff=int((S!=B).sum()); res[k]=(soort,n,diff); print(k,soort,'bronpixels',n,'afwijkend t.o.v. r2',diff)
# vel
def rgba(im): return im.convert('RGBA')
z=12; vel=Image.new('RGBA',(3*(16*z+12*8+40)+20,16*z+120),(236,236,236,255)); d=ImageDraw.Draw(vel)
x0=10
for k,(soort,px,cm,_) in BRON.items():
    im=Image.open('oog_%s.png'%k).convert('RGBA')
    kop=im.crop((8,22,24,38)).resize((16*z,16*z),Image.NEAREST); bg=Image.new('RGBA',kop.size,(200,220,200,255)); bg.alpha_composite(kop)
    vel.alpha_composite(bg,(x0,30)); d.text((x0,10),'oog_%s: %s'%(k,soort),fill=(0,0,0))
    a,pal=bron(soort); xs=[p[0] for p in px]; ys=[p[1] for p in px]
    b=(min(xs)-2,min(ys)-2,max(xs)+3,max(ys)+3)
    src=Image.fromarray(a.astype('uint8'),'P'); src.putpalette(pal+[0]*(768-48))
    sc=src.convert('RGB').crop(b); sc=sc.resize((sc.width*8,sc.height*8),Image.NEAREST)
    vel.paste(sc,(x0+16*z+8,30)); d.text((x0+16*z+8,30+sc.height+4),'bron 8x',fill=(0,0,0))
    for j,bgc in enumerate([(248,248,240,255),(40,44,52,255)]):
        t=Image.new('RGBA',(64,64),bgc); t.alpha_composite(im); vel.alpha_composite(t,(x0+16*z+8+j*70,30+sc.height+20))
    x0+=16*z+12*8+40
vel.save('vel_ogen.png')
