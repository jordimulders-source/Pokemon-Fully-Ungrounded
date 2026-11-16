import sys; from PIL import Image, ImageDraw
x0,y0,x1,y1=map(int,sys.argv[1:5]); Z=int(sys.argv[6]); files=sys.argv[7:]
def L(p):
    if p.endswith('model_geschaald.png'): return Image.open(p).convert('RGB')
    im=Image.open(p); im=im.convert('RGBA'); b=Image.new('RGBA',im.size,(255,255,255,255)); return Image.alpha_composite(b,im).convert('RGB')
w=(x1-x0)*Z; h=(y1-y0)*Z; V=Image.new('RGB',(len(files)*(w+10),h+14),'white'); d=ImageDraw.Draw(V)
for n,f in enumerate(files):
    V.paste(L(f).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(n*(w+10),14))
    for i in range(x0,x1,2): d.text((n*(w+10)+(i-x0)*Z+1,2),str(i%100),fill=(255,0,0))
    for j in range(y0,y1,2): d.text((n*(w+10)+1,14+(j-y0)*Z+1),str(j),fill=(255,0,0))
V.save(sys.argv[5])
