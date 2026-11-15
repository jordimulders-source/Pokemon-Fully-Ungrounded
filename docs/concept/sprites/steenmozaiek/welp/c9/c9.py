# c9: keuring c7 (MOET 1-3 + MAG (31,31), kinplooi) toegepast door Claude op de c8-cirkelvarianten
from PIL import Image
E={}
for y in range(49,57): E[(36,y)]=3
for y in range(51,55): E[(37,y)]=2
for p in [(35,47),(36,47),(35,48),(36,48),(37,48)]: E[p]=3
E[(44,42)]=3; E[(53,55)]=3
E[(31,31)]=4; E[(26,34)]=2; E[(27,34)]=2
for v in ['1','2','3']:
  for t in ['','_grijs']:
    im=Image.open(f'c8/welp_c8_{v}{t}.png'); px=im.load()
    if v=='1' and t=='':
        for k,c in E.items(): print(k,px[k],'->',c)
    for k,c in E.items(): px[k]=c
    n=f'c9/welp_c9_{v}{t}'; im.save(n+'.png',transparency=0)
    Image.open(n+'.png').convert('RGBA').resize((512,512),Image.NEAREST).save(n+'_8x.png')
