# r9: basis r5 115% geel + vlamtong (../r8/vlam8.py) + alleen het RECHTER (nabije) oog van r8-probeersel a of b.
# Het linker/verre oog van r8 vervalt helemaal: die pixels zijn exact r5. Bewijs: diff t.o.v. r5 = pupil (+ rand bij b) + vlamtong.
import sys, json, numpy as np; from PIL import Image
sys.path.insert(0,'../r8'); from vlam8 import vlam, WEG
PAL=json.load(open('palet.json'))
r5=np.asarray(Image.open('../r5/sprite_115_geel.png')).astype(int)
RECHTS={'a':{(12,22):1},                                   # pupil op de donkerste modelplek in het oog
        'b':{(12,22):1,(13,23):2,(14,22):2}}               # + rand rechtsonder dicht (niet uit het model)
for k,px in RECHTS.items():
    a=vlam(r5)
    for (x,y),v in px.items(): a[y,x]=v
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%s.png'%k,transparency=0)
    s=np.asarray(Image.open('sprite_%s.png'%k)).astype(int); d=sorted((int(x),int(y)) for y,x in zip(*np.where(s!=r5)))
    verwacht=sorted(set(px)|set(WEG))
    print(k,'diff t.o.v. r5 115%:',d,'| precies oog + vlamtong:',d==verwacht,'| kleuren',len(np.unique(s)))
