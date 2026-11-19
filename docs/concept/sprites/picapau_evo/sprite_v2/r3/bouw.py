# r3: r2 + reparaties 1-8 uit r2/KEURING.md (elk script benoemt zijn pixels) -> picaraio.png, normal.pal, picaraio_8x.png
# Werkt in png-coordinaten (geen hercentrering: positie gelijk aan r2).
import numpy as np; from PIL import Image
import vleugel, kuif, verre, buik, bliksem, nek, poot
PAL=[(152,208,160),(24,20,16),(226,150,96),(192,110,60),(142,74,42),(250,242,214),(230,210,166),(196,170,124),
     (232,82,74),(204,196,192),(142,132,130),(78,70,70),(252,226,96),(212,170,52),(255,255,255),(98,48,26)]
r2=np.array(Image.open('../r2/picaraio.png')).astype(int); o=r2.copy(); log={}
for naam,mod in [('1 vleugelpunten',vleugel),('2 kuif',kuif),('3 verre vleugel',verre),('4 buik',buik),('5+8 bliksem/koord',bliksem),('6 achterhoofd',nek),('7 rechterpoot',poot)]:
    n=mod.run(o)
    if naam=='3 verre vleugel': n[1,10]=1        # top van de verre vleugel: modelpunt (10,1) (3/9 bedekt), 1 px zwart
    log[naam]=int((n!=o).sum()); o=n
np.save('r3.npy',o)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('picaraio.png',transparency=0)
with open('normal.pal','w') as fh: fh.write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
rgb=np.array(PAL,'uint8')[o]; rgb[o==0]=(255,255,255); Image.fromarray(rgb).resize((512,512),0).save('picaraio_8x.png')
for k,v in log.items(): print('%-20s %3d px'%(k,v))
print('totaal r2->r3',int((o!=r2).sum()),'kleuren',len(set(o.ravel())))
