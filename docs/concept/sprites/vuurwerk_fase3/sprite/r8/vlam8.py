# r8 punt 1: vlamtong bovenop de kop (x14-16, y2-4). In r7 een blok van 3x3 (de 115%-reductie met drempel 0,35). Op het model
# (vervormd naar r5-coordinaten, 4x4 deelpunten per spritepixel gemeten) is de tong ±2,3 px breed met de punt boven bij x 15:
# (14,2) heeft alleen de onderste helft gevuld, (16,2) en (16,3) minder dan de helft. Die 3 pixels worden leeg; de rest
# blijft de r7-pixel (kleuren uit de r5-reductie). Resultaat: punt (15,2), daaronder 2 breed, onderaan 3 breed.
WEG=[(14,2),(16,2),(16,3)]
def vlam(a):
    a=a.copy()
    for x,y in WEG: a[y,x]=0
    return a
