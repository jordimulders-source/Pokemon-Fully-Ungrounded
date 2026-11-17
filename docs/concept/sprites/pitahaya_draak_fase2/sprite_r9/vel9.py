from PIL import Image, ImageDraw
n=Image.open('natief.png').convert('RGB')
def sp(f,bg): im=Image.open(f).convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
X0,X1,Y0,Y1=1,24,38,58
def bek(f): return sp(f,(255,255,255)).crop((X0,Y0,X1,Y1)).resize(((X1-X0)*12,(Y1-Y0)*12),Image.NEAREST)
m=n.crop((2+3*X0,3*(Y0-13),2+3*X1,3*(Y1-13))).resize(((X1-X0)*12,(Y1-Y0)*12),Image.NEAREST)
F=['pitahaya2_r9A.png','pitahaya2_r9B.png','pitahaya2_r9A_achter.png']
rows=[[m,bek('pitahaya2_r8A.png')]+[bek(f) for f in F],[sp(F[0],(255,255,255)).resize((512,512),Image.NEAREST)]]
kl=[];lk=[]
for bg,t in (((255,255,255),''),((40,40,48),' donker')):
    for f,nm in zip(F,('r9A','r9B','r9A_achter')): im=sp(f,bg); kl+=[im,im.resize((128,128),Image.NEAREST)]; lk+=[nm+' 1x'+t,'2x']
rows+= [kl[:6],kl[6:]]
labels=[['model (natief)','r8A','r9A','r9B','r9A_achter'],['r9A 8x'],lk[:6],lk[6:]]
W=max(sum(i.width+12 for i in r) for r in rows); H=sum(max(i.height for i in r)+26 for r in rows)
V=Image.new('RGB',(W,H),(235,235,235)); d=ImageDraw.Draw(V); y=0
for r,l in zip(rows,labels):
    x=0
    for im,t in zip(r,l): d.text((x+2,y+2),t,fill=(0,0,0)); V.paste(im,(x,y+14)); x+=im.width+12
    y+=max(i.height for i in r)+26
V.save('vel.png')
