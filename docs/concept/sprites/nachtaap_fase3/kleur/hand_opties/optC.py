from kijk import *
# groter (+2 rijen omlaag), zachte waaier: wijs naar links, ring en pink naar rechts, middel recht
G = {
 47: [(13, 'oo')],
 48: [(12, 'oWWo'), (18, 'oo')],
 49: [(7, 'oo'), (12, 'oWlo'), (17, 'oWWo')],
 50: [(6, 'oWWo'), (12, 'ollo'), (17, 'oWlo')],
 51: [(6, 'oWlo'), (12, 'ollmollooo')],
 52: [(7, 'ollo'), (12, 'ollmolloWlk')],
 53: [(8, 'ollmollolloWlk')],
 54: [(9, 'ollollmllollk')],
 55: [(5, 'oo'), (8, 'olllmlllllmlmk')],
 56: [(4, 'oWlomlWWlllllllmmk')],
 57: [(4, 'olWWlmlWlllllllmk')],
 58: [(5, 'olWllmlllllllmmk')],
 59: [(6, 'omlllmllllmmmmk')],
 60: [(7, 'ollllmlmmmmmoo')],
 61: [(8, 'kkkkkkmmmoo44k')],
 62: [(14, 'kkkk343k')],
 63: [(18, 'kkk')],
}
if __name__ == '__main__':
    for y, l in G.items():
        for x, s in l: assert x - 1 + len(s) <= 24, (y, x, s)
    a = bouw(ras(G), groot=True); controle(a, 'C', groot=True); kijk(a, 'C')
