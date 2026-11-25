# vel.png: r10 | r9 | model (8x, zelfde pixelmaat) + 1x; bokser_8x.png
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite_r6'); from palet import PAL
BG=(232,240,232); Z=8
def img(a,bg=BG): return Image.fromarray(np.array([bg]+PAL[1:],'uint8')[a])
def vol(a):  # in 64x64 kader, onderaan gecentreerd
    o=np.zeros((64,64),int); h,w=a.shape; y0=63-h; x0=(64-w)//2; o[y0:y0+h,x0:x0+w]=a; return o
r10=vol(np.load(sys.argv[1] if len(sys.argv)>1 else 'bokser.npy')); r9=np.load('../sprite_r9/bokser.npy')
m=Image.open('../r12.png').convert('RGB').resize((512,512),Image.LANCZOS)
ims=[('r10 (52 hoog)',img(r10).resize((512,512),Image.NEAREST),img(r10)),('r9 (61 hoog)',img(r9).resize((512,512),Image.NEAREST),img(r9)),('model r12',m,None)]
o=Image.new('RGB',(3*522,512+24+70),(255,255,255)); d=ImageDraw.Draw(o)
for i,(t,im,one) in enumerate(ims):
    o.paste(im,(i*522,22)); d.text((i*522,5),t,fill=(0,0,0))
    if one: o.paste(one,(i*522,540))
o.save(sys.argv[2] if len(sys.argv)>2 else 'vel.png')
img(r10,(255,255,255)).resize((512,512),Image.NEAREST).save('bokser_8x.png')
np.save('bokser64.npy',r10)
