# smalle donkere runs (draden) per spriterij: python3 draadpos.py
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(int); L=a.sum(2)/3
S=968/62
for sy in range(17,62):
    my=int(1+(sy+0.5-4)*S); row=L[my]; dk=row<150
    runs=[];x=0
    while x<1024:
        if dk[x]:
            x0=x
            while x<1024 and dk[x]: x+=1
            if x-x0<=10:
                l=row[max(0,x0-3)];r=row[min(1023,x+2)]
                if l>200 and r>200: runs.append(round((x0+x)/2/S-24/S+1,1))
        x+=1
    print(sy,runs)
