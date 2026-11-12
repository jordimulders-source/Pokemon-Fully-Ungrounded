# v7: uit Gemini's schets-hand (ronde 9) de duim linksboven weggehaald: drie vingers als waaier naar rechts (schuin omhoog, recht, schuin omlaag)
from PIL import Image
import numpy as np
a=np.asarray(Image.open('gemini/ronde9_schets_hand5.png').convert('RGB')).copy()
a[:, 984:]=(255,255,255)                      # zwarte balk rechts weg
fill=tuple(int(v) for v in np.median(a[380:387,803:825].reshape(-1,3),0)); dark=(16,15,22)
S=7
for x in range(772,842):
    xq=786+S*((x-786)//S)
    yl=368-int(round((xq-786)*(24/56)/S))*S   # trapjes van 7 px
    yl=min(yl,368)
    for y in range(280,380):
        if y<yl: a[y,x]=(255,255,255)
        elif y<yl+S: a[y,x]=dark if 786<=x<840 else a[y,x]
        elif x>=790 and y<379 and x<836: a[y,x]=fill
a[280:362,772:786]=(255,255,255)
out=Image.fromarray(a); out.save('model/model_hand_v7.png')
out.crop((700,230,990,530)).resize((580,600),Image.NEAREST).save('model/hand_v7_closeup.png')
