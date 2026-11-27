# vergelijkingsvel r5: r6 | r5 | model op 8x; 12x close-ups (r6 | r5 | model) van borst linker- en
# rechternek, koppen en kronkels; r5 op 1x/2x op licht en donker.
from PIL import Image, ImageDraw
F=64/92
M=Image.open('../../model/r2_natief.png').convert('RGB')
def plat(f):
    s=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',s.size,(255,255,255,255)); bg.alpha_composite(s); return bg.convert('RGB')
R5=plat('uku_pacha_r6.png'); R4=plat('../r5/uku_pacha_r5.png')
def mod(box,Z):
    x0,y0,x1,y1=box
    big=M.resize((round(100*F*Z),round(100*F*Z)),Image.NEAREST)
    im=Image.new('RGB',((x1-x0)*Z,(y1-y0)*Z),(255,255,255)); im.paste(big,(round((-5*F-x0)*Z),round((2-7*F-y0)*Z))); return im
def sp(im,box,Z):
    c=im.crop(box); return c.resize((c.width*Z,c.height*Z),Image.NEAREST)
rijen=[]
def rij(titel,ims):
    w=sum(i.width for i in ims)+12*(len(ims)-1); h=max(i.height for i in ims)+18
    r=Image.new('RGB',(w,h),(255,255,255)); d=ImageDraw.Draw(r); d.text((2,2),titel,fill=(0,0,0)); x=0
    for i in ims: r.paste(i,(x,18)); x+=i.width+12
    rijen.append(r)
B=(0,0,64,64)
rij('r6 | r5 | model (8x)',[sp(R5,B,8),sp(R4,B,8),mod(B,8)])
for t,box in (('linkerkop + tong 12x: r6 | r5 | model',(0,6,30,30)),('rechterkop (pupil, mond, streep) 12x: r6 | r5 | model',(28,0,52,16)),('tong 20x: r6 | r5 | model',(0,18,16,30))):
    Z=20 if '20x' in t else 12
    rij(t,[sp(R5,box,Z),sp(R4,box,Z),mod(box,Z)])
s=Image.open('uku_pacha_r6.png').convert('RGBA'); ims=[]
for bgc in ((248,248,248),(40,44,52)):
    for z in (1,2):
        bg=Image.new('RGBA',(64*z+16,64*z+16),bgc+(255,)); bg.alpha_composite(s.resize((64*z,64*z),Image.NEAREST),(8,8)); ims.append(bg.convert('RGB'))
rij('r6 1x/2x licht en donker',ims)
W=max(r.width for r in rijen); H=sum(r.height+10 for r in rijen)
V=Image.new('RGB',(W,H),(255,255,255)); y=0
for r in rijen: V.paste(r,(0,y)); y+=r.height+10
V.save('vel.png'); print(V.size)
