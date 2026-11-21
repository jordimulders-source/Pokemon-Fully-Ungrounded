# natief model met spriteraster (1 spritecel = 2x2 natief), voor het overtrekken van veervormen. sprite (r,c) = natief (13+2(r-9), 67+2(c-4))
import sys; from PIL import Image, ImageDraw
n=Image.open('natief.png').convert('RGB'); Z=10
def vel(c0,c1,r0,r1,out):
    x0=67+2*(c0-4); y0=13+2*(r0-9)
    pad=Image.new('RGB',(n.width+100,n.height+100),'white'); pad.paste(n,(50,50))
    im=pad.crop((x0+50,y0+50,x0+50+2*(c1-c0),y0+50+2*(r1-r0))).resize((2*(c1-c0)*Z,2*(r1-r0)*Z),Image.NEAREST); d=ImageDraw.Draw(im)
    for c in range(c0,c1+1):
        X=(c-c0)*2*Z; d.line([(X,0),(X,im.height)],fill=(255,0,0) if c%5==0 else (170,170,255))
        if c%5==0: d.text((X+2,2),str(c),fill=(255,0,0))
    for r in range(r0,r1+1):
        Y=(r-r0)*2*Z; d.line([(0,Y),(im.width,Y)],fill=(255,0,0) if r%5==0 else (170,170,255))
        if r%5==0: d.text((2,Y+2),str(r),fill=(255,0,0))
    im.save(out)
vel(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5])
