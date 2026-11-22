# vel r3: model_16 verkleind (8x) | voeten zoals model | binnen | buiten | slap (8x) + 1x/2x licht en donker
import numpy as np; from PIL import Image, ImageDraw
kop=np.load('../sprite_r2/kop_r1.npy')
V=[('voeten zoals model','model'),('binnen: L +20, R -20 gr','binnen'),('buiten: L -20, R +20 gr','buiten'),('slap: L +12, R +30 gr','slap')]
W=5*532; v=Image.new('RGB',(W,24+512+20+140),'white'); d=ImageDraw.Draw(v)
m=Image.open('model16_64_8x.png'); v.paste(m,(0,24)); d.text((4,6),'model_16 verkleind, zelfde raster (8x)',fill='black')
for k,(t,n) in enumerate(V):
    C=np.array(Image.open('sunflora_evo_r3_voet_%s.png'%n)); assert (C[kop>0]==kop[kop>0]).all()
    S=Image.open('sunflora_evo_r3_voet_%s.png'%n).convert('RGBA'); b=S.resize((512,512),Image.NEAREST)
    x=(k+1)*532; v.paste(b,(x,24),b); d.text((x+4,6),'r3 '+t,fill='black')
    for i,bg in enumerate([(248,248,248),(40,40,48)]):
        q=Image.new('RGB',(64,64),bg); q.paste(S,(0,0),S); v.paste(q,(x+i*74,556)); v.paste(q.resize((128,128),Image.NEAREST),(x+160+i*140,556))
    print(n,'kleuren',len(np.unique(C)))
v.save('vel.png')
