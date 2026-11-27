# vel.png: sprite 8x naast het model op dezelfde schaal, close-ups ogen/handen 12x, 1x op licht en donker.
import sys; from gemeen import *; from PIL import ImageDraw
SP=sys.argv[1]; OUT=sys.argv[2]; VORIG=sys.argv[3] if len(sys.argv)>3 else None
S=np.array(Image.open(SP)); g=geo(); T=g['T']
M=Image.open('../model.png').convert('RGB')
def modelcrop(i0,j0,i1,j1,z):
    x0,y0=s2m(i0,j0); x1,y1=s2m(i1,j1)
    return M.crop((int(x0),int(y0),int(x1),int(y1))).resize(((i1-i0)*z,(j1-j0)*z),Image.LANCZOS)
def sp(i0,j0,i1,j1,z,A=None):
    A=S if A is None else A
    return rgba(A[j0:j1,i0:i1],(255,255,255,255)).resize(((i1-i0)*z,(j1-j0)*z),0)
ys,xs=np.where(S>0); bx=(max(0,xs.min()-2),max(0,ys.min()-2),min(64,xs.max()+3),min(64,ys.max()+3))
Z=8; w=(bx[2]-bx[0])*Z; h=(bx[3]-bx[1])*Z
panels=[('sprite 8x',sp(*bx,Z)),('model zelfde schaal',modelcrop(*bx,Z))]
if VORIG: panels.insert(1,('vorige',sp(*bx,Z,np.array(Image.open(VORIG)))))
og=json.load(open('ogen_geo.json')) if os.path.exists('ogen_geo.json') else None
ZB=(26,22,47,35)   # ogen
HL=(8,28,21,39); HR=(44,37,55,46)
close=[]
for nm,b in [('ogen',ZB),('hand links',HL),('hand rechts',HR)]:
    close.append((nm+' sprite 12x',sp(*b,12))); close.append((nm+' model 12x',modelcrop(*b,12)))
W=max(sum(p.width+16 for _,p in panels), sum(p.width+16 for _,p in close[:2])+0)
rows=[panels,close[:2],close[2:]]
H=sum(max(p.height for _,p in r)+24 for r in rows)+160
vel=Image.new('RGB',(max(W,sum(p.width+16 for _,p in close[2:])),H),(255,255,255)); d=ImageDraw.Draw(vel); y=0
for r in rows:
    x=0
    for nm,p in r: d.text((x,y+4),nm,fill='black'); vel.paste(p,(x,y+18)); x+=p.width+16
    y+=max(p.height for _,p in r)+24
for k,bg in enumerate([(255,255,255,255),(232,232,224,255),(40,40,48,255),(0,0,0,255)]):
    vel.paste(rgba(S,bg),(k*80,y+10))
    vel.paste(rgba(S,bg).resize((128,128),0),(330+k*140,y+10))
vel.save(OUT); print(OUT,vel.size)
