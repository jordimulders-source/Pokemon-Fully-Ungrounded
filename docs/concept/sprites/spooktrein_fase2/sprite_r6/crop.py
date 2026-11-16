import sys; from PIL import Image
x0,y0,x1,y1=map(int,sys.argv[1:5]); Z=int(sys.argv[6]) if len(sys.argv)>6 else 10
def L(p):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,(255,255,255,255)); return Image.alpha_composite(b,im).convert('RGB')
ims=[L(sys.argv[7] if len(sys.argv)>7 else 'sprite.png'),L('r5.png'),Image.open('model_geschaald.png').convert('RGB')]
w=(x1-x0)*Z; h=(y1-y0)*Z; v=Image.new('RGB',(w,3*h+20),'white')
for n,im in enumerate(ims): v.paste(im.crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(0,n*(h+10)))
v.save(sys.argv[5])
