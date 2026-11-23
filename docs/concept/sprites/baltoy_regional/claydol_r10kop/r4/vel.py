# vel r4: r4 | r3 | g3r5 | variant 2 px op 8x; kop 12x naast r3; neus 12x naast g3r5; 1x licht/donker
import os; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
def rgba(p):
    im=Image.open(os.path.join(H,p))
    if im.mode=='P': im.info['transparency']=0
    return im.convert('RGBA')
A=rgba('claydol_r10kop_r4.png'); A2=rgba('claydol_r10kop_r4_ogen2px.png'); R3=rgba('../r3/claydol_r10kop_r3.png'); G=rgba('../../claydol_gemini_r3/r5/claydol_g3r5_paletB.png')
L=[('r4 (ogen+neus 1 px omlaag)',A),('r3',R3),('g3r5 palet B',G),('variant: 2 px omlaag',A2)]
W=4*522+10; v=Image.new('RGBA',(W,16+512+30+480+30+15*12+30+100),(255,255,255,255)); d=ImageDraw.Draw(v)
for i,(t,im) in enumerate(L):
    x=10+i*522; d.text((x,3),t,fill='black'); v.alpha_composite(im.resize((512,512),Image.NEAREST),(x,16))
y=16+512+12; d.text((10,y),'kop 12x: r4 | r3',fill='black'); y+=16
for i,im in enumerate([A,R3]): v.alpha_composite(im.crop((8,0,56,40)).resize((576,480),Image.NEAREST),(10+i*596,y))
y+=480+12; d.text((10,y),'neus 12x (x 19-31): r4 y 20-37 | g3r5 y 19-36',fill='black'); y+=16
v.alpha_composite(A.crop((19,20,31,37)).resize((144,204),Image.NEAREST),(10,y)); v.alpha_composite(G.crop((19,19,31,36)).resize((144,204),Image.NEAREST),(174,y))
y+=204+12
for i,(t,im) in enumerate(L):
    for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
        q=Image.new('RGBA',(80,80),bg); q.alpha_composite(im,(8,8)); v.alpha_composite(q,(10+i*200+j*90,y))
d.text((10+4*200,y+30),'1x licht/donker: r4 | r3 | g3r5 | 2 px',fill='black')
v.crop((0,0,W,y+90)).save(os.path.join(H,'vel.png'))
