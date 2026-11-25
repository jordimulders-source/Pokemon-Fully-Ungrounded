# vel.png: r7 | r6-meer | model (8x) + 1x; bokser_8x.png; kop_12x.png
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite_r6'); from palet import PAL
BG=(232,240,232)
def sp(a,box,Z):
    x0,y0,x1,y1=box; rgb=np.array([BG]+PAL[1:],'uint8')[a[y0:y1,x0:x1]]
    return Image.fromarray(rgb).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
m=Image.open('../r12.png').convert('RGB'); pad=Image.new('RGB',(1424,1424),(255,255,255)); pad.paste(m,(200,200))
p=10.24; ph=10.25; s=88/63
def mod(box,Z):
    x0,y0,x1,y1=box; X=lambda c:200+ph+(12+(c-10)*s)*p; Y=lambda r:200+ph+(5+r*s)*p
    return pad.crop((int(X(x0)),int(Y(y0)),int(X(x1)),int(Y(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def vel(naam,box,Z,F,een=True):
    ims=[(t,sp(np.load(f),box,Z)) for t,f in F]+[('model r12',mod(box,Z))]
    w,h=ims[0][1].size; H=h+24+(80 if een else 0); o=Image.new('RGB',(len(ims)*(w+10),H),(255,255,255)); d=ImageDraw.Draw(o)
    for i,(t,im) in enumerate(ims):
        o.paste(im,(i*(w+10),22)); d.text((i*(w+10),5),t,fill=(0,0,0))
        if een and i<len(F): o.paste(sp(np.load(F[i][1]),(0,0,64,64),1),(i*(w+10),h+30))
    o.save(naam)
if __name__=='__main__':
    F=[('r7','bokser.npy'),('r6 meer','../sprite_r6/var/meer.npy')]
    vel('vel.png',(0,0,64,64),8,F)
    vel('kop_12x.png',(24,0,56,20),12,F,False)
    a=np.load('bokser.npy'); Image.fromarray(np.array([(255,255,255)]+PAL[1:],'uint8')[a]).resize((512,512),Image.NEAREST).save('bokser_8x.png')
