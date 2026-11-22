# vel.py SPRITE.png UIT VORIGE.png: r5 8x | r3 8x | model (natief 4x = zelfde schaal); gezicht 16x naast het modelgezicht; 1x op licht en donker
import sys, subprocess, os; from PIL import Image, ImageDraw
X0,Y0,NX,NY=[int(v) for v in open('info.txt').read().split()]
def op(f,bgc=(255,255,255)):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(Image.open(f).convert('RGBA')); return b.convert('RGB')
n=Image.open('natief.png')
mod=Image.new('RGB',(128,128),'white'); cx,cy=NX-X0*2,NY-Y0*2; mod.paste(n.crop((max(cx,0),max(cy,0),cx+128,cy+128)),(max(-cx,0),max(-cy,0)))
pan=[op(sys.argv[1]).resize((512,512),Image.NEAREST),op(sys.argv[3]).resize((512,512),Image.NEAREST),mod.resize((512,512),Image.NEAREST)]
env=dict(os.environ,Z='16')
subprocess.run(['python3','kop.py',sys.argv[1],'_kop.png','12','20','33','42'],env=env)
k=Image.open('_kop.png'); os.remove('_kop.png')
W=max(3*522,k.width+10); H=20+512+30+k.height+30+150
v=Image.new('RGB',(W,H),(235,235,235)); d=ImageDraw.Draw(v)
for i,(p,t) in enumerate(zip(pan,['r5 (8x)','r3 (8x)','model (zelfde schaal)']) ):
    v.paste(p,(i*522,20)); d.text((i*522+4,4),t,fill='black')
d.text((4,20+512+12),'gezicht 16x: model (links) | r5 (rechts)',fill='black')
v.paste(k,(0,20+512+30))
y=20+512+30+k.height+30
d.text((4,y-14),'1x en 2x op licht en donker',fill='black')
for i,c in enumerate([(255,255,255),(200,220,200),(40,40,56),(16,16,16)]):
    v.paste(op(sys.argv[1],c),(i*74,y))
    v.paste(op(sys.argv[1],c).resize((128,128),Image.NEAREST),(320+i*138,y))
v.save(sys.argv[2])
