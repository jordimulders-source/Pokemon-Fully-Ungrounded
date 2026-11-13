# Keuringsvel: poesrups naast echte Gen 3-sprites en familie, licht + donker, 1x en 3x
from PIL import Image
import os
R='/home/user/Pokemon-Fully-Ungrounded/'
S=R+'docs/concept/sprites/'
def gen3(n):
    for f in('anim_front.png','front.png'):
        p=R+'graphics/pokemon/%s/%s'%(n,f)
        if os.path.exists(p):
            return p
def load(p):
    im=Image.open(p)
    if im.mode=='P':
        pal=im.getpalette(); im2=im.crop((0,0,64,64)).convert('RGBA'); px=im.crop((0,0,64,64)).load(); o=im2.load()
        for y in range(64):
            for x in range(64):
                if px[x,y]==0:o[x,y]=(0,0,0,0)
        return im2
    return im.convert('RGBA').crop((0,0,64,64))
items=[('poedellarve',S+'poedellarve/af/poedellarve.png'),('POESRUPS',S+'poesrups/kleur_r4/poesrups.png'),('poedelmot',S+'poedelmot/af/poedelmot.png')]
for n in['silcoon','cascoon','wurmple','swablu','altaria','mareep','seel','dewgong','swinub','castform']:
    items.append((n,gen3(n)))
ims=[load(p) for n,p in items]
def row(bg,sc):
    W=Image.new('RGBA',(len(ims)*64*sc,64*sc),bg)
    for i,im in enumerate(ims):
        b=im.resize((64*sc,64*sc),Image.NEAREST); W.paste(b,(i*64*sc,0),b)
    return W
bgs=[(248,248,248,255),(40,40,48,255),(120,168,96,255)]
def sheet(sc,name):
    rows=[row(b,sc) for b in bgs]
    W=Image.new('RGBA',(rows[0].width,sum(r.height for r in rows)))
    y=0
    for r in rows: W.paste(r,(0,y)); y+=r.height
    W.save(name)
sheet(1,'vel_1x.png'); sheet(3,'vel_3x.png')
# 1x-vel 2x vergroot zodat het in een viewer leesbaar blijft
Image.open('vel_1x.png').resize((len(ims)*128,len(bgs)*128),Image.NEAREST).save('vel_2x.png')
print([n for n,p in items])
