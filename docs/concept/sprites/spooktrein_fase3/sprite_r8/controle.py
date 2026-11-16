# Overlay: donkere pixels van het natieve model, met dezelfde rij-/kolomduplicatie geschaald, over r8 (kop ogen+mond).
# Rood kader = donker in het model; elke donkere r8-pixel in de zone moet binnen een kader vallen (en omgekeerd).
from PIL import Image, ImageDraw; import numpy as np
n=np.array(Image.open('model/natief.png').convert('RGB')).astype(int)[6:21,29:63]   # r6-20, x29-62
cols=[]; 
for i in range(n.shape[1]):
    cols.append(i)
    if i in (15,23): cols.append(i)
rows=[]
for r in range(n.shape[0]):
    rows.append(r)
    if r+6==12: rows.append(r)
s=n[np.ix_(rows,cols)]                      # geschaald model, 16x36
donker=(s[:,:,1]<150)&(s[:,:,1]>s[:,:,0]+25)
a=np.array(Image.open('sprite_r8/sprite.png'))
X0,X1,Y0,Y1=20,28,3,12                      # zone ogen+mond (sprite)
fout=[];mis=[]
for y in range(Y0,Y1+1):
    for x in range(X0,X1+1):
        m=donker[y,x-14]; d=a[y,x]==6
        if d and not m: fout.append((x,y))
        if m and not d: mis.append((x,y))
print('donker in r8 maar niet in model:',fout); print('donker in model maar niet in r8:',mis)
Z=24; c=Image.open('sprite_r8/sprite.png').convert('RGBA'); b=Image.new('RGBA',c.size,(255,255,255,255)); b.alpha_composite(c)
big=b.convert('RGB').crop((14,0,44,16)).resize((30*Z,16*Z),Image.NEAREST); dr=ImageDraw.Draw(big)
for y in range(16):
    for x in range(14,44):
        if donker[y,x-14]: dr.rectangle([(x-14)*Z+3,y*Z+3,(x-13)*Z-4,(y+1)*Z-4],outline=(255,0,0),width=2)
dr.rectangle([(X0-14)*Z,Y0*Z,(X1-13)*Z,(Y1+1)*Z],outline=(0,0,255),width=2)
big.save('sprite_r8/overlay.png')
Image.fromarray(s.astype('uint8')).save('sprite_r8/model_geschaald.png')
