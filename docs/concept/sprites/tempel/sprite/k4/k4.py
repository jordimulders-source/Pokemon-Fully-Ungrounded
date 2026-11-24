# Kleurronde k4 tempel: vanaf k3 (= af). Alleen tinten/voegen in de zijvlakken, bergwand, dakplaten.
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','k1'))
from gereedschap import *
HIER4=os.path.dirname(os.path.abspath(__file__))
a0,pal0=laad()
a=a0.copy(); pal=list(pal0)
E,F=14,15
MOS=(8,9,13)
def rij(y,x0,s):
    """zet tekst s vanaf (x0,y); '_' = laten staan"""
    for i,c in enumerate(s):
        if c=='_': continue
        a[y,x0+i]='0123456789ABCDEF'.index(c)
exec(open(os.path.join(HIER4,'zones.py')).read())
bewaar(a,pal,os.path.join(HIER4,'tempel.png'))
