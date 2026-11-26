# Jordi: "de mond moet nog wel wat duidelijker omlijnd worden zodat duidelijk is dat die ietwat uitsteekt" (model: donkere rand om de snavel).
# Basis oog_B_wit (Jordi: "rechts is beter"). Rode pixels die aan geel grenzen -> rode lijn (2); V2: onder de snavel zwart (outline shadow).
from PIL import Image
GEEL={12,13}; ROOD={3,4,5,6,7,14}
base=Image.open('oog_B_wit.png')
def maak(zwart_onder):
    im=base.copy(); w=[]
    for y in range(27,38):
        for x in range(12,38):
            if base.getpixel((x,y)) not in ROOD: continue
            buren=[(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
            if not any(base.getpixel(b) in GEEL for b in buren): continue
            onder = base.getpixel((x,y-1)) in GEEL
            im.putpixel((x,y), 1 if (zwart_onder and onder) else 2); w.append((x,y))
    return im,w
for n,z in (('V1',False),('V2',True)):
    im,w=maak(z); im.save('mond_%s.png'%n); print(n,len(w),w)
vel=Image.new('RGBA',(3*410,250),(200,200,200,255))
for i,p in enumerate(['oog_B_wit.png','mond_V1.png','mond_V2.png']):
    im=Image.open(p).convert('RGBA')
    vel.paste(im.crop((12,22,42,38)).resize((240,128),Image.NEAREST),(i*410,0))
    vel.paste(im.resize((128,128),Image.NEAREST),(i*410+250,0),im.resize((128,128),Image.NEAREST))
    vel.paste(im,(i*410,140),im)
vel.save('mond_vel.png')
