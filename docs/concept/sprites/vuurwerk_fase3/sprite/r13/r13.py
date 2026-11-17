# r13: linkeroog afmaken, basis ../r12/sprite_<B|rond>_p2.png (geel (5,22), pupil (5,23) in de modelwig).
# Opbouw als het rechteroog: lijn erboven, gele binnenkant, pupil, lijn eronder; vorm/hoek = modelwig (bovenlid x5 y20-21,
# rechterlid (6,22)-(6,23), buitenrand x3).
# a: binnenkant 2 px geel ((4,22) erbij), boven dicht (4,21), onder dicht (4,23) en (5,24): complete amandel
# b: a + bovenlid schuiner/dikker naar rechtsonder: (6,21) bruin (zoals het bovenlid van het rechteroog naar binnen zakt)
# c: voorstel: a zonder (5,24); de pupil sluit zelf de onderkant (zoals bij het rechteroog de pupil op de onderlijn rust)
import json, numpy as np; from PIL import Image
PAL=json.load(open('../r9/palet.json'))
A={(4,22):13,(4,21):2,(4,23):2,(5,24):2}
P={'a':A,'b':{**A,(6,21):2},'c':{k:v for k,v in A.items() if k!=(5,24)}}
Y,X=np.mgrid[:64,:64]; ZONE=(X>=3)&(X<=6)&(Y>=18)&(Y<=24)
for basis in ('B','rond'):
    r12=np.asarray(Image.open('../r12/sprite_%s_p2.png'%basis)).astype(int)
    for k,px in P.items():
        a=r12.copy()
        for (x,y),v in px.items(): a[y,x]=v
        im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%s_%s.png'%(basis,k),transparency=0)
        s=np.asarray(Image.open('sprite_%s_%s.png'%(basis,k))).astype(int); d=s!=r12
        print(basis,k,'gewijzigd (x,y,oud,nieuw)',sorted((int(x),int(y),int(r12[y,x]),int(s[y,x])) for y,x in zip(*np.where(d))),
              '| buiten zone x3-6 y18-24:',int((d&~ZONE).sum()),'| kleuren',len(np.unique(s)))
