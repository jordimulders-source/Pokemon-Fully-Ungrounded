# vel r3: r3 | r2 | model op 8x; kop 12x: oogvarianten A/B/C + model (vergroot gezicht); 1x
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image, ImageDraw
exec(open('r3/r3.py').read().split("PAL3=list(PAL);")[1].split("\n")[0].join(["PAL3=list(PAL);",""])) if False else None
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104)
MY,MX=-21,-2
def rgb(o,pal,bg=(255,255,255)): return Image.fromarray(np.array([[bg if v==0 else pal[v] for v in r] for r in o],np.uint8))
o=np.load('r3/pachamama_r3.npy'); o2=np.load('r2/pachamama_r2.npy')
r3=rgb(o,PAL3).resize((512,512),Image.NEAREST); r2=rgb(o2,PAL).resize((512,512),Image.NEAREST)
r3.save('r3/pachamama_r3_8x.png')
M=Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB'); PX,FX,PY,FY=5.704,5.16,5.692,3.088
md=Image.new('RGB',(int(192*PX),int(192*PY)),'white'); md.paste(M,(int(-(FX+MX*PX)),int(-(FY+MY*PY)))); md=md.resize((512,512),Image.LANCZOS)
y0,y1,x0,x1=9,33,18,42; S=12
koppen=[]
for v in 'ABC':
  f='r3/pachamama_r3.npy' if v=='A' else 'r3/pachamama_r3_%s.npy'%v
  koppen.append(('oog '+v,rgb(np.load(f)[y0:y1,x0:x1],PAL3).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)))
koppen.append(('r2',rgb(o2[y0:y1,x0:x1],PAL).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)))
mg=Image.open('natief_g1.png').convert('RGB').crop((MX+3*x0,MY+3*y0,MX+3*x1,MY+3*y1)).resize(((x1-x0)*S,(y1-y0)*S),Image.LANCZOS)
koppen.append(('model (vergroot gezicht)',mg))
kw,kh=koppen[0][1].size
W=max(3*522,5*(kw+10)); vel=Image.new('RGB',(W,20+512+30+kh+190),(235,235,235)); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(((r3,'r3 8x (oog A)'),(r2,'r2 8x'),(md,'model r7'))): vel.paste(im,(i*522,20)); d.text((i*522+4,4),t,fill=0)
yk=20+512+30
for i,(t,im) in enumerate(koppen): vel.paste(im,(i*(kw+10),yk)); d.text((i*(kw+10)+4,yk-14),'kop 12x: '+t,fill=0)
y2=yk+kh+20
for i,bg in enumerate(((255,255,255),(248,248,240),(40,40,48),(0,0,0))):
  t=rgb(o,PAL3,bg); vel.paste(t.resize((128,128),Image.NEAREST),(i*140,y2)); vel.paste(t,(600+i*80,y2+30))
d.text((600,y2+10),'1x',fill=0)
vel.save('r3/vel.png'); print(vel.size)
