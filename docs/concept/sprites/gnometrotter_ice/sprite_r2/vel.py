# vel.py [a.png b.png titelA titelB uit.png model] -> 8x: a | b | model op schaal; 1x op licht/donker; 1x/2x naast elkaar en Rock
import sys; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite'); from kijk import sprite, model_op_schaal
A=sys.argv[1] if len(sys.argv)>1 else 'gnometrotter_ice.png'; Bp=sys.argv[2] if len(sys.argv)>2 else '../sprite/gnometrotter_ice.png'
tA=sys.argv[3] if len(sys.argv)>3 else 'Ice r2'; tB=sys.argv[4] if len(sys.argv)>4 else 'Ice r1'
uit=sys.argv[5] if len(sys.argv)>5 else 'vel.png'; MOD=sys.argv[6] if len(sys.argv)>6 else '../r3/gemini_r3_lijf.png'
ROCK='../../gnometrotter_rock/sprite_r2/gnometrotter_rock.png'
sprite(A).resize((512,512),Image.NEAREST).save(A[:-4]+'_8x.png')
import kijk
V=Image.new('RGB',(3*524,24+512+20+80+20+150),'white'); d=ImageDraw.Draw(V)
mdl=kijk.model_op_schaal(MOD,n=512)
for i,(p,t) in enumerate(((sprite(A).resize((512,512),Image.NEAREST),tA),(sprite(Bp).resize((512,512),Image.NEAREST),tB),(mdl,'model op schaal (gedeelde reductie)'))):
    V.paste(p,(i*524,24)); d.text((i*524+4,6),t,fill=(0,0,0))
y=24+512+20; x=0; d.text((0,y-14),'1x op licht en donker: '+tA,fill=(0,0,0))
for bg in [(255,255,255),(248,248,232),(144,192,152),(112,120,136),(40,48,56),(16,16,16)]:
    V.paste(sprite(A,bg),(x,y)); x+=72
y2=y+80+20; d.text((0,y2-14),'1x en 2x: %s | %s | Rock (zelfde reductie)'%(tA,tB),fill=(0,0,0)); x=0
L=[A,Bp,ROCK]
for p in L: V.paste(sprite(p,(248,248,232)),(x,y2)); x+=68
x+=8
for p in L: V.paste(sprite(p,(248,248,232)).resize((128,128),Image.NEAREST),(x,y2)); x+=136
V.save(uit); print(uit,V.size)
