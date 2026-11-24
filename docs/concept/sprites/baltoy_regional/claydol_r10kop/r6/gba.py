from PIL import Image
def gba(mon,box=(0,0,64,64)):
    im=Image.open('graphics/pokemon/%s/anim_front_gba.png'%mon)
    try:
        L=open('graphics/pokemon/%s/normal_gba.pal'%mon).read().split('\n')[3:19]
        pal=[int(v) for l in L for v in l.split()]; im.putpalette(pal+[0]*(768-len(pal)))
    except Exception as e: print(e)
    im.info['transparency']=0
    return im.convert('RGBA').crop(box)
