# v13: kleurronde kuif, staart en handen (vlamkleuring naar Gen 3: geel hart, oranje, oranjerood, rode rand).
# Alleen herkleuren op hun plek; buiten de zones diff 0 (gecontroleerd onderaan).
# Letters: A=10 donkerrood (vast, ook mond), B=11 rood, C=12 oranje, D=13 geel, F=15 oranjerood (nieuw), 1=zwart.
from PIL import Image; import numpy as np
from scipy import ndimage
D='docs/concept/sprites/hauntflare/'
im=Image.open(D+'sprite_v12/hauntflare_v12.png'); pal=im.getpalette(); a0=np.array(im); a=a0.copy()
pal[11*3:11*3+3]=[224,48,40]    # rood
pal[15*3:15*3+3]=[240,104,40]   # oranjerood (nieuw op de vrije plek)
pal[12*3:12*3+3]=[248,160,48]   # oranje
pal[13*3:13*3+3]=[255,224,96]   # geel
def zet(y,x0,s):
    for i,ch in enumerate(s):
        a[y,x0+i]=0 if ch=='.' else int(ch,16)
# ---- kuif (x30..57)
K={9:"............BA..............",
10:"...........BFA..........BBBA",
11:".........BBFA.........BBFBA.",
12:"......BBBCFA.........BCFBA..",
13:"....BBDDCCFA........BCCFA...",
14:"...BDDDCCFA...BBBBBBCCFBA...",
15:"..BDDDDDCFA.BBDDDDCCFFBA....",
16:"55556DDDCCAADDDDCCFFFFBA....",
17:"88666661AAADDDDDDCCCFFBA....",
18:"866677771DDDDDDCCFFFBBBA....",
19:"6666677771DDDCCCCCFFFBBA....",
20:"77777666671DDCCCFFFFBBA.....",
21:"777777766771DCCFFBBBBA......",
22:"8766677666771CCCFFBBA.......",
23:"87666622266771CFFBAA........",
24:"888622E16667771FBB1111......",
25:"8722EEE16666771FBA133311....",
26:"22EEEEE17666771BA122234411.."}
for y,s in K.items(): zet(y,30,s)
# ---- staart
S1={41:"2211B1....",42:"1881FBB...",43:"881CCFFBB.",44:"81CCCFFFB.",45:"1DDCCCCFFA",46:"DDDDCCFFBA"}
for y,s in S1.items(): zet(y,40,s)
S2={47:"711DDDDDDDCCFBA........",
48:"BDDDDCCCCCCFFFBBBB.....",
49:".BDDDCCCFFFFFFFFBBBA...",
50:"..ACCCFFFFFFFFFFFBBBA..",
51:"...ACCFFFFBBBBBBFFBBA..",
52:"....AAFFBBAAAAAABBFBBA.",
53:"......AAAA......AABBBBA",
54:"..................AABBA",
55:"....................ABA",
56:".....................BA",
57:".....................AA"}
for y,s in S2.items(): zet(y,35,s)
# ---- linkerhand (x8..28)
H={48:"..........BB....11177",
49:"........BBCCBA.....11",
50:"......BBCDDCFFAA.....",
51:".....BCDDCCFFFBBA....",
52:"...BBCACCFFAFFBBBA...",
53:"..BCF1CFFBACFFBBBB1..",
54:"..BCFACFB1ACFBBBBBB1.",
55:"..BCACFBA1CFBB11FBB1.",
56:".BDCACF11CFBB1..1FB1.",
57:".BD1CF1.BCFB1....1C1.",
58:".BD1DC1.BDD1.....111.",
59:".111D1...1D1.........",
60:"...1D1....11........."}
for y,s in H.items(): zet(y,8,s)
# ---- rechterhand (x51..62)
R={37:"11...BBBA...",38:"..BBBCCF1BB.",39:".BCDDCCFF1CA",40:".BCCDCFCCC1A",
41:"BCFC11D11D1A",42:"BCF1..1.11C1",43:"BC1.....1111",44:"BC1.........",45:".BD1........"}
for y,s in R.items(): zet(y,51,s)
# ---- controle: alleen pixels in de vlam/hand-componenten of zwarte randpixels die geen bol/ring raken
m=np.isin(a0,[10,11,12,13]); lab,n=ndimage.label(m,structure=np.ones((3,3)))
zone=np.isin(lab,[i for i in range(1,n+1) if (lab==i).sum()>40])
ch=np.argwhere(a!=a0); bad=[]
for y,x in ch:
    if zone[y,x]: continue
    if a0[y,x]==1:
        nb=[a0[yy,xx] for yy,xx in((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if 0<=yy<64 and 0<=xx<64]
        if not any(v in(2,3,4,5,6,7,8,9,14) for v in nb): continue
    bad.append((x,y,a0[y,x],a[y,x]))
print('gewijzigd',len(ch),'buiten zone',bad)
assert not bad and (a==0).sum()==(a0==0).sum() and ((a==0)==(a0==0)).all()
assert not np.isin(a[~zone & (a!=a0)],[0]).any()
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save(D+'sprite_v13/hauntflare_v13.png',transparency=0)
r=Image.open(D+'sprite_v13/hauntflare_v13.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r)
bg.convert('RGB').resize((512,512),Image.NEAREST).save(D+'sprite_v13/hauntflare_v13_8x.png')
