from PIL import Image
src='sprite_r7/A0.png'
im=Image.open(src); a=im.copy()
P=im.getpalette()
P[2*3:2*3+3]=[38,38,52]; P[3*3:3*3+3]=[64,64,82]; P[4*3:4*3+3]=[98,96,114]
im.putpalette(P)
E=[]  # (x,y,expected_old,new,zone)
def s(zone,new,y,xs,old=None):
    for x in xs: E.append((x,y,old,new,zone))
K='kop';O='oor';L='lijf'
# kop: licht linksboven, schaduw rechtsonder (achter het nabije oor en naar het lijf)
s(K,3,51,[14,15],4); s(K,3,51,[17,18],4); s(K,2,51,[19,20],4)
s(K,3,52,range(13,19),4); s(K,2,52,[19,20,21],4)
s(K,3,53,range(11,16),4); s(K,3,53,[19,20],4); s(K,2,53,[21,22],4)
s(K,3,54,[21],4); s(K,2,54,[22],4); s(K,3,55,[21],4); s(K,3,56,[21],4)
# oor links: lichtrand x7 (4), x8 midden (3), rest schaduw (2); aansluiting op de kop
for y in range(45,48): s(O,3,y,[8],2)
s(O,3,48,[7,8],2); s(O,3,49,[8],2); s(O,3,50,[9,10],2)
# lijf/schouder: 4 linksboven, 3 als overgang, 2 rechtsonder
s(L,3,39,[29],4); s(L,3,40,[28],4); s(L,3,41,[27,28],4); s(L,3,42,[26,27],4)
s(L,3,43,[26],4); s(L,3,44,[23,25],4)
s(L,3,45,range(23,29),2); s(L,3,46,range(25,29),2); s(L,3,47,[27],2)
from collections import Counter
cnt=Counter()
for x,y,old,new,z in E:
    cur=a.getpixel((x,y))
    assert old is None or cur==old,(x,y,cur,old)
    if cur!=new: im.putpixel((x,y),new); cnt[z]+=1
mask=lambda i:[i.getpixel((x,y))==0 for y in range(64) for x in range(64)]
assert mask(a)==mask(im)
# omlijning (index 1) ongewijzigd
assert [a.getpixel((x,y))==1 for y in range(64) for x in range(64)]==[im.getpixel((x,y))==1 for y in range(64) for x in range(64)]
im.save('sprite_r8/A0.png',transparency=0)
print(cnt, sum(cnt.values()))
print('transparantiemasker identiek, omlijning (1) identiek')
im.convert('RGBA').resize((512,512),0).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/df5125ac-9381-5d71-af17-ce82baab011f/scratchpad/r8_8x.png')
