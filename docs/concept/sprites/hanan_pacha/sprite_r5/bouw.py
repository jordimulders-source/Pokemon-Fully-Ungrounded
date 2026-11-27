# r5 = r4 A buiten de klauwzone + r3 in de klauwzone (X 31-40, Y 47-54), dan max 10 lijn-/tintwissels op bestaande r3-pixels.
import numpy as np; from PIL import Image, ImageDraw
PAL=[(152,208,160),(26,16,20),(124,76,18),(196,148,53),(229,184,79),(246,214,124),(206,188,180),(244,240,234),
 (128,28,42),(166,48,63),(208,99,104),(186,82,38),(222,118,50),(50,41,52),(204,192,148),(92,80,96)]
def opslaan(o,pad):
    im=Image.new('P',(64,64)); flat=[x for c in PAL for x in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.putdata([int(v) for v in o.ravel()]); im.save(pad,transparency=0)
r3=np.array(Image.open('../sprite_r3/sprite.png')).astype(int); r4=np.array(Image.open('../sprite_r4/sprite.png')).astype(int)
Z=np.zeros((64,64),bool); Z[47:55,31:41]=True
o=np.where(Z,r3,r4)
WISSEL=[  # (X,Y): nieuw, reden
 ((38,49),1,'omlijning klauw rechts (was staartgoud 3)'),
 ((38,50),1,'omlijning klauw rechts (was staartgoud 3)'),
 ((35,52),1,'omlijning onder teen (was staartgoud 4)'),
 ((36,52),1,'omlijning onder klauwpunt (was staartgoud 4)'),
 ((37,52),1,'omlijning onder teen (was staartgoud 4)'),
 ((33,49),5,'teen eigen lichte tint (was goud 4, gelijk aan staart)'),
 ((34,49),5,'teen eigen lichte tint (was goud 4)'),
 ((35,49),5,'teen eigen lichte tint (was goud 4)'),
 ((33,50),5,'teen eigen lichte tint (was goud 4)'),
 ((35,50),5,'teen eigen lichte tint (was goud 4)'),
]
regels=[]
for (X,Y),k,r in WISSEL:
    assert o[Y,X]>0, 'geen nieuwe pixels'
    regels.append('(%d,%d) %d -> %d: %s'%(X,Y,o[Y,X],k,r)); o[Y,X]=k
d=o!=r4; assert not (d&~Z).any()
assert ((o!=r3)&Z).sum()==len(WISSEL) and ((o>0)==(r3>0))[Z].all()
opslaan(o,'sprite.png'); np.save('sprite.npy',o)
open('wissels.txt','w').write('\n'.join(regels)+'\n')
print('\n'.join(regels)); print('klauwzone anders dan r3:',int(((o!=r3)&Z).sum()),'| buiten zone anders dan r4:',int((d&~Z).sum()),'| kleuren',len(set(o.ravel()))-1)
def rgb(o,bg=(240,240,236)):
    a=np.array(PAL,'uint8')[o]; a[o==0]=bg; return Image.fromarray(a)
vs=[('r5',o),('r3',r3),('r4 A',r4)]
V=Image.new('RGB',(3*522,18+512+10+18+256+10+150),'white'); dv=ImageDraw.Draw(V)
for i,(t,a) in enumerate(vs):
    V.paste(rgb(a).resize((512,512),Image.NEAREST),(i*522,18)); dv.text((i*522+2,2),t+' (8x)',fill=(0,0,0))
    V.paste(rgb(a).crop((26,42,46,58)).resize((320,256),Image.NEAREST),(i*522,558)); dv.text((i*522+2,542),t+' klauw (16x)',fill=(0,0,0))
x=4
for bg in ((240,240,236),(40,40,56)):
    for s in (1,2): V.paste(rgb(o,bg).resize((64*s,64*s),Image.NEAREST),(x,830)); x+=64*s+10
V.save('vel.png')
