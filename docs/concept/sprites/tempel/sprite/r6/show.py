import sys
R=[l.rstrip('\n') for l in open(sys.argv[1])][:64]
x0,x1,y0,y1=map(int,sys.argv[2:6])
print('    '+''.join(str(x//10) for x in range(x0,x1))); print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print(f'{y:3d} '+R[y][x0:x1])
