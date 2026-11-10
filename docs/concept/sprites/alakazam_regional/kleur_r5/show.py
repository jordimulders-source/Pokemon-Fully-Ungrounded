import sys
R=[l.rstrip('\n').ljust(64,'.') for l in open(sys.argv[1])][:64]
a,b=(int(sys.argv[2]),int(sys.argv[3])) if len(sys.argv)>3 else (0,64)
print('   '+''.join(str(i//10) for i in range(64)));print('   '+''.join(str(i%10) for i in range(64)))
for y in range(a,b): print(f'{y:2d} '+R[y])
