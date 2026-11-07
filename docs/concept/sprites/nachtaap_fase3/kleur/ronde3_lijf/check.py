from PIL import Image
a=Image.open('../ronde1s/nachtaap_fase3.png'); b=Image.open('nachtaap_fase3.png')
A=a.load(); Bp=b.load()
alpha=sum((A[x,y]==0)!=(Bp[x,y]==0) for x in range(64) for y in range(64))
print('alpha-diff',alpha, 'palet gelijk', a.getpalette()[:48]==b.getpalette()[:48])
def box(x0,x1,y0,y1): return sum(A[x,y]!=Bp[x,y] for x in range(x0,x1+1) for y in range(y0,y1+1))
print('hand+gloed x4-23 r44-62:',box(4,23,44,62))
print('kop x0-19 r27-45 + x20 r35-43:',box(0,19,27,45)+box(20,20,35,43))
print('staart x44-63 r22-40:',box(44,63,22,40))
print('voeten: boven r4-11',box(30,42,4,11),' onder x52-63 r53-60',box(52,63,53,60))
nv=[(x,y,A[x,y],Bp[x,y]) for x in range(64) for y in range(64) if A[x,y]!=Bp[x,y] and (A[x,y]>5 or Bp[x,y]>5)]
print('niet-vacht indexen gewijzigd:',len(nv))
print('totaal gewijzigd:',sum(A[x,y]!=Bp[x,y] for x in range(64) for y in range(64)))
# open randen: tint 3/4/5 naast transparant (4-buren)
op=[]
for y in range(64):
  for x in range(64):
    if Bp[x,y] in (3,4,5):
      for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        X,Y=x+dx,y+dy
        if not(0<=X<64 and 0<=Y<64) or Bp[X,Y]==0: op.append((x,y,Bp[x,y])); break
print('open randen (vacht 3/4/5 naast transparant):',op)
