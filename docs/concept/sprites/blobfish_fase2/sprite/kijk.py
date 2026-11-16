import sys; from PIL import Image; import numpy as np
C=np.load('kaal_rgb.npy'); A=np.load('alpha.npy'); L=np.load('lijnfrac.npy'); LC=np.load('lijnkleur.npy')
outs=[]
for t in [float(v) for v in sys.argv[1:]]:
    o=np.full(C.shape+(0,),0); im=np.where((L>=t)[...,None],LC,C); im[A<0.45]=255
    outs.append(Image.fromarray(im.astype('uint8')).resize((C.shape[1]*8,C.shape[0]*8),Image.NEAREST))
v=Image.new('RGB',(sum(o.width+10 for o in outs),outs[0].height),'white'); x=0
for o in outs: v.paste(o,(x,0)); x+=o.width+10
v.save('kijk.png')
