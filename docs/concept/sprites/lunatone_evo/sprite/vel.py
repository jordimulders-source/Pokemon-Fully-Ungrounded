# Vel: sprite 8x | model verkleind 8x | close-up gezicht 12x naast model | 1x op licht en donker
# gebruik: python3 vel.py sprite.png vel.png [vorige.png]
import sys, numpy as np; from PIL import Image, ImageDraw
sp=Image.open(sys.argv[1]); sp.load()
spr=sp.convert('RGBA')
M=Image.open('../referenties/model.png').convert('RGB')
S=13.0; X0=63-(64*S-808)/2; Y0=194-(64*S-697)/2
box=(X0,Y0,X0+64*S,Y0+64*S)
mod=M.crop(tuple(int(round(v)) for v in box)).resize((64,64),Image.BOX)
def on(bgc,im,sc):
    b=Image.new('RGBA',im.size,bgc+(255,)); b.alpha_composite(im); b=b.convert('RGB')
    return b.resize((im.size[0]*sc,im.size[1]*sc),Image.NEAREST)
W=8*64
panels=[on((232,232,232),spr,8), mod.resize((W,W),Image.NEAREST)]
if len(sys.argv)>3:
    pv=Image.open(sys.argv[3]); pv.load(); panels.insert(1,on((232,232,232),pv.convert('RGBA'),8))
# gezicht: cols 4..46, rows 17..41
c0,r0,c1,r1=4,17,46,41
fs=on((232,232,232),spr.crop((c0,r0,c1,r1)),12)
mcrop=M.crop((int(X0+c0*S),int(Y0+r0*S),int(X0+c1*S),int(Y0+r1*S))).resize(fs.size,Image.LANCZOS)
tot_w=max(len(panels)*W, fs.size[0]*2+20)
out=Image.new('RGB',(tot_w, W+20+fs.size[1]+20+64+10),(255,255,255))
for k,p in enumerate(panels): out.paste(p,(k*W,0))
out.paste(fs,(0,W+20)); out.paste(mcrop,(fs.size[0]+20,W+20))
y=W+20+fs.size[1]+20
out.paste(on((232,232,232),spr,1),(10,y)); out.paste(on((40,40,48),spr,1),(90,y)); out.paste(on((152,208,160),spr,1),(170,y))
out.paste(on((232,232,232),spr,2),(250,y-64+64))
out.save(sys.argv[2])
