# r7 -> model: korte 5e antenne weg, onderste antenne verlengd (Jordi, 23 nov)
from PIL import Image
im=Image.open('model/r7_natief.png').convert('RGB'); q=Image.open('model/r7_natief16.png')
W=(255,255,255); out=im.copy()
wit=lambda x,y: q.getpixel((x,y))<8
# 1) korte 5e antenne: alles rechts van de bolrand wit (rij: x van de bolrand)
rand={58:62,59:61,60:61,61:60,62:60,63:59,64:58}
for y,xr in rand.items():
    for x in range(xr+1,80):
        if y==58 and x<=65: continue   # onderrand van de lange antenne erboven
        out.putpixel((x,y),W)
# 2) onderste antenne verlengen: patroon herhaalt met stap (3,1)
src=im.copy(); EXTRA=5  # stappen van (3,1) => +15 px
for x in range(73,76):
    for y in range(64,80): out.putpixel((x,y),W)
for x in range(73,73+3*EXTRA):
    n=(x-70)//3; sx=x-3*n
    for y in range(64,80):
        if not wit(sx,y): out.putpixel((x,y+n),src.getpixel((sx,y)))
for x in range(73,76):           # punt verplaatsen
    for y in range(64,80):
        if not wit(x,y): out.putpixel((x+3*EXTRA,y+EXTRA),src.getpixel((x,y)))
out.save('model/model_r7b_natief.png')
out.resize((out.width*10,out.height*10),Image.NEAREST).save('model/model_r7b.png')
