# r11: 3 probeersels van het VERRE oog (links van het nabije), basis r10 (B en rond). Alleen de zone x3-10 y18-24 verschilt.
# Model (115%-kopvervorming, ../r10/modelmeet.py, donkerste 20% per spritepixel):
#   wenkbrauw/bovenlid = schuine okerlijn van (11,18) naar (9,20): (10,19) en (9,20) donker oker (~154,124,87 -> index 14)
#   oog = verticale spleet x9 y21-22: (9,21) rood (~168,89,67), (9,22) donkerrood (~155,48,34 -> index 10)
# p1: wenkbrauw bruin (2) + lichte binnenkant geel (13) op de plek van de spleet
# p2: wenkbrauw bruin (2) + geel (9,21) + pupil bijna-zwart (1) op (9,22) (donkerste modelplek)
# p3: model letterlijk: wenkbrauw oker (14) + spleet rood (11) / donkerrood (10)
import json, numpy as np; from PIL import Image
PAL=json.load(open('../r9/palet.json'))
P={'p1':{(10,19):2,(9,20):2,(9,21):13,(9,22):13},
   'p2':{(10,19):2,(9,20):2,(9,21):13,(9,22):1},
   'p3':{(10,19):14,(9,20):14,(9,21):11,(9,22):10}}
Y,X=np.mgrid[:64,:64]; ZONE=(X>=3)&(X<=10)&(Y>=18)&(Y<=24)
for basis in ('B','rond'):
    r10=np.asarray(Image.open('../r10/sprite_%s.png'%basis)).astype(int)
    for k,px in P.items():
        a=r10.copy()
        for (x,y),v in px.items(): a[y,x]=v
        im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%s_%s.png'%(basis,k),transparency=0)
        s=np.asarray(Image.open('sprite_%s_%s.png'%(basis,k))).astype(int); d=s!=r10
        print(basis,k,'gewijzigd',sorted((int(x),int(y),int(r10[y,x]),int(s[y,x])) for y,x in zip(*np.where(d))),
              '| buiten zone:',int((d&~ZONE).sum()),'| kleuren',len(np.unique(s)))
