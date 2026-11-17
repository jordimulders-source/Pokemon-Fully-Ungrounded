# r12: het LINKERoog = Jordi's omcirkeling (referenties/jordi_linkeroog_omcirkeld.png): de bruine lijnen aan de linker koprand.
# Model (115%-kopvervorming, hoge resolutie): buitenrand x2->x4; daarbinnen een smalle wig (verre oog in 3/4):
#   bovenlid x5 y19-21, onderlid schuin (5.6,20.5)->(6.5,23.5) = r10 (6,22),(6,23); opening licht op ~(5,22);
#   tussen buitenrand en bovenlid een tan strook (x4). Ooglijnen van r10 blijven; alleen binnenkant (13) en pupil (1) erbij,
#   opgebouwd als het rechteroog (geel + pupil links/onder), maar kleiner: 1 px geel + 1 px pupil.
# p1: geel in de modelopening (5,22), pupil links ervan (4,22) tegen de buitenrand
# p2: geel in de modelopening (5,22), pupil eronder (5,23) in de onderhoek van de wig
# p3: oog in de tan strook tussen buitenrand en bovenlid: geel (4,21), pupil (4,22)
import json, numpy as np; from PIL import Image
PAL=json.load(open('../r9/palet.json'))
P={'p1':{(5,22):13,(4,22):1},'p2':{(5,22):13,(5,23):1},'p3':{(4,21):13,(4,22):1}}
Y,X=np.mgrid[:64,:64]; ZONE=(X>=3)&(X<=6)&(Y>=18)&(Y<=24)
for basis in ('B','rond'):
    r10=np.asarray(Image.open('../r10/sprite_%s.png'%basis)).astype(int)
    for k,px in P.items():
        a=r10.copy()
        for (x,y),v in px.items(): a[y,x]=v
        im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%s_%s.png'%(basis,k),transparency=0)
        s=np.asarray(Image.open('sprite_%s_%s.png'%(basis,k))).astype(int); d=s!=r10
        print(basis,k,'gewijzigd (x,y,oud,nieuw)',sorted((int(x),int(y),int(r10[y,x]),int(s[y,x])) for y,x in zip(*np.where(d))),
              '| buiten zone x3-6 y18-24:',int((d&~ZONE).sum()),'| kleuren',len(np.unique(s)))
