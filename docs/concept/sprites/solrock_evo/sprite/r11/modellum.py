import sys,numpy as np; from PIL import Image
sys.path.insert(0,'../r6'); from toon_gezicht import S,X0,Y0
M=np.asarray(Image.open('../../referenties/model.png').convert('RGB')).astype(float)
def lum(x,y):
    a=M[int(round(Y0+y*S)):int(round(Y0+(y+1)*S)), int(round(X0+x*S)):int(round(X0+(x+1)*S))].reshape(-1,3)
    l=a.mean(1); g=a[(np.abs(a[:,0]-a[:,2])<30)&(l<150)]   # alleen grijze steenpixels
    return g.mean() if len(g)>10 else np.nan
