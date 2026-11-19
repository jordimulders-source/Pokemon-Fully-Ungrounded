# r3 = r2 + vleugelpixels die aan de staart grenzen (zone x45-52, y10-23) → index 11 (vleugelschaduw), zodat de vleugel een eigen rand krijgt (Jordi: "scheiding tussen de rechtervleugel en de staart, qua belijning/schaduw/kleur").
from PIL import Image
im=Image.open('r2/frame2.png'); px=im.load(); W=[12,13,14,4]; T=[1,2,5,6,7]; ch=[]
for y in range(10,24):
  for x in range(45,53):
    if px[x,y] in W and any(px[x+dx,y+dy] in T for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): ch.append((x,y,px[x,y]))
for x,y,_ in ch: px[x,y]=11
im.save('r3/frame2.png',transparency=0); print(len(ch),ch)
