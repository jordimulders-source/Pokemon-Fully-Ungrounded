import numpy as np
from PIL import Image,ImageDraw
nat=np.load('comp_nat.npy').astype('uint8')
m=Image.fromarray(nat[52:63,16:29]).resize((13*8+4,11*8+4),Image.NEAREST)
def S(f,bgc=(255,255,255,255)):
    sp=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',(64,64),bgc); bg.alpha_composite(sp); return bg.convert('RGB')
LP=[tuple(p) for p in np.load('r5_lijnpix.npy')]; LID=LP[-5:]
o=Image.new('RGB',(900,560),(235,235,235)); d=ImageDraw.Draw(o)
d.text((6,4),'model natief (x16-28,y52-62) | rood omrand = meegekleurd, blauw = pupil zwart, uitsnede x2-23 y37-44',fill=0); o.paste(m,(6,18))
x=200
for f,lbl in [('r5_A','A: lid grijs 10'),('r5_B','B: lid bruin 5'),('r5_A_lijn','A + hele lijn'),('r5_B_lijn','B + hele lijn')]:
    c=S(f+'.png').crop((2,37,24,45)).resize((22*12,8*12),Image.NEAREST)
    dd=ImageDraw.Draw(c)
    for px,py in (LP if 'lijn' in f else LID):
        dd.rectangle([(px-2)*12,(py-37)*12,(px-2)*12+11,(py-37)*12+11],outline=(255,0,0),width=1)
    dd.rectangle([(15-2)*12,(41-37)*12,(15-2)*12+11,(41-37)*12+11],outline=(0,120,255),width=2)
    i=['r5_A','r5_B','r5_A_lijn','r5_B_lijn'].index(f); X=6+(i%2)*(22*12+20); Y=130+(i//2)*120
    d.text((X,Y-14),lbl+' (12x)',fill=0); o.paste(c,(X,Y))
y=380
for i,f in enumerate(['r5_A','r5_B','r5_A_lijn','r5_B_lijn']):
    X=6+i*200; d.text((X,y),f+' 2x / 1x',fill=0)
    o.paste(S(f+'.png').resize((128,128),Image.NEAREST),(X,y+14)); o.paste(S(f+'.png'),(X+132,y+14)); o.paste(S(f+'.png',(40,44,52,255)),(X+132,y+80))
o.save('vel_r5.png')
