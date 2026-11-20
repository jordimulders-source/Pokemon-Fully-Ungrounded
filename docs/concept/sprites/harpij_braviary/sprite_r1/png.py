# png.py raster.txt uit.png : letters -> 64x64 geindexeerde png (index 0 transparant) + _8x
import sys, numpy as np; from PIL import Image
PAL=[('.',(152,208,160)),
 ('K',(16,18,26)),      # 1 lijn
 ('a',(54,62,78)),      # 2 leisteen donker
 ('b',(86,98,118)),     # 3 leisteen midden
 ('c',(128,142,164)),   # 4 leisteen licht
 ('g',(136,134,156)),   # 5 kopgrijs schaduw / selout
 ('h',(184,182,200)),   # 6 kopgrijs midden
 ('i',(224,224,236)),   # 7 kopgrijs licht / buik schaduw
 ('W',(250,250,252)),   # 8 wit
 ('n',(32,34,46)),      # 9 halsband
 ('s',(54,72,94)),     # 10 staal donker
 ('t',(122,146,168)),   # 11 staal midden
 ('u',(192,214,230)),   # 12 staal licht
 ('e',(200,144,48)),    # 13 oog amber
 ('d',(128,84,28)),     # 14 oog donker amber
]
L={c:i for i,(c,_) in enumerate(PAL)}
rows=[r.rstrip('\n') for r in open(sys.argv[1]) if r.strip('\n')]
H=len(rows); W=max(len(r) for r in rows)
a=np.zeros((64,64),'uint8')
oy=int(sys.argv[3]) if len(sys.argv)>3 else 63-(H-1); ox=int(sys.argv[4]) if len(sys.argv)>4 else (64-W)//2
for y,r in enumerate(rows):
    for x,c in enumerate(r): a[oy+y,ox+x]=L[c]
im=Image.fromarray(a,'P'); im.putpalette([v for _,c in PAL for v in c]+[0]*(768-3*len(PAL)))
im.save(sys.argv[2],transparency=0)
im2=Image.open(sys.argv[2]).convert('RGBA'); bg=Image.new('RGBA',im2.size,(232,232,232,255)); bg.alpha_composite(im2)
bg.convert('RGB').resize((512,512),Image.NEAREST).save(sys.argv[2].replace('.png','_8x.png'))
print('kleuren',len(set(a.ravel()))-1, 'bbox', np.argwhere(a>0).min(0), np.argwhere(a>0).max(0))
