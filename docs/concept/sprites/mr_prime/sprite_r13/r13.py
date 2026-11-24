# r13: Dragonfly Cave-eindkeuring op r12 O3 (Jordi koos O3). Jordi: "teken niks opnieuw": alleen omkleuren van bestaande
# pixels binnen het silhouet; alpha-diff met O3 moet 0 zijn (wordt hieronder gecontroleerd). Tinten: 0=16 1=40 2=66 3=100
# 4=128 5=164 6=200 7=224 8=wit. R(y,x0,'...') zet een rij vanaf x0; '.' = pixel ongemoeid.
import numpy as np; from PIL import Image, ImageDraw
O3=np.asarray(Image.open('oog_O3.png')).astype(int); PAL=Image.open('oog_O3.png').getpalette()
T2I={0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:9,8:8}
C=O3.copy(); PUNT={}; cur=[None]
def punt(n): cur[0]=n; PUNT.setdefault(n,set())
def S(x,y,t):
    assert O3[y,x]!=0, ('transparant',x,y)
    if C[y,x]!=T2I[t]: C[y,x]=T2I[t]; PUNT[cur[0]].add((x,y))
def R(y,x0,s):
    for i,ch in enumerate(s):
        if ch!='.': S(x0+i,y,int(ch))

punt('1 snorkrulgaten')      # wit -> 5, zodat ze niet als tweede ogen lezen; (41,20) tint 1 -> wit
S(26,22,5); S(41,22,5); S(41,20,8)

punt('2 linker kopomtrek')   # 4 -> 2, verre oog los van de rand (wit x28 ertussen)
S(28,16,2); S(27,17,2); S(27,18,2); S(27,19,2)

punt('3 kraag/schouder')     # één lijn waar de arm over het lijf valt: (26,31)0 (27,30)0 (28,29)1; schouder 3, rest 2/3
R(28,28,'33...2')            # x28-29 schouder licht, (34,28) -> 2
R(29,28,'1332222')           # x28 lijn (taps 1), x29-31 schouder, x32-35 schaduw onder kraag/strik
R(30,27,'0332')              # x27 lijn, x28-29 schouder, (30,30) 3 -> blijft 2-rand bij het hemd; (31,30) -> 2
S(30,30,3); S(31,30,2)

punt('4 mouw')
S(24,31,2); S(25,31,2); S(22,32,0); S(23,32,0)

punt('5 hoedband')           # rechte zwarte binnenlijn: x32-38 -> 1, zwart alleen rechts
R(8,32,'2111111')            # x32 = 2 (taps aan de lichte kant)

punt('6 hoedrand')           # licht aan de linkerpunt/voorkant, diagonale tintgrenzen naar donker rechtsonder
R(9,32,'44443333322222')            # x32-45
R(10,29,'4443333322222211111100')    # x29-50; x49-50 kernschaduw in de hoek tegen de omlijning
S(50,11,0)
R(11,27,'4443333322222211111100')     # x27-48; x47-48 kernschaduw (sikkel rechtsonder)
R(12,26,'333221')                   # x26-31 onderkant voorpunt
S(44,12,0); S(45,12,0)              # lichte pixels in de onderlijn -> lijn

punt('7 rechterarm')         # licht bovenop (bovenarm/elleboog), schaduw als sikkel rechtsonder, geen kolommen
R(31,50,'443')
R(32,49,'33332')
R(33,52,'332')
R(34,52,'3322')
R(35,53,'221')
R(36,52,'221')
R(37,53,'11')
R(38,53,'1')

punt('8 linker jaspand')     # tint 4 als ovaal bovenaan, onderkant naar 3 en 2
R(31,27,'343')
R(32,26,'3443')
R(33,26,'4444')
R(34,26,'4443')
R(35,25,'34433')
R(36,25,'33433')
R(37,25,'33333')
R(38,25,'33333')
R(39,25,'3332')
R(40,25,'3322')
R(41,25,'3222')

