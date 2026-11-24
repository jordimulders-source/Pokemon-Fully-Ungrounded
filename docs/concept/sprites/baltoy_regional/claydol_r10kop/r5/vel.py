# vel r5: r5 | r4 op 8x; lijf 12x r5 | r4; lijnbocht 12x k2 | k3 | r4; 1x licht/donker
import os; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
def rgba(p):
    im=Image.open(os.path.join(H,p)); im.info['transparency']=0; return im.convert('RGBA')
A=rgba('claydol_r10kop_r5.png'); R4=rgba('../r4/claydol_r10kop_r4.png'); K2=rgba('claydol_r10kop_r5_bocht2.png'); K3=rgba('claydol_r10kop_r5_bocht3.png')
W=2*522+10; v=Image.new('RGBA',(1290,2000),(255,255,255,255)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate([('r5 (bocht 2 px hoger)',A),('r4',R4)]):
    d.text((10+i*522,3),t,fill='black'); v.alpha_composite(im.resize((512,512),Image.NEAREST),(10+i*522,16))
y=540; d.text((10,y),'lijf 12x (x 13-51, y 39-61): r5 | r4',fill='black'); y+=16
for i,im in enumerate([A,R4]): v.alpha_composite(im.crop((13,39,52,61)).resize((468,264),Image.NEAREST),(10+i*478,y))
y+=264+14; d.text((10,y),'lijnbocht 12x (x 30-56, y 14-32): 2 px hoger (gekozen) | 3 px hoger | r4',fill='black'); y+=16
for i,im in enumerate([K2,K3,R4]): v.alpha_composite(im.crop((30,14,56,32)).resize((312,216),Image.NEAREST),(10+i*322,y))
y+=216+14
for i,(t,im) in enumerate([('r5',A),('r4',R4),('bocht 3',K3)]):
    for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
        q=Image.new('RGBA',(80,80),bg); q.alpha_composite(im,(8,8)); v.alpha_composite(q,(10+i*200+j*90,y))
d.text((610,y+30),'1x licht/donker: r5 | r4 | bocht 3',fill='black')
v.crop((0,0,1290,y+90)).save(os.path.join(H,'vel.png'))
