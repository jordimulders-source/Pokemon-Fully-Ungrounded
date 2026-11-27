# vel r2: r2 | v8 | model (8x), rode modelomtrek over r2, 1x/2x licht en donker
import numpy as np; from PIL import Image, ImageDraw
import lib1 as lib, modelover
def groot(p,s=8):
    a=Image.open(p).convert('RGBA').resize((64*s,64*s),Image.NEAREST); b=Image.new('RGBA',a.size,(255,255,255,255)); b.alpha_composite(a); return b
m=np.asarray(Image.open('../gemini/r1_eenvoud.png').convert('RGB')).astype(int).min(2)<225
f=lib.S/10.24*8; ox=(lib.OX+((0-9.25)/10.24-lib.X0)*lib.S)*8; oy=(lib.OY+((0-9.25)/10.24-lib.Y0)*lib.S)*8
z=Image.fromarray((m*255).astype('uint8')).resize((round(1024*f),round(1024*f)),Image.BILINEAR); can=Image.new('L',(512,512),0); can.paste(z,(round(ox),round(oy)))
M=np.asarray(can)>127; P=np.pad(M,1); rand=M&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
W=512; C0=160
vel=Image.new('RGBA',(3*(W+10)+10,2*(W-C0)+120),(236,236,236,255)); d=ImageDraw.Draw(vel)
for i,(t,p) in enumerate([('r2 8x',groot('terreurvogel_bijl_r2.png')),('v8 (start) 8x',groot('../swaps_r1/v8.png')),('model op spriteschaal',modelover.model_op(8).convert('RGBA'))]):
    x=10+i*(W+10); vel.alpha_composite(p.crop((0,C0,W,W)),(x,24)); d.text((x,8),t,fill=(0,0,0))
y2=24+W-C0+30
a=np.array(groot('terreurvogel_bijl_r2.png')); a[rand]=(230,0,0,255)
vel.alpha_composite(Image.fromarray(a).crop((0,C0,W,W)),(10,y2)); d.text((10,y2-16),'r2 met rode modelomtrek',fill=(0,0,0))
x=W+30
for j,(bg,nm) in enumerate([((248,248,240,255),'licht'),((40,44,52,255),'donker')]):
    d.text((x+j*330,y2-16),nm+': r2 1x 2x | v8 1x',fill=(0,0,0))
    for k,(p,s,o) in enumerate([('terreurvogel_bijl_r2.png',1,0),('terreurvogel_bijl_r2.png',2,70),('../swaps_r1/v8.png',1,206)]):
        b=Image.new('RGBA',(64*s,64*s),bg); b.alpha_composite(Image.open(p).convert('RGBA').resize((64*s,64*s),Image.NEAREST)); vel.alpha_composite(b,(x+j*330+o,y2))
vel.save('vel.png'); print(vel.size)
