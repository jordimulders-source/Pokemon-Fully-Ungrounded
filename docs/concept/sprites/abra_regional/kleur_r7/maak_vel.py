# maak_vel.py (vanuit kleur_r7/): abra_r7_A_8x.png, abra_r7_B_8x.png, vel.png
# vel: r7 A 8x | r7 B 8x | basis_F 8x | model (natief raster) zelfde schaal | 1x A en B op licht/donker + regionale Kadabra 1x
from PIL import Image, ImageDraw
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/e768f5de-0252-58bb-8bc9-76aca5f6423c/scratchpad/'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save(S+'_v.png',transparency=im.info.get('transparency',0)); im=Image.open(S+'_v.png')
    return im.convert('RGBA')
def op(img,kl=(255,255,255,255)):
    b=Image.new('RGBA',img.size,kl); b.alpha_composite(img); return b.convert('RGB')
A=rgba('abra_r7_A.png'); B=rgba('abra_r7_B.png'); F=rgba('basis_F.png')
kd=Image.open('../../kadabra_regional/af/kadabra_charlatan.png'); kd.save(S+'_k.png',transparency=0); kd=Image.open(S+'_k.png').convert('RGBA')
op(A).resize((512,512),Image.NEAREST).save('abra_r7_A_8x.png'); op(B).resize((512,512),Image.NEAREST).save('abra_r7_B_8x.png')
nat=Image.open('../kleur_r1/natief.png').convert('RGB')
mod=Image.new('RGB',(128,128),'white'); mod.paste(nat,(1,14)); mod=mod.resize((512,512),Image.NEAREST)
klein=Image.new('RGB',(512,512),(220,220,220)); dk=ImageDraw.Draw(klein)
dk.text((16,6),'1x:  A        B        Kadabra (regionaal)',fill=(0,0,0))
for r,(kl,t) in enumerate((((248,248,248,255),'licht'),((40,40,48,255),'donker'),((152,208,160,255),'groen'))):
    for k,img in enumerate((A,B,kd)): klein.paste(op(img,kl),(16+k*80,20+r*80))
    dk.text((260,44+r*80),t,fill=(0,0,0))
dk.text((16,272),'2x: A licht | B licht | A donker',fill=(0,0,0))
for k,(img,kl) in enumerate(((A,(248,248,248,255)),(B,(248,248,248,255)),(A,(40,40,48,255)))):
    klein.paste(op(img,kl).resize((128,128),Image.NEAREST),(16+k*164,290))
v=Image.new('RGB',(5*532,560),'white'); d=ImageDraw.Draw(v)
for k,(x,t) in enumerate(((op(A).resize((512,512),Image.NEAREST),'r7 A (modeltonen) 8x'),(op(B).resize((512,512),Image.NEAREST),'r7 B (huid naar Kadabra) 8x'),
                          (op(F).resize((512,512),Image.NEAREST),'basis_F 8x'),(mod,'model (natief raster), zelfde schaal'),(klein,'1x/2x op licht, donker, groen'))):
    v.paste(x,(k*532,40)); d.text((k*532+8,12),t,fill=(0,0,0))
v.save('vel.png')
