import sys,numpy as np; from PIL import Image, ImageDraw
H=lambda c:[int(c[i:i+2],16) for i in (1,3,5)]
PAL=['#1e170e','#433425','#5f4b3a','#765a43','#9f7e65','#b39b87','#36332b','#4e4a44','#7b7975','#a39b93','#d8c8b0']
P=np.array([H(c) for c in PAL],np.uint8)
def rgba(o):
    r=np.zeros((64,64,4),np.uint8); r[o>0,:3]=P[o[o>0]-1]; r[o>0,3]=255; return Image.fromarray(r,'RGBA')
if __name__=='__main__':
    o=np.load(sys.argv[1]); im=rgba(o); w=Image.new('RGBA',(64,64),'white'); w=Image.alpha_composite(w,im).convert('RGB')
    Z=14; c=w.crop((2,24,60,64)).resize((58*Z,40*Z),Image.NEAREST); d=ImageDraw.Draw(c)
    for x in range(2,60):
        if x%5==0: d.line([((x-2)*Z,0),((x-2)*Z,c.size[1])],fill=(255,0,0)); d.text(((x-2)*Z+2,2),str(x),fill=(255,0,0))
    for y in range(24,64):
        if y%5==0: d.line([(0,(y-24)*Z),(c.size[0],(y-24)*Z)],fill=(255,0,0)); d.text((2,(y-24)*Z+2),str(y),fill=(255,0,0))
    c.save(sys.argv[2])
