# Eindkeuring r7 Gnomad: meet zwart, simuleer reparaties, maak vergelijkingen.
import os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(os.path.join(D,'../../../../..'))
src=Image.open(os.path.join(D,'../sprite_r7/gnomad_A.png'))
m,p=2,6  # m=(112,95,138) donkerste mutstint, p=(172,72,102) donkerste roze
REP=[ # (nr, kleur, pixels)
 (1,m,[(13,27),(14,27),(15,27),(16,26),(17,25),(18,25),(19,25),(20,25),(21,26),(22,26),(22,27),(23,27)]), # mutsrand boven neus
 (2,m,[(24,28),(25,28),(26,28)]+[(x,29) for x in range(26,36)]), # mutsrand rechts van neus
 (3,m,[(36,28),(37,28),(38,27),(39,27),(40,28)]), # mutsrand boven rechter snorpluk
 (4,m,[(39,22),(39,23),(40,23),(39,24)]), # mutsvouw
 (5,p,[(x,39) for x in range(22,31)]), # onderlijn rechter snorhelft -> slagschaduw
 (6,p,[(14,39),(15,39)]), # dubbele lijn onder linker snorhelft
 (7,p,[(33,30),(33,31),(34,32),(34,33)]), # grens gezicht / rechter snorhelft
]
def zw(im):
  px=im.load(); f=sum(1 for x in range(64) for y in range(64) if px[x,y]); k=sum(1 for x in range(64) for y in range(64) if px[x,y]==1)
  return k,f,100*k/f
im=src.copy(); px=im.load(); print('r7: zwart %d/%d = %.1f%%'%zw(src))
for nr,c,pp in REP:
  for xy in pp:
    assert px[xy]==1,(nr,xy,px[xy]); px[xy]=c
  print('na reparatie %d: %.1f%%'%(nr,zw(im)[2]))
im.save(os.path.join(D,'voorstel.png'))
def big(i,s): return i.convert('RGB').resize((64*s,64*s),Image.NEAREST)
big(im,8).save(os.path.join(D,'voorstel_8x.png'))
# r7 | voorstel 6x, met gewijzigde pixels gemarkeerd
w=Image.new('RGB',(64*6*3+20,64*6),(255,255,255))
w.paste(big(src,6),(0,0)); w.paste(big(im,6),(64*6+10,0))
mk=big(im,6); mp=mk.load(); sp=src.load()
for y in range(64):
  for x in range(64):
    if sp[x,y]!=px[x,y]:
      for i in range(6):
        for j in range(6):
          if i in(0,5) or j in(0,5): mp[x*6+i,y*6+j]=(0,255,0)
w.paste(mk,(64*12+20,0)); w.save(os.path.join(D,'r7_voorstel_markering_6x.png'))
# 1x en 2x naast Gen 3-middenfases
refs=['machoke','jigglypuff','loudred','vigoroth','sudowoodo']
tiles=[src,im,Image.open(os.path.join(D,'../../gnomini/af/gnomini.png'))]
for r in refs:
  a=Image.open(os.path.join(R,'graphics/pokemon',r,'anim_front.png')); tiles.append(a.crop((0,0,64,64)))
for s,n in((1,'vergelijk_1x.png'),(2,'vergelijk_2x.png')):
  c=Image.new('RGB',(len(tiles)*66*s,66*s),(255,255,255))
  for i,t in enumerate(tiles):
    t=t.convert('RGBA'); bgc=t.getpixel((0,0))
    d=[(0,0,0,0) if q==bgc else q for q in t.getdata()]; t.putdata(d)
    c.paste(t.resize((64*s,64*s),Image.NEAREST),(i*66*s+s,s),t.resize((64*s,64*s),Image.NEAREST))
  c.save(os.path.join(D,n))
for r in refs:
  a=Image.open(os.path.join(R,'graphics/pokemon',r,'anim_front.png')).convert('RGB').crop((0,0,64,64)); q=a.load(); bgc=q[0,0]
  pix=[q[x,y] for x in range(64) for y in range(64) if q[x,y]!=bgc]; dk=min(set(pix),key=sum)
  print('%s: zwart %.1f%%'%(r,100*pix.count(dk)/len(pix)))
