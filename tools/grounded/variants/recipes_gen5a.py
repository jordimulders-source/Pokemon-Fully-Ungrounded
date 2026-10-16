"""Kleurvarianten Unova, eerste helft (Victini t/m Deerling/Sawsbuck).

Formaat: zie recipes.py. Regionale vormen (Hisui/Galar) hebben eigen indexen per map.
"""

ALBINO = {'l': 1.0}
DARK = {'l': 1.3}

LINES = {
    'victini': {
        # Psychic/Fire, de overwinningspokémon: V-oren, lijf, ogen, mond
        'species': {
            'victini': {'ears': [3, 2, 1], 'body': [5, 7, 6, 15], 'eyes': [9, 12], 'mouth': [13, 14]},
        },
        'variants': [
            {'naam': 'Laurierkrans (olijfgroene V, gouden ogen)', 'ears': '#4a8a38', 'body': '#e0d0a0',
             'eyes': '#c89020', 'mouth': '#d87070'},
            {'naam': 'Ferrari (raceroode V, gele motorkap)', 'ears': '#d81818', 'body': '#e8c840',
             'eyes': '#2c2c34', 'mouth': '#c03030'},
            {'naam': 'Mewtwo-kleuren (lila lijf, paarse V)', 'ears': '#7a40b0', 'body': '#c8bcd8',
             'eyes': '#a030c0', 'mouth': '#b878c8'},
            {'naam': 'Chocolade-paasei (melkchocolade, roze strik-V)', 'ears': '#e878a8', 'body': '#9a6840',
             'eyes': '#f0e0c0', 'mouth': '#e08090'},
            {'naam': 'Blauw vuur met zwart pak (V for Victory-poster)', 'ears': '#2858d8', 'body': ('#4a4a54', DARK),
             'eyes': '#f0d030', 'mouth': '#e04050'},
            {'naam': 'Olympisch goud (gouden V, robijnen ogen)', 'ears': ('#e0b030', {'h': 0}), 'body': '#f4ecd0',
             'eyes': '#d02040', 'mouth': '#e07080'},
        ],
    },
    'snivy': {
        # grasslangen: lijf, crème buik/gezicht, gouden kraag, ogen; Serperior ook de witte hals en lichte onderkant
        'species': {
            'snivy': {'body': [2, 13, 1], 'cream': [5, 7, 6], 'collar': [4, 8], 'eyes': [9, 12, 10]},
            'servine': {'body': [5, 2, 1], 'cream': [6, 9, 12], 'collar': [3, 13, 4], 'eyes': [11, 10]},
            'serperior': {'body': [6, 5, 14], 'belly': [11, 9], 'cream': [8, 10, 4], 'collar': [2, 3, 1],
                          'eyes': [13, 12]},
        },
        'variants': [
            {'naam': 'Esdoornblad (herfstrood, bruine kraag)', 'body': '#c04428', 'belly': '#e89870', 'cream': '#f0dcb0',
             'collar': '#7a4a22', 'eyes': '#3a8a30'},
            {'naam': 'Kersenbloesem (roze blad, kersenkraag)', 'body': '#e48cb0', 'belly': '#f4c8d8', 'cream': '#fcf0f0',
             'collar': '#b83868', 'eyes': '#3a7040'},
            {'naam': 'Byzantijns keizerpurper (zilveren kraag)', 'body': '#6a3090', 'belly': '#a880c0', 'cream': '#e8dcf0',
             'collar': '#d0d4e0', 'eyes': '#e0b030'},
            {'naam': 'Albino (wit, roze kraag, rode ogen)', 'body': ('#dcdcd0', ALBINO), 'serperior:body': ('#c4c4b8', {'l': 1.6}), 'belly': ('#ecece4', ALBINO),
             'cream': ('#f8f0c8', ALBINO), 'collar': '#f0a0b0', 'eyes': '#e02030'},
            {'naam': 'Nachtslang (zwart, turquoise kraag)', 'body': ('#34383c', DARK), 'belly': ('#585e64', DARK),
             'cream': '#a8b0b8', 'collar': '#30c8c0', 'eyes': '#e03030'},
            {'naam': 'Gouden keizerin (goud, robijnen kraag)', 'body': ('#c89828', {'h': 0}), 'belly': '#e8d080',
             'cream': '#fcf4dc', 'collar': '#c02040', 'eyes': '#3080e0'},
        ],
    },
    'tepig': {
        # vuurvarkens: lijf, donkere kop/rug (Emboar: zwart lijf), snuit, vuur (neus/staartbol, Emboars baard),
        # gordel (Pignite/Emboar), rook (Pignite)
        'species': {
            'tepig': {'body': [9, 5, 4], 'dark': [2, 3], 'snout': [10, 8], 'fire': [7, 6, 13]},
            'pignite': {'body': [6, 5, 7], 'dark': [12, 2], 'belt': [8, 9, 10], 'fire': [11], 'smoke': [13, 14]},
            'emboar': {'dark': [4, 2], 'fire': [3, 1, 13, 6, 7, 5, 9], 'belt': [11, 15, 14], 'cuffs': [12, 10]},
        },
        'variants': [
            {'naam': 'Wild zwijn (grijsbruin, wit vuur)', 'body': '#8a7868', 'dark': ('#4a3c34', DARK), 'snout': '#5a4a40',
             'fire': ('#f0ecd8', {'l': 0.7}), 'belt': '#c8b088', 'smoke': '#a8a8b0', 'cuffs': '#e0d8c8',
             'emboar:dark': ('#5a4a40', DARK)},
            {'naam': 'Pata negra (zwart Iberisch varken, groen kopervuur)', 'body': ('#5a4c50', DARK), 'dark': ('#2c2428', DARK),
             'snout': '#d8a890', 'fire': '#40d060', 'belt': '#c8ccd8', 'smoke': '#406848', 'cuffs': '#c8ccd8'},
            {'naam': 'Peppa Pig (roze, rood jurkje, roze vuur)', 'body': '#f090b0', 'dark': '#d03040', 'snout': '#f8c0d0',
             'fire': '#f860a0', 'belt': '#f8e060', 'smoke': '#f0c8d8', 'cuffs': '#f8f0f0'},
            {'naam': 'Hampshire-varken (zwart met witte band, rood vuur)', 'body': ('#38343a', DARK), 'dark': '#e8e4e0',
             'snout': '#e8b8b0', 'fire': '#e03030', 'belt': ('#38343a', DARK), 'smoke': '#d8d8d8', 'cuffs': '#e03030',
             'emboar:dark': ('#d8d4d0', {'l': 1.2})},
            {'naam': 'Chocoladevarken (paars kaliumvuur)', 'body': '#8a5634', 'dark': ('#3a2418', DARK), 'snout': '#d8a878',
             'fire': '#a050f0', 'belt': '#e0c8a0', 'smoke': '#8060a0', 'cuffs': '#e0c8a0',
             'emboar:dark': ('#4a3020', DARK)},
            {'naam': 'Gullinbursti (Freyrs gouden everzwijn)', 'body': ('#d8a828', {'h': 0}), 'dark': ('#5a3a18', DARK),
             'snout': '#f0d890', 'fire': ('#f8f0b0', {'l': 0.7}), 'belt': '#c02830', 'smoke': '#e8d8a0', 'cuffs': '#f0e0a0',
             'emboar:dark': ('#b88a20', {'h': 0})},
        ],
    },
    'oshawott': {
        # samoeraiotters: lijf, donkerblauw (oren/voeten/staart, Dewotts rok, Hisui-mantel), witte kop/snor,
        # schelp (Samurotts harnas, Hisui: rood harnas), buik (Samurott)
        'species': {
            'oshawott': {'body': [13, 12, 11], 'navy': [5, 4, 6], 'head': [3, 10, 2, 1], 'shell': [15, 9, 8]},
            'dewott': {'body': [4, 3, 1], 'navy': [10, 11], 'head': [5, 9, 6], 'shell': [12, 14, 13],
                       '_base': {'head': 6}},
            'samurott': {'body': [10, 9, 14], 'shell': [5, 3, 2, 4], 'head': [7, 12, 6], 'belly': [8, 13]},
            'samurott/hisui': {'body': [9, 13], 'navy': [14, 7, 11], 'shell': [2, 5, 10], 'head': [4, 12, 3],
                               'belly': [1, 8]},
        },
        'variants': [
            {'naam': 'Akazonae (rood harnas van Ii Naomasa, zwarte lakschelp)', 'body': '#c03030', 'navy': ('#3a2a2a', DARK),
             'head': '#f0ece4', 'shell': ('#34343c', DARK), 'belly': '#d8a8a0'},
            {'naam': 'Ninja (zwart, zilveren schelp)', 'body': ('#40404c', DARK), 'navy': ('#24242c', DARK),
             'head': '#c8c8d4', 'shell': '#d0d4e0', 'belly': '#686878'},
            {'naam': 'Kappa (groene watergeest, schildpadschelp)', 'body': '#4a9a40', 'navy': '#2c5a30',
             'head': '#e8f0c0', 'shell': '#a07040', 'belly': '#c8d890'},
            {'naam': 'Sakura (roze, witte schelp)', 'body': '#f0a0c0', 'navy': '#b05080', 'head': '#fff4f8',
             'shell': '#f4f0f0', 'belly': '#f8d8e4'},
            {'naam': 'Shogun (keizerlijk paars met goud)', 'body': '#6040a0', 'navy': '#2c2050', 'head': '#e8e0f0',
             'shell': ('#f0c030', {'h': 0}), 'belly': '#a090c0'},
            {'naam': 'Kinkaku-ji (het Gouden Paviljoen, rode schelp)', 'body': ('#d8a830', {'h': 0}), 'navy': '#5a3a10',
             'head': '#f8f0d0', 'shell': '#c02830', 'belly': '#f0d890'},
        ],
    },
    'patrat': {
        # uitkijkposten: lijf, strepen/staart (Watchog: gele strepen), buik, ogen, wit (Watchogs staartpunt/voeten)
        'species': {
            'patrat': {'body': [1, 2], 'stripe': [3, 4, 15, 6], 'belly': [13, 12, 10], 'eyes': [7, 8, 9]},
            'watchog': {'body': [14, 5, 4], 'stripe': [10, 15], 'belly': [12, 13, 11], 'eyes': [9, 8], 'white': [3, 6, 2]},
        },
        'variants': [
            {'naam': 'Stokstaartje (zand, donkere strepen, amberogen)', 'body': '#b8a080', 'stripe': '#5a4838',
             'belly': '#ece0c4', 'eyes': '#e0a020'},
            {'naam': 'Grijze eekhoorn (roestbruine strepen)', 'body': '#8a8a92', 'stripe': '#c07840', 'belly': '#ecece8',
             'eyes': '#c03030'},
            {'naam': 'Zwitserse Garde (Vaticaan: blauw met geel, rode ogen)', 'body': '#2848a0', 'stripe': '#f0b020',
             'belly': '#f0e0c0', 'eyes': '#e03030', 'white': '#e83838'},
            {'naam': 'Albino (wit, roze strepen, rode ogen)', 'body': ('#d8d0c8', ALBINO), 'stripe': '#ecc4c0',
             'belly': ('#f8f4f0', ALBINO), 'eyes': '#e02030'},
            {'naam': 'Bewakingscamera (zwart, zilver, rood opnamelampje)', 'body': ('#3a3c48', DARK), 'stripe': '#d0d4e0',
             'belly': '#9ca0b0', 'eyes': '#ff3030', 'white': '#d0d4e0'},
            {'naam': 'Nachtzicht (groen nachtkijkerbeeld)', 'body': '#2a5a2a', 'stripe': '#68f068', 'belly': '#a0e0a0',
             'eyes': '#e0ff80', 'white': '#c8ffc8'},
        ],
    },
    'lillipup': {
        # honden: vacht, gezicht/baard, mantel (Herdier/Stoutland), ogen (Lillipup), wit (Stoutlands poten)
        'species': {
            'lillipup': {'body': [2, 1, 3, 14], 'face': [5, 7, 6], 'eyes': [9, 10, 12]},
            'herdier': {'body': [1, 2, 3], 'face': [5, 9, 8], 'cape': [7, 13, 6]},
            'stoutland': {'body': [1, 2, 4], 'face': [3, 11, 8], 'cape': [7, 6, 12, 14, 13, 15], 'white': [9, 10]},
        },
        'variants': [
            {'naam': 'Border collie (zwart-wit, blue-merle-mantel)', 'body': ('#38383e', DARK), 'face': '#f0eeea',
             'cape': '#8890a0', 'eyes': '#7a5030', 'white': '#f0f0f0'},
            {'naam': 'Bluey (blauwe heeler uit de tekenfilm)', 'body': '#5078c0', 'face': '#b0cce8', 'cape': '#283868',
             'eyes': '#3a2a20', 'white': '#e8d8a8'},
            {'naam': 'Samojeed (sneeuwwit, ijsblauwe mantel)', 'body': ('#dcd8d0', {'l': 1.4}), 'face': ('#f0ece4', {'l': 1.3}),
             'cape': '#80a8d0', 'eyes': '#2c2c34', 'white': '#fcfcfc'},
            {'naam': 'Wolf (grijs, gele ogen)', 'body': '#7a7a82', 'face': '#d8d4cc', 'cape': ('#3a3a44', DARK),
             'eyes': '#e8c030', 'white': '#c8c4bc'},
            {'naam': 'Clifford (de grote rode hond)', 'body': '#d02828', 'face': '#f07060', 'cape': '#3a68c8',
             'eyes': '#2c2c34', 'white': '#f8d8d0'},
            {'naam': 'Anubis (zwart en goud, lapis-mantel)', 'body': ('#2c2c34', DARK), 'face': ('#d8a828', {'h': 0}),
             'cape': '#2050a0', 'eyes': '#e8c030', 'white': '#d8a828'},
        ],
    },
    'purrloin': {
        # katten/dieven: vacht, roze masker, crème (Liepards poten), vlekken (Liepard), ogen
        'species': {
            'purrloin': {'body': [2, 11, 1], 'mask': [5, 4], 'cream': [6, 7, 12, 13], 'eyes': [9, 10]},
            'liepard': {'body': [3, 1, 2], 'spots': [9, 7, 8, 13], 'mask': [6, 5], 'eyes': [11, 14]},
        },
        'variants': [
            {'naam': 'Zwarte panter (vage rozetten, gouden ogen)', 'body': ('#383440', DARK), 'mask': '#7a5a70',
             'cream': '#6a6070', 'spots': '#5a5464', 'eyes': '#f0c030'},
            {'naam': 'Sneeuwluipaard (grijswit, zwarte rozetten)', 'body': '#c4c4c8', 'mask': '#e8b8c0',
             'cream': '#f4f4f4', 'spots': ('#3a3a40', DARK), 'eyes': '#60b0d0'},
            {'naam': 'Luipaard (goud, zwarte rozetten)', 'body': '#d8a038', 'mask': '#a05a30', 'cream': '#f0e4c8',
             'spots': ('#3a2a20', DARK), 'eyes': '#58b048'},
            {'naam': 'Cheshire Cat (roze met paarse strepen)', 'body': '#d870b0', 'mask': '#7a3080', 'cream': '#f8d0e8',
             'spots': '#7a3080', 'eyes': '#f0e040'},
            {'naam': 'Lupin III (rood jasje, gele das)', 'body': '#c03030', 'mask': '#f0c030', 'cream': '#e8d8b0',
             'spots': ('#2c2c34', DARK), 'eyes': '#30a050'},
            {'naam': 'Neon-dief (cyberpunk: teal met magenta)', 'body': '#2c7a80', 'mask': '#ff40b0', 'cream': '#c0f0f0',
             'spots': '#ff40b0', 'eyes': '#f0f040'},
        ],
    },
    'pansage': {
        # broccoli-aap: lijf/kuif, gezicht, wangen (Pansage), witte borstvacht (Simisage)
        'species': {
            'pansage': {'body': [4, 3, 1, 7], 'face': [5, 6, 12, 15], 'cheeks': [14, 13]},
            'simisage': {'body': [3, 4, 1, 10], 'face': [5, 6, 7, 13], 'fluff': [8, 12, 9, 11]},
        },
        'variants': [
            {'naam': 'Paarse broccoli', 'body': '#7a4a9a', 'face': '#e8d8b0', 'cheeks': '#f0a0c0', 'fluff': '#f0e8f4'},
            {'naam': 'Bloemkool (witte roosjes, groene bladkraag)', 'body': ('#e8e4d0', {'l': 1.2}), 'face': '#f0dcb4',
             'cheeks': '#98c070', 'fluff': '#90b870'},
            {'naam': 'Rode biet', 'body': '#902048', 'face': '#f0d0c8', 'cheeks': '#f05880', 'fluff': '#f8e0e8'},
            {'naam': 'Shiitake (paddenstoelbruin)', 'body': '#7a5030', 'face': '#e8dcc4', 'cheeks': '#d89070',
             'fluff': '#f0e8dc'},
            {'naam': 'Bonsai in bloei (sakura-roze)', 'body': '#e890b8', 'face': '#f8ecd8', 'cheeks': '#d04070',
             'fluff': '#fff0f4'},
            {'naam': 'Gouden appel van de Hesperiden', 'body': ('#d8a828', {'h': 0}), 'face': '#f8ecc8', 'cheeks': '#e05050',
             'fluff': '#fcf8e8'},
        ],
    },
    'pansear': {
        # vuuraap: lijf/kuif, vlamrand (lichte kuif), gezicht, borstvacht (Simisear)
        'species': {
            'pansear': {'body': [2, 4, 1], 'flame': [5], 'face': [9, 10, 12, 13]},
            'simisear': {'body': [4, 3, 1], 'flame': [5], 'face': [11, 9, 12, 13], 'fluff': [6, 10, 7, 8]},
        },
        'variants': [
            {'naam': 'Sintels (zwart, gloeiende kuif)', 'body': ('#3a3438', DARK), 'flame': '#f08020', 'face': '#b0a090',
             'fluff': '#f0a040'},
            {'naam': 'Kaliumvlam (lila)', 'body': '#9050c8', 'flame': '#e8b0f8', 'face': '#f0e0f0', 'fluff': '#f8f0ff'},
            {'naam': 'Witheet (bleekgeel, witte kuif)', 'body': '#f0dc90', 'flame': '#fcfcf0', 'face': '#f8f0e0',
             'fluff': '#f8e070'},
            {'naam': 'Vuurwerk (strontium-roze)', 'body': '#d83890', 'flame': '#f8b0d8', 'face': '#f8e0c8',
             'fluff': '#f8e8f0'},
            {'naam': 'Kampvuur (houtbruin, oranje kuif)', 'body': '#6a4428', 'flame': '#f0a020', 'face': '#e0c8a0',
             'fluff': '#f0b030'},
            {'naam': 'Feniks (goud, karmijnen kuif)', 'body': ('#e0b030', {'h': 0}), 'flame': '#d02040', 'face': '#f8ecd0',
             'fluff': '#e83040'},
        ],
    },
    'panpour': {
        # waterspuitaap (drankjes): lijf/kuif, lichte kuifrand, gezicht, borstvacht (Simipour)
        'species': {
            'panpour': {'body': [5, 4, 1, 3], 'foam': [6], 'face': [10, 8, 11, 12]},
            'simipour': {'body': [4, 5, 1, 2], 'foam': [6], 'face': [11, 8, 14, 9], 'fluff': [7, 10, 15, 12, 13]},
        },
        'variants': [
            {'naam': 'Cola (bruin met schuimkop)', 'body': '#6a3420', 'foam': '#f0e8d8', 'face': '#e8c8a0',
             'fluff': '#f0e4d0'},
            {'naam': 'Druivensap', 'body': '#6a2a8a', 'foam': '#c088e0', 'face': '#f0e0f0', 'fluff': '#e0c8f0'},
            {'naam': 'Melk (wit, crème gezicht)', 'body': ('#e4e8ec', {'l': 1.2}), 'foam': '#ffffff', 'face': '#f0d4a8',
             'fluff': '#c8d8f0'},
            {'naam': 'Aardbeienlimonade (roze)', 'body': '#e86888', 'foam': '#ffd0e0', 'face': '#f8f0e0',
             'fluff': '#fff0f4'},
            {'naam': 'Octopusinkt (zwart)', 'body': ('#2c2c38', DARK), 'foam': '#6a6a80', 'face': '#b0a8b8',
             'fluff': '#8a8aa0'},
            {'naam': 'Champagne (goud met bubbels)', 'body': ('#d8b040', {'h': 0}), 'foam': '#fff8d0', 'face': '#f8ecd0',
             'fluff': '#fffaf0'},
        ],
    },
    'munna': {
        # droomtapirs (Maleise tapir): lijf, bloempatroon, roze stippen (Munna), ogen (Munna), droomrook (Musharna)
        'species': {
            'munna': {'body': [2, 1, 5, 13, 3], 'pattern': [6, 4, 14], 'spots': [8, 9], 'eyes': [12, 10]},
            'musharna': {'body': [7, 9, 5], 'pattern': [4, 8, 3], 'smoke': [2, 1, 11, 12]},
        },
        'variants': [
            {'naam': 'Mintdroom (mintgroen, zeegroen patroon)', 'body': '#b8e8c8', 'pattern': '#2c8a78', 'spots': '#f0a0b0',
             'eyes': '#e04060', 'smoke': '#80d0b0'},
            {'naam': 'Perzik-dagdroom (perzik met mint)', 'body': '#f8c8a0', 'pattern': '#58b898', 'spots': '#f08870',
             'eyes': '#c04020', 'smoke': '#f0a888'},
            {'naam': 'Maleise tapir (wit met zwart zadel)', 'body': ('#ecece8', {'l': 1.2}), 'pattern': ('#34343c', DARK),
             'spots': '#a8a8b0', 'eyes': '#c03040', 'smoke': '#b8b8c4'},
            {'naam': 'Nachtmerrie (Darkrai-kleuren: zwart met rood)', 'body': ('#4a4258', DARK), 'pattern': '#c02838',
             'spots': '#8a3048', 'eyes': '#40d0f0', 'smoke': '#5a3a70'},
            {'naam': 'Suikerspin (hemelsblauw met roze)', 'body': '#b0dcf8', 'pattern': '#f080b8', 'spots': '#f8f0f8',
             'eyes': '#7040c0', 'smoke': '#f8b0d8'},
            {'naam': 'Hypnos (gouden slaap, paarse droom)', 'body': '#f0d890', 'pattern': '#7040a0', 'spots': '#e0a030',
             'eyes': '#7040a0', 'smoke': ('#e0b040', {'h': 0})},
        ],
    },
    'pidove': {
        # duiven en fazanten: lijf, donker (kop/rug), borst, ogen/snavel, roze poten; Tranquill/Unfezant ook kam/lellen en
        # Unfezants groene borstveren (vrouwtje: bruine borst, zie remap in de keuring)
        'species': {
            'pidove': {'body': [5, 1], 'dark': [2, 13, 14], 'belly': [15, 4], 'beak': [8, 7, 9], 'feet': [10, 6, 11]},
            'tranquill': {'body': [9, 7, 10, 13], 'dark': [2, 1], 'belly': [6], 'wattle': [5, 4], 'beak': [11, 12],
                          'feet': [14, 15]},
            'unfezant': {'body': [12, 7], 'dark': [14, 8, 4], 'green': [9, 5], 'wattle': [10, 11, 6], 'beak': [2]},
        },
        'variants': [
            {'naam': 'Tortelduif (zandbeige, roze borst)', 'body': '#c8b090', 'dark': '#8a7058', 'belly': '#e8c8c0',
             'beak': '#e05030', 'feet': '#c06070', 'wattle': '#a04060', 'green': '#c89878'},
            {'naam': 'Vredesduif (wit met olijftak)', 'body': ('#e0e0e0', {'l': 1.3}), 'dark': ('#b4b4bc', {'l': 1.3}),
             'belly': '#fcfcfc', 'beak': '#e8a020', 'feet': '#f090a0', 'wattle': '#e04050', 'green': '#7a9a40'},
            {'naam': 'Victoria-kroonduif (blauwgrijs, kastanjebruine borst)', 'body': '#6880b0', 'dark': '#3a4a78',
             'belly': '#8a3040', 'beak': '#e02030', 'feet': '#c03040', 'wattle': '#4870d8', 'green': '#8a3040'},
            {'naam': 'Nicobarduif (metaalgroen en koper)', 'body': '#3a7a5a', 'dark': '#2a4038', 'belly': '#b87838',
             'beak': '#f0e0a0', 'feet': '#d07060', 'wattle': '#e0c040', 'green': '#c07830'},
            {'naam': 'Raaf (Nevermore: zwart met rood oog)', 'body': ('#4a4a56', DARK), 'dark': ('#24242c', DARK),
             'belly': '#686878', 'beak': '#e03030', 'feet': '#3a3a44', 'wattle': '#a01828', 'green': '#384050'},
            {'naam': 'Pauw (koningsblauw, groen en goud)', 'body': '#2850c0', 'dark': '#183078', 'belly': '#30a080',
             'beak': '#f0c030', 'feet': '#a0a8b8', 'wattle': '#f0c030', 'green': '#30c0a0'},
        ],
    },
    'blitzle': {
        # elektrische zebra's: donkere vacht, witte strepen/manen, gele bliksem, blauwe ogen
        'species': {
            'blitzle': {'dark': [1, 10, 5], 'white': [2, 12, 11, 13], 'bolt': [8, 7], 'eyes': [4, 9]},
            'zebstrika': {'dark': [2, 13, 8, 14], 'white': [6, 4, 3, 7], 'bolt': [12, 11], 'eyes': [10, 9, 1]},
        },
        'variants': [
            {'naam': 'Quagga (bruin met crème strepen)', 'dark': '#7a5a3a', 'white': '#e8d8b0', 'bolt': '#f8f4e0',
             'eyes': '#e0a020'},
            {'naam': 'Tijger (oranje met zwarte strepen)', 'dark': ('#2c2c34', DARK), 'white': '#e88030', 'bolt': '#f8f0e0',
             'eyes': '#40a040'},
            {'naam': 'Negatief (wit lijf, zwarte strepen, blauwe bliksem)', 'dark': ('#dcdce4', {'l': 1.3}),
             'white': ('#3a3a44', DARK), 'bolt': '#40a0f0', 'eyes': '#e03030'},
            {'naam': 'Neonreclame (zwart met cyaan en roze)', 'dark': ('#2c2c38', DARK), 'white': '#40e0f0',
             'bolt': '#ff40b0', 'eyes': '#ff40b0'},
            {'naam': 'Bloedrode storm (rood met zwarte bliksem)', 'dark': '#a02028', 'white': '#f0d0c8',
             'bolt': ('#2c2c34', DARK), 'eyes': '#f0e040'},
            {'naam': 'Goud en zilver (cyaan bliksem)', 'dark': ('#c89828', {'h': 0}), 'white': '#e8e8f0', 'bolt': '#40c0f0',
             'eyes': '#40c0f0'},
        ],
    },
    'roggenrola': {
        # gesteente: lijf, aardlaag (Roggenrola's top/voeten), kristallen (Boldore/Gigalith), kern, grijs (Gigalith)
        'species': {
            'roggenrola': {'body': [6, 7, 5], 'top': [3, 4, 1], 'core': [10, 9, 8]},
            'boldore': {'body': [3, 1, 4], 'crystal': [8, 6, 7, 5], 'core': [11, 10, 9]},
            'gigalith': {'body': [7, 8, 6, 11], 'crystal': [5, 4, 1, 2], 'core': [10, 9], 'top': [12, 13]},
        },
        'variants': [
            {'naam': 'Malachiet (groen met koperen kristallen)', 'body': '#2a6a50', 'top': '#5a4030', 'crystal': '#d07838',
             'core': '#f0e060'},
            {'naam': 'Zandsteen met amethist', 'body': '#b89870', 'top': '#7a6048', 'crystal': '#9050c0', 'core': '#f0d8f8'},
            {'naam': 'Obsidiaan met lava', 'body': ('#34343e', DARK), 'top': '#4a3a30', 'crystal': '#f08020',
             'core': '#f8e040'},
            {'naam': 'Marmer met jade (robijnen kern)', 'body': ('#ccc8c4', {'l': 1.5}), 'top': '#9a9490', 'crystal': '#30a070',
             'core': '#d03040'},
            {'naam': 'Himalayazout (roze met witte kristallen)', 'body': '#e0a8a0', 'top': '#a07060', 'crystal': ('#e8e0e0', {'l': 1.3}),
             'core': '#c04050'},
            {'naam': 'Pyriet (kattengoud met smaragden)', 'body': ('#b89838', {'h': 0}), 'top': '#6a5020', 'crystal': '#20b060',
             'core': '#e03040'},
        ],
    },
    'woobat': {
        # vleermuizen met een hartneus: vacht, vleugels, hart (neus/staart), kop (Swoobat)
        'species': {
            'woobat': {'fur': [8, 6, 5, 7], 'wings': [2, 1, 4], 'heart': [10, 11, 9, 14]},
            'swoobat': {'fur': [10, 8, 9], 'head': [5, 7, 4, 6], 'wings': [1, 3], 'heart': [14, 15, 11]},
        },
        'variants': [
            {'naam': 'Vliegende hond (roestbruine vacht)', 'fur': '#c07838', 'head': '#7a4020', 'wings': ('#3a2c28', DARK),
             'heart': '#f0a0a0'},
            {'naam': 'Hondurese witte vleermuis (wit met geel)', 'fur': ('#e8e8e0', {'l': 1.3}), 'head': '#e8c830',
             'wings': '#4a4a54', 'heart': '#f0c030'},
            {'naam': 'Valentijn (roze met rood hart)', 'fur': '#f0a8c8', 'head': '#d04878', 'wings': '#7a2848',
             'heart': '#e02040'},
            {'naam': 'Dracula (zwart met bloedrood)', 'fur': ('#3a3440', DARK), 'head': ('#2c2830', DARK), 'wings': '#8a1820',
             'heart': '#e02020'},
            {'naam': 'Halloween (pompoenoranje met paars)', 'fur': '#f08830', 'head': '#7030a0', 'wings': '#3a2050',
             'heart': '#9040c0'},
            {'naam': 'Batman (grijs pak, zwarte cape, geel embleem)', 'fur': '#8a8a94', 'head': ('#2c2c34', DARK),
             'wings': ('#24242c', DARK), 'heart': '#f0d030'},
        ],
    },
    'drilbur': {
        # mollen: lijf, streep (Excadrill: rode tekening), klauwen/boor, neus (Drilbur)
        'species': {
            'drilbur': {'body': [9, 2, 14], 'stripe': [11, 10], 'metal': [6, 4, 5, 1], 'nose': [7, 8]},
            'excadrill': {'body': [6, 5, 7], 'stripe': [9, 8, 12, 11, 13], 'metal': [4, 2, 1, 10]},
        },
        'variants': [
            {'naam': 'Zandmol (zandbeige, koperen klauwen)', 'body': '#a88a64', 'stripe': '#6a4a30', 'metal': '#c87840',
             'nose': '#e08070'},
            {'naam': 'Diamantboor (zwart, ijsblauwe diamanten)', 'body': ('#34343c', DARK), 'stripe': '#40a0e0',
             'metal': '#c8e8f8', 'nose': '#e08090'},
            {'naam': 'Roestbak (leisteen, roestige klauwen)', 'body': '#5a6a62', 'stripe': '#e07030', 'metal': '#b06030',
             'nose': '#f0a080'},
            {'naam': 'Albino mol (wit, roze)', 'body': ('#d0ccc8', {'l': 1.5}), 'stripe': '#f0a8b8', 'metal': '#e8e0d8',
             'nose': '#f07890'},
            {'naam': 'Gouden boor (paars lijf)', 'body': '#5a3a7a', 'stripe': '#b070e0', 'metal': ('#e0b030', {'h': 0}),
             'nose': '#f090b0'},
            {'naam': 'Bouwmachine (Caterpillar-geel, waarschuwingsstrepen)', 'body': '#d8b020', 'stripe': ('#2c2c34', DARK),
             'metal': '#c8ccd8', 'nose': '#f08080'},
        ],
    },
    'audino': {
        # verpleegster: roze vacht, crème buik/oorlellen, blauwe ogen, witte staartkrullen
        'species': {
            'audino': {'pink': [1, 2, 3], 'cream': [5, 6, 10, 4], 'eyes': [7], 'white': [12, 13, 11]},
        },
        'variants': [
            {'naam': 'OK-groen (chirurgenpak)', 'pink': '#4a9a80', 'cream': '#e8f0e0', 'eyes': '#c03040', 'white': '#d8e8f0'},
            {'naam': 'Rode Kruis (rood met wit)', 'pink': '#d82030', 'cream': ('#f4f0ec', {'l': 1.3}), 'eyes': '#2c50c0',
             'white': '#f8f8f8'},
            {'naam': 'Kraamafdeling (babyblauw)', 'pink': '#80b0e8', 'cream': '#fff4e0', 'eyes': '#e06080', 'white': '#f8d0e0'},
            {'naam': 'Kamillethee (geel met wit)', 'pink': '#e8c838', 'cream': '#fcf8ec', 'eyes': '#5aa040', 'white': '#f0f0e0'},
            {'naam': 'Pleister (huidkleur, blauwe ogen)', 'pink': '#d0a078', 'cream': '#f0dcc0', 'eyes': '#3060c0',
             'white': '#f0f0f0'},
            {'naam': 'Florence Nightingale (nachtblauw met lamplicht)', 'pink': '#2c3a70', 'cream': '#f0e0b0', 'eyes': '#f0c030',
             'white': '#f0c030'},
        ],
    },
    'timburr': {
        # bouwvakkers: huid, aders/neus, gereedschap (balk, stalen ligger, betonpilaren)
        'species': {
            'timburr': {'skin': [6, 3, 1], 'veins': [5, 7, 4], 'tool': [14, 13, 12, 15]},
            'gurdurr': {'skin': [7, 8, 6], 'veins': [11, 10, 9], 'tool': [4, 2, 5, 3, 14, 13]},
            'conkeldurr': {'skin': [1, 3, 2], 'veins': [6, 7, 5], 'tool': [8, 9, 10], 'nose': [13, 12]},
        },
        'variants': [
            {'naam': 'Bob de Bouwer (perzik, blauwe overall, gele helm)', 'skin': '#e8c8a8', 'veins': '#3a6ac8',
             'tool': '#f0c020', 'nose': '#e07060'},
            {'naam': 'Hulk (groene huid, paarse broek)', 'skin': '#58a040', 'veins': '#7a3a9a', 'tool': '#a0a0a8',
             'nose': '#3a7a30'},
            {'naam': 'The Thing (oranje steenhuid, blauw)', 'skin': '#e07830', 'veins': '#2850a0', 'tool': '#8a7060',
             'nose': '#a04020'},
            {'naam': 'Michelangelo (marmeren David)', 'skin': ('#e0dcd4', {'l': 1.4}), 'veins': '#a8a098',
             'tool': ('#d8d4cc', {'l': 1.4}), 'nose': '#b8b0a8'},
            {'naam': 'Smurf (blauw met wit)', 'skin': '#5888d8', 'veins': '#f0f0f0', 'tool': '#d8b080', 'nose': '#3a68b8'},
            {'naam': 'Oni (rode demon, zwarte knots, goud)', 'skin': '#c84030', 'veins': '#f0c030', 'tool': ('#2c2c34', DARK),
             'nose': '#f0c030'},
        ],
    },
    'tympole': {
        # kikkers en padden: blauw lijf (Tympole: staart/wangen), bulten, donkere kop/rug, buik/gezicht
        'species': {
            'tympole': {'dark': [1, 2, 8, 12], 'belly': [4, 5, 9], 'blue': [11, 10, 7]},
            'palpitoad': {'blue': [8, 10, 9], 'bumps': [3, 4, 1], 'dark': [5, 7, 6], 'belly': [15, 14, 13]},
            'seismitoad': {'blue': [10, 9, 8], 'bumps': [5, 4, 1], 'dark': [3, 6, 7]},
        },
        'variants': [
            {'naam': 'Rietpad (koperbruin met olijf)', 'blue': '#8a6a40', 'bumps': '#a0a050', 'dark': '#4a3a2a', 'belly': '#e8d8b0'},
            {'naam': 'Roodoogmakikikker (groen, oranje, blauwe flanken)', 'blue': '#40a040', 'bumps': '#f08030',
             'dark': '#2a4a7a', 'belly': '#f0f0d8'},
            {'naam': 'Tomatenkikker (rood)', 'blue': '#d04028', 'bumps': '#f0a040', 'dark': '#5a2a20', 'belly': '#f8d8c0'},
            {'naam': 'Glaskikker (doorschijnend lichtgroen)', 'blue': ('#a8dca0', {'l': 1.3}), 'bumps': '#e8f8e0',
             'dark': '#5a8a6a', 'belly': '#f0f8f0'},
            {'naam': 'Basbox (zwarte speaker met blauwe led)', 'blue': ('#34343c', DARK), 'bumps': '#c8ccd8', 'dark': '#5a5a64',
             'belly': '#40a0f0'},
            {'naam': 'Kikkerkoning (Grimm: groen met gouden bulten)', 'blue': '#3a8a40', 'bumps': ('#e0b030', {'h': 0}),
             'dark': '#2c4a2c', 'belly': '#f0e8c0'},
        ],
    },
    'throh': {
        # judoka: kop/handen, judogi, band
        'species': {'throh': {'skin': [2, 5, 1], 'gi': [9, 6, 8], 'belt': [4, 7]}},
        'variants': [
            {'naam': 'Wedstrijdjudo (blauwe judogi, oranje kop)', 'skin': '#e08030', 'gi': '#3a68c8', 'belt': '#f0f0f0'},
            {'naam': 'Sensei (zwarte gi, rode band, bruine kop)', 'skin': '#8a5030', 'gi': ('#3a3a44', DARK), 'belt': '#d02020'},
            {'naam': 'Sawk-ruil (blauwe kop, teal gi)', 'skin': '#3a70d8', 'gi': '#78c0b8', 'belt': ('#2c2c34', DARK)},
            {'naam': 'Kersenbloesem (roze kop, witte gi, roze band)', 'skin': '#f090a8', 'gi': ('#f4f4f4', {'l': 1.3}),
             'belt': '#d04070'},
            {'naam': 'Kung Fu Panda (witte kop met zwarte vlekken, zwarte gi)', 'skin': ('#ecece8', {'l': 1.3}), 'gi': ('#3a3a44', DARK),
             'belt': ('#2c2c34', DARK)},
            {'naam': 'Olympisch goud (gouden gi, zwarte band)', 'skin': '#c03050', 'gi': ('#e0b840', {'h': 0}),
             'belt': ('#2c2c34', DARK)},
        ],
    },
    'sawk': {
        # karateka: kop/handen, karategi, band
        'species': {'sawk': {'skin': [2, 3, 6], 'gi': [8, 9, 11, 12, 13, 1], 'belt': [5, 7]}},
        'variants': [
            {'naam': 'Kyokushin (witte gi, groene kop)', 'skin': '#40a050', 'gi': ('#e8e8e8', {'l': 1.3}),
             'belt': ('#2c2c34', DARK)},
            {'naam': 'Sensei (zwarte gi, rode band, paarse kop)', 'skin': '#7a48c0', 'gi': ('#3a3a44', DARK), 'belt': '#d02020'},
            {'naam': 'Throh-ruil (rode kop, crème gi)', 'skin': '#d85858', 'gi': '#e0d8c4', 'belt': ('#2c2c34', DARK)},
            {'naam': 'Kersenbloesem (roze kop, witte gi, roze band)', 'skin': '#f090a8', 'gi': ('#f4f4f4', {'l': 1.3}),
             'belt': '#d04070'},
            {'naam': 'Kung Fu Panda (witte kop met zwarte vlekken, zwarte gi)', 'skin': ('#ecece8', {'l': 1.3}), 'gi': ('#3a3a44', DARK),
             'belt': ('#2c2c34', DARK)},
            {'naam': 'Olympisch goud (gouden gi, zwarte band)', 'skin': '#2c50a0', 'gi': ('#e0b840', {'h': 0}),
             'belt': ('#2c2c34', DARK)},
        ],
    },
    'sewaddle': {
        # bladkleermakers: bladjas, geel gezicht/lijf, donkere onderbladeren (Swadloon/Leavanny), accenten (mond/voeten/ogen)
        'species': {
            'sewaddle': {'leaf': [4, 3, 2], 'face': [8, 7, 5, 6], 'accent': [11, 12, 14]},
            'swadloon': {'leaf': [3, 4, 2], 'dark': [6, 5, 7], 'face': [9, 8, 10, 11]},
            'leavanny': {'leaf': [5, 6, 4], 'face': [3, 11, 2, 7], 'dark': [13, 14, 12], 'accent': [10, 8]},
        },
        'variants': [
            {'naam': 'Herfstblad (oranje met rood)', 'leaf': '#d87830', 'face': '#f0d870', 'dark': '#8a3020', 'accent': '#c03030'},
            {'naam': 'Bloedbeuk (purperen blad)', 'leaf': '#7a3050', 'face': '#f0c8a0', 'dark': '#3a1830', 'accent': '#f0d040'},
            {'naam': 'Wandelend blad (dor bruin)', 'leaf': '#a08050', 'face': '#e8d8a8', 'dark': '#5a4028', 'accent': '#e07030'},
            {'naam': 'Rijp (berijpt wit blad)', 'leaf': ('#d4e0d8', {'l': 1.4}), 'face': '#f0f0c8', 'dark': '#88a8a0',
             'accent': '#e06070'},
            {'naam': 'Haute couture (zwart met roze)', 'leaf': ('#38383e', DARK), 'face': '#f0a0c0', 'dark': '#5a5a68',
             'accent': '#f0f0f0'},
            {'naam': 'Repelsteeltje (gesponnen goud)', 'leaf': ('#d8a828', {'h': 0}), 'face': '#f8f0d0', 'dark': '#6a4810',
             'accent': '#c02040'},
        ],
    },
    'venipede': {
        # duizendpoten: lijf (Venipede rood, Whirlipede paars, Scolipede magenta), accent (groen/roze vlekken/paarse
        # ringen), donkere onderkant, ogen
        'species': {
            'venipede': {'body': [3, 4, 1], 'accent': [9, 10, 7], 'dark': [8], 'eyes': [6, 5]},
            'whirlipede': {'body': [4, 2, 1, 10], 'accent': [6, 5, 13, 14], 'dark': [7, 8, 9], 'eyes': [11, 12]},
            'scolipede': {'body': [8, 3, 2, 7], 'accent': [5, 4, 6, 11], 'dark': [13, 10, 9], 'eyes': [12]},
        },
        'variants': [
            {'naam': 'Scolopendra (oranje, zwarte ringen)', 'body': '#e07020', 'accent': ('#2c2c34', DARK), 'dark': '#5a3020',
             'eyes': '#f0e040'},
            {'naam': 'Blauwe reuzenduizendpoot (blauw met geel)', 'body': '#2860b0', 'accent': '#f0c030', 'dark': '#1a2440',
             'eyes': '#f0c030'},
            {'naam': 'Gifgroen met paars', 'body': '#58b040', 'accent': '#a040c0', 'dark': '#2a4020', 'eyes': '#f04060'},
            {'naam': 'Skelet (bot, rode ogen)', 'body': ('#d8d4cc', {'l': 1.4}), 'accent': '#a8a098', 'dark': '#5a5450',
             'eyes': '#e02020'},
            {'naam': 'Lava (zwart met gloeiende scheuren)', 'body': ('#3a3438', DARK), 'accent': '#f06020', 'dark': '#24202a',
             'eyes': '#f8e040'},
            {'naam': 'Chroom (zilver met neonroze)', 'body': '#c0c4d0', 'accent': '#ff40b0', 'dark': '#4a4c58', 'eyes': '#40e0f0'},
        ],
    },
    'cottonee': {
        # katoenpluisjes: wol, blaadjes (Cottonee) / hoorns (Whimsicott), oranje puntjes, lijf (Whimsicott)
        'species': {
            'cottonee': {'cotton': [2, 1, 3, 4], 'leaves': [10, 8, 9], 'tips': [13, 11]},
            'whimsicott': {'cotton': [3, 4, 1, 2], 'body': [9, 12, 10], 'leaves': [8, 7, 6], 'tips': [14, 11]},
        },
        'variants': [
            {'naam': 'Suikerspin (roze wol, hemelsblauw blad)', 'cotton': '#f4bcd4', 'leaves': '#58b8e0', 'tips': '#f8f8f8',
             'body': '#a06070'},
            {'naam': 'Zwart schaap (zwarte wol, witte kop)', 'cotton': ('#4a4650', DARK), 'leaves': '#7a9a60', 'tips': '#e0d0b0',
             'body': ('#e8e0d4', {'l': 1.3})},
            {'naam': 'Blauwe regen (hemelsblauw wolkje, paars blad)', 'cotton': '#b8d0f0', 'leaves': '#7058b8', 'tips': '#f8f0a0',
             'body': '#4a5a8a'},
            {'naam': 'Mint (mintwol, roze blad)', 'cotton': '#c8ecd8', 'leaves': '#e070a0', 'tips': '#f0c030', 'body': '#6a8a70'},
            {'naam': 'Onweerswolk (grijs met gele bliksem)', 'cotton': '#8a8e9a', 'leaves': '#f0d030', 'tips': '#f0d030',
             'body': '#3a3c48'},
            {'naam': 'Gulden vlies (gouden wol, robijnen blad)', 'cotton': ('#e8c050', {'h': 0}), 'leaves': '#c03040',
             'tips': '#f8f0d0', 'body': '#7a4a20'},
        ],
    },
    'petilil': {
        # bloemen: bloem (Petilils blaadjes), bloemhart, bladeren, jurk/lijf
        'species': {
            'petilil': {'flower': [2, 3, 1], 'dress': [5, 7, 6, 12]},
            'lilligant': {'flower': [3, 4, 2], 'heart': [6, 5], 'leaves': [11, 8, 7], 'dress': [13, 14, 12]},
            'lilligant/hisui': {'flower': [3, 4, 15, 2], 'heart': [5, 1], 'leaves': [8, 12, 10], 'dress': [14, 13, 7],
                                '_base': {'leaves': 12}},
        },
        'variants': [
            {'naam': 'Klaproos (rood, zwart hart)', 'flower': '#d82020', 'heart': ('#2c2c34', DARK), 'leaves': '#4a8a40',
             'dress': '#e4dcc0'},
            {'naam': 'Lavendel (paars, zilvergroen)', 'flower': '#9070d0', 'heart': '#f0e0f0', 'leaves': '#7a9a80',
             'dress': '#c8d8c8'},
            {'naam': 'Zonnebloem (geel, bruin hart)', 'flower': '#f0c020', 'heart': '#6a4020', 'leaves': '#3a7a30',
             'dress': '#98b860'},
            {'naam': 'Witte lelie (bruidsjurk)', 'flower': ('#f0f0e8', {'l': 1.3}), 'heart': '#f0c030', 'leaves': '#5a9a50',
             'dress': ('#e8e8e0', {'l': 1.4})},
            {'naam': 'Zwarte tulp (Dumas: dieppaars-zwart)', 'flower': ('#3a2440', DARK), 'heart': '#a03060', 'leaves': '#2a4a30',
             'dress': '#5a4a68'},
            {'naam': 'Blauwe roos (de onmogelijke bloem)', 'flower': '#3a60e0', 'heart': '#c8ccd8', 'leaves': '#2a5a6a',
             'dress': '#a8c8e8'},
        ],
    },
    'sandile': {
        # woestijnkrokodillen: lijf (Krookodile: rood), strepen (Krookodile: zwart), buik/bek
        'species': {
            'sandile': {'body': [6, 1, 4, 3], 'stripes': [7, 2, 9], 'belly': [10, 11, 12]},
            'krokorok': {'body': [3, 1, 2, 4], 'stripes': [5, 7, 14, 9], 'belly': [12, 11]},
            'krookodile': {'body': [6, 3, 2, 5, 12], 'stripes': [1, 4], 'belly': [14, 13]},
        },
        'variants': [
            {'naam': 'Nijlkrokodil (olijfgroen)', 'body': '#7a8a40', 'stripes': ('#3a4020', DARK), 'belly': '#e8d8a0'},
            {'naam': 'Zwarte kaaiman (zwart met gele strepen)', 'body': ('#3a3a34', DARK), 'stripes': '#e0c030', 'belly': '#c8c0a0'},
            {'naam': 'Sobek (Egyptisch turkoois met goud)', 'body': '#3aa8a0', 'stripes': '#c89820', 'belly': '#f0e0b0'},
            {'naam': 'Albino alligator (wit, roze)', 'body': ('#dcd8cc', {'l': 1.4}), 'stripes': '#a8a0a0', 'belly': '#f0b0bc'},
            {'naam': 'Zandstorm (bleek zand, oranje strepen)', 'body': '#e0c890', 'stripes': '#d06020', 'belly': '#f8f0e0'},
            {'naam': 'Farao-sieraad (goud met lapis lazuli)', 'body': ('#d8a828', {'h': 0}), 'stripes': '#2040a0',
             'belly': '#f8ecc0'},
        ],
    },
    'darumaka': {
        # daruma-poppen, elke kleur een wens: lijf, geel (wenkbrauwen/vlamkern), huid (gezicht/handen), vlammen
        # (Darmanitan), zen = het stenen beeld (Zen-modus)
        'species': {
            'darumaka': {'body': [6, 7, 8], 'yellow': [4, 5, 1], 'skin': [10, 9]},
            'darmanitan': {'body': [7, 6, 8], 'fire': [2, 1], 'yellow': [4, 3, 5], 'skin': [12, 10, 15]},
            'darmanitan/zen': {'zen': [12, 2, 1, 13, 7, 8], 'skin': [5, 4, 3]},
        },
        'variants': [
            {'naam': 'Witte daruma (zuiverheid)', 'body': ('#e4e0d8', {'l': 1.3}), 'yellow': '#e0b030', 'skin': '#f0c8a0',
             'fire': '#f08030', 'zen': '#c8c8c4'},
            {'naam': 'Zwarte daruma (zakensucces)', 'body': ('#34343c', DARK), 'yellow': '#e0b030', 'skin': '#c8a080',
             'fire': '#e03030', 'zen': '#5a5a64'},
            {'naam': 'Groene daruma (gezondheid, jade beeld)', 'body': '#3a9a50', 'yellow': '#f0e060', 'skin': '#f0c090',
             'fire': '#80e040', 'zen': '#5a9a78'},
            {'naam': 'Paarse daruma (zelfverbetering, amethist beeld)', 'body': '#7040a0', 'yellow': '#f0c040',
             'skin': '#e8b090', 'fire': '#c060f0', 'zen': '#9070b0'},
            {'naam': 'Roze daruma (liefde, rozenkwarts beeld)', 'body': '#f080a8', 'yellow': '#f8e8a0', 'skin': '#f8d0b0',
             'fire': '#ff60a0', 'zen': '#d8a8c0'},
            {'naam': 'Gouden daruma (rijkdom)', 'body': ('#d8a828', {'h': 0}), 'yellow': '#c02020', 'skin': '#f0d090',
             'fire': '#f8f0c0', 'zen': ('#c89838', {'h': 0})},
        ],
    },
    'darumaka_galar': {
        # sneeuwdaruma's: sneeuw, ijs (handen/voeten/wenkbrauwen), ijsedelstenen; Zen: vuur, handen, masker
        'species': {
            'darumaka/galar': {'snow': [6, 7, 11, 13, 14], 'ice': [9, 10, 8], 'gems': [5, 3, 4, 1]},
            'darmanitan/galar_standard': {'snow': [3, 1, 2, 4], 'ice': [11, 13, 12], 'gems': [6, 7, 10, 8]},
            'darmanitan/galar_zen': {'snow': [6, 8, 7, 10], 'fire': [2, 5, 4, 3], 'hands': [9, 14, 1], 'mask': [13, 12]},
        },
        'variants': [
            {'naam': 'Bloedsneeuw (roze sneeuwalgen op gletsjers)', 'snow': '#ecc4c8', 'ice': '#c03048', 'gems': '#f080a0',
             'fire': '#f8f0f0', 'hands': '#c03048', 'mask': '#802030'},
            {'naam': 'Gletsjer (ijsblauw, blauw vuur)', 'snow': '#c4d8ec', 'ice': '#2850a0', 'gems': '#40d0f0',
             'fire': '#4080f0', 'hands': '#3060c0', 'mask': '#1c3880'},
            {'naam': 'Pistache-ijs (mintgroen)', 'snow': '#c8e4bc', 'ice': '#3a8040', 'gems': '#e0f080', 'fire': '#60d040',
             'hands': '#4a9a40', 'mask': '#2a6030'},
            {'naam': 'Stracciatella (vanille met chocolade)', 'snow': '#e8d4b0', 'ice': '#6a4028', 'gems': '#c08850',
             'fire': '#f08030', 'hands': '#8a5030', 'mask': '#5a3020'},
            {'naam': 'Noorderlicht (lila met groen)', 'snow': '#d0c8ec', 'ice': '#5030a0', 'gems': '#40f0a0', 'fire': '#40f0a0',
             'hands': '#6040b0', 'mask': '#2c2070'},
            {'naam': 'Gouden sneeuw (goud met robijnen ijs)', 'snow': '#f0dca0', 'ice': '#c02040', 'gems': '#f8f0c0',
             'fire': '#f8e060', 'hands': ('#d8a828', {'h': 0}), 'mask': '#c02040'},
        ],
    },
    'maractus': {
        # maraca-cactus: lijf, donkere onderkant/benen, bloemen, gele stippen
        'species': {'maractus': {'body': [7, 6, 3], 'legs': [10, 9, 11], 'flower': [2, 1, 13], 'yellow': [5, 4, 12]}},
        'variants': [
            {'naam': 'Blauwe agave (blauwgrijs, gele bloemen)', 'body': '#6a9aa8', 'legs': '#2a5a6a', 'flower': '#f0d040',
             'yellow': '#f08030'},
            {'naam': 'Hibotan (rode entcactus op groene stam)', 'body': '#d03040', 'legs': '#3a7a40', 'flower': '#f8a0c0',
             'yellow': '#f0e060'},
            {'naam': 'Saguaro in bloei (olijfgroen, witte bloemen)', 'body': '#6a8a40', 'legs': '#4a5a30', 'flower': '#f4f0e8',
             'yellow': '#f0c030'},
            {'naam': 'Mariachi (zwart pak, zilveren knopen, rode roos)', 'body': ('#38383e', DARK), 'legs': '#5a5a68',
             'flower': '#d02030', 'yellow': '#d0d4e0'},
            {'naam': 'Paarse schijfcactus (Opuntia santa-rita)', 'body': '#8a5aa0', 'legs': '#5a3a70', 'flower': '#f0e040',
             'yellow': '#f08030'},
            {'naam': 'Día de los Muertos (turkoois met goudsbloemen)', 'body': '#30b0b0', 'legs': '#2060a0',
             'flower': '#f09020', 'yellow': '#e03070'},
        ],
    },
    'dwebble': {
        # heremietkreeften met een rotshuis: rots, ader/streep, krab
        'species': {
            'dwebble': {'shell': [4, 1, 2, 7], 'stripe': [3], 'body': [8, 9, 10, 11, 12]},
            'crustle': {'shell': [1, 2, 3, 13], 'stripe': [4, 6], 'body': [8, 12, 7, 9]},
        },
        'variants': [
            {'naam': 'Petra (rode zandsteen, blauwe krab)', 'shell': '#b06048', 'stripe': '#f0d8a0', 'body': '#4070c0'},
            {'naam': 'Graniet (grijs, paarse krab)', 'shell': '#a0a0a8', 'stripe': '#e8e8f0', 'body': '#8050a0'},
            {'naam': 'Marmer met goudader', 'shell': ('#dcd8d0', {'l': 1.4}), 'stripe': '#d8a828', 'body': '#e08070'},
            {'naam': 'Obsidiaan met lava', 'shell': ('#38383e', DARK), 'stripe': '#f07020', 'body': '#d03030'},
            {'naam': 'Turkoois (Navajo-sieraad, zilveren ader)', 'shell': '#40a8a0', 'stripe': '#d0d4e0', 'body': '#c06030'},
            {'naam': 'Ananashuis (SpongeBob, met Mr. Krabs erin)', 'shell': '#f0b020', 'stripe': '#3a8a30', 'body': '#e03030'},
        ],
    },
    'scraggy': {
        # straatboefjes: huid, afgestroopte broek, kuif/kraag
        'species': {
            'scraggy': {'body': [7, 6, 4], 'pants': [13, 12, 14], 'crest': [3, 1, 2]},
            'scrafty': {'body': [6, 5, 1, 7], 'pants': [14, 15, 13], 'crest': [4, 2]},
        },
        'variants': [
            {'naam': 'Gekko (groen, oranje kuif)', 'body': '#58b040', 'pants': '#e0d8a0', 'crest': '#f09020'},
            {'naam': 'Punk (grijsblauw, tartanrode broek, groene hanenkam)', 'body': '#8890a8', 'pants': '#c02028',
             'crest': '#40d040'},
            {'naam': 'Fresh Prince (turkoois met felroze broek)', 'body': '#40b8c0', 'pants': '#f060a8', 'crest': '#f0e040'},
            {'naam': 'Albino gekko (wit, perzik broek)', 'body': ('#dcd8cc', {'l': 1.4}), 'pants': '#f0c8b0', 'crest': '#f08030'},
            {'naam': 'Maffia (zwart, krijtstreepgrijs, witte kuif)', 'body': ('#3a3a44', DARK), 'pants': '#8a8a94',
             'crest': '#e8e8e8'},
            {'naam': 'Vaporwave (lila, cyaan broek, roze kuif)', 'body': '#b080e0', 'pants': '#40e0f0', 'crest': '#ff60b0'},
        ],
    },
    'sigilyph': {
        # Psychic/Flying, levende glyph: hoofdkleur (geel), blauw, rood, groen, zwart lijf
        'species': {'sigilyph': {'gold': [5, 7, 8], 'blue': [3, 1], 'red': [4, 6], 'green': [11, 13], 'body': [9]}},
        'variants': [
            {'naam': 'Nazca-lijnen (woestijnzand en roest)', 'gold': '#c8a070', 'blue': '#a05030', 'red': '#e8d8b0',
             'green': '#7a6040', 'body': '#5a4a40'},
            {'naam': 'Maya (jade en obsidiaan)', 'gold': '#40a070', 'blue': '#205a48', 'red': '#e0c040', 'green': '#f0f0e0',
             'body': ('#2c2c34', DARK)},
            {'naam': 'Delfts blauw (wit en kobalt)', 'gold': ('#e8ecf0', {'l': 1.3}), 'blue': '#2040a0', 'red': '#4060c0',
             'green': '#90a8d8', 'body': '#1c2c70'},
            {'naam': 'Mondriaan (wit, rood, blauw, geel)', 'gold': ('#f0f0e8', {'l': 1.3}), 'blue': '#2040b0', 'red': '#d02020',
             'green': '#f0d020', 'body': ('#2c2c34', DARK)},
            {'naam': 'Warhol-popart (roze, groen, oranje)', 'gold': '#f070b0', 'blue': '#40c040', 'red': '#f08020',
             'green': '#40a0f0', 'body': '#4020a0'},
            {'naam': 'Toetanchamon (goud op lapis lazuli, turkoois, carneool)', 'gold': ('#f0c030', {'h': 0}),
             'blue': '#40c0c0', 'red': '#c03020', 'green': '#f0c030', 'body': '#2040a0'},
        ],
    },
    'yamask': {
        # dodenmaskers: schaduwlijf (Cofagrigus: handen), masker / sarcofaag, spookoog, teal tekening (Cofagrigus)
        'species': {
            'yamask': {'body': [1, 2], 'mask': [9, 10, 7, 8], 'eye': [5, 4, 6]},
            'cofagrigus': {'body': [1], 'teal': [3, 5, 4], 'mask': [7, 8, 9], 'eye': [10, 11]},
        },
        'variants': [
            {'naam': 'Kopermasker (rood koper, turkoois spookoog)', 'body': ('#3a3430', DARK), 'mask': '#b85a38',
             'eye': '#30d0c0', 'teal': '#30a0a0'},
            {'naam': 'Jade-lijkwade (Chinees jadepak, gouden oog)', 'body': '#2c3a34', 'mask': '#40a070', 'eye': '#f0d040',
             'teal': '#e0c040'},
            {'naam': 'Día de los Muertos (suikerschedel)', 'body': '#5a2a6a', 'mask': ('#f0ece0', {'l': 1.3}),
             'eye': '#ff60b0', 'teal': '#30c0c0'},
            {'naam': 'Bloedmaan (rood masker, wit oog)', 'body': ('#3a2028', DARK), 'mask': '#b02830', 'eye': '#f0f0f0',
             'teal': '#6a2830'},
            {'naam': 'Obsidiaan (zwart masker, groen spookvuur)', 'body': '#4a4a58', 'mask': ('#38383e', DARK),
             'eye': '#40f060', 'teal': '#40f060'},
            {'naam': 'Rozengoud op lapis lazuli', 'body': '#20306a', 'mask': '#e8a890', 'eye': '#40c0f0', 'teal': '#2848a8'},
        ],
    },
    'yamask_galar': {
        # Galar: kleitablet, tekens erop, spookoog, schaduwlijf (Runerigus heeft nog geen recept)
        'species': {'yamask/galar': {'body': [1, 2], 'tablet': [8, 9, 11], 'glyph': [7, 10], 'eye': [5, 4]}},
        'variants': [
            {'naam': 'Terracotta (oranje klei, groen oog)', 'tablet': '#c87048', 'glyph': '#5a2818', 'eye': '#40c070',
             'body': ('#3a3438', DARK)},
            {'naam': 'Rosettasteen (zwart graniet, wit schrift)', 'tablet': ('#3a3a44', DARK), 'glyph': '#e8e8e0',
             'eye': '#f0c030', 'body': '#5a5a64'},
            {'naam': 'Kleitablet van Gilgamesj (zand, spijkerschrift)', 'tablet': '#d8c090', 'glyph': '#7a5a30',
             'eye': '#e04040', 'body': '#4a4038'},
            {'naam': 'Jadetablet (gouden tekens)', 'tablet': '#60a080', 'glyph': '#e0c040', 'eye': '#f04080',
             'body': '#2c3a34'},
            {'naam': 'Lapis lazuli met goud', 'tablet': '#3050a0', 'glyph': '#e0b030', 'eye': '#f0f0f0', 'body': '#2c2c44'},
            {'naam': 'Sumerisch goud (robijnen tekens)', 'tablet': ('#d8a828', {'h': 0}), 'glyph': '#c02040',
             'eye': '#40c0f0', 'body': '#3a3028'},
        ],
    },
    'tirtouga': {
        # oerschildpadden: blauwe vinnen/huid, schild/rots, lichte buik (Carracosta)
        'species': {
            'tirtouga': {'blue': [2, 5, 1, 9], 'shell': [6, 7, 4, 12]},
            'carracosta': {'blue': [5, 4, 8, 6, 12], 'shell': [2, 7, 9, 1], 'light': [10]},
        },
        'variants': [
            {'naam': 'Fossiel (zandsteen, crème)', 'blue': '#c8b080', 'shell': '#7a6a58', 'light': '#f0e8d0'},
            {'naam': 'Soepschildpad (groen, bruin schild)', 'blue': '#4a9a50', 'shell': '#6a5a3a', 'light': '#d8e8b0'},
            {'naam': 'Lederschildpad (zwart, witte vlekken)', 'blue': ('#3a3a44', DARK), 'shell': '#6a6a78', 'light': '#e8e8f0'},
            {'naam': 'Karetschildpad (schildpad-oranje)', 'blue': '#b86830', 'shell': '#5a3020', 'light': '#f0c890'},
            {'naam': 'Koraalrif (koraalroze, turkoois schild)', 'blue': '#f07890', 'shell': '#30a8a0', 'light': '#f8e0e8'},
            {'naam': 'Kim Qui (de gouden schildpad uit Hanoi, jade schild)', 'blue': ('#d8a828', {'h': 0}), 'shell': '#3a7a50',
             'light': '#f8f0c8'},
        ],
    },
    'archen': {
        # oervogels: rood (kop/staart), blauw (vleugels), geel (lijf), teal (Archeops)
        'species': {
            'archen': {'red': [3, 5, 1], 'blue': [4, 9, 2], 'yellow': [13, 12, 11]},
            'archeops': {'red': [10, 11, 15, 14], 'blue': [4, 3, 2], 'yellow': [9, 8, 7], 'teal': [12, 13]},
        },
        'variants': [
            {'naam': 'Velociraptor (Jurassic Park: zand met bruin)', 'red': '#8a5a30', 'blue': '#b89058', 'yellow': '#e8d8b0',
             'teal': '#6a4a28'},
            {'naam': 'Hyacinth-ara (kobaltblauw met geel)', 'red': '#2840b0', 'blue': '#1c2c80', 'yellow': '#f0d030',
             'teal': '#3050c0'},
            {'naam': 'Versteend (grijs met barnsteen)', 'red': '#a07040', 'blue': '#7a7a80', 'yellow': '#c8c0b0',
             'teal': '#5a5a60'},
            {'naam': 'Albino (wit, roze kop)', 'red': '#f0a0b0', 'blue': ('#dcdcdc', {'l': 1.4}), 'yellow': '#f8f0e0',
             'teal': '#d0d0d0'},
            {'naam': 'Toekan (zwart, oranje, wit)', 'red': '#f08020', 'blue': ('#34343c', DARK), 'yellow': '#f8f0e0',
             'teal': '#f0c030'},
            {'naam': 'Feniks (goud met karmijn en vuurstaart)', 'red': ('#e0b030', {'h': 0}), 'blue': '#c02020',
             'yellow': '#f8e080', 'teal': '#f07020'},
        ],
    },
    'trubbish': {
        # vuilniszakken: zak (Garbodor: groene slijmlagen), afval (Garbodor: bruin lijf), roze en blauwe rommel
        'species': {
            'trubbish': {'bag': [1, 3, 7, 4], 'trash': [9, 10, 8], 'pink': [14, 11], 'blue': [12, 13]},
            'garbodor': {'bag': [10, 11, 9], 'trash': [4, 1, 2], 'pink': [6, 5], 'blue': [8, 7]},
        },
        'variants': [
            {'naam': 'Zwarte vuilniszak (grijs afval)', 'bag': ('#38383e', DARK), 'trash': '#8a8a94', 'pink': '#e04040', 'blue': '#40c0f0'},
            {'naam': 'Gele zak (bedrijfsafval, leisteen)', 'bag': '#d8b828', 'trash': '#6a7080', 'pink': '#c03040', 'blue': '#3060c0'},
            {'naam': 'Plasticsoep (turkoois met bont plastic)', 'bag': '#40a0b0', 'trash': '#e0d0a0', 'pink': '#f060a0',
             'blue': '#f0e040'},
            {'naam': 'Barbie-afval (roze met glitter)', 'bag': '#f080b8', 'trash': '#c8a8c0', 'pink': '#a030a0',
             'blue': '#40e0f0'},
            {'naam': 'PMD-zak (oranje plasticzak)', 'bag': '#f08020', 'trash': '#e0d8c0', 'pink': '#d03030', 'blue': '#3070d0'},
            {'naam': 'Gouden vuilnisbak (vergulde kitsch)', 'bag': ('#d8a828', {'h': 0}), 'trash': '#a8a8b0', 'pink': '#c02040',
             'blue': '#30c0f0'},
        ],
    },
    'zorua': {
        # illusievossen: vacht, manen/kuif, ogen; Zoroark ook de lichtere poten
        'species': {
            'zorua': {'body': [6, 3, 10, 4], 'mane': [2, 1], 'eyes': [7, 9]},
            'zoroark': {'body': [3, 2], 'legs': [7, 9, 8], 'mane': [4, 6, 5], 'eyes': [12, 11]},
        },
        'variants': [
            {'naam': 'Zilvervos (zwart met zilveren manen)', 'body': ('#2c2c34', DARK), 'legs': '#5a5a64', 'mane': '#c8ccd8',
             'eyes': '#f0c030'},
            {'naam': 'Poolvos (wit met ijsblauwe manen)', 'body': ('#d4d8e0', {'l': 1.4}), 'legs': ('#c0c4d0', {'l': 1.4}),
             'mane': '#60a0e0', 'eyes': '#3060c0'},
            {'naam': 'Loki (groen en goud)', 'body': '#2c4a30', 'legs': '#5a7a50', 'mane': '#40a050', 'eyes': '#e0c030'},
            {'naam': 'Fennek (zand met crème)', 'body': '#c8a870', 'legs': '#e0c898', 'mane': '#f0e0c0', 'eyes': '#e07020'},
            {'naam': 'Joker (paars pak, groen haar)', 'body': '#5a3a7a', 'legs': '#8060a0', 'mane': '#40c040', 'eyes': '#f0e040'},
            {'naam': 'Kurama (negenstaartige vos: goudoranje met rood)', 'body': ('#e09030', {'h': 0}), 'legs': '#f0c070',
             'mane': '#c02020', 'eyes': '#f0e040'},
        ],
    },
    'zorua_hisui': {
        # Hisui-spookvossen: witte vacht, grijze schaduw, spookvuur/haar
        'species': {
            'zorua/hisui': {'fur': [5, 7, 9, 11, 15], 'shade': [4, 8], 'fire': [2, 1, 3, 12]},
            'zoroark/hisui': {'fur': [14, 10, 13, 9], 'shade': [2, 3], 'fire': [4, 5, 6, 7, 1, 11]},
        },
        'variants': [
            {'naam': 'Dwaallicht (groen spookvuur)', 'fur': ('#d8e8d8', {'l': 1.2}), 'shade': '#4a5a50', 'fire': '#40c060'},
            {'naam': 'Nachtvos (zwarte vacht, rood vuur)', 'fur': ('#4a4a58', DARK), 'shade': '#2c2c34', 'fire': '#e03030'},
            {'naam': 'Inari (goud vuur op crème)', 'fur': '#f0e4c8', 'shade': '#7a6a50', 'fire': '#e0a020'},
            {'naam': 'Sakura-geest (roze vacht, kersenvuur)', 'fur': '#f8dce8', 'shade': '#7a5a68', 'fire': '#e05090'},
            {'naam': 'Sumi-e (inktschilderij: wit met zwart vuur)', 'fur': ('#d8d8dc', {'l': 1.3}), 'shade': '#5a5a64',
             'fire': ('#34343c', DARK)},
            {'naam': 'Zonsondergang (lila vacht, oranje vuur)', 'fur': '#c0a8dc', 'shade': '#4a3a68', 'fire': '#f08030'},
        ],
    },
    'basculin': {
        # roodgestreepte vorm (de streepvormen zijn kleurvormen): lijf, streep, vinnen, donkere kop
        'species': {'basculin': {'body': [9, 11, 10], 'stripe': [8, 7], 'fins': [3, 4, 2], 'head': [6, 5]}},
        'variants': [
            {'naam': 'Rode piranha (zilver met rood)', 'body': '#a8a8b0', 'stripe': '#d02020', 'fins': '#606870', 'head': '#3a4048'},
            {'naam': 'Koi (wit met oranje)', 'body': ('#ece8e0', {'l': 1.3}), 'stripe': '#f07020', 'fins': '#f0b080',
             'head': '#e04020'},
            {'naam': 'Zwarte piranha (rode streep)', 'body': ('#38383e', DARK), 'stripe': '#c02020', 'fins': '#5a5a68',
             'head': '#24242c'},
            {'naam': 'Neontetra (blauw met rode streep)', 'body': '#3070e0', 'stripe': '#e02030', 'fins': '#c8e0f0',
             'head': '#1c3070'},
            {'naam': 'Goudvis (oranje, witte streep)', 'body': '#f08020', 'stripe': '#f8f0d0', 'fins': '#f8c060',
             'head': '#c04010'},
            {'naam': 'Arowana (drakenvis met gouden schubben)', 'body': ('#d8a828', {'h': 0}), 'stripe': '#c02040',
             'fins': '#f0e0a0', 'head': '#6a4a18'},
        ],
    },
    'deerling': {
        # alleen de lentevorm (seizoensvormen zijn kleurvormen): vacht, crème, bloem/bloesem
        'species': {
            'deerling': {'body': [7, 3, 1], 'cream': [8, 12, 9], 'flower': [5, 4, 6]},
            'sawsbuck': {'body': [11, 8, 9, 5], 'cream': [6, 12], 'flower': [7, 3, 4], 'gold': [10]},
        },
        'variants': [
            {'naam': 'Rendier (grijsbruin, rode bloem van Rudolph)', 'body': '#8a7a6a', 'sawsbuck:body': '#7a7470', 'cream': '#e8e0d0', 'flower': '#e02020',
             'gold': '#d8ccb8'},
            {'naam': 'Sikahert (kastanje, witte bloesem)', 'body': '#a05a38', 'sawsbuck:body': '#8a3a20', 'cream': '#f0e0c8',
             'flower': ('#f4f4ec', {'l': 1.3}), 'gold': '#f8f0e0'},
            {'naam': 'Lavendelveld (lila met paarse bloem)', 'body': '#b098d0', 'sawsbuck:body': '#8a70b0', 'cream': '#f0e8f4',
             'flower': '#7040b0', 'gold': '#7040b0'},
            {'naam': 'Witte hinde (Arthurlegende, roze bloesem)', 'body': ('#e0dcd4', {'l': 1.4}), 'cream': '#fcf8f0',
             'flower': '#f0a0c0', 'gold': '#f0a0c0'},
            {'naam': 'Shishigami (Mononoke: mosgroen, rode bloem)', 'body': '#5a7a40', 'cream': '#c8d8a0', 'flower': '#e04050',
             'gold': '#e04050'},
            {'naam': 'Hinde van Ceryneia (goud, zilveren bloesem)', 'body': ('#d8a828', {'h': 0}), 'cream': '#f8f0d0',
             'flower': '#d8dce8', 'gold': '#d8dce8'},
        ],
    },
}
