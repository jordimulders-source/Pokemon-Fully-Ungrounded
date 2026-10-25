# maakt vel.png; draaien vanuit de repo-root
from PIL import Image, ImageDraw
D='docs/concept/sprites/olinguito_v2/'
r2=Image.open(D+'kleur/ronde2/olinguito.png').convert('RGBA')
r1=Image.open(D+'kleur/ronde1/olinguito.png').convert('RGBA')
ont=Image.open(D+'referenties/ONTWERP_GEKOZEN.png').convert('RGBA'); ont.thumbnail((256,256))
refs=['linoone','zigzagoon','poochyena','sentret','furret']
def tr(n):
    im=Image.open(f'graphics/pokemon/{n}/anim_front.png').crop((0,0,64,64)); im.info['transparency']=0
    return im.convert('RGBA')
R=[tr(n) for n in refs]
LIGHT=(236,236,230,255); DARK=(40,40,48,255)
o=Image.new('RGBA',(1350,880),LIGHT); d=ImageDraw.Draw(o)
def put(im,x,y,bg=None,l=None):
    if bg:
        b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); im=b
    o.paste(im,(x,y),im)
    if l: d.text((x,y+im.size[1]+3),l,fill=(30,30,30,255))
put(r2.resize((256,256),Image.NEAREST),0,0,LIGHT,'ronde 2, 4x (licht)')
put(r2.resize((256,256),Image.NEAREST),266,0,DARK,'ronde 2, 4x (donker)')
put(r1.resize((256,256),Image.NEAREST),532,0,LIGHT,'ronde 1, 4x')
put(ont,798,0,(255,255,255,255),'gekozen ontwerp')
put(r2,1070,10,LIGHT,'r2 1x'); put(r2,1150,10,DARK,'')
put(r1,1070,100,LIGHT,'r1 1x'); put(r1,1150,100,DARK,'')
for i,(n,r) in enumerate(zip(refs,R)):
    put(r.resize((256,256),Image.NEAREST),i*266,290,LIGHT,n+' (Gen 3), 4x')
row=[('ronde 2',r2),('ronde 1',r1)]+list(zip(refs,R))
for i,(n,r) in enumerate(row):
    put(r,10+i*80,575,LIGHT,n); put(r,10+i*80,665,DARK,'')
o.save(D+'kleur/ronde2/vel.png')