punt('9 buikband')           # band volgt de buik: uiteinden hoger, midden lager; zwarte lijn -> 1 / slagschaduw 6
R(46,35,'8811117')           # x35-36 band, x37-40 onderrand buik (1), x41 7
S(42,46,7); S(43,46,7)
S(40,47,7); S(41,47,7)
R(48,35,'6666')              # band zakt in het midden een rij (schaduwkant onder)

punt('10 benen')
# voorbeen (dij): grenzen schuin langs het been, hooglicht taps naar de heup
R(46,24,'444332')
R(47,23,'44433322')
R(48,23,'3443322222')
R(49,23,'3322211111')
# rij 50 zwarte run breken met 1 (lijn boven de jaspand ertussen)
R(50,37,'1111')
# achterbeen: grenzen schuin langs het been (licht bovenop, taps naar de voet)
R(49,44,'23333332223')     # hooglicht als wig bij de heup, taps; bovenrand bij de voet (54,49)(55,50)(56,51) licht
R(50,45,'22333222233')
R(51,45,'111222222333')
R(52,46,'11111112222')

punt('11 haarvleugel rechts')
R(4,56,'2222')                # x53-55 blijft 1 (aanzet), x56-59 -> 2

punt('12 buik')              # bolling-licht als ovaal, aflopend
R(35,35,'44444')
R(36,34,'444444')
R(37,34,'44433')
R(38,35,'443')

# MAG (14,29) -> 7 geprobeerd: wist het hooglicht van de stok en leest als losse witte pixel; niet gedaan.

# controle: silhouet gelijk
a0=O3!=0; a1=C!=0
assert (a0!=a1).sum()==0
print('alpha-diff met O3:',int((a0!=a1).sum()))
for k,v in PUNT.items(): print('%-24s %3d px'%(k,len(v)))
print('totaal gewijzigd:',int((C!=O3).sum()))
def png(A,p):
    im=Image.fromarray(A.astype('uint8'),'P'); im.putpalette(PAL); im.save(p,transparency=0)
png(C,'mr_prime.png')
BG=(152,208,160); L,D=(232,236,240),(40,44,52)
def groot(p,z,box=None,bg=(224,224,224)):
    im=Image.open(p).convert('RGBA'); W=Image.new('RGBA',im.size,bg+(255,)); W.alpha_composite(im); im=W.convert('RGB')
    if box: im=im.crop(box)
    return im.resize((im.width*z,im.height*z),0)
groot('mr_prime.png',8).save('mr_prime_8x.png')
KOP=(22,0,64,28); LIJF=(18,24,60,58)
rows=[('r13 | O3 (8x)',[groot('mr_prime.png',8),groot('oog_O3.png',8)]),
      ('kop 12x: r13 | O3',[groot('mr_prime.png',12,KOP),groot('oog_O3.png',12,KOP)]),
      ('lijf 12x: r13 | O3',[groot('mr_prime.png',12,LIJF),groot('oog_O3.png',12,LIJF)]),
      ('r13 1x/2x licht/donker | O3',[groot('mr_prime.png',1,bg=L),groot('mr_prime.png',2,bg=L),groot('mr_prime.png',1,bg=D),
        groot('mr_prime.png',2,bg=D),groot('oog_O3.png',1,bg=L),groot('oog_O3.png',2,bg=L)])]
pad=12; Wd=max(sum(i.width+pad for i in r) for _,r in rows); Ht=sum(max(i.height for i in r)+26 for _,r in rows)
V=Image.new('RGB',(Wd,Ht),(255,255,255)); d=ImageDraw.Draw(V); y=0
for t,r in rows:
    d.text((4,y+7),t,fill=(0,0,0)); y+=26; x=0
    for i in r: V.paste(i,(x,y)); x+=i.width+pad
    y+=max(i.height for i in r)
V.save('vel.png')
