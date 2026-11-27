# Onderdelen Hexpress (27 nov): kleine geest (rook boven de schoorsteen), wolken achter, twee geestwielen.
import numpy as np
from PIL import Image
B = '../../'
im = Image.open(B+'spooktrein_fase3/af/spooktrein.png'); a = np.array(im); pal = im.getpalette()
yy, xx = np.mgrid[0:64, 0:64]
GROEN = np.isin(a, [2, 3, 4, 5, 6, 13])
GEEST = (a > 0) & (yy <= 13)                                   # kleine geest uit de schoorsteen
WOLK = GROEN & (((yy >= 17) & (yy <= 28) & (xx >= 28)) | ((yy >= 17) & (yy <= 40) & (xx >= 46)) | ((yy > 40) & (yy <= 47) & (xx >= 56)))
WIEL1 = GROEN & ((xx-33)**2 + (yy-54.5)**2 <= 9.5**2) & (yy >= 45)
WIEL2 = GROEN & ((xx-48)**2 + (yy-49)**2 <= 8**2) & ~WIEL1 & ~WOLK
if __name__ == '__main__':
    rgb = np.array(im.convert('RGB')); rgb[a == 0] = 255
    for m, c in ((GEEST, (255, 0, 0)), (WOLK, (0, 0, 255)), (WIEL1, (255, 160, 0)), (WIEL2, (200, 0, 200))):
        rgb[m] = (rgb[m]*0.4 + np.array(c)*0.6).astype(np.uint8)
    Image.fromarray(rgb).resize((512, 512), Image.NEAREST).save('/tmp/claude-0/hexmask.png')
