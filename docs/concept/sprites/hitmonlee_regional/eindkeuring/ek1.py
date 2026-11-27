# ek1 = kandidaat (= r13, figuur op x+2) + eindkeuring: alleen tintwissels op bestaande pixels, waarde uit modelmeting
# (M_gem / M_zonderlijn uit sprite/meet.py). Silhouet ongewijzigd. Gebruik: python3 ek1.py (vanuit de repo-root)
from PIL import Image; import numpy as np
D='docs/concept/sprites/hitmonlee_regional/'
im=Image.open(D+'sprite/kandidaat.png'); L=np.array(im).copy(); OX=2
W=[ # (x,y in r13-coord., van, naar, reden)
 (41,1,1,2,'B buitenlijn trapvoet bovenkant: zwart tussen donkerrood (om-en-om) -> selout; M_gem 2'),
 (44,2,1,6,'B dubbele zwarte hoek trapvoet rechtsboven -> vulling; M_zonderlijn/M_2e 6'),
 (45,10,1,5,'B buitenlijn trapbeen 2 px dik (naast (46,10)) -> vulling; M_zonderlijn/M_2e 5'),
 (18,39,1,3,'B binnenlijn romp/schouder zwart -> eigen donkere tint; M_gem 3'),
 (18,40,1,2,'B binnenlijn romp/schouder zwart -> donkerrood; M_gem 2'),
 (17,41,1,2,'B binnenlijn romp/schouder zwart -> donkerrood; M_gem 2 (loopt taps uit in de zwarte onderlijn)'),
 (8,53,1,2,'B binnenlijn hand (duim) zwart -> donkerrood; M_gem 2'),
 (5,54,1,2,'B binnenlijn hand (vinger) zwart -> donkerrood; M_gem 2'),
 (5,55,1,2,'B binnenlijn hand (vinger) zwart -> donkerrood; M_gem 2'),
 (4,55,1,2,'B binnenlijn hand (vinger) zwart -> donkerrood; M_gem D, 2 gekozen voor een doorlopende lijn'),
 (51,42,1,13,'K losse zwarte spikkel in doorschijnende knie -> bruinmauve; M_gem D'),
 (53,42,1,13,'B dubbele zwarte rand knie (naast (54,42)) -> bruinmauve; M_gem D'),
 (36,29,12,15,'K doorschijnend kickbeen in de romp: modeltint terug (r11-toonkaart had het overschreven); M_gem/M_zonderlijn F'),
 (35,30,7,15,'K idem; M F'),
 (39,31,11,14,'K idem; M E'),
 (36,32,12,14,'K idem; M E'),
 (39,32,12,14,'K idem; M E'),
 (40,32,7,15,'K idem; M F'),
 (35,33,7,14,'K idem; M E'),
 (36,33,12,14,'K idem; M E'),
 (37,33,12,14,'K idem; M E'),
 (39,33,7,14,'K idem; M E'),
 (37,34,7,14,'K idem (ronde onderkant van het been); M E'),
]
log=open(D+'eindkeuring/ek1_log.txt','w')
for x,y,a,b,r in W:
    assert L[y,x+OX]==a,(x,y,L[y,x+OX])
    L[y,x+OX]=b; log.write(f'({x},{y}) [64x64: ({x+OX},{y})] {a}->{b} {r}\n')
out=Image.fromarray(L.astype(np.uint8),'P'); out.putpalette(im.getpalette()); 
if 'transparency' in im.info: out.info['transparency']=im.info['transparency']
out.save(D+'eindkeuring/ek1.png',transparency=0)
print(len(W),'pixels')
