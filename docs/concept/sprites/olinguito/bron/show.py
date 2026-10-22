import sys
rows=[l.rstrip('\n')[1:-1] for l in open(sys.argv[1])]
x0=int(sys.argv[2]) if len(sys.argv)>2 else 0; x1=int(sys.argv[3]) if len(sys.argv)>3 else 64
print('   '+''.join(str(x//10) for x in range(x0,x1))); print('   '+''.join(str(x%10) for x in range(x0,x1)))
for y,r in enumerate(rows):
    if r.strip(): print('%2d %s'%(y,r[x0:x1]))
