"""Gen 3-glitch: de spritepointer wijst naar tegelgraphics van een kaart (tileset) in plaats van
naar een Pokémon. Tilesets zijn ook 4bpp-tegels van 8x8, dus de game toont ze gewoon als
sprite: brokken gras, dak, water, hek door elkaar. Plus een maat-/startfout (zoals MissingNo)
en een verkeerd palet. Kleur 0 blijft doorzichtig, dus een onregelmatige omtrek.
Gebruik: python3 gen3_tileset.py UITMAP [aantal]"""
import sys, os, random, glob
from PIL import Image, ImageDraw
sys.path.insert(0,os.path.dirname(__file__))
from gen3_missingno import pal_none, REPO
from gen3_afmeting import lees
def bytes4(png):
    im=Image.open(png); w,h=im.size; px=im.load(); out=bytearray()
    for ty in range(h//8):
        for tx in range(w//8):
            for y in range(8):
                for x in range(0,8,2):
                    out.append((px[tx*8+x,ty*8+y]&0xF)|((px[tx*8+x+1,ty*8+y]&0xF)<<4))
    return bytes(out)
def jasc(p):
    l=open(p).read().split('\n')[3:19]; return [tuple(int(v) for v in x.split()) for x in l]
if __name__=='__main__':
    uit=sys.argv[1]; aantal=int(sys.argv[2]) if len(sys.argv)>2 else 32
    os.makedirs(uit,exist_ok=True); r=random.Random(5)
    sets=[p for p in glob.glob(os.path.join(REPO,'data/tilesets/*/*/tiles.png')) if Image.open(p).mode=='P']
    pals=[jasc(p) for p in glob.glob(os.path.join(REPO,'data/tilesets/*/*/palettes/0[0-5].pal'))[:200]]
    pn=pal_none(); kand=[]
    while len(kand)<aantal*4:
        ts=r.choice(sets); data=bytes4(ts)
        if len(data)<4096: continue
        start=r.randrange(0,len(data)-2048)//32*32
        per=r.choice([7,7,6,9,8]); fout=r.choice([0,-r.randrange(200,900)])
        pal=r.choice([pn,pn,r.choice(pals)])
        im=lees(data[start:start+2048],pal,per,fout)
        a=sum(1 for p in im.getdata() if p[3])/4096
        if 0.2<a<0.7: kand.append((os.path.basename(os.path.dirname(ts)),start,per,fout,im))
    r.shuffle(kand); kand=kand[:aantal]
    cols=8; rows=(len(kand)+cols-1)//cols
    sh=Image.new('RGB',(cols*76,rows*84),(255,255,255)); d=ImageDraw.Draw(sh)
    with open(f'{uit}/kandidaten.txt','w') as fh:
        for i,(ts,st,per,fout,im) in enumerate(kand):
            x,y=(i%cols)*76+6,(i//cols)*84+4; sh.paste(im,(x,y),im); d.text((x,y+66),str(i+1),fill=(200,0,0))
            im.save(f'{uit}/k{i+1:02d}.png'); fh.write(f'{i+1}\t{ts}\tstart={st}\t{per}/rij\tfout={fout}\n')
    sh.resize((sh.size[0]*2,sh.size[1]*2),Image.NEAREST).save(f'{uit}/vel.png')
