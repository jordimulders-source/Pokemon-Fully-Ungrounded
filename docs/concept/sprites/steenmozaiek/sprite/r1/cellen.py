# per spritecel de 4 modelklassen (zelfde letters als het tekstraster) naast de spriteregel
import sys, numpy as np
c = np.load(sys.argv[1]); rows = [l.rstrip('\n') for l in open(sys.argv[2])]
j0, j1, i0, i1 = map(int, sys.argv[3:7])
print('     ' + ''.join('%-3d' % i for i in range(i0, i1)))
for j in range(j0, j1):
    for dy in range(2):
        s = ''.join(c[2*j+dy, 2*i] + c[2*j+dy, 2*i+1] + ' ' for i in range(i0, i1))
        print(('%3d  ' % j if dy == 0 else '     ') + s + ('  ' + ''.join('%-3s' % ch for ch in rows[j][i0:i1]) if dy == 0 else ''))
