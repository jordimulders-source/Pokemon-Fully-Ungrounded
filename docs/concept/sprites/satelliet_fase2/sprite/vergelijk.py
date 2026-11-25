# r5: naast elkaar op 8x en 1x (wit en donker): r4 (panelen 100 %) en de r5-versies
import sys; from PIL import Image, ImageDraw
P=sys.argv[2:]; UIT=sys.argv[1]
def on(im,bg):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
ims=[Image.open(p).convert('RGBA') for p in P]
out=Image.new('RGB',(len(P)*532,512+30+150),(205,205,205)); d=ImageDraw.Draw(out)
for n,(p,im) in enumerate(zip(P,ims)):
    out.paste(on(im,(255,255,255)).resize((512,512),Image.NEAREST),(n*532,0)); d.text((n*532+4,516),p,fill=(0,0,0))
for n,im in enumerate(ims):
    out.paste(on(im,(255,255,255)),(20+n*80,560)); out.paste(on(im,(40,40,48)),(20+n*80,630))
for n,im in enumerate(ims):
    out.paste(on(im,(255,255,255)).resize((128,128),Image.NEAREST),(len(P)*80+60+n*140,550))
d.text((20,545),'1x (wit / donker) en 2x, zelfde volgorde',fill=(0,0,0))
out.save(UIT); print(UIT)
