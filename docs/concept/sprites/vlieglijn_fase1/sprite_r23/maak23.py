# r23 = r21 + ALLEEN de lijn tussen de vleugels (Jordi: "de lijn tussen de vleugel in is het enige wat je moet veranderen";
# eerder: "misschien lijn met lichte kleur"). Pad van de lijn uit r22 (wortel -> rij 21), verder niets gewijzigd.
# Varianten: lijn in index 12 (lichtblauwgrijs, 116,146,162) en index 9 (132,148,162); wit (10) valt weg tegen de witte vleugel.
from PIL import Image
PAD=[(x,21) for x in range(40,47)]+[(x,22) for x in range(37,40)]+[(x,23) for x in range(34,37)]+[(x,24) for x in range(31,34)]+[(x,25) for x in range(27,32)]
r21=Image.open('keuring_r20/vlieg_r21.png'); a=r21.load()
for idx,naam in ((12,'L12'),(9,'L9')):
    out=r21.copy(); o=out.load(); ch=[]
    for x,y in PAD:
        if a[x,y] in (10,11,12,9) and a[x,y]!=idx: o[x,y]=idx; ch.append((x,y,a[x,y]))
    out.save(f'sprite_r23/vlieg_r23_{naam}.png',transparency=0)
    i=Image.open(f'sprite_r23/vlieg_r23_{naam}.png').convert('RGBA'); bg=Image.new('RGBA',i.size,(255,255,255,255)); bg.alpha_composite(i)
    bg.convert('RGB').resize((512,512),Image.NEAREST).save(f'sprite_r23/vlieg_r23_{naam}_8x.png')
    bg.convert('RGB').crop((24,14,58,30)).resize((34*14,16*14),Image.NEAREST).save(f'sprite_r23/vleugels_{naam}_14x.png')
    print(naam,len(ch),ch)
