"""Na Jordi: "het leest niet echt als een glitch". Analyse: een nette, doorlopende omlijning maakt
er een voorwerp met een patroon van. Een glitch leest als de VORM zelf kapot is (zoals MissingNo):
banen verschoven, omlijning onderbroken, stukken herhaald/verkeerd geplaatst, rommeldata die buiten
de vorm doorloopt, een stuk in het verkeerde palet.
Gebruik: python3 eigen_missingno_kapot.py UITMAP basis1.png basis2.png ..."""
import sys, os, random
from PIL import Image
uit=sys.argv[1]; os.makedirs(uit,exist_ok=True); bases=[Image.open(p).convert('RGBA') for p in sys.argv[2:]]
def kapot(im,seed,omlijning='breek',lek=True,palet=True):
    r=random.Random(seed); im=im.copy(); px=im.load()
    if omlijning in ('weg','breek'):
        for y in range(64):
            for x in range(64):
                p=px[x,y]
                if p[3] and max(p[:3])<30 and (omlijning=='weg' or r.random()<0.5 or y%8<3):
                    px[x,y]=(0,0,0,0)
    out=Image.new('RGBA',(64,64),(0,0,0,0))
    y=0
    while y<64:   # banen van wisselende hoogte, elk eigen verschuiving
        h=r.choice([2,3,4,6,8]); dx=r.choice([0,0,0,-2,2,-4,4,-6,6,8])
        out.alpha_composite(im.crop((0,y,64,y+h)),(max(0,dx),y),(max(0,-dx),0)); y+=h
    for _ in range(2):   # stuk herhalen op een verkeerde plek
        w,h=r.choice([(8,4),(16,4),(8,8)]); sx,sy=r.randrange(8,48),r.randrange(8,52)
        out.alpha_composite(out.crop((sx,sy,sx+w,sy+h)),(min(56,max(0,sx+r.choice([-16,-8,8,16]))),min(60,max(0,sy+r.choice([-8,0,8])))))
    if lek:   # rommel lekt buiten de vorm, MissingNo-achtig in blokjes aan één kant
        kant=r.choice(['links','rechts']); bron=im
        for _ in range(r.randrange(4,8)):
            w,h=r.choice([(4,4),(8,2),(4,8),(8,4)]); sx,sy=r.randrange(10,50),r.randrange(30,58)
            tx=r.randrange(0,6) if kant=='links' else r.randrange(54,60)
            out.alpha_composite(bron.crop((sx,sy,sx+w,sy+h)),(tx,r.randrange(20,60)))
    if palet:   # een baan in het verkeerde palet
        y0=r.randrange(36,54); h=r.choice([3,4,6]); kleur=r.choice([(232,60,200),(60,220,230),(240,220,40)])
        po=out.load()
        for yy in range(y0,min(64,y0+h)):
            for xx in range(64):
                p=po[xx,yy]
                if p[3]:
                    l=(p[0]+p[1]+p[2])/765
                    po[xx,yy]=tuple(int(c*(0.35+0.75*l)) for c in kleur)+(255,)
    return out
ims=[]
for b,base in enumerate(bases):
    for k,(om,lek,pal) in enumerate([('breek',True,False),('breek',True,True),('weg',True,True)]):
        im=kapot(base,b*10+k,om,lek,pal); ims.append(im); im.save(f'{uit}/k{b+1}_{k+1}.png')
cols=len(ims)//len(bases)
sh=Image.new('RGB',(cols*68+4,len(bases)*68+4),(255,255,255))
for i,im in enumerate(ims): sh.paste(im,(4+(i%cols)*68,4+(i//cols)*68),im)
sh.resize((sh.size[0]*3,sh.size[1]*3),Image.NEAREST).save(f'{uit}/vel.png')
