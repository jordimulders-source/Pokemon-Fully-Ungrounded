from kijk import *
from optA import G
import copy
# als C (+2), maar zachte scheiding (middentoon) waar de vingers elkaar raken, Drowzee-palm (licht boven, schaduw onder)
D = copy.deepcopy(G)
D[49] = [(7, 'oo'), (12, 'oWlo'), (17, 'oWWo')]
D[50] = [(6, 'oWWo'), (12, 'oWlo'), (17, 'oWlo')]
D[52] = [(7, 'oWlo'), (12, 'ollmmllooo')]
D[53] = [(8, 'ollmmllmllmoWlk')]
D[54] = [(9, 'ollmllmllmllk')]
D[55] = [(4, 'ooo'), (8, 'oWlllWllllllmk')]
D[56] = [(3, 'oWWlomWWWllllllllmk')]
D[57] = [(3, 'olllWWmllllllmmmmk')]
D[58] = [(4, 'oolWWlmllmmmmmmmk')]
D[59] = [(6, 'olllmmmmmmmmmmk')]
D[60] = [(7, 'ommmmmmmmmmmoo')]
if __name__ == '__main__':
    a = bouw(ras(D), groot=True); controle(a, 'B', groot=True); kijk(a, 'B'); save(a, 'optie_B.png')
