# a | b | model op dezelfde schaal (hi-res crop van het spritevlak, verhouding PX:PY behouden)
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image, ImageDraw
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104)
def rgb(o,pal): return Image.fromarray(np.array([[(255,255,255) if v==0 else pal[v] for v in r] for r in o],np.uint8))
PX,FX,PY,FY=5.704,5.16,5.692,3.088; MY,MX=-21,-2; S=int(sys.argv[1])
M=Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')
# spritevlak 64x64 cellen = 192 natief breed (192*PX px) en 192 natief hoog (192*PY px): eigen verhouding, niet uitgerekt
x0=FX+MX*PX; y0=FY+MY*PY; md=Image.new('RGB',(int(round(192*PX)),int(round(192*PY))),'white'); md.paste(M,(int(round(-x0)),int(round(-y0))))
md=md.resize((64*S,int(round(64*S*PY/PX))),Image.LANCZOS)
ims=[]
for a in sys.argv[3:]:
  t,f=a.split('='); pal=PAL if 'r2' in f else PAL3
  ims.append((t,rgb(np.load(f),pal).resize((64*S,64*S),Image.NEAREST)))
ims.append(('model r7 (eigen verhouding)',md))
v=Image.new('RGB',(len(ims)*(64*S+10),64*S+20),(235,235,235)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate(ims): v.paste(im,(i*(64*S+10),18)); d.text((i*(64*S+10)+4,3),t,fill=0)
v.save(sys.argv[2]); print(v.size)
