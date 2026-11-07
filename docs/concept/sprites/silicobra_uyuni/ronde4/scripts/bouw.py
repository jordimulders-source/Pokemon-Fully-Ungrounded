# Ronde 2: bouwt silicobra_uyuni.png uit het handbewerkte tekstraster silicobra_uyuni_raster.txt
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/ronde4/'
rows=[l.rstrip('\n') for l in open(D+'silicobra_uyuni_raster.txt')][:64]
P=[('.',(152,208,160)),('O',(54,44,42)),('K',(100,86,76)),('h',(124,108,90)),('e',(146,128,104)),('d',(176,160,136)),('c',(204,192,170)),('b',(228,220,202)),('a',(248,244,232)),
   ('f',(220,204,170)),('g',(186,164,126)),('q',(184,244,228)),('r',(96,204,192)),('s',(44,148,152)),('t',(24,92,104))]
idx={c:i for i,(c,_) in enumerate(P)}
out=Image.new('P',(64,64)); pal=[]
for _,rgb in P: pal+=rgb
out.putpalette(pal+[0]*(768-len(pal)))
out.putdata([idx[rows[y][x]] for y in range(64) for x in range(64)])
out.save(D+'silicobra_uyuni.png',transparency=0)
