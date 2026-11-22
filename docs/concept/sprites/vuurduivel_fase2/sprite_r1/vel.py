# vel.py SPRITE.png UIT [VORIGE.png]: sprite 8x | (vorige 8x) | model (natief op 4x = zelfde schaal) ;
# daaronder gezicht 12x naast het model (kop.py-gebied) en 1x op licht en donker
import sys, subprocess; from PIL import Image, ImageDraw
X0,Y0,NX,NY=[int(v) for v in open('info.txt').read().split()]
def op(f,bgc=(255,255,255)):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(Image.open(f).convert('RGBA')); return b.convert('RGB')
n=Image.open('natief.png')
mod=Image.new('RGB',(128,128),'white'); cx,cy=NX-X0*2,NY-Y0*2; mod.paste(n.crop((max(cx,0),max(cy,0),cx+128,cy+128)),(max(-cx,0),max(-cy,0)))
pan=[op(sys.argv[1]).resize((512,512),Image.NEAREST)]
if len(sys.argv)>3: pan.append(op(sys.argv[3]).resize((512,512),Image.NEAREST))
pan.append(mod.resize((512,512),Image.NEAREST))
subprocess.run(['python3','kop.py',sys.argv[1],'_kop.png','14','10','34','30'])
k=Image.open('_kop.png')
W=max(len(pan)*522,k.width+10); H=512+10+k.height+10+80
v=Image.new('RGB',(W,H),(235,235,235))
for i,p in enumerate(pan): v.paste(p,(i*522,0))
v.paste(k,(0,522))
y=522+k.height+10
for i,c in enumerate([(255,255,255),(200,220,200),(40,40,56),(16,16,16)]):
    v.paste(op(sys.argv[1],c),(i*74,y))
v.save(sys.argv[2])
