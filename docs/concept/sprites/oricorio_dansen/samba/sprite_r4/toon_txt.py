# tekst met kolomliniaal: toon_txt.py bestand.txt y0 y1 x0 x1
import sys
r=open(sys.argv[1]).read().split('\n'); y0,y1,x0,x1=map(int,sys.argv[2:6])
print('    '+''.join(str((x//10)%10) for x in range(x0,x1))); print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1): print('%2d  %s'%(y,r[y][x0:x1]))
