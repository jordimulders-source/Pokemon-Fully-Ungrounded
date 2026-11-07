# Ronde 7c: alleen de staartwortel van ronde 7 optie B. Geen plooi/kraag meer; de lichtkant van de staart
# loopt als band schuin door op de heup en vervaagt, de schaduwkant loopt door in de heupschaduw.
from PIL import Image
im=Image.open('../ronde7_opties/optie_B.png'); a=im.load()
RIJ={  # x42..47
 35:"332454",
 36:"344553",
 37:"445443",
 38:"444433",
 39:"3433",   # x42-45 (x46-47 = omlijning, blijft)
}
for y,s in RIJ.items():
    for i,c in enumerate(s):
        x=42+i; assert 1<=a[x,y]<=5; a[x,y]=int(c)
im.save('nachtaap_fase3.png')
