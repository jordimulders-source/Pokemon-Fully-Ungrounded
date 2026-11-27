# r7: losse pixels van r6. Geen nieuwe tinten, geen vormwijziging.
# - lijnpixels (1) zonder enige lijnbuur (8-buren) binnen de figuur -> 2 (donkerste ijstint): (31,17) kuif, (19,20) gezichtsfacet,
#   (28,48) rok/been, (33,55) rechterbeen. Het model heeft daar een donkere snede, maar als losse zwarte stip leest het als vuil.
# - (8,9): lichte stip (4) midden in het donkere voorvlak van de opgeheven kubus -> 2, zodat het voorvlak een eigen tint houdt.
import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); from toon import save_idx, save_p64
S=np.load(D+'r6/idx.npy'); pal=eval(open(D+'pal.txt').read()); T=S.copy(); log=[]
for (x,y),v in {(31,17):2,(19,20):2,(28,48):2,(33,55):2,(8,9):2}.items():
    log.append(f'({x},{y}) {T[y,x]}->{v}'); T[y,x]=v
np.save(D+'r7/idx.npy',T); open(D+'r7/log.txt','w').write('\n'.join(log)+'\n'); print(log)
save_p64(T,pal,D+'r7/sprite.png'); save_idx(T,pal,D+'r7/r7_8x.png',8)
