from PIL import Image, ImageDraw; import numpy as np
S='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
im=Image.open(S+'sprite_r9/sprite.png'); a=np.array(im)
M=[ # schoorsteen
((12,15),12,11),((13,15),12,11),((11,16),12,11),((13,16),10,7),
((13,17),7,10),((21,17),9,12),
((13,19),12,11),((15,19),10,7),((16,19),11,10),((17,19),11,10),((18,19),9,1),
((14,20),1,11),((15,20),8,7),((16,20),8,10),((17,20),8,10),((18,20),8,1),
((15,21),1,11),((16,21),8,10),((17,21),8,10),((18,21),8,1),
# kop links rond
((0,30),9,0),((1,30),8,9),((0,31),9,0),((1,31),8,9),((0,32),9,0),((1,32),8,9),
((0,40),9,0),((0,41),9,0),((0,42),9,0),
((0,43),1,0),((1,43),8,1),((0,45),1,0),((0,46),1,0),((0,47),1,0),((1,47),9,1),
]
G={2,3,4,5,6,13}
for (x,y),o,n in M:
    assert a[y,x]==o,(x,y,a[y,x],o); assert o not in G
    a[y,x]=n
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save(S+'sprite_r9/keuring_voorstel.png',transparency=0)
print(len(M))
