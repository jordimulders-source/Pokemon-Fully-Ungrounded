# vel.png: rij 1 bek 12x: model (natief, zelfde uitsnede) | r5 | r4; rij 2 hele sprite 8x: r5 | r4; rij 3: 1x en 2x op licht en donker (r5, r4)
from PIL import Image, ImageDraw
n=Image.open('natief.png').convert('RGB')
def sp(f,bg): im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
X0,X1,Y0,Y1=1,24,38,58
def bek(f): return sp(f,(255,255,255)).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*12,(Y1-Y0)*12),Image.NEAREST)
m=n.crop((2+3*X0,3*(Y0-13),2+3*X1,3*(Y1-13))).resize(((X1-X0)*12,(Y1-Y0)*12),Image.NEAREST)
rows=[[m,bek('pitahaya2_r6.png'),bek('pitahaya2_r6B.png'),bek('pitahaya2_r5.png')],
      [sp(f,(255,255,255)).resize((512,512),Image.NEAREST) for f in ('pitahaya2_r6.png','pitahaya2_r5.png')]]
kl=[]
for bg in ((255,255,255),(40,40,48)):
    for f in ('pitahaya2_r6.png','pitahaya2_r5.png'):
        im=sp(f,bg); kl+= [im, im.resize((128,128),Image.NEAREST)]
rows.append(kl)
labels=[['model (natief)','r6','r6B (twijfelpixels ook grijs)','r5'],['r6 8x','r5 8x'],['r6 1x','r6 2x','r5 1x','r5 2x','r6 1x donker','r6 2x','r5 1x donker','r5 2x']]
W=max(sum(i.width+12 for i in r) for r in rows); H=sum(max(i.height for i in r)+26 for r in rows)
V=Image.new('RGB',(W,H),(235,235,235)); d=ImageDraw.Draw(V); y=0
for r,l in zip(rows,labels):
    x=0
    for im,t in zip(r,l): d.text((x+2,y+2),t,fill=(0,0,0)); V.paste(im,(x,y+14)); x+=im.width+12
    y+=max(i.height for i in r)+26
V.save('vel.png'); print(V.size)
