# kies.py: model-oog + varianten A/B/C: oog 12x, kop 8x, hele sprite 1x/2x (licht en donker).
from PIL import Image, ImageDraw
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
nat=Image.open(B+'sprite_r9/natief.png').convert('RGB')
def sp(f,bg):
    im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def mod(x0,y0,x1,y1,S): return nat.crop((2+3*x0,3*(y0-13),2+3*x1,3*(y1-13))).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
L=(232,234,238); D=(40,40,48)
F=[(B+'eind/pitahaya2_eind2.png','nu (eind2)')]+[(B+f'sprite_r13/pitahaya2_r13_oog{k}.png','oog '+k) for k in 'ABC']
e=(10,34,24,44); h=(2,30,28,56)
rows=[[mod(*e,12)]+[sp(f,L).crop(e).resize(((e[2]-e[0])*12,(e[3]-e[1])*12),Image.NEAREST) for f,_ in F],
      [mod(*h,8)]+[sp(f,L).crop(h).resize(((h[2]-h[0])*8,(h[3]-h[1])*8),Image.NEAREST) for f,_ in F]]
labels=[['model oog 12x']+[n+' 12x' for _,n in F],['model kop 8x']+[n+' kop 8x' for _,n in F]]
for bg,t in ((L,'licht'),(D,'donker')):
    r=[];l=[]
    for f,n in F: im=sp(f,bg); r+=[im,im.resize((128,128),Image.NEAREST)]; l+=[n+' 1x','2x '+t]
    rows.append(r); labels.append(l)
W=max(sum(i.width+12 for i in r) for r in rows); H=sum(max(i.height for i in r)+26 for r in rows)
V=Image.new('RGB',(W,H),(250,250,250)); d=ImageDraw.Draw(V); y=0
for r,l in zip(rows,labels):
    x=0
    for im,t in zip(r,l): d.text((x+2,y+2),t,fill=(0,0,0)); V.paste(im,(x,y+14)); x+=im.width+12
    y+=max(i.height for i in r)+26
V.save(B+'sprite_r13/kies.png'); print(V.size)
