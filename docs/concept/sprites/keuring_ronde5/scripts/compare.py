import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from sheet import *
O = sys.argv[1]


def g(n):
    return (n.capitalize() + ' (G3)', G + n + '/anim_front_gba.png', 0)


def ds(n):
    return (n.capitalize() + ' (DS)', G + n + '/anim_front.png', 0)


def c(name, rd, sub='', fr=0, lab=None):
    return (lab or (name + ' ' + rd), S + name + '/' + rd + '/' + sub + 'anim_front.png', fr)


sheet([[c('alpaca', 'ronde4'), c('alpaca', 'ronde5'), g('mareep'), g('ponyta'), g('electrike')],
       [g('torchic'), g('growlithe'), g('eevee'), g('skitty'), g('chikorita')]], O + 'v_alpaca.png')
sheet([[c('olinguito', 'ronde4'), c('olinguito', 'ronde5'), g('zigzagoon'), g('sentret'), g('teddiursa')],
       [g('poochyena'), g('sneasel'), g('totodile'), g('cyndaquil'), g('treecko')]], O + 'v_olinguito.png')
sheet([[c('nachtaap', 'ronde3'), c('nachtaap', 'ronde4'), c('nachtaap', 'ronde5'), g('aipom'), g('abra')],
       [g('natu'), g('spoink'), g('smoochum'), ds('chimchar'), ds('espurr')]], O + 'v_nachtaap.png')
sheet([[c('cuyby', 'ronde1', lab='cuyby A'), c('cuyby', 'ronde1', 'B/', lab='cuyby B'), g('rattata'), g('sentret'), g('zigzagoon')],
       [g('skitty'), g('whismur'), g('teddiursa'), ds('pachirisu'), ds('bidoof')]], O + 'v_cuyby.png')
sheet([[c('alpaca', 'ronde5'), c('olinguito', 'ronde5'), c('nachtaap', 'ronde5'), c('cuyby', 'ronde1', lab='cuyby A')],
       [g('treecko'), g('torchic'), g('mudkip'), g('cyndaquil')],
       [g('chikorita'), g('totodile'), g('bulbasaur'), g('charmander')]], O + 'v_overzicht.png')
