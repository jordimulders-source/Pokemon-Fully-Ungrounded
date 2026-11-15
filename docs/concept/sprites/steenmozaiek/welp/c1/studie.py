# Studie Gen 3 steen/gravure: eerste frame van regirock, relicanth, claydol, baltoy, golem, onix op 6x naast elkaar
from PIL import Image
G='../../../../../../graphics/pokemon/'
L=['regirock','relicanth','claydol','baltoy','golem','onix']
out=Image.new('RGB',(64*6*len(L),64*6),(255,255,255))
for i,s in enumerate(L):
    f=G+s+'/anim_front_gba.png'
    try: im=Image.open(f)
    except: im=Image.open(G+s+'/anim_front.png')
    im=im.convert('RGBA').crop((0,0,64,64))
    bg=Image.new('RGBA',(64,64),(255,255,255,255)); 
    if im.getpixel((0,0))[3]==255:
        # transparant = index 0 kleur
        c=im.getpixel((0,0)); px=im.load()
        for y in range(64):
            for x in range(64):
                if px[x,y]==c: px[x,y]=(255,255,255,255)
    bg.alpha_composite(im); out.paste(bg.resize((384,384),Image.NEAREST),(i*384,0))
out.save('studie.png')
