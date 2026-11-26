# Keurder r4: verfijnde vensters + lichte pixels op de buitenrand.
exec(open('docs/concept/sprites/satelliet_fase3/keuring_r4/bollen.py').read().split('# vensters')[0])
B={'grote oogbol LO':((10,24,44,55),(80,250)),
   'kleine oogbol R':((46,55,35,42),(-40,140)),
   'kleine oogbol L':((15,22,27,34),(110,250)),
   'bol RB':((44,57,17,28),(-150,30))}
for n,(w,(h0,h1)) in B.items():
    p=edge(*w); cx,cy,r,res=fit(p)
    ang=np.degrees(np.arctan2(p[:,1]-cy,p[:,0]-cx)); ang=np.where(ang<h0,ang+360,ang); sel=(ang>=h0)&(ang<=h1)
    q=p[sel]; cx,cy,r,res=fit(q)
    print(f'{n}: c=({cx:.1f},{cy:.1f}) r={r:.2f} n={len(q)} max={abs(res).max():.2f} rms={np.sqrt((res**2).mean()):.2f}')
    for (x,y),e in zip(q.astype(int),res): print('   ',x,y,a[y,x],round(e,2))
print('lichte randpixels (index>4 aan transparant):')
for y in range(64):
  for x in range(64):
    if a[y,x]>4:
      nb=[a[y+dy,x+dx]>0 if 0<=y+dy<64 and 0<=x+dx<64 else False for dy,dx in((0,1),(1,0),(0,-1),(-1,0))]
      if not all(nb): print(' ',x,y,a[y,x])
