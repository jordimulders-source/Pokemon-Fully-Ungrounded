# kwart.py X0 Y0 X1 Y1 : model op kwart-spritepixels als tekens (#<50 +<100 o<150 -<190 ' '=licht, ','=achtergrond)
import sys,numpy as np
from PIL import Image
c=np.asarray(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poesrups/referenties/model_gekozen.png').convert('RGB')).astype(float);L=c.mean(2)
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from bg import masker; g=masker()
x0,y0,s=69,240,16.648; q=s/4
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
print('      '+''.join((str(X0+i//4)[-1] if i%4==0 else ' ') for i in range(4*(X1-X0))))
for j in range(4*(Y1-Y0)):
  yy=y0+(Y0+j/4-29)*s; row=''
  for i in range(4*(X1-X0)):
    xx=x0+(X0+i/4-5)*s; sl=(slice(int(yy),int(yy+q)),slice(int(xx),int(xx+q)))
    if g[sl].mean()>.5: row+=','; continue
    v=L[sl].mean(); row+= '#' if v<50 else '+' if v<100 else 'o' if v<150 else '-' if v<190 else ' '
  print(('%3d   '%(Y0+j//4) if j%4==0 else '      ')+row)
