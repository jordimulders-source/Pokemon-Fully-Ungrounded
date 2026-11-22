# Pinsir-evolutie r9. Jordi bij r8 (letterlijk): "wat is er gebeurd met het hoofd?", "lekker opnieuw tekenen want dat kan je zo
# goed", "gewoon het model volgen", "je moest alleen de ogen een paar pixels aanpassen".
# r9: KOP (kopschild, stekels, gezicht, rug boven het schild) = r7 met kopstekels (sprite_r7/pinsir_evo_r7.png) pixel voor pixel;
#     alleen de ogen een paar pixels puntiger (niet kleiner, zoals het model), varianten A (met pupil) en B (zonder).
#     REST = r8 (sprite_r8/pinsir_evo_r8_A_<schild>.png): kaken, mond, romp, arm, been, staart, dekschild A/B, rugdoorns langs het schild.
# Bouwen: cd pinsir_evo && python3 sprite_r9/bouw.py [raster]
import sys, numpy as np
from PIL import Image
UIT='sprite_r9'
CH='.KLabcdopqrsvwxT'; C={c:i for i,c in enumerate(CH)}
R7=np.asarray(Image.open('sprite_r7/pinsir_evo_r7.png')).astype(int)
R8={s:np.asarray(Image.open('sprite_r8/pinsir_evo_r8_A_%s.png'%s)).astype(int) for s in 'AB'}
PAL=Image.open('sprite_r7/pinsir_evo_r7.png').getpalette()[:48]
assert PAL==Image.open('sprite_r8/pinsir_evo_r8_A_A.png').getpalette()[:48]
DEEL=np.load('sprite_r8/r7_delen.npy')
H=W=64; yy,xx=np.mgrid[:H,:W]
# kopzone: alles t/m rij 23 links van de rugdoorn van r8 (x<=45), en rij 24-28 t/m x44 behalve het dekschild (r7-delenkaart)
KOP=((yy<=23)&(xx<=45)) | ((yy>=24)&(yy<=28)&(xx<=44)&(DEEL!='schild'))
# ogen: alleen deze pixels wijken af van r7 (y, x): r7-waarde -> nieuw
OOG={'B':{(27,22):'T',(27,23):'T',            # nabij oog: rij erboven erbij -> wig met de punt links (naar het midden), 3 -> 5 px
          (28,17):'T',(28,18):'T'},           # ver oog: onderrij naar rechts verlengd -> wig met de punt naar het midden, 2 -> 4 px
     'A':{(27,22):'T',(27,23):'T',(28,22):'K',  # nabij oog: zelfde wig, pupil onderin het midden (zoals Gen 3 Pinsir / r8 A)
          (28,18):'T'}}                         # ver oog: r7-zwart op (28,17) wordt de pupil, punt (28,18) erbij
# naad rug r7 <-> rugdoorn r8 ((22,45) ligt net in de kopzone, de rest in r8-gebied): de r8-rugrand stond 2 px verder rechts dan de r7-rug -> losse
# r8-lijnresten weg en de r7-buitenlijn (x44) met 2 px lijn doorgetrokken naar de voet van de eerste rugdoorn (y, x): nieuw
NAAD={(20,46):'.',(21,46):'.',(22,45):'K',(22,46):'K'}
def opslaan(q,path):
    p=Image.fromarray(q.astype('uint8'),'P'); p.putpalette(PAL+[0]*(768-len(PAL))); p.save(path,transparency=0)
VAR={}
for ov in 'AB':
    for sv in 'AB':
        q=R8[sv].copy(); q[KOP]=R7[KOP]
        for (Y,X),ch in OOG[ov].items(): assert KOP[Y,X]; q[Y,X]=C[ch]
        for (Y,X),ch in NAAD.items(): q[Y,X]=C[ch]
        VAR[(ov,sv)]=q; opslaan(q,UIT+'/pinsir_evo_r9_%s_%s.png'%(ov,sv))
print('controle:')
for (ov,sv),q in VAR.items():
    im=Image.open(UIT+'/pinsir_evo_r9_%s_%s.png'%(ov,sv)); assert im.info.get('transparency')==0 and (np.asarray(im)==q).all()
    ogen=np.zeros((H,W),bool)
    for (Y,X) in OOG[ov]: ogen[Y,X]=True
    naad=np.zeros((H,W),bool)
    for (Y,X) in NAAD: naad[Y,X]=True
    dk=int((q[KOP&~ogen&~naad]!=R7[KOP&~ogen&~naad]).sum()); dr=int((q[~KOP&~naad]!=R8[sv][~KOP&~naad]).sum())
    eye=[(X,Y,CH[R7[Y,X]]+'>'+CH[q[Y,X]]) for (Y,X) in OOG[ov] if R7[Y,X]!=q[Y,X]]
    print('  %s_%s: kleuren %d | kop vs r7 buiten ogen/naad diff %d | rest vs r8_A_%s diff %d (buiten 4 naadpixels) | oogpixels %s'%(ov,sv,len(set(q.ravel())),dk,sv,dr,eye))
    assert dk==0 and dr==0 and len(set(q.ravel()))<=16
