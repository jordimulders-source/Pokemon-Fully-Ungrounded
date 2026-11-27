# keuzevel r5: hoofden 12x (A B C D | r4 v1 | model gezicht 1,28x) + elke variant op 1x en 4x in de hele sprite
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image, ImageDraw
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104); MY,MX=-21,-2
def rgb(o,bg=(255,255,255)): return Image.fromarray(np.array([[bg if v==0 else PAL3[v] for v in r] for r in o],np.uint8))
y0,y1,x0,x1=10,32,19,40; S=12; W,H=(x1-x0)*S,(y1-y0)*S
T={'A':'A: pupil midden','B':'B: A + poten recht omlaag','C':'C: A + bovenlijn tint 3','D':'D: A + B + wenkbrauw neutraal'}
O={k:np.load('r5/pachamama_r5_%s.npy'%k) for k in 'ABCD'}; r4=np.load('r4/pachamama_r4.npy')
koppen=[(T[k],rgb(O[k][y0:y1,x0:x1]).resize((W,H),Image.NEAREST)) for k in 'ABCD']+[('r4 v1',rgb(r4[y0:y1,x0:x1]).resize((W,H),Image.NEAREST))]
koppen.append(('model (gezicht 1,28x)',Image.open('r4/natief_g2.png').convert('RGB').crop((MX+3*x0,MY+3*y0,MX+3*x1,MY+3*y1)).resize((W,H),Image.LANCZOS)))
vel=Image.new('RGB',(6*(W+8),H+16+240),(235,235,235)); d=ImageDraw.Draw(vel)
for i,(t,im) in enumerate(koppen): vel.paste(im,(i*(W+8),16)); d.text((i*(W+8)+3,2),t,fill=0)
y2=H+40
for i,k in enumerate('ABCD'):
  x=i*(W+8); d.text((x+3,y2-14),k+' (3x en 1x)',fill=0)
  vel.paste(rgb(O[k]).resize((180,180),Image.NEAREST),(x,y2)); vel.paste(rgb(O[k]),(x+186,y2+20)); vel.paste(rgb(O[k],(40,40,48)),(x+186,y2+100))
vel.save('r5/vel.png'); print(vel.size)
