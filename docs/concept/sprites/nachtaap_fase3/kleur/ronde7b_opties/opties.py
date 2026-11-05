# Ronde 7b: vanaf ronde7 optie B. Massa's borstkas / buik / bekken: kern bovenaan, schaduwband (3) van 2 px
# eronder, gebogen; de banden komen samen in een zachte Y bij de taille. Met de hand gezet als pixeltabel.
from PIL import Image
B=Image.open('../ronde7_opties/optie_B.png')
def zet(im,tab):
    a=im.load()
    for (x,y),v in tab.items():
        assert a[x,y]!=0 and 1<=a[x,y]<=5 and 1<=v<=5,(x,y)
        a[x,y]=v
    return im
def T(v,*pts): return {p:v for p in pts}
M={}
# borstkas: schaduwband onder de kern, 2 px, loopt schuin op naar de taille
M.update(T(3,(31,37),(32,37),(29,38),(30,38),(31,38),(27,39),(28,39),(29,39),(27,40),(28,40)))
# taille (Y waar borst, buik en heup samenkomen)
M.update(T(3,(33,37)))
# bekken/heup: schaduwband linksonder, gaat over in de liesplooi
M.update(T(3,(33,38),(34,38),(34,39),(35,39),(35,40),(36,40),(36,41)))
# heup: schaduwkant rechts breder, gebogen
M.update(T(3,(41,36),(40,37),(41,37),(40,38),(41,38),(39,39),(40,39),(41,39),(39,40),(40,40)))
# heupkern iets ronder
M.update(T(5,(36,36)))
S=dict(M)
# sterk: kernen groter (5), schaduwbanden een pixel breder aan de onderkant van elke massa; geen losse 2-stippen
S.update(T(5,(28,37),(29,37),(28,38),(37,36),(36,37)))          # borstkern en heupkern ronder
S.update(T(3,(32,38),(33,39),(34,40),(35,41)))                  # heupband 2 px breed
S.update(T(3,(32,44),(33,44),(34,44),(33,43)))                  # buik: onderkant donkerder
S.update(T(3,(39,37),(39,38),(38,39),(38,40),(39,41)))          # heup rechtsonder
S.update(T(2,(36,43)))                                          # liesplooi diepst
OPT={'matig':M,'sterk':S}
if __name__=='__main__':
    for k,t in OPT.items(): zet(B.copy(),t).save('optie_%s.png'%k)
