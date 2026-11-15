# vel.png: v3 | v2 | model 8x; v3 1x/2x op licht en donker; close-ups 12x per keuringspunt (v3 | v2 | model).
# Bij de gezichtspunten staat het model VERSCHOVEN (+5 kol, +1 rij), zodat het op dezelfde plek staat als het gezicht.
from PIL import Image, ImageDraw
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
def rgba(p): return Image.open(p).convert('RGBA')
V3=rgba(D+'gengas_v3.png'); V2=rgba(D+'../sprite_v2/gengas_v2.png'); M=rgba(D+'../model/model_64_geschrapt.png')
NAT=rgba(D+'../model/gekozen_v3_natief.png')
MS='verschoven'  # model-uitsnede op de oude gezichtsplek (box -1 rij, -5 kol): zelfde inhoud naast elkaar
LICHT=(255,255,255,255); DONKER=(40,40,48,255)
def op(im,kleur,s):
    b=Image.new('RGBA',im.size,kleur); b.alpha_composite(im); return b.resize((im.width*s,im.height*s),Image.NEAREST)
def crop(im,box,s=12):
    y0,y1,x0,x1=box; return op(im,LICHT,1).crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
W=64*8*3+64; V=Image.new('RGB',(W,6000),(235,235,235)); d=ImageDraw.Draw(V); y=8
for i,t in enumerate(('v3 (gengas_v3.png) 8x','v2 8x','model_64_geschrapt 8x')): d.text((16+i*(512+16),y),t,fill=(0,0,0))
y+=14
for i,im in enumerate((V3,V2,M)): V.paste(op(im,LICHT,8),(16+i*(512+16),y))
y+=512+12; x=16
for kleur in (LICHT,DONKER):
    for s in (1,2): V.paste(op(V3,kleur,s),(x,y)); x+=64*s+16
d.text((x+8,y+8),'v3 1x en 2x op licht en donker',fill=(0,0,0)); y+=128+18
punten=[('MOET 1 gat tussen rookarm en rechtermaan (rij 22, kol 51-52)',(17,28,44,60),M),
        ('MOET 2 bandgrens rechtsonder de grijns',(39,50,20,38),M),
        ('MOET 3 naad links van het gezicht (maskerrand schuin, lichte strook l->m->r)',(25,49,6,22),MS),
        ('MOET 4 krul (model: geschrapt; natief ernaast)',(29,42,32,48),M),
        ('MOET 5 lichte wig in het masker + MAG streep boven de ogen',(24,38,6,32),MS),
        ('MAG maan boven',(0,11,23,39),M),('MAG maan links',(39,53,0,12),M),
        ('MAG maan rechts',(18,33,50,64),M),('MAG maan rechtsonder',(47,64,37,58),M)]
for naam,box,ref in punten:
    rb=(box[0]-1,box[1]-1,box[2]-5,box[3]-5) if ref is MS else box
    pad=Image.new('RGBA',(74,74),(255,255,255,255)); pad.paste(M,(5,1))
    imgs=[crop(V3,box),crop(V2,box),(op(pad,LICHT,1).crop((rb[2]+5,rb[0]+1,rb[3]+5,rb[1]+1)).resize(((box[3]-box[2])*12,(box[1]-box[0])*12),Image.NEAREST) if ref is MS else crop(ref,box))]
    if naam.startswith('MOET 4'): imgs.append(op(NAT,LICHT,1).crop((41,35,55,49)).resize((14*12,14*12),Image.NEAREST))
    tot=sum(i.width for i in imgs)+12*len(imgs)
    d.text((16,y),naam+'   [v3 | v2 | model'+(' (oude plek, uitsnede -1 rij/-5 kol: zelfde inhoud)' if ref is MS else '')+(' | natief' if len(imgs)==4 else '')+']',fill=(0,0,0)); y+=14
    x=16
    for im in imgs: V.paste(im,(x,y)); x+=im.width+12
    y+=max(i.height for i in imgs)+16
V.crop((0,0,W,y)).save(D+'vel.png'); print('vel.png',W,y)
