from PIL import Image
g=[r for r in open('raster_grid.txt').read().split()]
sil=[l.strip() for l in open('../../../silhouet_hand/ronde5/silhouet.txt') if l.strip()]
PAL={'.':'98d0a0','k':'1a0f0b','m':'241712','d':'4c3121','b':'6a4630','l':'8a603e','g':'6b5442','h':'8a6c55',
 's':'54443c','e':'4a3324','r':'6e2418','i':'a8462a','w':'f2ead6','n':'b0a28a','p':'c08a80','q':'8e4f58'}
ORDER='.kmdblghseriwnpq'
flat=[]
for ch in ORDER: flat+=[int(PAL[ch][i:i+2],16) for i in (0,2,4)]
im=Image.new('P',(64,64)); im.putpalette(flat+[0]*(768-len(flat)))
im.putdata([ORDER.index(g[y][x]) for y in range(64) for x in range(64)])
im.save('../olinguito.png',transparency=0)
print('alpha-diff',sum((g[y][x]!='.')!=(sil[y][x]=='#') for y in range(64) for x in range(64)))
