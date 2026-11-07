# vleugelnaad 1 px: per kolom alleen de onderste naadpixel houden (rest wordt vleugelvlak)
for x in range(41,60):
    ys=[y for y in range(33,39) if r[y][x] in '23']
    if len(ys)>1:
        keep=max(ys)
        for y in ys:
            if y!=keep and abs(y-keep)>0 and not (y==keep-1 and x>41 and (r[keep][x-1] not in '23' and r[y][x-1] in '23')):
                r[y][x]='A' if y<keep else r[y][x]
# kopomtrek rechts: doorlopende lijn (36,34)->(42,46) zoals het model
pts=[(36,34),(37,35),(37,36),(38,37),(38,38),(39,39),(39,40),(40,41),(40,42),(41,43),(41,44),(42,45),(42,46)]
for x,y in pts:
    if r[y][x]!='.': r[y][x]='3'
