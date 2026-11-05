import numpy as np
from PIL import Image
im = Image.open('B1/wit.png').convert('RGBA').resize((64, 64), Image.BOX)
a = np.asarray(im).astype(float); L = a[..., :3].mean(-1); m = a[..., 3] > 100
sil = np.asarray(Image.open('../silhouet/silhouet_b1_1x.png'))[..., 3] > 0
q = np.digitize(L, np.percentile(L[m], [20, 50, 80]))     # 0 donker .. 3 licht
tonen = np.array([(60, 60, 70), (120, 120, 130), (185, 185, 190), (240, 240, 240)])
out = np.zeros((64, 64, 4), np.uint8); out[sil, :3] = tonen[q[sil]]; out[sil, 3] = 255
Image.fromarray(out).save('B1/toonkaart_1x.png'); Image.fromarray(out).resize((512, 512), Image.NEAREST).save('B1/toonkaart_8x.png')
