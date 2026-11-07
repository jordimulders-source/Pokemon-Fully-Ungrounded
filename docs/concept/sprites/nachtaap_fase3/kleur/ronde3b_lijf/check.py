from PIL import Image
s1=Image.open('../ronde1s/nachtaap_fase3.png').load(); r3=Image.open('../ronde3_lijf/nachtaap_fase3.png').load()
im=Image.open('nachtaap_fase3.png'); B=im.load()
xy=[(x,y) for x in range(64) for y in range(64)]
print('alpha-diff met ronde3_lijf',sum((r3[p]==0)!=(B[p]==0) for p in xy),' met 1s',sum((s1[p]==0)!=(B[p]==0) for p in xy))
print('palet = 1s',Image.open('../ronde1s/nachtaap_fase3.png').getpalette()[:48]==im.getpalette()[:48])
def box(ref,x0,x1,y0,y1): return sum(ref[x,y]!=B[x,y] for x in range(x0,x1+1) for y in range(y0,y1+1))
va=box(s1,0,25,14,30)+box(s1,19,22,31,31)
print('vuistarm (x0-25 r14-30 + x19-22 r31) vs 1s:',va)
print('hand+gloed x4-23 r44-62 vs 1s:',box(s1,4,23,44,62))
print('staart x44-63 r22-40 vs 1s:',box(s1,44,63,22,40))
print('voeten vs 1s:',box(s1,30,42,4,11)+box(s1,52,63,53,60))
kop=[(x,y) for x in range(0,21) for y in range(27,46) if s1[x,y]!=B[x,y]]
print('kopvak x0-20 r27-45 wijzigingen vs 1s:',kop)
print('niet-vacht gewijzigd vs 1s:',sum(1 for p in xy if s1[p]!=B[p] and (s1[p]>5 or B[p]>5)))
print('gewijzigd vs 1s:',sum(s1[p]!=B[p] for p in xy),' vs ronde3_lijf:',sum(r3[p]!=B[p] for p in xy))
op=[p for p in xy if B[p] in (3,4,5) and any(not(0<=p[0]+a<64 and 0<=p[1]+b<64) or B[p[0]+a,p[1]+b]==0 for a,b in ((1,0),(-1,0),(0,1),(0,-1)))]
print('open randen:',op)