if 'raster' in sys.argv:
    q=VAR[('A','A')]; print('   '+''.join(str(x%10) for x in range(64)))
    for Y in range(10,34): print('%2d '%Y+''.join(CH[v] for v in q[Y]))
if 'raster' not in sys.argv:
    # vel: kop 12x r9 (B_A, A_A) | r8 | r7 | model; modelmasker (rode omtrek) over de r9-kop; hele sprite r9 | model 8x; 1x alle varianten
    sys.path.insert(0,'gereedschap')
    from PIL import ImageDraw
    from vel import rgbp, model_crop, M, CEL, MX0, MY0, DY
    a=np.asarray(M).astype(int); fg=a.min(2)<215; msk=np.zeros((H,W),bool)
    for j in range(H):
        for i in range(W):
            ya,yb=int(round(MY0+(j-DY)*CEL)),int(round(MY0+(j+1-DY)*CEL)); xa,xb=int(round(MX0+i*CEL)),int(round(MX0+(i+1)*CEL))
            blk=fg[max(ya,0):max(yb,0),max(xa,0):max(xb,0)]
            msk[j,i]=blk.size>0 and blk.mean()>=0.45
    box=(8,10,48,42); z=12; bw,bh=(box[2]-box[0])*z,(box[3]-box[1])*z
    f=lambda ov,sv: UIT+'/pinsir_evo_r9_%s_%s.png'%(ov,sv)
    Wv=4*bw+5*8; v=Image.new('RGB',(max(Wv,1100),2*bh+512+250),'white'); d=ImageDraw.Draw(v); y=2
    d.text((4,y),'kop 12x: r9 oog A (schild A) | r8 A_A | r7 | model',fill=(0,0,0)); y+=14
    ims=[rgbp(f('A','A')).crop(box).resize((bw,bh),Image.NEAREST),rgbp('sprite_r8/pinsir_evo_r8_A_A.png').crop(box).resize((bw,bh),Image.NEAREST),
         rgbp('sprite_r7/pinsir_evo_r7.png').crop(box).resize((bw,bh),Image.NEAREST),model_crop(*box,z)]
    for i,im in enumerate(ims): v.paste(im,(8+i*(bw+8),y))
    y+=bh+6
    d.text((4,y),'kop 12x: r9 oog B (schild A) met modelmasker (rood) | r9 oog A met modelmasker | 1x: AA AB BA BB',fill=(0,0,0)); y+=14
    for k,ov in enumerate('BA'):
        im=rgbp(f(ov,'A')).crop(box).resize((bw,bh),Image.NEAREST); dd=ImageDraw.Draw(im)
        for Y in range(box[1],box[3]):
            for X in range(box[0],box[2]):
                if not msk[Y,X]: continue
                px,py=(X-box[0])*z,(Y-box[1])*z
                if Y==0 or not msk[Y-1,X]: dd.line((px,py,px+z,py),fill=(255,0,0),width=2)
                if Y==H-1 or not msk[Y+1,X]: dd.line((px,py+z-1,px+z,py+z-1),fill=(255,0,0),width=2)
                if X==0 or not msk[Y,X-1]: dd.line((px,py,px,py+z),fill=(255,0,0),width=2)
                if X==W-1 or not msk[Y,X+1]: dd.line((px+z-1,py,px+z-1,py+z),fill=(255,0,0),width=2)
        v.paste(im,(8+k*(bw+8),y))
    for i,(ov,sv) in enumerate((('A','A'),('A','B'),('B','A'),('B','B'))):
        v.paste(rgbp(f(ov,sv)),(8+2*(bw+8)+i*70,y)); v.paste(rgbp(f(ov,sv),(40,48,56)),(8+2*(bw+8)+i*70,y+70))
    y+=bh+6
    d.text((4,y),'hele sprite 8x: r9 A_A | model op dezelfde maat',fill=(0,0,0)); y+=14
    v.paste(rgbp(f('A','A')).resize((512,512),Image.NEAREST),(8,y)); v.paste(model_crop(0,0,64,64,8),(528,y)); y+=520
    v=v.crop((0,0,v.width,y)); v.save(UIT+'/vel.png'); print('vel',v.size)
