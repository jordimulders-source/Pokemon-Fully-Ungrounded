# r14: linkeroog = de VORM van het rechteroog, verkleind tot de maat van r12 p2 (geen uitrekken). Basis ../r12/sprite_B_p2.png.
# Rechteroog (x12-14 y19-23): schuin bovenlid dat naar binnen/links zakt, gele binnenkant, pupil links-onder het geel, onderlijn.
# Blok x4-6, y20-23 (x3 = buitenrand en y24 blijven); tekens: t=tan(3) .=creme(4) b=bruin(2) y=geel(13) p=pupil(1)
#   r12 p2 = "tb." "tb." ".yb" ".pb"  (oogkern op x5-6: 2 breed, 4 hoog; nooit breder/hoger dan dat)
import json, numpy as np; from PIL import Image
PAL=json.load(open('../r9/palet.json')); C={'t':3,'.':4,'b':2,'y':13,'p':1}
V={1:("t.b","tby",".pb",".bb","niet gespiegeld: bovenlid zakt naar links, geel rechts, pupil links-onder (als rechteroog)"),
   2:("tb.","tyb",".bp",".bb","gespiegeld: bovenlid zakt naar rechts, geel links, pupil rechts-onder"),
   3:("t.b","tb.",".yb",".pb","p2-kern (geel boven, pupil onder) + bovenlid als 2 px schuine streep naar links zakkend"),
   4:("tb.","tbb",".yb",".pb","p2-kern + bovenlid naar rechts/binnen zakkend (1 bovenlidpixel extra)"),
   5:("tb.","tb.","pyb",".bb","pupil links van het geel (als rechteroog), onderlijn eronder"),
   6:("tb.","tbb",".yp",".bb","pupil rechts van het geel, bovenlid schuin, onderlijn eronder")}
p2=np.asarray(Image.open('../r12/sprite_B_p2.png')).astype(int)
Y,X=np.mgrid[:64,:64]; ZONE=(X>=4)&(X<=6)&(Y>=20)&(Y<=23)
for n,(*rows,uitleg) in V.items():
    a=p2.copy()
    for j,r in enumerate(rows):
        for i,ch in enumerate(r): a[20+j,4+i]=C[ch]
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%d.png'%n,transparency=0)
    s=np.asarray(Image.open('sprite_%d.png'%n)).astype(int); d=s!=p2
    print(n,uitleg,'| gewijzigd t.o.v. p2 (x,y,oud,nieuw):',sorted((int(x),int(y),int(p2[y,x]),int(s[y,x])) for y,x in zip(*np.where(d))),
          '| buiten blok:',int((d&~ZONE).sum()),'| kleuren',len(np.unique(s)))
