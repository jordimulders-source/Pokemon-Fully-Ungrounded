import os
from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
front=['aipom','ambipom','vigoroth','linoone','zangoose','absol','flygon','pidgeot','salamence','charizard','scyther','ninjask']
back=['primeape','machamp','hariyama','vigoroth','slaking','medicham','aipom','pidgeot','charizard','salamence','blaziken','sceptile']
def get(n,kind):
    for f in ([kind+'_gba.png',kind+'.png'] if kind=='back' else ['anim_front_gba.png','anim_front.png','front.png']):
        p=G+n+'/'+f
        if os.path.exists(p): return Image.open(p).convert('RGBA').crop((0,0,64,64))
    return None
Z=4
cols=6
cell=64*Z+8
rows=[(k,n) for k in ('front','back') for n in (front if k=='front' else back)]
H=((len(rows)+cols-1)//cols)
out=Image.new('RGBA',(cols*cell, H*(cell+14)),(200,220,200,255))
d=ImageDraw.Draw(out)
missing=[]
for i,(k,n) in enumerate(rows):
    im=get(n,k)
    x=(i%cols)*cell; y=(i//cols)*(cell+14)
    d.text((x+4,y+2),k+' '+n,fill=(0,0,0,255))
    if im is None: missing.append(n); continue
    out.alpha_composite(im.resize((64*Z,64*Z),Image.NEAREST),(x+4,y+14))
out.save('studie_rug.png'); print('ontbreekt',missing, out.size)
