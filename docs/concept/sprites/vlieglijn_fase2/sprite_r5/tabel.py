from celmeting import *
import sys
DX, DY = 0, 2
a = np.array(Image.open('mug_r5.png')); a4 = np.array(Image.open('../sprite_r4/mug_r4B.png'))
CH = '.#kdgwPpqLliYyEe'
if __name__ == '__main__':
    print('cel: model zwart%%/luma(niet-zwart) r4B r5   (model verschoven dx=%d dy=%d modelpx)' % (DX, DY))
    print('    ' + ' '.join('%-10d' % x for x in range(23, 38)))
    for y in range(33, 51):
        row = []
        for x in range(23, 38):
            b, z, k = cel(x, y, DX, DY)
            if b > 0.6:
                s = '   .   '
            else:
                L = int(0.299 * k[0] + 0.587 * k[1] + 0.114 * k[2]) if k else 0
                s = '%3d/%3d' % (int(z * 100), L)
            row.append(s + ' ' + CH[a4[y, x]] + CH[a[y, x]])
        print('%2d ' % y + ' '.join(row))
