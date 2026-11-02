"""Poppetje (alpha) over het goedgekeurde silhouet v3A, op dezelfde bbox-hoogte. Groen = beide, rood = alleen silhouet,
blauw = alleen poppetje. Meet overlap (IoU)."""
import sys, numpy as np
from PIL import Image
import pop3d_kuiken as K
def masker(m, yaw, pitch=0):
    img, a = K.view(m, yaw, pitch)
    A = Image.fromarray((a * 255).astype(np.uint8))
    return A
def vergelijk(m, yaw, pitch=0, uit=None):
    S = np.asarray(Image.open('../silhouet/silhouet_v3a_hand_1x.png').convert('L')) < 128
    ys, xs = np.nonzero(S); sb = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    A = masker(m, yaw, pitch); A = A.crop(A.getbbox())
    h = sb[3] - sb[1]; w = round(A.width * h / A.height)
    a = np.asarray(A.resize((w, h), Image.LANCZOS)) >= 128
    P = np.zeros((64, 64), bool)
    x0 = sb[0] + ((sb[2] - sb[0]) - w) // 2
    x0 = max(0, min(64 - w, x0)); P[sb[1]:sb[3], x0:x0 + w] = a
    iou = (P & S).sum() / (P | S).sum()
    if uit:
        rgb = np.full((64, 64, 3), 255, np.uint8)
        rgb[P & S] = (90, 170, 90); rgb[S & ~P] = (220, 60, 60); rgb[P & ~S] = (60, 90, 220)
        Image.fromarray(rgb).resize((256, 256), Image.NEAREST).save(uit)
    return iou, P.sum(), S.sum()
if __name__ == '__main__':
    K.set_palet('fluweel (als eindvorm)')
    print(vergelijk(K.kuiken(hs=1.05), K.YAW, 8, 'overlay_ronde1.png'))
