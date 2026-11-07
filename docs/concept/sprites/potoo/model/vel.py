# Vergelijkingsvel lijfmaten: boven op 0,5x, onder dezelfde maat verkleind tot 62 px hoog en 4x vergroot (nearest)
from PIL import Image, ImageDraw
o=Image.open('model_los.png').transpose(Image.FLIP_LEFT_RIGHT)
ims=[('origineel',o)]+[(f'+{p}%',Image.open(f'model_lijf_{p}.png')) for p in (10,20,30)]
crops=[(n,i.crop(i.getbbox())) for n,i in ims]
Hmax=max(c.height for n,c in crops); sc=0.5; pw=max(c.width for n,c in crops); col=int(pw*sc+30)
sheet=Image.new('RGB',(len(crops)*col, int(Hmax*sc)+60+62*4+20),(64,160,64)); d=ImageDraw.Draw(sheet)
for k,(n,c) in enumerate(crops):
    x=k*col+15; c2=c.resize((int(c.width*sc),int(c.height*sc)),Image.LANCZOS)
    sheet.paste(c2,(x,40),c2); d.text((x,10),n,fill=(255,255,255))
    f=62/c.height; t=c.resize((max(1,round(c.width*f)),62),Image.LANCZOS)
    t=t.resize((t.width*4,t.height*4),Image.NEAREST); sheet.paste(t,(x,int(Hmax*sc)+50),t)
    t8=c.resize((max(1,round(c.width*f)),62),Image.LANCZOS); t8=t8.resize((t8.width*8,496),Image.NEAREST)
    bg=Image.new('RGB',t8.size,(64,160,64)); bg.paste(t8,(0,0),t8); bg.save(f'preview_8x_{n.strip("+%")}.png')
sheet.save('lijf_maten_vel.png')
