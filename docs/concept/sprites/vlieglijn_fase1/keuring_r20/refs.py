from PIL import Image
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def pal(p):
    L=open(p).read().split('\n')[3:19]; return [tuple(map(int,l.split())) for l in L]
def load(s):
    im=Image.open(G+s+'/anim_front_gba.png'); im=im.crop((0,0,64,64)).convert('P') if im.mode=='P' else im.crop((0,0,64,64))
    P=pal(G+s+'/normal_gba.pal'); out=Image.new('RGBA',(64,64)); o=out.load(); px=im.load()
    for y in range(64):
        for x in range(64):
            i=px[x,y]
            if i: o[x,y]=P[i]+(255,)
    return out
if __name__=='__main__':
    names=['ninjask','volbeat','beldum','nincada','surskit']
    c=Image.new('RGB',(5*520,540),'white')
    for k,n in enumerate(names):
        c.paste(load(n).resize((512,512),Image.NEAREST),(k*520,20),load(n).resize((512,512),Image.NEAREST))
    c.save('refs8x.png')
    for n in names:
        im=Image.open(G+n+'/anim_front_gba.png'); print(n, im.mode, pal(G+n+'/normal_gba.pal'))
