import sys
R=open('raster.txt').read().split('\n')[:64]
a,b=(int(sys.argv[1]),int(sys.argv[2])) if len(sys.argv)>2 else (0,64)
print('   '+''.join(str(i//10) for i in range(64)));print('   '+''.join(str(i%10) for i in range(64)))
for y in range(a,b): print(f'{y:2d} '+R[y])
