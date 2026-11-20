# gedeelde geometrie: blok (r,c) van de 3x-reductie -> spritepixel (OX+c, OY+r); modelcoord per spritepixel
OX,OY=7,3; PY,PX=7,32; P=5.12
def model_box(sx0,sy0,sx1,sy1):
    f=lambda s,o,ph:((s-o)*3+ph)*P-0.12
    return f(sx0,OX,PX),f(sy0,OY,PY),f(sx1,OX,PX),f(sy1,OY,PY)
