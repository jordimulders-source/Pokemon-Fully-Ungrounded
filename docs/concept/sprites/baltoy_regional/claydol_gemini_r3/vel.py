# vel.png: sprite 8x | model geschrapt 8x ; 1x naast elkaar ; gezicht 12x (sprite|model) ; krans 12x (sprite|model) ; 1x licht/donker
import numpy as np; from PIL import Image, ImageDraw
from bouw import rgb, S
from kaal3 import kaal
from zoom import zoom
S0,A,*_=kaal()
M=Image.fromarray(A.astype('uint8'))
sp=Image.open('claydol_g3.png'); sp.save('/tmp/_c.png'); spr=Image.open('/tmp/_c.png').convert('RGBA')
W=1300; vel=Image.new('RGB',(W,2000),(236,236,236)); d=ImageDraw.Draw(vel)
def lab(t,x,y): d.text((x,y),t,fill=(0,0,0))
lab('claydol_g3 (8x)',10,5); vel.paste(rgb(S).resize((512,512),0),(10,20))
lab('model r3 natief, geschrapt (8x)',540,5); vel.paste(M.resize((512,512),0),(540,20))
lab('1x',1070,5); vel.paste(rgb(S),(1070,20)); vel.paste(M,(1150,20))
lab('1x licht / donker',1070,100)
for i,bg in enumerate([(255,255,255),(48,48,56)]):
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(spr); vel.paste(b.convert('RGB'),(1070+i*80,115))
lab('gezicht 12x: sprite | model',10,545); g=zoom(14,31,7,58,12); vel.paste(g,(10,560))
lab('krans close-up 12x (linksboven): sprite | model',10,775+0); k=zoom(0,20,4,30,12); vel.paste(k,(10,790))
lab('krans close-up 12x (rechts): sprite | model',680,775); k2=zoom(9,40,44,64,12); vel.paste(k2,(680,790))
h=max(790+k.height,790+k2.height)+10
vel=vel.crop((0,0,W,h)); vel.save('vel.png'); print(vel.size)
