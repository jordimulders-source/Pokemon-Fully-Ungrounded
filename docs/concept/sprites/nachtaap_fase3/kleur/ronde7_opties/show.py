# toont een uitsnede als tekstraster (x20..47) of maakt een 8x/3x vergelijking
import sys
from PIL import Image
def dump(f,x0=20,x1=48,y0=20,y1=50):
    a=Image.open(f).load()
    print('     '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1):
        print('r%2d  '%y+''.join('.' if a[x,y]==0 else '0123456789abcdef'[a[x,y]] for x in range(x0,x1)))
if __name__=='__main__':
    for f in sys.argv[1:]: print(f); dump(f)
