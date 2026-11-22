import numpy as np; from PIL import Image
o=np.load('idx.npy')
for v in 'AB':
    p=Image.open(f'../r10/{v}.png').getpalette()[:48]
    x=Image.fromarray(o.astype('uint8'),'P'); x.putpalette(p+[0]*(768-48)); x.save(f'{v}.png',transparency=0)
