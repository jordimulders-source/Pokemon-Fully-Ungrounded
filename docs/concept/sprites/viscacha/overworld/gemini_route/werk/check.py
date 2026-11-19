import numpy as np; from PIL import Image
a=np.array(Image.open('../af/overworld.png'))
for i,n in enumerate(['voor','voor-lopen','achter','achter-lopen','opzij','opzij-lopen']):
    f=a[:,i*32:i*32+32]; ys,xs=np.where(f>0)
    m=(f>0)
    sym=(m & m[:,::-1]).sum()/m.sum() if True else 0
    # symmetrie rond eigen middenas
    x0,x1=xs.min(),xs.max(); sub=m[:,x0:x1+1]; s2=(sub&sub[:,::-1]).sum()/sub.sum()
    print(f'{n:13s} h={ys.max()-ys.min()+1:2d} w={x1-x0+1:2d} onder y={ys.max()} midden x={(x0+x1)/2:.1f} symm={s2:.3f} kleuren={len(set(f[m].tolist()))}')
for b in (0,2,4):
    d=(a[:,b*32:b*32+32]!=a[:,(b+1)*32:(b+1)*32+32]).sum(); print('loopverschil frame',b,'->',b+1,':',d,'px')
# losse pixels: niet-transparante pixel zonder 4-buur van dezelfde kleur, behalve omlijning/glans
P=a
lone=0
for i in range(6):
    f=a[:,i*32:i*32+32]
    for y in range(1,31):
        for x in range(1,31):
            c=f[y,x]
            if c in (0,1): continue
            nb=[f[y-1,x],f[y+1,x],f[y,x-1],f[y,x+1]]
            if c not in nb: lone+=1; print('  los',i,x,y,'idx',c)
print('losse pixels',lone)
