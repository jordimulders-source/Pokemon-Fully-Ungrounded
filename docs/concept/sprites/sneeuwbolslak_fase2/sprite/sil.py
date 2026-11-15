# Silhouet 56 px (Jordi 15 nov: "56 is goed") uit het model sprite/r8_bol_r7.png, zelfde verkleining als maattest.py.
import sys; sys.argv=['x']
exec(open('sprite/maattest.py').read().split('widths=')[0])
W=56; m,mean,H=sil(W)
ox=(64-W)//2; oy=64-H-4
M=np.zeros((64,64),bool); M[oy:oy+H,ox:ox+W]=m
G=np.zeros((64,64,3)); G[oy:oy+H,ox:ox+W]=mean
np.save('sprite/sil56.npy',M); np.save('sprite/gids56.npy',G)
a=np.zeros((64,64,4),'uint8'); a[M]=[0,0,0,255]; Image.fromarray(a).save('sprite/silhouet56.png')
g=np.zeros((64,64,4),'uint8'); g[M,:3]=G[M].astype('uint8'); g[M,3]=255; Image.fromarray(g).save('sprite/gids56.png')
print('offset',ox,oy,'schaal',(x1-x0)/W)
