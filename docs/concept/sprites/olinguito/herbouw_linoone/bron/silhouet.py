# Silhouet-schets op Galar-Linoone (Linoone-coordinaten). Rijen: y -> spans (x0,x1) incl.
import sys
from PIL import Image
D='/home/user/projectgrounded/docs/concept/sprites/olinguito/'
S=sys.argv[1] if len(sys.argv)>1 else '/tmp/sil.png'
parts={
'oor_ver':{22:[(8,9)],23:[(7,10)],24:[(7,10)]},
'oor_nabij':{20:[(16,19)],21:[(15,20)],22:[(15,20)],23:[(15,20)],24:[(15,20)]},
'kop':{25:[(6,21)],26:[(5,22)],27:[(4,22)],28:[(4,23)],29:[(3,23)],30:[(3,23)],31:[(2,23)],
       32:[(1,23)],33:[(1,23)],34:[(1,23)],35:[(2,22)],36:[(3,22)],37:[(5,21)],38:[(7,20)]},
'romp':{26:[(28,42)],27:[(23,44)],28:[(22,46)],29:[(22,47)],30:[(22,47)],31:[(22,48)],32:[(22,48)],33:[(22,48)],
        34:[(22,48)],35:[(22,48)],36:[(21,47)],37:[(21,47)],38:[(21,46)],39:[(24,34),(36,45)]},
'voor_nabij':{38:[(12,20)],39:[(12,20)],40:[(12,20)],41:[(12,19)],42:[(11,18)],43:[(11,18)],44:[(10,17)],45:[(10,17)],
              46:[(9,17)],47:[(9,17)],48:[(9,16)]},
'klauw_nabij':{47:[(7,8)],48:[(6,8)],49:[(6,9),(10,11)],50:[(6,7),(9,11)],51:[(9,10)]},
'voor_ver':{39:[(19,25)],40:[(19,25)],41:[(19,25)],42:[(19,24)],43:[(19,24)],44:[(19,24)],45:[(18,24)],46:[(18,24)]},
'klauw_ver':{46:[(16,17)],47:[(15,17),(18,19)]},
'achter_ver':{39:[(26,33)],40:[(26,33)],41:[(26,32)],42:[(25,32)],43:[(24,31)],44:[(24,31)]},
'achter_nabij':{39:[(35,46)],40:[(36,45)],41:[(37,45)],42:[(38,45)],43:[(38,44)],44:[(37,44)],45:[(36,44)],46:[(35,44)],47:[(35,44)]},
'staart':{28:[(45,49)],29:[(46,51)],30:[(48,52)],31:[(49,53)],32:[(49,54)],33:[(50,54)],34:[(50,55)],35:[(50,55)],
          36:[(50,55)],37:[(50,55)],38:[(50,55)],39:[(50,55)],40:[(50,55)],41:[(50,55)],42:[(49,55)],43:[(47,49),(50,55)],
          44:[(47,55)],45:[(47,55)],46:[(47,54)],47:[(48,53)],48:[(49,52)]},
}
cols={'oor_ver':(90,60,50),'oor_nabij':(150,110,80),'kop':(150,110,80),'romp':(120,85,65),'voor_nabij':(150,110,80),
'klauw_nabij':(220,220,220),'voor_ver':(80,55,45),'klauw_ver':(180,180,180),'achter_ver':(80,55,45),'achter_nabij':(150,110,80),'staart':(110,75,55)}
order=['staart','achter_ver','voor_ver','klauw_ver','romp','achter_nabij','oor_ver','oor_nabij','kop','voor_nabij','klauw_nabij']
im=Image.new('RGBA',(64,64),(0,0,0,0)); px=im.load()
for k in order:
    for y,sp in parts[k].items():
        for a,b in sp:
            for x in range(a,b+1): px[x,y]=cols[k]+(255,)
n=sum(1 for x in range(64) for y in range(64) if px[x,y][3])
print('px',n)
base=Image.open(D+'referenties/galar_linoone_front.png').convert('RGBA')
z=8
out=Image.new('RGBA',(64*z*2+8,64*z),(255,255,255,255))
b=base.resize((512,512),Image.NEAREST); out.paste(b,(0,0),b)
g=base.copy(); g.putalpha(70); g=g.resize((512,512),Image.NEAREST)
out.paste(Image.new('RGBA',(512,512),(240,240,240,255)),(520,0))
out.paste(g,(520,0),g); s=im.resize((512,512),Image.NEAREST)
sa=s.copy(); sa.putalpha(s.getchannel('A').point(lambda v:200 if v else 0)); out.paste(sa,(520,0),sa)
out.crop((0,120,1032,440)).save(S)
im.save(S.replace('.png','_1x.png'))
