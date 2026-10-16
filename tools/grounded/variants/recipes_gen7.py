"""Kleurvarianten, generatie 7 (Alola). Formaat: zie recipes.py."""

ALBINO = {'l': 1.0}
DARK = {'l': 1.3}

LINES = {
    'rowlet': {
        # blad (strik/kap), bruin lijf/mantel, wit gezicht, grijze buik (Rowlet), snavel/poten, punten (Decidueye)
        'species': {
            'rowlet': {'body': [1, 2, 3], 'white': [4], 'grey': [5, 6], 'beak': [8, 9, 10], 'leaf': [11, 12, 13]},
            'dartrix': {'leaf': [1, 2, 4], 'body': [3, 5, 10], 'white': [7, 8, 9], 'beak': [11, 12, 13]},
            'decidueye': {'leaf': [8, 9, 10], 'tips': [11, 12], 'white': [1, 2, 5], 'body': [13, 14, 15],
                          'beak': [4, 6, 7]},
            'decidueye/hisui': {'leaf': [3, 7, 8], 'body': [1, 4, 9, 12], 'beak': [10, 11], 'white': [6, 13, 15]},
        },
        'variants': [
            {'naam': 'Kerkuil (goudbruin, hartvormig wit gezicht, herfstblad)', 'body': '#c89850', 'white': '#f8f4ec',
             'grey': '#e0d0b0', 'beak': '#e8d0b0', 'leaf': '#e07020', 'tips': '#a04010'},
            {'naam': 'Sneeuwuil (Hedwig: wit, zwarte snavel, berijpte den)', 'body': '#d8d8d8', 'white': '#f8f8f8',
             'grey': '#b8b8c0', 'beak': '#404048', 'leaf': '#6890a0', 'tips': '#304858'},
            {'naam': 'Kersenbloesem (roze blad, crème veren)', 'body': '#d8b8a0', 'white': '#fff0f4',
             'grey': '#c8a0a8', 'beak': '#806070', 'leaf': '#f090b8', 'tips': '#a04878'},
            {'naam': 'Laplanduil (zilvergrijs met zilverspar)', 'body': '#808890', 'white': '#e0e0e8',
             'grey': '#686870', 'beak': '#e0c040', 'leaf': '#88b8c8', 'tips': '#405870',
             'decidueye/hisui:leaf': '#4878a0'},
            {'naam': 'Spookschutter (zwart met paars dwaallicht: Grass/Ghost)', 'body': ('#383040', DARK),
             'white': '#9088a0', 'grey': '#484050', 'beak': '#e04080', 'leaf': '#8040d0', 'tips': '#40e0c0'},
            {'naam': 'Uil van Athena (goud met olijfgroene lauwerkrans)', 'body': ('#d8a830', {'h': 0}),
             'white': '#f8f0c8', 'grey': '#c0a060', 'beak': '#c03028', 'leaf': '#808830', 'tips': '#405018'},
        ],
    },
    'litten': {
        # vacht, rode strepen, ogen/belletje (geel), vlamgordel en grijze buik (Incineroar)
        'species': {
            'litten': {'fur': [1, 3, 5], 'red': [7, 8, 12], 'eyes': [9, 10]},
            'torracat': {'fur': [1, 2, 7], 'red': [4, 5, 6], 'eyes': [10, 11]},
            'incineroar': {'fur': [3, 5], 'red': [2, 4, 6], 'flame': [7, 14], 'belly': [10, 11, 13], 'eyes': [8]},
        },
        'variants': [
            {'naam': 'Bengaalse tijger (oranje vacht, zwarte strepen)', 'fur': '#d87830', 'red': ('#383038', DARK),
             'eyes': '#60d040', 'flame': '#f8e060', 'belly': '#e8e0d0'},
            {'naam': 'Sneeuwluipaard (rookgrijs, leigrijze strepen, ijsogen)', 'fur': '#b0b0b8', 'red': '#585868',
             'eyes': '#80c8f0', 'flame': '#a0d8f8', 'belly': '#e8e8f0'},
            {'naam': 'Blauw vuur (nachtblauw, cyaan vlammen)', 'fur': ('#283050', DARK), 'red': '#30a0f0',
             'eyes': '#f0c040', 'flame': '#60f0f0', 'belly': '#506080'},
            {'naam': 'Hulkamania (Hulk Hogan: rood en geel)', 'fur': '#c02020', 'red': '#f0d020',
             'eyes': '#3070e0', 'flame': '#f8f0a0', 'belly': '#d8a070'},
            {'naam': 'Nekomata (spookkat-yokai: paars met groene ogen)', 'fur': ('#403050', DARK), 'red': '#b048e0',
             'eyes': '#60f060', 'flame': '#e080f8', 'belly': '#9080a8'},
            {'naam': 'Sekhmet (gouden leeuwengodin met robijn)', 'fur': ('#d8a830', {'h': 0}), 'red': '#b01830',
             'eyes': '#30c0e0', 'flame': '#f8f8e0', 'belly': '#f0e0b0'},
        ],
    },
    'popplio': {
        # lijf, kraag/haar, neus/parels (roze), wit (snuit/ruches), vinnen en huid (Primarina)
        'species': {
            'popplio': {'body': [1, 2, 3, 8], 'pink': [4, 5, 7], 'hair': [6, 14, 15], 'white': [10, 11, 12]},
            'brionne': {'body': [8, 9, 10], 'white': [1, 2, 4], 'hair': [3, 5, 6], 'pink': [11, 13, 14]},
            'primarina': {'hair': [1, 3, 5], 'body': [4, 6], 'white': [2, 9, 11], 'pink': [8, 10, 12],
                          'fin': [13, 14, 15]},
        },
        'variants': [
            {'naam': 'Zeeleeuw (bruin, crème snuit)', 'body': '#806048', 'hair': '#d0b080', 'pink': '#303030',
             'white': '#e8d8c0', 'primarina:body': '#c8a888', 'fin': '#604030'},
            {'naam': 'De kleine zeemeermin (rood haar, groene staart, lila schelpen)', 'body': '#30a088',
             'hair': '#e03028', 'pink': '#b088e0', 'white': '#f8f8f8', 'primarina:body': '#f0c8b0', 'fin': '#20a078'},
            {'naam': 'Pierrot (wit gezicht, zwarte ruches, rode neus)', 'body': '#e0e0e8', 'hair': ('#383840', DARK),
             'pink': '#e02030', 'white': '#f8f8f8', 'primarina:body': '#f0f0f8', 'fin': '#404048'},
            {'naam': 'Orka (zwart met witte kraag, gouden bal)', 'body': ('#38383c', DARK),
             'hair': '#f0f0f0', 'pink': '#f0c040', 'white': '#f8f8f8', 'primarina:body': '#c8c8d0',
             'fin': ('#303034', DARK)},
            {'naam': 'Barbie (roze met blond haar)', 'body': '#f080b0', 'hair': '#f8e080', 'pink': '#40c0e0',
             'white': '#f8f8f8', 'primarina:body': '#f8c0d8', 'fin': '#e04090'},
            {'naam': 'Ranchu-goudvis (oranje met witte sluier)', 'body': '#f07028', 'hair': '#f8f0d0',
             'pink': '#e02020', 'white': '#f8f0e0', 'primarina:body': '#f8b070', 'fin': '#e05020'},
        ],
    },
    'pikipek': {
        # lijf, wit, snavel/kuif/keel (rood-oranje), gele snavelpunt (Toucannon), blauw (ogen, poten, gezicht)
        'species': {
            'pikipek': {'beak': [1, 2], 'body': [4, 5, 11], 'white': [6, 7, 9], 'blue': [8]},
            'trumbeak': {'body': [1, 2, 4], 'white': [5, 6, 7, 8], 'blue': [9, 14], 'beak': [10, 11, 12, 13, 15]},
            'toucannon': {'body': [2, 3, 6], 'beak': [4, 7], 'beak2': [9, 11, 14], 'blue': [5, 8, 12],
                          'white': [10, 13, 15]},
        },
        'variants': [
            {'naam': 'Groene specht (olijfgroen, rode kuif)', 'body': '#587838', 'white': '#e0e8b8',
             'beak': '#d82020', 'beak2': '#f0c030', 'blue': '#383838'},
            {'naam': 'Kaneel (roodbruin met crème, gouden snavel)', 'body': '#985030', 'white': '#f0d8b0',
             'beak': '#e8b020', 'beak2': '#f8f0a0', 'blue': '#40b0a0'},
            {'naam': 'Woody Woodpecker (blauw, rode kuif, gele snavel)', 'body': '#3868c0', 'white': '#f8f8f8',
             'beak': '#e02020', 'beak2': '#f8d030', 'blue': '#f0a020'},
            {'naam': 'Albino (roze snavel)', 'body': ('#d8d8dc', ALBINO), 'white': '#f8f8f8', 'beak': '#f08098',
             'beak2': '#f8c8d0', 'blue': '#e05060'},
            {'naam': 'Miami Vice (aubergine met neonroze en cyaan)', 'body': ('#382840', DARK), 'white': '#f0c8e8',
             'beak': '#f040a0', 'beak2': '#40e0f0', 'blue': '#40f0a0'},
            {'naam': 'Gouden kanon (goud met robijnrode snavel)', 'body': ('#d0a030', {'h': 0}), 'white': '#f8f0c8',
             'beak': '#c01830', 'beak2': '#f05050', 'blue': '#3050d0'},
        ],
    },
    'yungoos': {
        # vacht, gele manen/jas, roze (oren, neus)
        'species': {
            'yungoos': {'fur': [3, 5, 6], 'yellow': [1, 2, 4], 'pink': [7]},
            'gumshoos': {'fur': [3, 4, 8], 'yellow': [1, 2, 6], 'pink': [12]},
        },
        'variants': [
            {'naam': 'Stokstaartje (zandbruin met donkere manen)', 'fur': '#c8a878', 'yellow': '#705038',
             'pink': '#303030'},
            {'naam': 'Sherlock Holmes (groen tweed, bruine deerstalker)', 'fur': '#6a7048', 'yellow': '#a07850',
             'pink': '#c08070'},
            {'naam': 'Rikki-Tikki-Tavi (Kipling: roodbruin met zilver)', 'fur': '#b05030', 'yellow': '#d0d0d8',
             'pink': '#f0a0a0'},
            {'naam': 'Film noir (zwart-wit)', 'fur': ('#505058', DARK), 'yellow': '#e8e8e8', 'pink': '#c0c0c0'},
            {'naam': 'Roze Panter (roze met witte manen)', 'fur': '#e088b0', 'yellow': '#f8f0f4', 'pink': '#f04080'},
            {'naam': 'Gouden detectivepenning (goud met nachtblauwe manen)', 'fur': ('#d8a830', {'h': 0}),
             'yellow': '#283870', 'pink': '#e04040'},
        ],
    },
    'grubbin': {
        # hoofd/lijf (Grubbin oranje, Charjabug groen, Vikavolt teal), geel/oranje accent, wit/grijs, ramen/blauw
        'species': {
            'grubbin': {'main': [2, 4, 5, 11, 12], 'yellow': [8, 9], 'white': [1, 3, 7]},
            'charjabug': {'main': [1, 2, 3, 4], 'blue': [7, 10, 14], 'yellow': [11, 12, 13], 'white': [8, 9, 15]},
            'vikavolt': {'main': [1, 3, 4], 'white': [5, 6, 7], 'yellow': [10, 12], 'blue': [13, 14]},
        },
        'variants': [
            {'naam': 'Duracell (zwart en koper)', 'main': ('#383838', DARK), 'yellow': '#d88830', 'white': '#c8c8d0',
             'blue': '#f0c040'},
            {'naam': 'Witte oplader (wit en grijs met groene laadled)', 'main': ('#e0e0e4', ALBINO),
             'yellow': '#8890a0', 'white': '#c8c8d0', 'blue': '#70e040', 'grubbin:yellow': '#70e040'},
            {'naam': 'Glimworm (bruin met groengeel licht)', 'main': '#685038', 'yellow': '#c8f040',
             'white': '#e0e0c0', 'blue': '#a0f060'},
            {'naam': 'Tron (zwart met cyaan licht)', 'main': ('#202838', DARK), 'yellow': '#40e0f0',
             'white': '#606878', 'blue': '#40f0f0'},
            {'naam': 'Juwelkever (Chrysochroa: paars metaal met rood)', 'main': '#9030a0', 'yellow': '#f04040',
             'white': '#e0c0f0', 'blue': '#40c0f0'},
            {'naam': 'Gouden scarabee (goud met lapis lazuli)', 'main': ('#d8a830', {'h': 0}), 'yellow': '#2050c0',
             'white': '#f8f0d0', 'blue': '#40c0f0'},
        ],
    },
    'crabrawler': {
        # schild/klauwschalen, vuisten, crème (sprieten/buik), vacht (Crabominable)
        'species': {
            'crabrawler': {'shell': [9, 10, 13], 'fist': [3, 4, 5, 8], 'tan': [1, 2, 7]},
            'crabominable': {'fur': [1, 2, 5], 'shell': [4, 7, 8], 'fist': [6, 9, 10], 'tan': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Gekookte kreeft (rood)', 'shell': '#c83020', 'fist': '#e86030', 'tan': '#f0d8b0',
             'fur': '#f0d8c8'},
            {'naam': 'Wenkkrab (nachtblauw met oranje scharen)', 'shell': '#304060', 'fist': '#f09020',
             'tan': '#e0e0c8', 'fur': '#d8e0e8'},
            {'naam': 'Spookkrab (bleek zand)', 'shell': '#c8b088', 'fist': '#f0e8d0', 'tan': '#a08060',
             'fur': '#e8e0d0'},
            {'naam': 'Rocky Balboa (zwart met rode handschoenen)', 'shell': ('#383038', DARK), 'fist': '#d02020',
             'tan': '#f0c890', 'fur': '#909098'},
            {'naam': 'Kokoskrab (blauwpaars met oranje)', 'shell': '#5040c0', 'fist': '#f05030', 'tan': '#e0a060',
             'fur': '#c8c0f0'},
            {'naam': 'Golden Gloves (goud op nachtblauw)', 'shell': ('#283068', DARK), 'fist': ('#e8b020', {'h': 0}),
             'tan': '#f8f0c0', 'fur': '#f8e8b0'},
        ],
    },
    'cutiefly': {
        # wit (vleugels/pluis), vlekken (vleugelstippen), geel lijf, bruin (sjaal/poten, Ribombee)
        'species': {
            'cutiefly': {'white': [1, 2, 5, 12], 'spots': [3, 4], 'yellow': [7, 8, 11]},
            'ribombee': {'white': [1, 2, 3, 10], 'spots': [6, 8, 15], 'yellow': [7, 9, 11], 'brown': [12, 13, 14]},
        },
        'variants': [
            {'naam': 'Honingbij (oranje met bruine stippen)', 'yellow': '#f0a020', 'spots': '#c08040',
             'brown': '#604020', 'white': '#f8f0e0'},
            {'naam': 'Blauwe houtbij (Xylocopa: blauwzwart met blauwe vleugels)', 'yellow': ('#404058', DARK),
             'spots': '#4060d0', 'brown': '#282838', 'white': '#c8d8f8'},
            {'naam': 'Lavendel (paars stuifmeel)', 'yellow': '#b080e0', 'spots': '#8050c0', 'brown': '#604880',
             'white': '#f0e8f8'},
            {'naam': 'Aardbei (rood met groene kroontjes)', 'yellow': '#e03040', 'spots': '#48a848',
             'brown': '#286028', 'white': '#fff4f0'},
            {'naam': 'Tinkerbell (groen jurkje, gouden feeënstof)', 'yellow': '#60c050', 'spots': '#f0d040',
             'brown': '#306030', 'white': '#f0f8e0'},
            {'naam': 'Klimt (bladgoud met zwarte ornamenten)', 'yellow': ('#e0b020', {'h': 0}), 'spots': '#282020',
             'brown': '#382818', 'white': '#f0e0a0'},
        ],
    },
    'rockruff': {
        # vacht, crème manen/kraag, donkere rotsen/poten, ogen (Midnight: rode manen via eigen sleutel)
        'species': {
            'rockruff': {'fur': [1, 2, 3], 'cream': [9, 10, 11], 'rock': [5, 7, 8], 'eyes': [12]},
            'lycanroc': {'fur': [7, 8, 9], 'cream': [3, 6, 11], 'rock': [1, 2, 5], 'eyes': [13]},
            'lycanroc/dusk': {'fur': [7, 8, 14], 'cream': [3, 6, 11], 'rock': [1, 2, 5], 'eyes': [13]},
            'lycanroc/midnight': {'fur': [8, 10, 12, 13], 'cream': [3, 6, 11], 'rock': [1, 2, 5]},
        },
        'variants': [
            {'naam': 'Grijze wolf (gele ogen)', 'fur': '#888890', 'cream': '#e0e0e0', 'rock': '#404048',
             'eyes': '#f0c030', 'lycanroc/midnight:fur': '#5878a8'},
            {'naam': 'Poolwolf (wit met ijsblauwe ogen)', 'fur': '#e0e0e4', 'cream': '#f8f8f8', 'rock': '#808088',
             'eyes': '#60b0f0', 'lycanroc/midnight:fur': '#80b8e8'},
            {'naam': 'Dobermann (zwart met roestbruin)', 'fur': ('#383038', DARK), 'cream': '#b06030',
             'rock': '#282428', 'eyes': '#f0a020', 'lycanroc/midnight:fur': '#c06830',
             'lycanroc/midnight:cream': ('#403840', DARK)},
            {'naam': 'Amethistgeode (paars met kristal)', 'fur': '#7050a0', 'cream': '#d8c8f0', 'rock': '#c0a0f0',
             'eyes': '#f0e060', 'lycanroc/midnight:fur': '#a050e0'},
            {'naam': 'Lapis lazuli (blauw met goudvlekken)', 'fur': '#2848a0', 'cream': '#d8d8f0', 'rock': '#e0b030',
             'eyes': '#f0f0f0', 'lycanroc/midnight:fur': '#e0b030'},
            {'naam': 'Lupa Capitolina (bronzen wolvin van Rome)', 'fur': ('#c09030', {'h': 0}), 'cream': ('#f8e8b8', {'h': 0}),
             'rock': '#805020', 'eyes': '#30a060', 'lycanroc/midnight:fur': '#c02030'},
        ],
    },
    'mareanie': {
        # tentakels (teal), lijf/kern (paars-roze), gouden kroon/oogring, stekels (Toxapex)
        'species': {
            'mareanie': {'teal': [8, 9, 11], 'purple': [3, 4, 6, 10], 'gold': [1, 2, 5]},
            'toxapex': {'teal': [5, 6, 7, 8, 9, 10], 'purple': [11, 12, 13, 14], 'gold': [15], 'spikes': [1, 3, 4]},
        },
        'variants': [
            {'naam': 'Doornenkroonzeester (grijsgroen met rode stekels)', 'teal': '#708868', 'purple': '#c04030',
             'gold': '#f0d040', 'spikes': '#e02020'},
            {'naam': 'Blauwgeringde octopus (geel met blauwe ringen)', 'teal': '#e0c040', 'purple': '#3050d0',
             'gold': '#40c0f0', 'spikes': '#3050d0'},
            {'naam': 'IJskoraal (wit met ijsblauw)', 'teal': '#d8e8f0', 'purple': '#60a0e0', 'gold': '#f8f8f8',
             'spikes': '#a0d0f0'},
            {'naam': 'Gifgroen (giftige zee-egel)', 'teal': '#60c040', 'purple': '#402850', 'gold': '#f0f040',
             'spikes': '#a0f060'},
            {'naam': 'Vuurkoraal (zwart met oranje)', 'teal': ('#383040', DARK), 'purple': '#f08020',
             'gold': '#f0d040', 'spikes': '#f05020'},
            {'naam': 'Ursula (De kleine zeemeermin: lila met zwart)', 'teal': '#a080d0', 'purple': ('#302838', DARK),
             'gold': '#f0c040', 'spikes': '#e04080'},
        ],
    },
    'mudbray': {
        # lijf, manen, modderpoten/klei
        'species': {
            'mudbray': {'body': [1, 2, 4], 'mane': [5, 6, 8], 'mud': [10, 11, 12]},
            'mudsdale': {'body': [6, 9], 'mane': [3, 7, 8], 'mud': [2, 4, 5]},
        },
        'variants': [
            {'naam': 'Appelschimmel (grijswit met grijze manen)', 'body': '#d0d0c8', 'mane': '#606068',
             'mud': '#909098'},
            {'naam': 'Palomino (goudgeel met witte manen)', 'body': '#e0b060', 'mane': '#f8f0e0', 'mud': '#f0e0c0'},
            {'naam': 'Terracottaleger (Xi\'an-kleisoldaten)', 'body': '#c07850', 'mane': '#704030', 'mud': '#a05838'},
            {'naam': 'Black Beauty (zwart met witte sokken)', 'body': ('#383840', DARK), 'mane': '#686878',
             'mud': '#e8e8e8'},
            {'naam': 'Delfts blauw (porselein)', 'body': '#4870b0', 'mane': '#f0f0f8', 'mud': '#283870'},
            {'naam': 'Thracisch goud (goud met lapis manen)', 'body': ('#d0a030', {'h': 0}), 'mane': '#2848a0',
             'mud': '#805020'},
        ],
    },
    'dewpider': {
        # waterbel, lijf, poten (geelgroen), bruine strepen (Araquanid)
        'species': {
            'dewpider': {'bubble': [1, 2, 3], 'body': [7, 8, 9, 10, 12], 'legs': [4, 5, 6]},
            'araquanid': {'bubble': [1, 2, 3, 13], 'body': [9, 10, 14, 15], 'legs': [6, 7, 8], 'brown': [11, 12]},
        },
        'variants': [
            {'naam': 'Kruisspin (bruin en oranje)', 'legs': '#a06030', 'body': '#c08040', 'bubble': '#d0e0e0',
             'brown': '#f0e0c0'},
            {'naam': 'Zwarte weduwe (zwart met rood)', 'legs': ('#383038', DARK), 'body': '#d02020',
             'bubble': '#d0d0d8', 'brown': '#f03030'},
            {'naam': 'Pauwspin (Maratus: blauw, oranje en rood)', 'legs': '#3050c0', 'body': '#f08020',
             'bubble': '#c0e0f8', 'brown': '#d02020'},
            {'naam': 'Groene lynxspin (felgroen)', 'legs': '#40c040', 'body': '#90e070', 'bubble': '#e0f8d0',
             'brown': '#e04040'},
            {'naam': 'Roze-teen-vogelspin (Avicularia: zwart met roze tenen)', 'legs': '#e070a0',
             'body': ('#383040', DARK), 'bubble': '#e8d0e0', 'brown': '#f0a0c0'},
            {'naam': 'Gouden zijdespin (Nephila: goudweb)', 'legs': ('#e0b020', {'h': 0}), 'body': '#584830',
             'bubble': '#f8f0b0', 'brown': '#c03030'},
        ],
    },
    'fomantis': {
        # roze (bloem/lijf), blad (Fomantis' kruin), groen (bladeren/kraag), wit (Lurantis' sikkels)
        'species': {
            'fomantis': {'pink': [9, 10, 11, 13, 14, 15], 'leaf': [1, 2, 3], 'green': [5, 6, 7, 8]},
            'lurantis': {'pink': [1, 2, 4, 6, 12, 13], 'green': [3, 5, 8], 'white': [9, 10, 11]},
        },
        'variants': [
            {'naam': 'Witte orchideebidsprinkhaan (wit met lila)', 'pink': '#f0e0f0', 'leaf': '#e8c0e0',
             'green': '#70a060', 'white': '#d0a8e0'},
            {'naam': 'Hibiscus (rood met geel)', 'pink': '#e02030', 'leaf': '#206030', 'green': '#f0d040',
             'white': '#f8e050'},
            {'naam': 'Iris (paars met geel hart)', 'pink': '#8050c0', 'leaf': '#4060c0', 'green': '#509060',
             'white': '#f0d040'},
            {'naam': 'Zonnebloem (geel met bruin)', 'pink': '#f0c020', 'leaf': '#60902c', 'green': '#704020',
             'white': '#f8f0c0'},
            {'naam': 'Spookbidsprinkhaan (Phyllocrania: dor blad)', 'pink': '#906848', 'leaf': '#605030',
             'green': '#a08050', 'white': '#d0c0a0'},
            {'naam': 'Zwarte tulp (Dumas)', 'pink': ('#402838', DARK), 'leaf': '#5a2848', 'green': '#305838',
             'white': '#a090b0'},
        ],
    },
    'morelull': {
        # hoed (paars), roze hoedrand/lijf, gloeistippen, steel, groen (voetjes/plaatjes)
        'species': {
            'morelull': {'pink': [1, 3], 'cap': [2, 5, 7, 15], 'spots': [6, 8], 'stem': [9, 10, 11, 12],
                         'green': [13, 14]},
            'shiinotic': {'cap': [2, 5, 7], 'pink': [8, 9, 10, 15], 'green': [1, 3, 4], 'stem': [11, 12, 13, 14]},
        },
        'variants': [
            {'naam': 'Vliegenzwam (rood met witte stippen)', 'cap': '#d02020', 'pink': '#f04030', 'spots': '#f8f8f8',
             'stem': '#f8f0e0', 'green': '#f0e8d0'},
            {'naam': 'Cantharel (dooiergeel)', 'cap': '#e0a020', 'pink': '#f0c040', 'spots': '#f8e8a0',
             'stem': '#f0d080', 'green': '#c08020'},
            {'naam': 'Lichtgevende Mycena (groen gloeiend)', 'cap': '#304030', 'pink': '#80f060', 'spots': '#c0ff80',
             'stem': '#a0c090', 'green': '#60d040'},
            {'naam': 'Indigo-melkzwam (Lactarius indigo)', 'cap': '#3858a8', 'pink': '#6080d0', 'spots': '#a0c0f0',
             'stem': '#8090b0', 'green': '#304880'},
            {'naam': 'Bloedende tandzwam (Hydnellum peckii: wit met rode druppels)', 'cap': '#f0e8e8',
             'pink': '#e02030', 'spots': '#f03040', 'stem': '#d8c8c0', 'green': '#a08080'},
            {'naam': 'Super Mario 1-UP (groen met witte stippen)', 'cap': '#30a040', 'pink': '#50c050',
             'spots': '#f8f8f8', 'stem': '#f8e8c8', 'green': '#208030'},
        ],
    },
    'salandit': {
        # lijf (donkergrijs), roze/oranje accenten (staartpunt, zijkanten), sjerp (Salazzle blauwpaars), kuif/ogen
        'species': {
            'salandit': {'body': [1, 2, 5, 6, 7, 12, 13], 'pink': [4, 15], 'crest': [9, 10, 11], '_base': {'body': 6}},
            'salazzle': {'body': [1, 2, 4], 'pink': [9, 11, 12], 'sash': [6, 8, 10], 'crest': [5, 7],
                         '_base': {'body': 4}},
        },
        'variants': [
            {'naam': 'Gilamonster (zalmoranje met zwarte banden)', 'body': '#d88858', 'pink': '#282828',
             'sash': '#383030', 'crest': '#f0e0c0'},
            {'naam': 'Axolotl (roze met dieproze kieuwen)', 'body': '#e8a8b8', 'pink': '#d03070', 'sash': '#f8e0e8',
             'crest': '#c04080'},
            {'naam': 'Blauwe pijlgifkikker (blauw met zwart)', 'body': '#3058c0', 'pink': '#202838',
             'sash': '#80c0f0', 'crest': '#f0f0f0'},
            {'naam': 'Poison Ivy (groen met rood)', 'body': '#307838', 'pink': '#d02030', 'sash': '#80c040',
             'crest': '#f0d040'},
            {'naam': 'Lavastroom (donkerrood met gloeiend oranje)', 'body': '#902018', 'pink': '#f8a020',
             'sash': '#f05010', 'crest': '#f8e060'},
            {'naam': 'Cruella de Vil (wit en zwart, rode handschoenen)', 'body': '#d8d8dc', 'pink': '#d02020',
             'sash': ('#303030', DARK), 'crest': '#303030'},
        ],
    },
    'stufful': {
        # roze vacht, wit (gezicht/oren), donker (armen/lijf), kussentjes (Stufful)
        'species': {
            'stufful': {'pink': [5, 6, 7], 'white': [1, 2, 4], 'dark': [8, 9, 11], 'pads': [10, 12]},
            'bewear': {'pink': [1, 2, 7, 11], 'white': [3, 4, 6], 'dark': [8, 9, 10]},
        },
        'variants': [
            {'naam': 'Teddybeer (bruin met crème)', 'pink': '#a87048', 'white': '#e8d0b0', 'dark': '#503828',
             'pads': '#f0c0a0'},
            {'naam': 'IJsbeer (wit met zwarte neus)', 'pink': '#e4e4dc', 'white': '#f8f8f8', 'dark': '#a0a8b0',
             'pads': '#303030'},
            {'naam': 'Knorrige Troetelbeer (blauw)', 'pink': '#6090d0', 'white': '#c8dcf0', 'dark': '#304070',
             'pads': '#f0f0f0'},
            {'naam': 'Gummibeer (doorschijnend groen)', 'pink': '#60d060', 'white': '#c8f0a8', 'dark': '#208030',
             'pads': '#f0f040'},
            {'naam': 'Lotso (Toy Story: lila aardbeienbeer)', 'pink': '#c090d8', 'white': '#f0e0f0',
             'dark': '#704888', 'pads': '#e04080'},
            {'naam': 'Steiff-teddy (goud mohair, knoop in het oor)', 'pink': ('#d8a840', {'h': 0}),
             'white': '#f8f0c8', 'dark': '#704818', 'pads': '#c03030'},
        ],
    },
    'bounsweet': {
        # vrucht/lijf (roze), blad, wit (rok/beenkappen), geel (kelk/stippen)
        'species': {
            'bounsweet': {'pink': [5, 6, 7, 8, 11], 'leaf': [1, 2, 3], 'white': [12, 13, 14]},
            'steenee': {'leaf': [1, 2, 3], 'pink': [8, 9, 11, 12, 13], 'white': [6, 7, 10], 'yellow': [5]},
            'tsareena': {'leaf': [2, 7, 8, 14], 'pink': [1, 3, 5, 6, 10], 'yellow': [4], 'white': [11, 12, 13, 15]},
        },
        'variants': [
            {'naam': 'Blauwe bes (berijpt blauw, saliegroen blad)', 'pink': '#5060b0', 'leaf': '#90b0a0',
             'white': '#e8e8f8', 'yellow': '#c0c8f0'},
            {'naam': 'Mandarijn (oranje, donker glanzend blad)', 'pink': '#f09020', 'leaf': '#205830',
             'white': '#f8f0e0', 'yellow': '#f8e040'},
            {'naam': 'Witte aardbei (pineberry: wit met rode pitjes)', 'pink': '#f0e8e0', 'leaf': '#a0d070',
             'white': '#f8d0d0', 'yellow': '#e03030'},
            {'naam': 'Druif (paars met herfstblad)', 'pink': '#7040a0', 'leaf': '#c08030', 'white': '#e0d0f0',
             'yellow': '#a0c040'},
            {'naam': 'Boze koningin (Sneeuwwitje: zwart, paars en goud)', 'pink': ('#302838', DARK),
             'leaf': '#5a2878', 'white': '#c0b0d0', 'yellow': '#e0b020'},
            {'naam': 'Gouden appel van de Hesperiden (goud met zilverblad)', 'pink': ('#e0b020', {'h': 0}),
             'leaf': '#b8c0c8', 'white': '#f8f8f0', 'yellow': '#f04040'},
        ],
    },
    'comfey': {
        # bladkrans, rode/gele/roze bloemen, witte bloemen
        'species': {
            'comfey': {'leaf': [1, 2, 3], 'red': [5, 13, 14], 'yellow': [6, 8, 10], 'pink': [12, 15],
                       'white': [7, 9, 11]},
        },
        'variants': [
            {'naam': 'Frangipani-lei (wit en geel, donker blad)', 'red': '#f8f0e0', 'yellow': '#f8d040',
             'pink': '#f8e0a0', 'white': '#f0f0f0', 'leaf': '#2e7040'},
            {'naam': 'Hortensia (blauw en lila)', 'red': '#5070d0', 'yellow': '#a080e0', 'pink': '#80b0f0',
             'white': '#e0e8f8', 'leaf': '#507858'},
            {'naam': 'Herfstkrans (oranje en roest, bruin blad)', 'red': '#c04010', 'yellow': '#e08020',
             'pink': '#a06030', 'white': '#f0d8a0', 'leaf': '#806020'},
            {'naam': 'Hulstkrans (Kerst: rood en wit, donkergroen)', 'red': '#d01818', 'yellow': '#f8f8f8',
             'pink': '#e03030', 'white': '#f8f8f8', 'leaf': '#1a5028'},
            {'naam': 'Día de los Muertos (cempasúchil-oranje en magenta)', 'red': '#f08000', 'yellow': '#f0a000',
             'pink': '#e02090', 'white': '#f0e0f0', 'leaf': '#702878'},
            {'naam': 'Gouden lauwerkrans (Olympia)', 'red': '#e0b020', 'yellow': '#f8e080', 'pink': '#c08020',
             'white': '#f8f0c0', 'leaf': ('#d0a030', {'h': 0})},
        ],
    },
    'oranguru': {
        # cape (paars), waaierblad, witte manen, huid, goud
        'species': {
            'oranguru': {'cape': [9, 10, 14], 'leaf': [1, 3, 7], 'white': [4, 5], 'skin': [2, 12, 13], 'gold': [6]},
        },
        'variants': [
            {'naam': 'Orang-oetan (roodbruine vacht)', 'white': '#c06030', 'cape': '#704020', 'leaf': '#c0a040',
             'skin': '#806050', 'gold': '#f0e0a0'},
            {'naam': 'Gandalf de Grijze (grijze mantel, houten staf)', 'white': '#c8c8c8', 'cape': '#686870',
             'leaf': '#8a6a40', 'skin': '#a09090', 'gold': '#f0f0f0'},
            {'naam': 'Drie wijze apen van Nikko (zwart lak met rood)', 'cape': ('#282830', DARK),
             'white': '#f0f0f0', 'leaf': '#d02020', 'skin': '#c0a090', 'gold': '#f0c040'},
            {'naam': 'Merlijn (sterrenblauw)', 'cape': '#2840a0', 'white': '#f0f0f8', 'leaf': '#e0c040',
             'skin': '#a08888', 'gold': '#f8f8a0'},
            {'naam': 'Sun Wukong (de Apenkoning: rood en goud)', 'cape': '#c01818', 'white': '#e8c060',
             'leaf': '#f0d040', 'skin': '#c09070', 'gold': '#f8f0c0'},
            {'naam': 'Jadekeizer (jade met gouden waaier)', 'cape': '#208060', 'white': '#f8f0d0',
             'leaf': ('#e0b020', {'h': 0}), 'skin': '#b0a090', 'gold': '#f04040'},
        ],
    },
    'passimian': {
        # rugbyteams: vacht, wit, bal/haar (limoen), groene strepen, geel
        'species': {
            'passimian': {'fur': [1, 2, 6, 7, 8], 'white': [4, 5, 9, 10], 'lime': [12, 13], 'green': [15],
                          'yellow': [11, 14], '_base': {'fur': 2}},
        },
        'variants': [
            {'naam': 'Oranje (Nederlands elftal)', 'lime': '#f08020', 'green': '#303030', 'yellow': '#f8f8f8',
             'fur': '#605040', 'white': '#f8f8f8'},
            {'naam': 'Springboks (groen en goud)', 'lime': '#207040', 'green': '#f0c020', 'yellow': '#f0c020',
             'fur': '#504838', 'white': '#e8e0c8'},
            {'naam': 'Les Bleus (blauw, wit, rood)', 'lime': '#3050c0', 'green': '#e02020', 'yellow': '#f8f8f8',
             'fur': '#585868', 'white': '#f8f8f8'},
            {'naam': 'Mandril (olijfvacht, rood-blauwe snuit)', 'fur': '#707040', 'white': '#c0b890',
             'lime': '#e03030', 'green': '#3070e0', 'yellow': '#f0c040'},
            {'naam': 'Wales (rode draak)', 'lime': '#d02020', 'green': '#f8f8f8', 'fur': ('#383838', DARK),
             'white': '#f0f0f0', 'yellow': '#40a040'},
            {'naam': 'Gouden bal (goud op zwart)', 'lime': ('#e0b020', {'h': 0}), 'green': '#f8f8f8',
             'fur': ('#302820', DARK), 'white': '#f8f0c8', 'yellow': '#f8f8f8'},
        ],
    },
    'wimpod': {
        # pantser, paarse delen, mauve (Golisopod), ogen
        'species': {
            'wimpod': {'shell': [5, 6, 8, 9], 'purple': [1, 2, 4], 'eyes': [10]},
            'golisopod': {'shell': [1, 3, 4, 5], 'purple': [6, 7], 'mauve': [8, 10, 11]},
        },
        'variants': [
            {'naam': 'Pissebed (leigrijs)', 'shell': '#808890', 'purple': '#505060', 'mauve': '#686870',
             'eyes': '#f0f0f0'},
            {'naam': 'Samoerai (zwart lak met rood)', 'shell': ('#383038', DARK), 'purple': '#d02020',
             'mauve': '#a02020', 'eyes': '#f0c040'},
            {'naam': 'Kreeftrood (rood met goud)', 'shell': '#d05030', 'purple': '#f0c060', 'mauve': '#903020',
             'eyes': '#282828'},
            {'naam': 'Ridder van de Ronde Tafel (zilver, blauw en goud)', 'shell': '#c0c8d0', 'purple': '#3050c0',
             'mauve': '#c0a040', 'eyes': '#f04040'},
            {'naam': 'Diepzeelicht (nachtblauw met cyaan)', 'shell': ('#283868', DARK), 'purple': '#40e0f0',
             'mauve': '#305080', 'eyes': '#f0f040'},
            {'naam': 'Gouden harnas (goud met purper)', 'shell': ('#d8b040', {'h': 0}), 'purple': '#7020a0',
             'mauve': '#a07020', 'eyes': '#40f0f0'},
        ],
    },
    'sandygast': {
        # zand, rood (schepje/vlag), metaal (schephandvat), roze en blauw (schelpen, Palossand)
        'species': {
            'sandygast': {'sand': [8, 9, 10], 'red': [5, 6, 7], 'metal': [1, 2, 3]},
            'palossand': {'sand': [5, 6, 7], 'red': [1, 3, 4], 'pink': [8, 9], 'blue': [10, 11]},
        },
        'variants': [
            {'naam': 'Noordzeestrand (grijsbeige met blauw schepje)', 'sand': '#a8a090', 'red': '#3070d0',
             'metal': '#c0c0c8', 'pink': '#f0e0b0', 'blue': '#e04040'},
            {'naam': 'Roze strand (Bermuda)', 'sand': '#f0c8c0', 'red': '#40a0e0', 'metal': '#f8f8f8',
             'pink': '#e06080', 'blue': '#40c0e0'},
            {'naam': 'Sneeuwkasteel (ijs met blauwe vlag)', 'sand': '#d0e0ec', 'red': '#3070d0', 'metal': '#8090a0',
             'pink': '#a0c8f0', 'blue': '#e8f4ff'},
            {'naam': 'Olivijnstrand (groen zand van Papakōlea)', 'sand': '#8a9a50', 'red': '#d03030',
             'metal': '#c0c0a0', 'pink': '#f0e080', 'blue': '#40c080'},
            {'naam': 'Zeeglas (gesmolten zand: turquoise met wit)', 'sand': '#70c8c0', 'red': '#f0f0f0',
             'metal': '#406060', 'pink': '#f8f8f8', 'blue': '#3080c0'},
            {'naam': 'Spookkasteel (Halloween: paars met pompoenoranje)', 'sand': '#504070', 'red': '#f08020',
             'metal': '#c0c0c0', 'pink': '#a0f060', 'blue': '#a0f060'},
        ],
    },
    'pyukumuku': {
        # lijf, roze stekels, wit (mond/hand)
        'species': {
            'pyukumuku': {'body': [5, 6, 7, 8], 'pink': [1, 2, 4], 'white': [9, 10]},
        },
        'variants': [
            {'naam': 'Gele zeekomkommer (Colochirus: geel met rode stekels)', 'body': '#d0b040', 'pink': '#e02020',
             'white': '#f8f8e0'},
            {'naam': 'Namako (Japanse zeekomkommer: olijfbruin)', 'body': '#705840', 'pink': '#c0a060',
             'white': '#e0e0c8'},
            {'naam': 'Zeeappel (Pseudocolochirus: paars met geel)', 'body': '#7040a0', 'pink': '#f0c020',
             'white': '#f0e8f8'},
            {'naam': 'Albino (wit met roze stekels)', 'body': ('#d8d8dc', ALBINO), 'pink': '#f0a0b0',
             'white': '#f8f8f8'},
            {'naam': 'Tijgerstaart-zeekomkommer (oranje met zwart)', 'body': '#c06020', 'pink': '#282828',
             'white': '#f8e0c0'},
            {'naam': 'Kosmische zeekomkommer (nachtblauw met cyaan)', 'body': ('#202858', DARK), 'pink': '#40e0f0',
             'white': '#f8f8a0'},
        ],
    },
    'type_null': {
        # Zoals Arceus: Silvally's typekleur (index 1/2, kuif en staartvin) hangt van de memory af en
        # blijft. Het lijf (zilver), de donkere poten, het rode oog en de klauwen dragen de variant, met
        # precies dezelfde doelkleuren in elke typemap. Type: Null: helm (metaal), roodbruine manen.
        'species': dict(
            [('type_null', {'body': [2, 4, 8], 'mane': [3, 6, 7], 'dark': [1, 9], 'claws': [11, 12, 13, 14], '_base': {'claws': 14},
                            'eye': [10]})] +
            [('silvally', {'body': [3, 4, 5, 6], 'dark': [9, 10], 'eye': [8], 'claws': [11, 12, 13, 14],
                           '_base': {'body': 4, 'claws': 14, 'dark': 9}})] +
            [('silvally/' + t, {'body': [3, 4, 5, 6], 'dark': [9, 10], 'eye': [8], 'claws': [11, 12, 13, 14],
                                '_base': {'body': 4, 'claws': 14, 'dark': 9}}) for t in (
                'bug', 'dark', 'dragon', 'electric', 'fairy', 'fighting', 'fire', 'flying', 'ghost', 'grass',
                'ground', 'ice', 'poison', 'psychic', 'rock', 'steel', 'water')]),
        'variants': [
            {'naam': 'Laboratoriumstaal (blauw gelegeerd, oranje klauwen)', 'body': '#7090c0', 'dark': '#283858',
             'eye': '#f0f040', 'claws': '#f08020', 'mane': '#506890'},
            {'naam': 'Roest en patina (koper met kopergroen)', 'body': '#b07040', 'dark': '#503020',
             'eye': '#40e0a0', 'claws': '#30a090', 'mane': '#806040'},
            {'naam': 'Evangelion Unit-01 (paars met neongroen)', 'body': '#7048a8', 'dark': '#40c040',
             'eye': '#f0a020', 'claws': '#40e040', 'mane': '#40c040'},
            {'naam': 'Camouflageprototype (legergroen met oker)', 'body': '#687850', 'dark': '#383820',
             'eye': '#f04020', 'claws': '#c0a040', 'mane': '#504830'},
            {'naam': 'Gladion (zwart met rood)', 'body': ('#404048', DARK), 'dark': '#c02030', 'eye': '#40f0a0',
             'claws': '#d02030', 'mane': '#282830'},
            {'naam': 'RKS-prisma (ijskristal met roze)', 'body': '#90d8e0', 'dark': '#3070a0',
             'eye': '#f040a0', 'claws': '#f080d0', 'mane': '#60b0d0'},
        ],
    },
    'komala': {
        # vacht, boomstam, oren (binnenkant), oogvlekken
        'species': {
            'komala': {'fur': [1, 2, 4], 'log': [9, 10, 11, 12, 14], 'ears': [5], 'patch': [7, 8]},
        },
        'variants': [
            {'naam': 'Echte koala (grijs met roze oren)', 'fur': '#909098', 'log': '#a07850', 'ears': '#f0d8d8',
             'patch': '#303038'},
            {'naam': 'Pyjama (roze met wit kussen)', 'fur': '#e098b8', 'log': '#e8e8f0', 'ears': '#f8e0e8',
             'patch': '#704060'},
            {'naam': 'Eucalyptus (mintgroen)', 'fur': '#80c0a0', 'log': '#706050', 'ears': '#f0e8c0',
             'patch': '#305040'},
            {'naam': 'Nachtmerrie (zwart met bloedrode stam)', 'fur': ('#383040', DARK), 'log': '#802020',
             'ears': '#d04040', 'patch': '#601818'},
            {'naam': 'Klaas Vaak (zandgoud met nachtblauw blok)', 'fur': '#d8b070', 'log': '#283868',
             'ears': '#f8f0d0', 'patch': '#806030'},
            {'naam': 'Dromenland (sterrennacht met gouden stam)', 'fur': ('#283070', DARK), 'log': '#e0b030',
             'ears': '#f0d060', 'patch': '#101838'},
        ],
    },
    'turtonator': {
        # schild, gele stekels/buik, huid, donkere schilddelen
        'species': {
            'turtonator': {'shell': [3, 5, 6], 'yellow': [7, 8, 14, 15], 'skin': [9, 10, 11], 'dark': [1, 4, 12]},
        },
        'variants': [
            {'naam': 'Afgekoelde lava (zwart met gloeiende spleten)', 'shell': ('#383038', DARK), 'yellow': '#f08020',
             'skin': '#909088', 'dark': '#201818'},
            {'naam': 'Bowser (groen schild, oranje huid)', 'shell': '#30a040', 'yellow': '#f0e0a0',
             'skin': '#e0a040', 'dark': '#205828'},
            {'naam': 'IJsvulkaan (ijsblauw met witte vlam)', 'shell': '#60a0d0', 'yellow': '#e0f8ff',
             'skin': '#a0a8b0', 'dark': '#304868'},
            {'naam': 'Amethistvulkaan (paars met roze vuur)', 'shell': '#7040b0', 'yellow': '#f080e0',
             'skin': '#a098a8', 'dark': '#301848'},
            {'naam': 'Witte fosfor (wit met groene vlam)', 'shell': '#e0e0d8', 'yellow': '#60e060', 'skin': '#787870',
             'dark': '#808078'},
            {'naam': 'Goud en platina (gouden schild, platina stekels)', 'shell': ('#d8a830', {'h': 0}),
             'yellow': '#f0f0f0', 'skin': '#706858', 'dark': '#704010'},
        ],
    },
    'togedemaru': {
        # lijf (grijs), wit, geel (wangen/stekel), bruin (handjes)
        'species': {
            'togedemaru': {'body': [4, 6, 7, 8], 'white': [9, 10, 11], 'yellow': [1, 2, 5], 'brown': [13, 14]},
        },
        'variants': [
            {'naam': 'Bruine egel', 'body': '#806048', 'white': '#e8d8c0', 'yellow': '#f0c040', 'brown': '#503020'},
            {'naam': 'Muntegel (mint met roze wangen)', 'body': '#80c8a8', 'white': '#e8f8f0',
             'yellow': '#f080a0', 'brown': '#407058'},
            {'naam': 'Pikachu (geel met rode wangen)', 'body': '#f0c830', 'white': '#f8f0c0', 'yellow': '#e02020',
             'brown': '#704020'},
            {'naam': 'Sonic (blauw, perzik, rode schoenen)', 'body': '#3060d0', 'white': '#f0c8a0',
             'yellow': '#e02020', 'brown': '#f0f0f0'},
            {'naam': 'Neonbliksem (zwart met cyaan)', 'body': ('#303040', DARK), 'white': '#686e80',
             'yellow': '#40f0f0', 'brown': '#f0f040'},
            {'naam': 'Koperen spoel (koper met kopergroen)', 'body': '#c06838', 'white': '#f0d0b0',
             'yellow': '#40c0a0', 'brown': '#603018'},
        ],
    },
    'mimikyu': {
        # vermomming (doek), getekende ogen/mond, wangen, stokstaart
        'species': {
            'mimikyu': {'cloth': [1, 3, 5], 'eyes': [4], 'cheeks': [6], 'stick': [7, 8, 9]},
            'mimikyu/busted': {'cloth': [1, 3, 5], 'eyes': [4], 'cheeks': [6], 'stick': [7, 8, 9]},
        },
        'variants': [
            {'naam': 'Raichu-kostuum (oranje met gele wangen)', 'cloth': '#e09040', 'eyes': '#503020',
             'cheeks': '#f0e040', 'stick': '#806040'},
            {'naam': 'Spooklaken (wit Halloweenlaken)', 'cloth': ('#e8e8f0', ALBINO), 'eyes': '#303040',
             'cheeks': '#a0a0b0', 'stick': '#605860'},
            {'naam': 'Kawaii-merch (roze knuffel)', 'cloth': '#f0b0c8', 'eyes': '#603040', 'cheeks': '#f04080',
             'stick': '#f8f0f0'},
            {'naam': 'Gengar-kostuum (paars met rode ogen)', 'cloth': '#7050a8', 'eyes': '#e02020',
             'cheeks': '#f0f0f0', 'stick': '#403060'},
            {'naam': 'Zombie-Pikachu (rottend groen)', 'cloth': '#90a860', 'eyes': '#402030', 'cheeks': '#c04040',
             'stick': '#504030'},
            {'naam': 'Kerstmuts (rood laken met witte rand)', 'cloth': '#d02828', 'eyes': '#f8f8f8',
             'cheeks': '#f0e040', 'stick': '#f0f0f0'},
        ],
    },
    'bruxish': {
        # lijf (roze), vinnen (paars), blauw, geel
        'species': {
            'bruxish': {'pink': [5, 6, 7], 'purple': [1, 2, 3], 'blue': [8, 9, 10], 'yellow': [11, 12, 15]},
        },
        'variants': [
            {'naam': 'Clownvis (oranje, zwart en wit)', 'pink': '#f07020', 'purple': '#303030', 'blue': '#f8f8f8',
             'yellow': '#f0a020'},
            {'naam': 'Dory (doktersvis: blauw, zwart en geel)', 'pink': '#3060d0', 'purple': '#202838',
             'blue': '#80c0f0', 'yellow': '#f0d020'},
            {'naam': 'Siamese kempvis (rood met blauwe vinnen)', 'pink': '#c02030', 'purple': '#3040c0',
             'blue': '#e04050', 'yellow': '#f080a0'},
            {'naam': 'Papegaaivis (turkoois met roze)', 'pink': '#40c0a0', 'purple': '#e060a0', 'blue': '#80e0c0',
             'yellow': '#f0e080'},
            {'naam': 'Spookvis (wit met pastel)', 'pink': ('#f0e8f0', ALBINO), 'purple': '#b8b8d8',
             'blue': '#e0eaf4', 'yellow': '#f0c0d0'},
            {'naam': 'Gouden arowana (Aziatische draakvis: goud met rood)', 'pink': ('#e0b030', {'h': 0}),
             'purple': '#c02020', 'blue': '#f8e8a0', 'yellow': '#f04040'},
        ],
    },
    'drampa': {
        # witte vacht, lijf (teal), groene manen/buik, geel (hoorns/ogen), roze
        'species': {
            'drampa': {'fur': [4, 6, 7], 'body': [1, 3, 5], 'green': [11, 13, 15], 'yellow': [8, 9, 10],
                       'pink': [12, 14], '_base': {'fur': 6}},
        },
        'variants': [
            {'naam': 'Nieuwjaarsdraak (rood met goud)', 'body': '#c02020', 'fur': '#f0e8d0', 'green': '#e0b030',
             'yellow': '#f8e060', 'pink': '#30a050'},
            {'naam': 'Falkor (Het oneindige verhaal: roze en parelwit)', 'body': '#e8b8c8', 'fur': '#f8f0f0',
             'green': '#e0a0b0', 'yellow': '#f0d080', 'pink': '#80c0f0'},
            {'naam': 'Haku (Spirited Away: wit met jade manen)', 'body': '#e0eaf0', 'fur': '#d8e4e4',
             'green': '#60c0a0', 'yellow': '#40a080', 'pink': '#e04050'},
            {'naam': 'Stormdraak (onweerswolken met bliksem)', 'body': '#304878', 'fur': '#a0a8b8',
             'green': '#80a0d0', 'yellow': '#f0f060', 'pink': '#f0f060'},
            {'naam': 'Spyro (paarse draak met goud)', 'body': '#8040c0', 'fur': '#f0e0a0',
             'green': '#f0c040', 'yellow': '#f0c040', 'pink': '#f0f040'},
            {'naam': 'Keizerlijke draak (goud met purper)', 'body': ('#d8a830', {'h': 0}), 'fur': '#f8f0e0',
             'green': '#8040a0', 'yellow': '#f04040', 'pink': '#40c0f0'},
        ],
    },
    'dhelmise': {
        # anker, goud (stuurwiel), roze (wiel/algen), kelp (bruin)
        'species': {
            'dhelmise': {'anchor': [2, 5, 9], 'gold': [1, 4, 11, 12], 'pink': [7, 8], 'kelp': [6, 10, 14, 15]},
        },
        'variants': [
            {'naam': 'Roestanker (oranjebruin met groen wier)', 'anchor': '#a05030', 'gold': '#c09040',
             'pink': '#806050', 'kelp': '#405828'},
            {'naam': 'De Vliegende Hollander (spookgroen)', 'anchor': '#607068', 'gold': '#80f080',
             'pink': '#a0b0a0', 'kelp': '#304030'},
            {'naam': 'Zeeanemoon (paars met turkoois en roze)', 'anchor': '#8050b0', 'gold': '#f0e080',
             'pink': '#40c0c0', 'kelp': '#e05080'},
            {'naam': 'Zwartbaard (zwart met goud en rood)', 'anchor': ('#383840', DARK), 'gold': '#e0b020',
             'pink': '#c02020', 'kelp': '#2a3a28'},
            {'naam': 'IJszee (Titanic: wit en blauw)', 'anchor': '#d0e0f0', 'gold': '#c0c8d0', 'pink': '#6090d0',
             'kelp': '#5878a0'},
            {'naam': 'Schat van de Black Pearl (gouden anker met parels)', 'anchor': ('#d8b040', {'h': 0}),
             'gold': '#f8f8f0', 'pink': '#f0e0e8', 'kelp': '#506030'},
        ],
    },
    'jangmo_o': {
        # schubben (goud), lijf (grijs), donker (poten/staart), rood (hart/oog)
        'species': {
            'jangmo_o': {'scale': [1, 3, 4], 'body': [5, 6, 7], 'dark': [12, 13, 14], 'red': [8, 9]},
            'hakamo_o': {'scale': [1, 2, 4, 13], 'body': [5, 6, 7], 'dark': [11, 12], 'red': [9, 10]},
            'kommo_o': {'scale': [1, 3, 4, 6, 12], 'body': [7, 13], 'dark': [8, 11, 15], 'red': [5, 14]},
        },
        'variants': [
            {'naam': 'Zilveren samoerai (zilveren schubben, zwart lijf)', 'scale': '#c8c8d0', 'body': '#585860',
             'dark': '#303034', 'red': '#3070e0'},
            {'naam': 'Griekse hopliet (brons)', 'scale': '#c07838', 'body': '#c0b098', 'dark': '#605040',
             'red': '#e02020'},
            {'naam': 'Jade-krijger (jade met goud)', 'scale': '#40b070', 'body': '#e0d8c8', 'dark': '#705848',
             'red': '#f0c020'},
            {'naam': 'Robijnharnas (rood met wit)', 'scale': '#d02030', 'body': '#e8e0e0', 'dark': '#808088',
             'red': '#f0e040'},
            {'naam': 'Obsidiaan (zwart met paars)', 'scale': '#6040a0', 'body': ('#383840', DARK),
             'dark': '#202024', 'red': '#e040f0'},
            {'naam': 'Kristaldraak (ijsblauw met roze hart)', 'scale': '#80d0f0', 'body': '#f0f4f8',
             'dark': '#6880a0', 'red': '#f04080'},
        ],
    },
    'tapu_koko': {
        # De vier Tapu's als één set (beschermgeesten; geen evolutielijn): schaal (hoofdkleur van het
        # masker/schild), accent, donker lijf, wit. Dezelfde thema's, per Tapu een eigen uitwerking.
        'species': {
            'tapu_koko': {'shell': [1, 2, 4, 14], 'accent': [5, 6, 7], 'body': [9, 10], 'white': [11, 12],
                          '_base': {'shell': 4}},
            'tapu_lele': {'shell': [1, 2, 5, 14], 'accent': [9, 10, 11], 'body': [3, 4], 'white': [6, 7]},
            'tapu_bulu': {'shell': [7, 8, 9, 14], 'accent': [4, 5, 12], 'body': [2, 6], 'white': [10, 11]},
            'tapu_fini': {'shell': [1, 2, 6, 14], 'accent': [7, 8, 9], 'body': [3, 5, 10], 'white': [11, 12]},
        },
        'variants': [
            {'naam': 'Pounamu (Maori-groensteen met eigen accent)', 'shell': '#3a8a50',
             'tapu_koko:accent': '#f0d020', 'tapu_lele:accent': '#90d8b0', 'tapu_bulu:accent': '#e03030',
             'tapu_fini:accent': '#8060e0', 'body': '#585850', 'white': '#f0f0e0'},
            {'naam': 'Koa-hout (gesneden houten masker)', 'shell': '#a06838', 'accent': '#e0c080',
             'body': '#504030', 'white': '#f0e8d8'},
            {'naam': 'Rollenwissel (elke Tapu in de kleuren van een andere)', 'tapu_koko:shell': '#e03030',
             'tapu_lele:shell': '#f0d020', 'tapu_bulu:shell': '#8060c8', 'tapu_fini:shell': '#f08cb8',
             'tapu_koko:accent': '#f0d020', 'tapu_lele:accent': '#f08020', 'tapu_bulu:accent': '#70b0f0',
             'tapu_fini:accent': '#c03060', 'body': '#585858', 'white': '#f8f8f8'},
            {'naam': 'Gebleekt koraal (wit schild, eigen accent)', 'shell': '#e8e4dc', 'tapu_koko:accent': '#f0a020',
             'tapu_lele:accent': '#f0c040', 'tapu_bulu:accent': '#e0b020', 'tapu_fini:accent': '#5080e0',
             'body': '#686870', 'white': '#f8f8f8'},
            {'naam': 'Lapis lazuli (diepblauw met goud)', 'shell': '#2840a0', 'accent': '#e0b030',
             'body': '#303850', 'white': '#f0e8c0'},
            {'naam': "Ho'okupu (gouden offergave)", 'shell': ('#d8a830', {'h': 0}), 'tapu_koko:shell': '#b06818',
             'tapu_koko:accent': '#f8f0c0', 'tapu_lele:accent': '#f8f0d8', 'tapu_bulu:accent': '#30a040',
             'tapu_fini:accent': '#3070d0', 'body': '#605040', 'white': '#f8f0c8'},
        ],
    },
    'cosmog': {
        # nevel (Cosmog-wolk, Cosmoem-kern), paars, goud (sterren, schaal, manen, maansikkel), roze,
        # Solgaleo: lijf, donker, rood, blauw; Lunala: lijf (zilver), blauw (teal)
        'species': {
            'cosmog': {'cloud': [1, 2, 3, 11, 12], 'purple': [5, 7, 13], 'gold': [8, 9], 'pink': [14]},
            'cosmoem': {'cloud': [7, 8, 12], 'purple': [9, 13], 'gold': [1, 3, 5, 6], 'pink': [11, 14]},
            'solgaleo': {'body': [8, 9, 15], 'dark': [7, 10, 12], 'gold': [1, 3, 6], 'red': [2, 5],
                         'blue': [11, 13], '_base': {'body': 9}},
            'lunala': {'purple': [4, 5, 9, 11], 'gold': [1, 2, 8, 10], 'body': [6, 7, 12], 'pink': [13],
                       'blue': [14]},
        },
        'variants': [
            {'naam': 'Oogstmaan (oranje met roodbruin)', 'cloud': '#f09030', 'purple': '#603018', 'gold': '#f8e0a0',
             'pink': '#f0f0f0', 'body': '#e09858', 'dark': '#604028', 'red': '#f8f0c0', 'blue': '#40a0e0',
             'cosmoem:gold': '#c06028', 'cosmoem:cloud': '#f8d070'},
            {'naam': 'Noorderlicht (groen en violet)', 'cloud': '#40e0a0', 'purple': '#4030a0', 'gold': '#80f0c0',
             'pink': '#f080f0', 'body': '#c0e8d8', 'dark': '#304050', 'red': '#a040f0', 'blue': '#40f0a0'},
            {'naam': 'Witte dwerg (wit en ijsblauw)', 'cloud': '#e0f0ff', 'purple': '#90a8d8', 'gold': '#c0e0f8',
             'pink': '#f0f0f0', 'body': '#f0f4f8', 'dark': '#6878a0', 'red': '#80c0f0', 'blue': '#3060c0'},
            {'naam': 'Zonsverduistering (zwart met gouden corona)', 'cloud': ('#383848', DARK), 'purple': '#202030',
             'gold': '#f0c020', 'pink': '#f04020', 'body': ('#404048', DARK), 'dark': '#202024', 'red': '#f0c020',
             'blue': '#f04020', 'cosmoem:gold': ('#383848', DARK), 'cosmoem:cloud': '#f0c020'},
            {'naam': 'Orionnevel (roze en cyaan)', 'cloud': '#f070c0', 'purple': '#3050b0', 'gold': '#60e0f0',
             'pink': '#f8f8f8', 'body': '#f8d8e8', 'dark': '#403070', 'red': '#40e0f0', 'blue': '#f070c0',
             'lunala:purple': '#c84898'},
            {'naam': 'Gouden kosmos (de legende in bladgoud)', 'cloud': ('#e0b030', {'h': 0}), 'purple': '#805010',
             'gold': '#f8f0c0', 'pink': '#f04040', 'body': ('#e8c050', {'h': 0}), 'dark': '#604010',
             'red': '#f04040', 'blue': '#3060d0', 'lunala:purple': ('#d8a830', {'h': 0})},
        ],
    },
    'nihilego': {
        # gelei/glas, blauw (kraag), lila
        'species': {
            'nihilego': {'jelly': [1, 2, 3, 9], 'blue': [5, 6, 7], 'lilac': [8]},
        },
        'variants': [
            {'naam': 'Parelkwal (Pelagia: lila-roze)', 'jelly': '#f0d0e8', 'blue': '#d04090', 'lilac': '#a060c0'},
            {'naam': 'Neurotoxine (gifgroen)', 'jelly': '#d0f0c0', 'blue': '#40b040', 'lilac': '#c0e040'},
            {'naam': 'Vuurkwal (oranje en rood)', 'jelly': '#f8e0c8', 'blue': '#e05020', 'lilac': '#f0a040'},
            {'naam': 'Ultra-zwart glas (cyaan en violet)', 'jelly': ('#383848', DARK), 'blue': '#40e0f0',
             'lilac': '#9060e0'},
            {'naam': 'Atolla (diepzeekwal: violet met rood)', 'jelly': '#d8c8f0', 'blue': '#6030a0', 'lilac': '#e03050'},
            {'naam': 'Opaal (wit met regenboogglans)', 'jelly': '#f0f0f8', 'blue': '#40d0a0', 'lilac': '#f080c0'},
        ],
    },
    'buzzwole': {
        # spieren (rood), donker lijf, oranje (vlekken/zuigsnuit)
        'species': {
            'buzzwole': {'muscle': [3, 5, 6, 11, 12], 'dark': [1, 2, 4, 14], 'orange': [8, 9, 13]},
        },
        'variants': [
            {'naam': 'Thanos (paars met gouden handschoen)', 'muscle': '#8050b0', 'dark': '#3a3048', 'orange': '#f0c020'},
            {'naam': 'Arnold (bronzen bodybuilder)', 'muscle': '#c07840', 'dark': '#403028', 'orange': '#f0d080'},
            {'naam': 'Dr. Manhattan (blauw gloeiend)', 'muscle': '#4080e0', 'dark': '#202840', 'orange': '#80f0f0'},
            {'naam': 'Tijgermug (zwart met witte strepen)', 'muscle': ('#404044', DARK), 'dark': '#202020',
             'orange': '#f0f0f0'},
            {'naam': 'Kauwgombal (roze)', 'muscle': '#f080b0', 'dark': '#603050', 'orange': '#f0f080'},
            {'naam': 'Herculesbeeld (goud)', 'muscle': ('#d8a830', {'h': 0}), 'dark': '#605040', 'orange': '#f8f0d0'},
        ],
    },
    'pheromosa': {
        # wit lijf, grijze poten, gele voelsprieten, ogen
        'species': {
            'pheromosa': {'white': [3, 7, 11, 12, 13, 15], 'grey': [1, 10, 14], 'yellow': [4, 5, 6], 'eyes': [8, 9],
                          '_base': {'white': 3}},
        },
        'variants': [
            {'naam': 'Kakkerlak (bruine glans)', 'white': '#a06838', 'grey': '#503020', 'yellow': '#e0c080',
             'eyes': '#f0e040'},
            {'naam': 'Little Black Dress (Chanel: zwart met parels)', 'white': ('#404048', DARK), 'grey': '#202024',
             'yellow': '#f0e0c0', 'eyes': '#f04080'},
            {'naam': 'Barbiecore (roze couture)', 'white': '#f8c0d8', 'grey': '#a05078', 'yellow': '#f040a0',
             'eyes': '#40c0f0'},
            {'naam': 'Tiffany (turquoise met zilver)', 'white': '#a0e0d0', 'grey': '#508078', 'yellow': '#c0c8d0',
             'eyes': '#f8f8f8'},
            {'naam': 'Rode loper (Met Gala-rood)', 'white': '#d02838', 'grey': '#501018', 'yellow': '#f0d040',
             'eyes': '#f8f8f8'},
            {'naam': 'Gouden Oscarjurk', 'white': ('#e0b830', {'h': 0}), 'grey': '#705010', 'yellow': '#f8f8f0',
             'eyes': '#d02020'},
        ],
    },
    'xurkitree': {
        # kabelhaar (wit), lijf (zwarte kabels), oranje (stekkers/lampjes), grijs
        'species': {
            'xurkitree': {'hair': [1, 2, 3, 4], 'body': [10, 11, 12, 14], 'orange': [5, 7, 9, 15], 'grey': [8, 13]},
        },
        'variants': [
            {'naam': 'Koperdraad (koperen vezels, roodbruine isolatie)', 'hair': '#d08850', 'body': '#6a3828',
             'orange': '#f0d040', 'grey': '#909098'},
            {'naam': 'Kerstverlichting (groene draad, rode lampjes)', 'hair': '#f0f0a0', 'body': '#307040',
             'orange': '#e02020', 'grey': '#c0c0c8'},
            {'naam': 'Neonbuis (roze en cyaan)', 'hair': '#f060c0', 'body': '#303050', 'orange': '#40f0f0',
             'grey': '#9090b0'},
            {'naam': 'Plasmabol (paars met witte vonken)', 'hair': '#c080f0', 'body': '#382050', 'orange': '#f0f0f0',
             'grey': '#8070a0'},
            {'naam': 'Noodstroom (rood alarm)', 'hair': '#f05040', 'body': '#401010', 'orange': '#f0f040',
             'grey': '#a08080'},
            {'naam': 'Gouden glasvezel (goud met cyaan licht)', 'hair': ('#e8c040', {'h': 0}), 'body': '#605030',
             'orange': '#40e0f0', 'grey': '#e0d0a0'},
        ],
    },
    'celesteela': {
        # romp (bamboegroen), cyaan strepen, wit/grijs, geel (lichtjes)
        'species': {
            'celesteela': {'body': [5, 6, 8, 12, 13, 14, 15], 'cyan': [2, 3], 'white': [1, 4, 11], 'yellow': [9, 10]},
        },
        'variants': [
            {'naam': 'Bamboeprinses (Kaguya-hime: geel bamboe)', 'body': '#b0a050', 'cyan': '#40a040',
             'white': '#f0f0e0', 'yellow': '#f0e040'},
            {'naam': 'Saturnus V (wit met zwarte banden)', 'body': '#d8d8d8', 'cyan': '#303030', 'white': '#f8f8f8',
             'yellow': '#e02020'},
            {'naam': 'Lapisraket (diepblauw met zilver)', 'body': '#2848a0', 'cyan': '#c0c8d8', 'white': '#e0e0f0',
             'yellow': '#f0c020'},
            {'naam': 'Houtskool (zwart met oranje stuwkracht)', 'body': ('#484850', DARK), 'cyan': '#f08020',
             'white': '#a0a0a8', 'yellow': '#f0e040'},
            {'naam': 'Lavendelraket (lila met geel en roze)', 'body': '#b090e0', 'cyan': '#f0e040',
             'white': '#f8f8f8', 'yellow': '#f04080'},
            {'naam': 'Kuifjes maanraket (rood en wit)', 'body': ('#c01818', DARK), 'cyan': '#f8f8f8', 'white': '#f8f0f0',
             'yellow': '#f0d020'},
        ],
    },
    'kartana': {
        # papier, vouwen (grijs), oranje, rood
        'species': {
            'kartana': {'paper': [2, 3, 4, 13, 14], 'fold': [1, 12, 15], 'orange': [6, 8, 10], 'red': [7, 9, 11]},
        },
        'variants': [
            {'naam': 'Krantenpapier (grijs met zwarte inkt)', 'paper': '#a8a8a0', 'fold': '#505050',
             'orange': '#303030', 'red': '#808080'},
            {'naam': 'Washi (Japans rood papier met goud)', 'paper': '#d03030', 'fold': '#701818', 'orange': '#f0c040',
             'red': '#f8f0e0'},
            {'naam': 'Kraftpapier (bruin met wit)', 'paper': '#c09868', 'fold': '#705030', 'orange': '#f8f8f0',
             'red': '#404040'},
            {'naam': 'Blauwdruk (blauw met witte lijnen)', 'paper': '#3060b0', 'fold': '#183060', 'orange': '#f0f0f0',
             'red': '#a0c0f0'},
            {'naam': 'Zwarte katana (zwart lak, rood koord)', 'paper': ('#383840', DARK), 'fold': '#181818',
             'orange': '#d02020', 'red': '#f0c020'},
            {'naam': 'Gouden kraanvogel (senbazuru in bladgoud)', 'paper': ('#e0c050', {'h': 0}), 'fold': '#806020',
             'orange': '#d02020', 'red': '#f8f8f0'},
        ],
    },
    'guzzlord': {
        # lijf (donker), gele tanden/banden, cyaan
        'species': {
            'guzzlord': {'body': [2, 5, 7, 12], 'yellow': [1, 3, 6], 'cyan': [8, 9, 10, 11]},
        },
        'variants': [
            {'naam': 'Kirby (roze: alles opslokken)', 'body': '#e080a8', 'yellow': '#e02060', 'cyan': '#f8f8f8'},
            {'naam': 'Zwart gat (zwart met paarse accretieschijf)', 'body': ('#282830', DARK), 'yellow': '#9040e0',
             'cyan': '#40f0f0'},
            {'naam': 'Lavamaag (rood met oranje)', 'body': '#802020', 'yellow': '#f08020', 'cyan': '#f8e040'},
            {'naam': 'Moerasmonster (groen met mos)', 'body': '#405830', 'yellow': '#a0c040', 'cyan': '#80d0a0'},
            {'naam': 'Koekiemonster (blauw met koekjesbruin)', 'body': '#3070d0', 'yellow': '#a06030',
             'cyan': '#f8f8f8'},
            {'naam': 'Mammon (goud met rood)', 'body': ('#c09030', {'h': 0}), 'yellow': '#c02020', 'cyan': '#f0f0d0'},
        ],
    },
    'necrozma': {
        # kristallijf (donker), wit prismalicht; Dawn Wings/Dusk Mane: vleugels/manen en hun lichte delen
        'species': {
            'necrozma': {'body': [1, 2, 3, 4], 'white': [12, 13]},
            'necrozma/dawn_wings': {'body': [7, 8, 9, 11], 'wing': [1, 2, 15], 'light': [5, 6, 10], 'pink': [14]},
            'necrozma/dusk_mane': {'body': [2, 6, 9, 11], 'wing': [1, 4, 5], 'light': [7, 8, 10, 15]},
        },
        'variants': [
            {'naam': 'Rookkwarts (bruin kristal)', 'body': '#584838', 'white': '#e0d0b0', 'wing': '#a07040',
             'light': '#e0c8a0', 'pink': '#f0e0a0'},
            {'naam': 'Amethist (paars kristal)', 'body': '#503070', 'white': '#e0c8f0', 'wing': '#9050d0',
             'light': '#d8c0f0', 'pink': '#f8f8f8'},
            {'naam': 'Robijn (rood kristal)', 'body': '#601820', 'white': '#f0c0c0', 'wing': '#d02030',
             'light': '#f0a0a0', 'pink': '#f0f040'},
            {'naam': 'Smaragd (groen kristal)', 'body': '#184830', 'white': '#c0f0d0', 'wing': '#20a060',
             'light': '#a0e8c0', 'pink': '#f0f0f0'},
            {'naam': 'Diamant (helder kristal)', 'body': '#8890a0', 'white': '#f8f8ff', 'wing': '#c8d8f0',
             'light': '#f8f8ff', 'pink': '#80c0f0'},
            {'naam': 'Ultra-straling (gouden licht)', 'body': ('#c8a040', {'h': 0}), 'white': '#f8f0c0',
             'wing': ('#f0c030', {'h': 0}), 'light': '#f8f0d0', 'pink': '#f04040',
             'necrozma/dusk_mane:wing': '#e8e8f4', 'necrozma/dusk_mane:light': '#f8f0c0'},
        ],
    },
    'magearna': {
        # lijf (porselein), goud, metaal, cyaan (kern/ogen), roze accenten; Original Color doet mee
        'species': {
            'magearna': {'body': [4, 5, 6], 'gold': [1, 2, 3], 'metal': [8, 9, 10, 15], 'cyan': [13, 14],
                         'pink': [11, 12]},
            'magearna/original_color': {'body': [4, 5, 6], 'gold': [1, 2, 3, 11, 12], 'metal': [8, 9, 10, 15],
                                        'cyan': [14], 'pink': [13]},
        },
        'variants': [
            {'naam': 'Mint en zilver (porselein)', 'body': '#a0d8c8', 'gold': '#c0c8d0', 'metal': '#e8e8e8',
             'cyan': '#f080a0', 'pink': '#f0f0f0'},
            {'naam': 'Delfts blauw (met goud)', 'body': '#5070c0', 'gold': '#f0c040', 'metal': '#f0f0f8',
             'cyan': '#f8f8f8', 'pink': '#e04050'},
            {'naam': 'Uurwerk (koper en messing, steampunk)', 'body': '#a86040', 'gold': '#e0b050',
             'metal': '#806858', 'cyan': '#40c0a0', 'pink': '#f0c040'},
            {'naam': 'Lavendelpop (lila met wit)', 'body': '#b098d8', 'gold': '#f0f0f0', 'metal': '#e0e0f0',
             'cyan': '#f0c040', 'pink': '#f080c0'},
            {'naam': 'Gotische porseleinpop (zwart met zilver)', 'body': ('#383040', DARK), 'gold': '#c0c0c8',
             'metal': '#606068', 'cyan': '#e02040', 'pink': '#e02040'},
            {'naam': 'Fabergé-ei (smaragd met goud)', 'body': '#30a070', 'gold': ('#f0c040', {'h': 0}),
             'metal': '#f8f0d0', 'cyan': '#f04060', 'pink': '#f8f8f8'},
        ],
    },
    'marshadow': {
        # schaduwlijf, haarvlam, teal (onderste schaduw), ogen/vuur
        'species': {
            'marshadow': {'body': [5, 6, 7], 'hair': [1, 2, 3], 'teal': [13, 14, 15], 'eyes': [8, 9, 10, 11, 12]},
        },
        'variants': [
            {'naam': 'Paarse schaduw', 'body': '#605088', 'hair': '#8050b0', 'teal': '#c040e0', 'eyes': '#f0e040'},
            {'naam': 'Woestijnschaduw (zand met oranje)', 'body': '#a09070', 'hair': '#d0b070', 'teal': '#e08030',
             'eyes': '#f8f8f8'},
            {'naam': 'Negatief (witte schaduw)', 'body': '#c8c8d4', 'hair': '#f0f0f8', 'teal': '#80c0f0',
             'eyes': '#303040'},
            {'naam': 'Bloedschaduw (zwart met rood)', 'body': ('#383038', DARK), 'hair': '#802020', 'teal': '#f02020',
             'eyes': '#f0e040'},
            {'naam': 'Inktvisinkt (marineblauw met cyaan)', 'body': '#283860', 'hair': '#406090', 'teal': '#40e0f0',
             'eyes': '#f0a020'},
            {'naam': 'Zenit (goud met groene geestvlam)', 'body': '#c0a050', 'hair': '#40f070', 'teal': '#40f070',
             'eyes': '#f8f8f8'},
        ],
    },
    'poipole': {
        # lijf (paars), roze, wit/grijs, blauw
        'species': {
            'poipole': {'body': [7, 8, 9, 10, 11], 'pink': [4, 5, 6, 14], 'white': [1, 2], 'blue': [12, 13]},
            'naganadel': {'body': [1, 2, 6, 7, 8, 9], 'pink': [4, 5, 10], 'white': [11, 13, 15], 'blue': [12, 14]},
        },
        'variants': [
            {'naam': 'Wesp (geel en zwart)', 'body': '#e0c020', 'pink': '#303030', 'white': '#f0f0f0',
             'blue': '#e02020'},
            {'naam': 'Gifgroen neon', 'body': '#40a040', 'pink': '#c0f040', 'white': '#e0f0e0', 'blue': '#f040a0'},
            {'naam': 'Hemelsblauw (lichtblauw met goud)', 'body': '#80b0e8', 'pink': '#f0c040', 'white': '#f0f8ff',
             'blue': '#e04080'},
            {'naam': 'Robijn (rood met goud)', 'body': '#b02030', 'pink': '#f0c040', 'white': '#f0e0d0',
             'blue': '#40e0f0'},
            {'naam': 'Koraalrif (koraaloranje met turkoois)', 'body': '#f08040', 'pink': '#40c0c0',
             'white': '#f8f0e0', 'blue': '#3050c0'},
            {'naam': 'Schorpioenkoning (goud met paars gif)', 'body': ('#d0a030', {'h': 0}), 'pink': '#7020a0',
             'white': '#f8f0d0', 'blue': '#30c060'},
        ],
    },
    'stakataka': {
        # stenen, blauwe ogen
        'species': {
            'stakataka': {'brick': [2, 3, 4, 5, 6, 7, 8], 'eyes': [10, 11]},
        },
        'variants': [
            {'naam': 'Rode baksteen', 'brick': '#a05038', 'eyes': '#f0e040'},
            {'naam': 'Zandsteen (Petra)', 'brick': '#c8a870', 'eyes': '#3060d0'},
            {'naam': 'Amethistmuur (paars met gouden ogen)', 'brick': '#7050a0', 'eyes': '#f0c020'},
            {'naam': 'Marmer (wit met gouden ogen)', 'brick': '#d0d0c8', 'eyes': '#e0b020'},
            {'naam': 'Obsidiaan (zwart met lava-ogen)', 'brick': ('#383038', DARK), 'eyes': '#f06020'},
            {'naam': 'Diamantblok (Minecraft)', 'brick': '#50c8c0', 'eyes': '#f8f8f8'},
        ],
    },
    'blacephalon': {
        # pak (wit), roze, teal, geel (vuurwerkhoofd)
        'species': {
            'blacephalon': {'white': [1, 3, 4, 5], 'pink': [2, 6, 12], 'teal': [7, 8, 10], 'yellow': [11, 13, 14]},
        },
        'variants': [
            {'naam': 'Joker (paars pak, groen en geel)', 'white': '#9070c0', 'pink': '#40a040', 'teal': '#e0e040',
             'yellow': '#f0f0f0'},
            {'naam': 'Harley Quinn (rood en zwart)', 'white': '#d02030', 'pink': '#303030', 'teal': '#303038',
             'yellow': '#f0f0f0'},
            {'naam': 'Zwarte pierrot (zwart pak, witte pompons)', 'white': ('#404048', DARK), 'pink': '#f0f0f0',
             'teal': '#e02020', 'yellow': '#f0d020'},
            {'naam': 'Pastelcircus (mint en roze)', 'white': '#c8f0e0', 'pink': '#f0a0c0', 'teal': '#80c0f0',
             'yellow': '#f8e080'},
            {'naam': 'Hamburgerclown (geel pak, rood haar)', 'white': '#f0d020', 'pink': '#e02020', 'teal': '#f8f8f8',
             'yellow': '#e02020'},
            {'naam': 'Gouden circusdirecteur (goud, rood en marine)', 'white': ('#d8a830', {'h': 0}),
             'pink': '#c02030', 'teal': '#203080', 'yellow': '#f8f8f0'},
        ],
    },
    'zeraora': {
        # vacht (geel), donker, blauw (bliksem), rood
        'species': {
            'zeraora': {'fur': [1, 2, 3], 'dark': [7, 10, 11], 'blue': [4, 6, 9], 'red': [8]},
        },
        'variants': [
            {'naam': 'Zwarte panter (blauwe bliksem)', 'fur': ('#383840', DARK), 'dark': '#202024', 'blue': '#40c0f0',
             'red': '#f0e040'},
            {'naam': 'Bengaalse tijger (oranje met zwart)', 'fur': '#e08030', 'dark': '#202020', 'blue': '#40c0f0',
             'red': '#f8f8f8'},
            {'naam': 'The Flash (rood met gele bliksem)', 'fur': '#d02020', 'dark': '#601010', 'blue': '#f0e040',
             'red': '#f0e040'},
            {'naam': 'Plasmapaars (wit vuur)', 'fur': '#9050d0', 'dark': '#302040', 'blue': '#f0f0f0',
             'red': '#40f0f0'},
            {'naam': 'Kawasaki-groen (neon met zwart)', 'fur': '#60d040', 'dark': '#203018', 'blue': '#303030',
             'red': '#f0f040'},
            {'naam': 'Magical girl (Sailor Moon: roze met hemelsblauwe bliksem)', 'fur': '#f090c0',
             'dark': '#603050', 'blue': '#80e0f0', 'red': '#f0f040'},
        ],
    },
    'meltan': {
        # moer (hoofd/borst), metalen lijf, donker metaal (Melmetals armen), rode staartpunt
        'species': {
            'meltan': {'nut': [1, 2, 3, 4, 6], 'metal': [10, 11, 12, 13], 'dark': [8, 9], 'red': [14, 15]},
            'melmetal': {'nut': [3, 4, 5, 6, 10], 'metal': [2, 12, 13, 14], 'dark': [1, 7, 8, 9], 'red': [15]},
        },
        'variants': [
            {'naam': 'Vrijheidsbeeld (kopergroene moer, koperen lijf)', 'nut': '#40a088', 'metal': '#c07040',
             'dark': '#603020', 'red': '#f0e040'},
            {'naam': 'Chroom (zilveren moer, blauw staal)', 'nut': '#d0d8e0', 'metal': '#6080b0', 'dark': '#283850',
             'red': '#f0c020'},
            {'naam': 'Geanodiseerd titanium (paars en cyaan)', 'nut': '#8060d0', 'metal': '#60c0d0',
             'dark': '#303070', 'red': '#f0d040'},
            {'naam': 'Gietijzer (zwart met gloeiende staart)', 'nut': ('#505058', DARK), 'metal': ('#404048', DARK),
             'dark': '#202024', 'red': '#f06020'},
            {'naam': 'Roségoud', 'nut': '#e8a090', 'metal': '#f0d8d0', 'dark': '#806060', 'red': '#c03050'},
            {'naam': 'Puur goud (24 karaat)', 'nut': ('#f0c030', {'h': 0}), 'metal': '#e0c070', 'dark': '#806020',
             'red': '#e02020'},
        ],
    },
    'oricorio': {
        # Alleen de Baile-stijl: de stijlen zijn zelf al kleurvormen (nectar); Pa'u, Pom-Pom en Sensu
        # houden hun eigen kleur. Hoofdveren, zwarte rokdelen, wit, roze poten.
        'species': {
            'oricorio': {'main': [1, 2, 4], 'accent': [5, 6, 7], 'white': [8, 9, 10], 'legs': [11, 13, 14]},
        },
        'variants': [
            {'naam': 'Blauwe gaai (blauw met zwarte rok)', 'main': '#3060c0', 'accent': '#202840',
             'white': '#f0f0f0', 'legs': '#f0a040'},
            {'naam': 'Flamingo (roze met zwarte snavel)', 'main': '#f08cb0', 'accent': '#a04060', 'white': '#f8f0f0',
             'legs': '#303030'},
            {'naam': 'Het Zwanenmeer (wit tutu)', 'main': '#e0e0ec', 'accent': '#9898b8', 'white': '#f8f8f8',
             'legs': '#e0b8c8'},
            {'naam': 'Salsa (oranje en geel)', 'main': '#f08020', 'accent': '#f0d040', 'white': '#f8f0d0',
             'legs': '#e04040'},
            {'naam': 'Paradijsvogel (smaragd met goud)', 'main': '#30a060', 'accent': '#f0c040', 'white': '#f0f0e0',
             'legs': '#304030'},
            {'naam': 'Carnaval van Rio (paars met goud en groen)', 'main': '#8030c0', 'accent': '#f0c020',
             'white': '#40d060', 'legs': '#f040a0'},
        ],
    },
    'wishiwashi': {
        # solo: lijf (grijs/wit), blauwe rug, oog; school: blauw, donker, ogen (cyaan), wit
        'species': {
            'wishiwashi': {'body': [2, 6, 7, 13, 15], 'blue': [1, 3, 4], 'eye': [9, 11]},
            'wishiwashi/school': {'blue': [1, 2, 3, 6, 7, 8, 15], 'dark': [9, 10], 'eye': [4, 14],
                                  'body': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Makreel (blauwgroen met zilver)', 'blue': '#2a8080', 'body': '#d8e0e0', 'eye': '#f0e040',
             'dark': '#103838'},
            {'naam': 'Rode zalm', 'blue': '#d04040', 'body': '#f0b0a0', 'eye': '#f0e040', 'dark': '#601818'},
            {'naam': 'Zeewierschool (groen)', 'blue': '#40a050', 'body': '#d0e8c0', 'eye': '#f0e040',
             'dark': '#204020'},
            {'naam': 'Spookvis (wit met roze ogen)', 'blue': '#d8e0ec', 'body': '#f8f8f8', 'eye': '#f04060',
             'dark': '#8090a0'},
            {'naam': 'Paarse school (violet met geel)', 'blue': '#7040b0', 'body': '#d8c8f0', 'eye': '#f0e040',
             'dark': '#301848'},
            {'naam': 'Koi (goud met rood)', 'blue': ('#e0b030', {'h': 0}), 'body': '#f8f0e0', 'eye': '#e02020',
             'dark': '#804010'},
        ],
    },
    'minior': {
        # Alleen de meteoorvorm (de kernen niet): korst, witte kern die erdoor schemert
        'species': {
            'minior': {'rock': [5, 6, 7, 8, 10, 11], 'white': [1, 2, 4]},
        },
        'variants': [
            {'naam': 'IJzermeteoriet (grijs metaal)', 'rock': '#808890', 'white': '#f0f0f0'},
            {'naam': 'Pallasiet (olivijn in ijzer)', 'rock': '#9a9a50', 'white': '#f0f0a0'},
            {'naam': 'Chondriet (oker met crème kern)', 'rock': '#c09040', 'white': '#f8f0c0'},
            {'naam': 'Komeetijs (ijsblauw)', 'rock': '#a0c8e0', 'white': '#f8f8ff'},
            {'naam': 'Moldaviet (groen tektietglas)', 'rock': '#408040', 'white': '#c0f0a0'},
            {'naam': 'Sterrenstof (paars met goud)', 'rock': '#5040a0', 'white': '#f0e060'},
        ],
    },
}
