# r4: gezichtslijnen (neus, mond, wangen) als lijnen op de modelposities (Claude, per pixel); bouwt vanaf r3.
from PIL import Image; import numpy as np
im=Image.open('../r3/pachamama_r3.png'); a=np.array(im)
G={17:'234432222',     # x24..: brauwen donker, voorhoofd licht
18:'114321112',        # oogleden
19:'6142361632',       # ogen wit|pupil, neuszijde 2
20:'3442334332',       # neuszijde x27
21:'3311334141',       # neusonderkant x26-27, wanglijn rechts x31
22:'1311131332',       # mond x26-28, wanglijnen x24 en x30
23:'3144313332',       # mondhoek/wang x25 en x29
24:'3133313322',
25:'2313313322',
26:'233113322'}        # lijnen komen samen bij de kin
for y,s in G.items():
    for i,c in enumerate(s): a[y,24+i]=int(c,16)
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save('pachamama_r4.png',transparency=0)
