# Studie: Gen 3-sprites met lijfpatronen, eerste frame op 6x naast elkaar; plus per patroonkleurgroep de tinten.
from PIL import Image
G='../../../../../../graphics/pokemon/'
names=['seviper','zangoose','linoone','arcanine']
ims=[]
for n in names:
    im=Image.open(G+n+'/anim_front_gba.png').convert('RGBA').crop((0,0,64,64))
    bg=Image.new('RGBA',(64,64),(255,255,255,255)); px=im.load()
    q=Image.open(G+n+'/anim_front_gba.png'); t=q.getpixel((0,0)) if q.mode=='P' else None
    if q.mode=='P':
        a=q.load(); im2=q.convert('RGBA').crop((0,0,64,64)); p2=im2.load()
        for y in range(64):
            for x in range(64):
                if a[x,y]==0: p2[x,y]=(255,255,255,255)
        bg=im2
    ims.append(bg.resize((384,384),Image.NEAREST))
V=Image.new('RGBA',(4*392,384),(255,255,255,255))
for i,m in enumerate(ims): V.paste(m,(i*392,0))
V.save('studie.png')
for n in names:
    q=Image.open(G+n+'/anim_front_gba.png'); p=q.getpalette()[:48]
    print(n,[tuple(p[3*i:3*i+3]) for i in range(16)])
