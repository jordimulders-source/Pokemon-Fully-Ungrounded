# Ronde 7b: vanaf ronde7 optie B; massa's borstkas / buik / bekken met kern + gebogen schaduwrand.
# Pixeltabel (x,y):tint, met de hand gezet; alleen vachttinten 1-5, omtrek gelijk.
from PIL import Image
B=Image.open('../ronde7_opties/optie_B.png')
def zet(im,tab):
    a=im.load()
    for (x,y),v in tab.items():
        assert a[x,y]!=0 and 1<=a[x,y]<=5 and 1<=v<=5,(x,y)
        a[x,y]=v
    return im
M={}
# borstkas: schaduwboog onder de kern (doodlopend: raakt armplooi en heupboog niet)
for p in [(28,39),(29,39),(30,38),(31,38),(32,37)]: M[p]=3
# bekken/heup: schaduwboog linksonder, loopt over in de liesplooi
for p in [(33,39),(34,40),(35,41),(36,41)]: M[p]=3
M[(37,41)]=4                      # heupbol niet meer los
# heup: schaduwrand rechtsonder iets ronder
for p in [(40,39),(40,40),(39,40)]: M[p]=3
# buik: kern bovenaan (4) blijft, schaduw onderaan ronder
for p in [(32,44),(32,43)]: M[p]=3
S=dict(M)
# sterk: dubbele bogen, kern 5 in buik en borst, diepere lies
for p in [(28,40),(29,40),(30,39),(31,39),(33,38)]: S[p]=3
for p in [(34,41),(35,42)]: S[p]=3
for p in [(36,42),(36,43)]: S[p]=2
for p in [(30,41),(31,41),(31,40),(32,41)]: S[p]=5   # buikkern
for p in [(28,37),(29,36)]: S[p]=5                    # borstkern ronder
for p in [(41,38),(39,41),(40,41)]: S[p]=3
OPT={'matig':M,'sterk':S}
if __name__=='__main__':
    for k,t in OPT.items(): zet(B.copy(),t).save('optie_%s.png'%k)
