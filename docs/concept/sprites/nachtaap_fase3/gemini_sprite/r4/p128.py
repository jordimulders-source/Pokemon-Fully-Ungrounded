import numpy as np,sys
i=np.load('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/nachtaap_fase3/gemini_sprite/i128.npy')
x0,y0,x1,y1=map(int,sys.argv[1:5])  # sprite coords
print('    '+''.join(str((x//2)%10) if x%2==0 else ' ' for x in range(2*x0,2*x1)))
for y in range(2*y0,2*y1):
    print('%2d%s '%(y//2,'a' if y%2==0 else 'b')+''.join('.123456789ABCDEF'[v] for v in i[y,2*x0:2*x1]))
