import numpy as np,sys
i=np.load('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_fase3/gemini_sprite/i128.npy')
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('    '+' '.join('%-2d'%(x%100) for x in range(x0,x1)))
for y in range(y0,y1):
    for h in (0,1):
        print(('%2d '%y if h==0 else '   ')+' '+' '.join(''.join('.123456789ABCDEF'[v] for v in i[2*y+h,2*x:2*x+2]) for x in range(x0,x1)))
