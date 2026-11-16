# half.npy -> 64x64, gecentreerd, onderaan (onderste rij 62); zones mee
import numpy as np
o=np.load('half.npy'); y0,y1,x0,x1=map(int,open('half_crop.txt').read().split())
Z=np.load('zones_half.npy')[:,y0:y1,x0:x1]
hh,ww=o.shape; X=(64-ww)//2; Y=63-hh
full=np.zeros((64,64),int); full[Y:Y+hh,X:X+ww]=o
Z64=np.zeros((4,64,64),bool); Z64[:,Y:Y+hh,X:X+ww]=Z
np.save('basis.npy',full); np.save('z64.npy',Z64); open('plaats.txt','w').write(f'{X} {Y} {ww} {hh}')
print('geplaatst',ww,'x',hh,'op',X,Y)
