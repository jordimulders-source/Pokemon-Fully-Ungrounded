# vel: A | B | C op 8x + 1x/2x op licht en donker; controle hoofd = r1 (pixeldiff 0) en kleuren.
import numpy as np; from PIL import Image, ImageDraw
kop=np.load('kop_r1.npy'); R1=np.load('../sprite_r1/r1_schoon.npy')
assert ((kop>0)<= (R1>0)).all() and (R1[kop>0]==kop[kop>0]).all()
N=[('A: lijf 1x (exact)','sunflora_evo_r2_A'),('B: lijf 2x kleiner (2x2-regel)','sunflora_evo_r2_B'),('C: lijf 1,25x groter (vaste rij/kolomverdubbeling)','sunflora_evo_r2_C')]
v=Image.new('RGB',(3*532,512+30+150),'white'); d=ImageDraw.Draw(v)
for k,(t,f) in enumerate(N):
    C=np.load(f+'.npy'); print(f,'hoofddiff t.o.v. r1:',int((C[kop>0]!=kop[kop>0]).sum()),'kleuren:',len(np.unique(C)))
    S=Image.open(f+'.png').convert('RGBA'); b=S.resize((512,512),Image.NEAREST)
    v.paste(b,(k*532,24),b); d.text((k*532+4,6),t,fill='black')
    for i,bg in enumerate([(248,248,248),(40,40,48)]):
        q=Image.new('RGB',(64,64),bg); q.paste(S,(0,0),S); v.paste(q,(k*532+i*74,550)); v.paste(q.resize((128,128),Image.NEAREST),(k*532+160+i*140,550))
v.save('vel.png')
