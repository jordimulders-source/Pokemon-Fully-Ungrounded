# vel r3: r3 | r2 | r10kop | g3r5 op 8x; kop 12x (r3 | r2); 1x licht/donker
import os; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
def rgba(p):
    im=Image.open(os.path.join(H,p))
    if im.mode=='P': im.info['transparency']=0
    return im.convert('RGBA')
L=[('r3',rgba('claydol_r10kop_r3.png')),('r2',rgba('../r2/claydol_r10kop_r2.png')),('r10kop (ronde 1)',rgba('../claydol_r10kop.png')),('g3r5 palet B',rgba('../../claydol_gemini_r3/r5/claydol_g3r5_paletB.png'))]
W=4*522+10; v=Image.new('RGBA',(W,16+512+30+40*12+20+100),(255,255,255,255)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate(L):
    x=10+i*522; d.text((x,3),t,fill='black'); v.alpha_composite(im.resize((512,512),Image.NEAREST),(x,16))
y=16+512+12; d.text((10,y),'kop 12x (x 8-56, y 0-40): r3 | r2',fill='black'); y+=16
for i in range(2): v.alpha_composite(L[i][1].crop((8,0,56,40)).resize((576,480),Image.NEAREST),(10+i*596,y))
y+=480+12
for i,(t,im) in enumerate(L):
    for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
        q=Image.new('RGBA',(80,80),bg); q.alpha_composite(im,(8,8)); v.alpha_composite(q,(10+i*200+j*90,y))
d.text((10+4*200,y+30),'1x licht/donker: r3 | r2 | r10kop | g3r5',fill='black')
v.crop((0,0,W,y+90)).save(os.path.join(H,'vel.png'))
