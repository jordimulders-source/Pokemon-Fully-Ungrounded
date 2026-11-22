# C: dieper/donkerder groen. D: C + paars accent op het lijfje/de stengel (schaduwtint 12 -> paars, index 15). Pixels gelijk aan r5 behalve indexwissel 12->15 in de stengelzone.
import numpy as np; from PIL import Image, ImageDraw
im=Image.open('sunflora_evo_r5.png'); a=np.array(im); pal=im.getpalette()
donker={11:(36,70,40),12:(56,110,52),13:(86,150,66),14:(126,190,92)}
pC=list(pal)
for i,c in donker.items(): pC[3*i:3*i+3]=c
d=a.copy(); z=np.zeros_like(a,bool); z[47:54,30:39]=True; d[z&(a==12)]=15
pD=list(pC); pD[45:48]=(112,64,120)
def save(arr,p,n):
    o=Image.fromarray(arr,'P'); o.putpalette(p); o.save(n+'.png',transparency=0)
    Image.open(n+'.png').convert('RGBA').resize((512,512),Image.NEAREST).save(n+'_8x.png')
save(a,pC,'sunflora_evo_r5_C_donkergroen'); save(d,pD,'sunflora_evo_r5_D_paarsaccent')
names=[('A: modelgroen','sunflora_evo_r5_8x.png'),('B: Sunflora-groen','sunflora_evo_r5_sunfloragroen_8x.png'),('C: dieper groen','sunflora_evo_r5_C_donkergroen_8x.png'),('D: C + paars op lijfje','sunflora_evo_r5_D_paarsaccent_8x.png')]
v=Image.new('RGB',(4*530,600),'white'); dr=ImageDraw.Draw(v)
for k,(t,f) in enumerate(names):
    s=Image.open(f); v.paste(s,(k*530+10,30),s); dr.text((k*530+10,8),t,fill='black')
    one=Image.open(f.replace('_8x','')).convert('RGBA'); v.paste(one,(k*530+10,540),one)
    bg=Image.new('RGBA',(64,64),(40,40,48,255)); bg.alpha_composite(one); v.paste(bg,(k*530+90,540))
v.save('vel_abcd.png')
