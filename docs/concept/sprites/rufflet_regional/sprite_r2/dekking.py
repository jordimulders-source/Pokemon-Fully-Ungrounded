# dekking per spritepixel op het 1024-model (niet-achtergrond = min(rgb)<246), raster x=194+20.48sx, y=50.7+20.48sy
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../gemini/r1.png').convert('RGB')).astype(int)
fg=a.min(2)<246
def cov(sy,sx):
    x0=194+20.48*sx; y0=50.7+20.48*sy
    return fg[int(round(y0)):int(round(y0+20.48)),int(round(x0)):int(round(x0+20.48))].mean()
C=np.array([[cov(sy,sx) for sx in range(33)] for sy in range(45)]); np.save('dek.npy',C)
if __name__=='__main__':
    from pal import lees
    g=lees('rufflet_r1.txt')
    for sy in range(0,20):
        print('%2d '%sy+''.join(('#' if C[sy,sx]>=.5 else '+' if C[sy,sx]>=.3 else '-' if C[sy,sx]>=.12 else '.') if g[sy,sx]=='.' else ('o' if C[sy,sx]>=.5 else 'X') for sx in range(5,30)))
    print('   '+''.join(str(sx%10) for sx in range(5,30)))
