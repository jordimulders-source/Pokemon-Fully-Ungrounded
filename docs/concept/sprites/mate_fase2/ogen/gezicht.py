# Gezichtsvarianten ventje ("keihard aan het werk") op het natieve raster, terug in het 1024-model geplakt.
import numpy as np; from PIL import Image, ImageDraw
N=np.asarray(Image.open('ogen/natief.png').convert('RGB')).copy()
M=np.asarray(Image.open('r6_samengesteld/r6_water_r2.png').convert('RGB')).copy()
D=(14,15,10); G=(140,163,91); S=(93,113,63); W=(247,249,238)
def zet(img_n,img_m,pix):
    for (x,y),c in pix.items():
        img_n[y,x]=c
        x0,x1=int(round(x*10.24)),int(round((x+1)*10.24)); y0,y1=int(round(y*10.24)),int(round((y+1)*10.24))
        img_m[y0:y1,x0:x1]=c
basis={xy:G for xy in [(49,41),(50,41),(49,42),(50,42),(55,41),(56,41),(55,42),(56,42),(51,45),(52,45),(53,45),(54,45)]}  # alleen oude ogen en mond wissen; bladtextuur blijft
brauw={(48,39):D,(49,39):D,(50,40):D, (57,39):D,(56,39):D,(55,40):D}
brauw_s={(48,40):S,(57,40):S}
open_l={(49,41):D,(50,41):D,(49,42):W,(50,42):D}
open_r={(55,41):D,(56,41):D,(55,42):W,(56,42):D}
spleet_l={(49,42):D,(50,42):D,(48,41):S}
spleet_r={(55,42):D,(56,42):D,(57,41):S}
mond_strak={(51,45):D,(52,45):D,(53,45):D,(54,45):D,(50,46):D,(55,46):D}
mond_tand={(51,44):D,(52,44):D,(53,44):D,(54,44):D,(50,45):D,(51,45):W,(52,45):W,(53,45):W,(54,45):W,(55,45):D,(51,46):D,(52,46):D,(53,46):D,(54,46):D}
V={'A_vastberaden':[brauw,brauw_s,open_l,open_r,mond_strak],
   'B_inspanning':[brauw,brauw_s,spleet_l,spleet_r,mond_tand],
   'C_een_oog_dicht':[brauw,brauw_s,spleet_l,open_r,mond_strak],
   'D_open_tanden':[brauw,brauw_s,open_l,open_r,mond_tand]}
tegels=[]
for naam,lagen in V.items():
    n=N.copy(); m=M.copy(); zet(n,m,basis)
    for l in lagen: zet(n,m,l)
    Image.fromarray(m).save(f'ogen/model_{naam}.png')
    t=Image.fromarray(n).crop((38,28,66,58)).resize((28*12,30*12),Image.NEAREST)
    c=Image.new('RGB',(t.width,t.height+24),'white'); c.paste(t,(0,24)); ImageDraw.Draw(c).text((6,6),naam,fill='black'); tegels.append(c)
t=Image.fromarray(N).crop((38,28,66,58)).resize((28*12,30*12),Image.NEAREST)
c=Image.new('RGB',(t.width,t.height+24),'white'); c.paste(t,(0,24)); ImageDraw.Draw(c).text((6,6),'nu (r6)',fill='black'); tegels.insert(0,c)
vel=Image.new('RGB',(sum(x.width+10 for x in tegels),tegels[0].height),'white'); x=0
for tt in tegels: vel.paste(tt,(x,0)); x+=tt.width+10
vel.save('ogen/varianten_gezicht.png')
