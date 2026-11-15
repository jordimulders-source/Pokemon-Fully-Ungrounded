# c5: keuring c4 MOET 2 (kruinlijnen los van de oogbogen) en 3 (dijspiraal als voluut), toegepast door Claude.
# MOET 1 (oogbogen) NIET: Jordi keurde de lijnen om de ogen goed ("die lijnen om de ogen zijn prima") -> bevroren.
from PIL import Image
E={(15,24):5,(17,24):5,(18,23):5,(17,21):5,(16,23):5,
   (48,52):3,(48,53):3,(48,54):3,(48,55):3,(48,56):3,(40,49):2,(39,48):2}
for v in ['A','A_grijs']:
    im=Image.open(f'c4/welp_c4_{v}.png'); px=im.load()
    for k,c in E.items():
        if v=='A': print(k,px[k],'->',c)
        px[k]=c
    n='c5/welp_c5'+('' if v=='A' else '_grijs')
    im.save(n+'.png',transparency=0)
    Image.open(n+'.png').convert('RGBA').resize((512,512),Image.NEAREST).save(n+'_8x.png')
