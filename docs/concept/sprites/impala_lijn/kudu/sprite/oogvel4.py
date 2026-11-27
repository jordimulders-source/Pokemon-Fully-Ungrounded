# Vel zwarte oogvarianten r4: hoofd (spritex 0..24, y 14..32) op 8x per variant + model op dezelfde schaal + bron-oog op 8x
from PIL import Image, ImageDraw
import oog4
import tempfile; S=tempfile.gettempdir()+'/'
def rgba(p):
    im=Image.open(p); im.save(S+'_o.png',transparency=0); return Image.open(S+'_o.png').convert('RGBA')
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def g3(n,box):
    im=Image.open(G+n+'/anim_front_gba.png'); p=open(G+n+'/normal_gba.pal').read().split('\n')[3:19]
    cols=[v for l in p if l.strip() for v in map(int,l.split())]; im=im.copy(); im.putpalette(cols+[0]*(768-len(cols)))
    return im.convert('RGB').crop(box)
BRON={'A':('kangaskhan',(36,35,46,44)),'B':('ponyta',(14,22,24,31)),'C':('flareon',(20,26,30,35)),'D':('ponyta',(14,22,24,31))}
z=8; cx0,cy0,cx1,cy1=0,14,24,32; w=(cx1-cx0)*z; h=(cy1-cy0)*z
V=Image.new('RGBA',(5*(w+16)+10,h+80+110),(255,255,255,255)); d=ImageDraw.Draw(V)
for i,v in enumerate('ABCD'):
    f='r4/kudu_r4.png' if v=='B' else f'r4/kudu_r4_oog{v}.png'
    s=rgba(f).crop((6+cx0,cy0,6+cx1,cy1)).resize((w,h),Image.NEAREST); x=10+i*(w+16)
    V.paste(Image.new('RGBA',(w,h),(170,200,225,255)),(x,40)); V.paste(s,(x,40),s)
    d.text((x,4),v+': '+oog4.VAR[v][0],fill=(0,0,0)); d.text((x,18),'('+('in kudu_r4' if v=='B' else 'variant')+')',fill=(0,0,0))
    n,box=BRON[v]; b=g3(n,box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST); V.paste(b,(x,h+60)); d.text((x,h+46),'bron: %s %s (anim_front_gba)'%(n,box),fill=(0,0,0))
m=Image.open('r3/model_A3.png').convert('RGBA').crop((91+cx0*16,cy0*16,91+cx1*16,cy1*16)).resize((w,h),Image.LANCZOS)
x=10+4*(w+16); V.paste(m,(x,40)); d.text((x,4),'model A3 (lid rij 22, x 10-13)',fill=(0,0,0))
V.save('r4/oog_zwart_varianten.png'); print(V.size)
