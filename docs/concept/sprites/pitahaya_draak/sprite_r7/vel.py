# vel r7: r7 | r6 | model op 8x; rechter- en linkerarm 12x (r7 | r6 | natief model); 1x/2x licht/donker van r7 en r6
import numpy as np; from PIL import Image, ImageDraw
n=Image.open('natief.png').convert('RGB')          # spritepixel (X,Y) = natief blok (3X+4, 3Y+6)
def rgba(f,bg):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(Image.open(f).convert('RGBA')); return b.convert('RGB')
LG=(214,222,214); DG=(40,44,52); C=(12,4,50,58); z=8; w=(C[2]-C[0])*z; h=(C[3]-C[1])*z
m=n.crop((4,6,196,198)).resize((64,64),Image.BOX); ma=np.asarray(m).copy(); ma[ma.min(2)>=200]=LG; m=Image.fromarray(ma)
ARMEN=(('rechterarm',(33,35,48,50)),('linkerarm',(14,36,28,48)))
az=12
H=24+h+sum(14+(A[3]-A[1])*az+16 for _,A in ARMEN)+250
W=max(3*(w+10),max(3*((A[2]-A[0])*az+10) for _,A in ARMEN))+20
v=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(v)
for k,(t,im) in enumerate((('r7 (8x)',rgba('pitahaya_r7.png',LG)),('r6 (8x)',rgba('pitahaya_r6.png',LG)),('model verkleind (BOX 3x3, 8x)',m))):
    v.paste(im.crop(C).resize((w,h),Image.NEAREST),(10+k*(w+10),24)); d.text((10+k*(w+10),6),t,fill='black')
yy=h+40
for naam,A in ARMEN:
    aw=(A[2]-A[0])*az; ah=(A[3]-A[1])*az
    am=n.crop((3*A[0]+4,3*A[1]+6,3*A[2]+4,3*A[3]+6)).resize((aw,ah),Image.NEAREST)
    for k,(t,im) in enumerate(((f'r7 {naam} 12x',rgba('pitahaya_r7.png',LG).crop(A).resize((aw,ah),Image.NEAREST)),
                               (f'r6 {naam} 12x',rgba('pitahaya_r6.png',LG).crop(A).resize((aw,ah),Image.NEAREST)),('model natief',am))):
        v.paste(im,(10+k*(aw+10),yy+14)); d.text((10+k*(aw+10),yy),t,fill='black')
    yy+=ah+30
for k,(t,f) in enumerate((('r7','pitahaya_r7.png'),('r6','pitahaya_r6.png'))):
    X=10+k*300; d.text((X,yy),t+': 1x licht/donker, 2x licht/donker',fill='black')
    v.paste(rgba(f,LG),(X,yy+14)); v.paste(rgba(f,DG),(X+70,yy+14))
    v.paste(rgba(f,LG).resize((128,128),Image.NEAREST),(X,yy+84)); v.paste(rgba(f,DG).resize((128,128),Image.NEAREST),(X+136,yy+84))
v.save('vel.png'); print(v.size)
