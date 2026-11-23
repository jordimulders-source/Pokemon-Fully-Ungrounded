import numpy as np; from PIL import Image
E=np.array(Image.open('eindkeuring/claydol_eind.png')); PAL=np.array(Image.open('eindkeuring/claydol_eind.png').getpalette()[:48]).reshape(16,3).astype('uint8')
M=np.load('r5/M.npy').astype('uint8'); M[E==0]=255
a=PAL[E]; a[E==0]=255
y0,y1,x0,x1=24,62,8,54
im=np.concatenate([a[y0:y1,x0:x1],np.full((y1-y0,2,3),200,'uint8'),M[y0:y1,x0:x1]],1)
Image.fromarray(im).resize((im.shape[1]*10,im.shape[0]*10),0).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/81de79ab-6056-55f3-b3d2-5fcd03808eb6/scratchpad/k.png')
