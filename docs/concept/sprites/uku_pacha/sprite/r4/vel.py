# vel.png: r4 | r3 | model (8x), close-ups koppen en kronkels (12x, model | r4), r4 1x op licht en donker
import geom
from PIL import Image, ImageDraw
def modelvak(x0,y0,x1,y1,z):
    nat=Image.open(geom.D+'/../../model/r2_natief.png').convert('RGB').resize((1000,1000),Image.NEAREST)
    def s2b(i,j): return (geom.X0+(i-geom.OX)/geom.F)*10,(geom.Y0+(j-geom.OY)/geom.F)*10
    a=s2b(x0,y0); b=s2b(x1,y1)
    return nat.crop((round(a[0]),round(a[1]),round(b[0]),round(b[1]))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def sprite(p,x0,y0,x1,y1,z,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im)
    return b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
R2='uku_pacha_r4.png'; R1='../r3/uku_pacha_r3.png'
W=3*512+4*16; o=Image.new('RGB',(W,2600),(235,235,235)); d=ImageDraw.Draw(o)
for k,(im,t) in enumerate([(sprite(R2,0,0,64,64,8),'r4'),(sprite(R1,0,0,64,64,8),'r3'),(modelvak(0,0,64,64,8),'model (Gemini r2)')]):
    o.paste(im,(16+k*528,30)); d.text((16+k*528,10),t,fill='black')
y=580
for (x0,y0,x1,y1,t) in [(0,8,24,29,'linkerkop'),(27,1,51,17,'rechterkop'),(12,16,46,46,'borst/buik beide nekken')]:
    m=modelvak(x0,y0,x1,y1,12); s=sprite(R2,x0,y0,x1,y1,12)
    d.text((16,y),t+': model | r4 (12x)',fill='black'); o.paste(m,(16,y+20)); o.paste(s,(16+m.width+16,y+20)); y+=m.height+40
y0c=y
x=16
for (a,b,c,e,t) in [(2,40,30,63,'kronkels links'),(26,38,56,63,'kronkels rechts')]:
    m=modelvak(a,b,c,e,12); s=sprite(R2,a,b,c,e,12)
    d.text((x,y0c),t+': model | r4 (12x)',fill='black'); o.paste(m,(x,y0c+20)); o.paste(s,(x+m.width+8,y0c+20)); x+=2*m.width+40
    hmax=m.height
y=y0c+hmax+50
d.text((16,y),'r4 op 1x en 2x, licht en donker',fill='black')
for k,bg in enumerate([(255,255,255),(248,248,240),(40,48,64),(16,16,16)]):
    o.paste(sprite(R2,0,0,64,64,1,bg),(16+k*80,y+20)); o.paste(sprite(R2,0,0,64,64,2,bg),(360+k*140,y+20))
o=o.crop((0,0,W,y+170)); o.save('vel.png'); print(o.size)
