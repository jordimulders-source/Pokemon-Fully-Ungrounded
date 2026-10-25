# maakt vel.png; draaien vanuit de repo-root
from PIL import Image, ImageDraw
D='docs/concept/sprites/olinguito_v2/'
sp=Image.open(D+'kleur/ronde1/olinguito.png').convert('RGBA')
old=Image.open(D+'kleur/ronde1/bron/vorige_front.png').convert('RGBA')
ont=Image.open(D+'referenties/ONTWERP_GEKOZEN.png').convert('RGBA'); ont.thumbnail((256,256))
refs=['linoone','zigzagoon','poochyena','sentret','furret']
R=[Image.open(f'graphics/pokemon/{n}/anim_front.png').convert('RGBA').crop((0,0,64,64)) for n in refs]
LIGHT=(236,236,230,255); DARK=(40,40,48,255)
o=Image.new('RGBA',(1350,770),LIGHT); d=ImageDraw.Draw(o)
def put(im,x,y,bg=None,l=None):
    if bg:
        b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); im=b
    o.paste(im,(x,y),im)
    if l: d.text((x,y+im.size[1]+3),l,fill=(30,30,30,255))
x4=sp.resize((256,256),Image.NEAREST)
put(x4,0,0,LIGHT,'olinguito kleur r1, 4x (licht)'); put(x4,266,0,DARK,'4x (donker)')
put(ont,532,0,(255,255,255,255),'gekozen ontwerp')
put(old.resize((256,256),Image.NEAREST),798,0,(255,255,255,255),'vorige poging (front.png), afgekeurd')
put(sp,1070,10,LIGHT,'1x'); put(sp,1150,10,DARK,''); put(old,1070,100,LIGHT,'vorige 1x')
for i,(n,r) in enumerate(zip(refs,R)):
    put(r.resize((256,256),Image.NEAREST),i*266,290,None,n+' (Gen 3), 4x')
row=[('olinguito',sp)]+list(zip(refs,R))
for i,(n,r) in enumerate(row):
    put(r,10+i*80,575,LIGHT,n)
put(sp,10,665,DARK,'olinguito op donker')
o.save(D+'kleur/ronde1/vel.png')
