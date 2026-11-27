# vel r4: r4 | r3 | model op 8x (model in eigen verhouding); hoofd 12x: v1 | v2 | r3 | model (gezicht gelijk 1,28x) | overlay v1 op model; 1x
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image, ImageDraw
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104)
def rgb(o,pal=PAL3,bg=(255,255,255)): return Image.fromarray(np.array([[bg if v==0 else pal[v] for v in r] for r in o],np.uint8))
PX,FX,PY,FY=5.704,5.16,5.692,3.088; MY,MX=-21,-2
o=np.load('r4/pachamama_r4.npy'); o2=np.load('r4/pachamama_r4_v2.npy'); o3=np.load('r3/pachamama_r3.npy')
r4=rgb(o).resize((512,512),Image.NEAREST); r4.save('r4/pachamama_r4_8x.png')
M=Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')
md=Image.new('RGB',(int(round(192*PX)),int(round(192*PY))),'white'); md.paste(M,(int(round(-(FX+MX*PX))),int(round(-(FY+MY*PY)))))
md=md.resize((512,int(round(512*PY/PX))),Image.LANCZOS)
y0,y1,x0,x1=8,34,17,44; S=12; W,H=(x1-x0)*S,(y1-y0)*S
kop=lambda a: rgb(a[y0:y1,x0:x1]).resize((W,H),Image.NEAREST)
mg=Image.open('r4/natief_g2.png').convert('RGB').crop((MX+3*x0,MY+3*y0,MX+3*x1,MY+3*y1)).resize((W,H),Image.LANCZOS)
ov=Image.blend(mg,kop(o),.5)
koppen=[('v1: wenkbrauw op modelplek, lichtpixel modelplek',kop(o)),('v2: wenkbrauw hoger + licht ertussen',kop(o2)),('r3',kop(o3)),('model (gezicht gelijk 1,28x)',mg),('overlay v1 50% op model',ov)]
vel=Image.new('RGB',(max(3*522,5*(W+8)),20+512+34+H+180),(235,235,235)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(((r4,'r4 8x (hoofd v1)'),(rgb(o3).resize((512,512),Image.NEAREST),'r3 8x'),(md,'model r7 (eigen verhouding)'))): vel.paste(im,(i*522,20)); d.text((i*522+4,4),t,fill=0)
yk=20+512+34
for i,(t,im) in enumerate(koppen): vel.paste(im,(i*(W+8),yk)); d.text((i*(W+8)+3,yk-14),t,fill=0)
y2=yk+H+20
for i,bg in enumerate(((255,255,255),(248,248,240),(40,40,48),(0,0,0))):
  t=rgb(o,bg=bg); vel.paste(t.resize((128,128),Image.NEAREST),(i*140,y2)); vel.paste(t,(600+i*80,y2+30))
d.text((600,y2+10),'1x',fill=0)
vel.save('r4/vel.png'); print(vel.size)
