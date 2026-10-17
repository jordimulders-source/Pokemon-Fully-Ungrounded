"""Kleurvarianten, generatie 7 (deel b): de vier Tapu's (elk een eigen lijn) en de
Oricorio-stijlen Pa'u, Pom-Pom en Sensu. Formaat: zie recipes.py."""

ALBINO = {'l': 1.0}
DARK = {'l': 1.3}
GOLD = {'h': 0}

LINES = {
    'tapu_koko': {
        # Electric/Fairy, de haan van Melemele. Schild (geel), kam/staart (oranje), lijf (grijsgroen),
        # witte schildtekening, ogen (cyaan).
        'species': {
            'tapu_koko': {'shell': [1, 2, 4, 14], 'accent': [5, 6, 7], 'body': [9, 10], 'white': [11, 12],
                          'eye': [13], '_base': {'shell': 4}},
        },
        'variants': [
            {'naam': 'Rode bankivahoen (koperen nekveren, rode kam, groenzwarte staart)', 'shell': '#d06820',
             'accent': '#d82828', 'body': '#2c4838', 'white': '#f8e8b0', 'eye': '#f0c020'},
            {'naam': 'Teslaspoel (plasmablauw met violette vonken)', 'shell': '#38b0e8', 'accent': '#9050e0',
             'body': '#283048', 'white': '#f8f8ff', 'eye': '#f040c0'},
            {'naam': 'Witte leghorn (wit verenkleed, rode kam, gele poten)', 'shell': '#e8e8e0',
             'accent': '#e02828', 'body': '#b89038', 'white': '#a8a8b8', 'eye': '#e02828'},
            {'naam': 'Groene Java-hoen (iriserend groen met paarsrode kam)', 'shell': '#2a8a70',
             'accent': '#c83088', 'body': '#203040', 'white': '#b8f0d8', 'eye': '#f0a020'},
            {'naam': 'Supercel (onweerspaars met gele bliksem)', 'shell': '#5838a8', 'accent': '#f0e040',
             'body': '#282038', 'white': '#f8f8ff', 'eye': '#f0e040'},
            {'naam': "'Ahu'ula van Kamehameha (scharlaken i'iwi-veren met gouden 'o'o-banden)",
             'shell': '#c01828', 'accent': ('#f8c818', GOLD), 'body': '#3a2a20', 'white': '#f8d840',
             'eye': '#f8d040'},
        ],
    },
    'tapu_lele': {
        # Psychic/Fairy, de vlinder van Akala. Schild (roze), strepen (rood-roze), lijf (donker),
        # wit, ogen.
        'species': {
            'tapu_lele': {'shell': [1, 2, 5, 14], 'accent': [9, 10, 11], 'body': [3, 4], 'white': [6, 7],
                          'eye': [13]},
        },
        'variants': [
            {'naam': 'Citroenvlinder (citroengeel met oranje stip)', 'shell': '#f8e050', 'accent': '#e8c010',
             'body': '#586048', 'white': '#f8f8f0', 'eye': '#e08020'},
            {'naam': 'Monarchvlinder (oranje met zwarte aders)', 'shell': '#f08020', 'accent': ('#503028', DARK),
             'body': '#403030', 'white': '#f8f8f8', 'eye': '#f0d020'},
            {'naam': 'Morphovlinder (iriserend blauw met cyaan glans)', 'shell': '#3a78e0', 'accent': '#50e0f0',
             'body': '#283048', 'white': '#e0f0ff', 'eye': '#f8f080'},
            {'naam': 'Mewtwo (lila met paarse staart: Psychic-icoon)', 'shell': '#d8c8e8', 'accent': '#9050b0',
             'body': '#6a5878', 'white': '#ffffff', 'eye': '#8040c0'},
            {'naam': 'Maanvlinder (Actias luna: lichtgroen met paarse rand)', 'shell': '#904070',
             'accent': '#a8e090', 'body': '#506048', 'white': '#f8fff0', 'eye': '#e0d040'},
            {'naam': 'Lisa Frank (neon-turquoise met magenta)', 'shell': '#30d0c8', 'accent': '#f030b0',
             'body': '#402858', 'white': '#fff8a0', 'eye': '#f030b0'},
        ],
    },
    'tapu_bulu': {
        # Grass/Fairy, de stier van Ula'ula. Schild (rood), hoorns/staart (geel), lijf (donker), wit, ogen.
        'species': {
            'tapu_bulu': {'shell': [7, 8, 9, 14], 'accent': [4, 5, 12], 'body': [2, 6], 'white': [10, 11],
                          'eye': [13], '_base': {'shell': 8}},
        },
        'variants': [
            {'naam': 'Mos en eik (mosgroen schild, eikenhouten hoorns)', 'shell': '#4a8838', 'accent': '#a07040',
             'body': '#484838', 'white': '#e8f0c0', 'eye': '#f0d040'},
            {'naam': 'Schotse hooglander (roestbruine vacht, crème hoorns)', 'shell': '#b8602a',
             'accent': '#f0e0b8', 'body': '#4a3828', 'white': '#f8e8d0', 'eye': '#f0a030'},
            {'naam': 'Traje de luces (marineblauw matadorpak met goud)', 'shell': '#283878',
             'accent': ('#f0c030', GOLD), 'body': '#383848', 'white': '#f8f0d0', 'eye': '#f0c030'},
            {'naam': "Kalo (Hawaïaanse taro: paarse knol, groen blad)", 'shell': '#6a4a8a', 'accent': '#98c860',
             'body': '#405040', 'white': '#e8d8f0', 'eye': '#98c860'},
            {'naam': 'Berkenbast (wit met donkere hoorns, berkenblad)', 'shell': '#e8e4d8', 'accent': '#585048',
             'body': '#585048', 'white': '#80a850', 'eye': '#80c040'},
            {'naam': 'Gouden kalf (goud met robijn)', 'shell': ('#e0b030', GOLD), 'accent': '#c02030',
             'body': '#605030', 'white': '#fff8c0', 'eye': '#c02030'},
        ],
    },
    'tapu_fini': {
        # Water/Fairy, de beschermgeest van Poni. Schild (paars), vinnen (lichtblauw), lijf (donker), wit, ogen.
        'species': {
            'tapu_fini': {'shell': [1, 2, 6, 14], 'accent': [7, 8, 9], 'body': [3, 5, 10], 'white': [11, 12],
                          'eye': [13]},
        },
        'variants': [
            {'naam': 'Zeemist (zilvergrijs met nevelwit)', 'shell': '#9098b8', 'accent': '#e8f0f8',
             'body': '#484858', 'white': '#ffffff', 'eye': '#80e0f0'},
            {'naam': 'Koraalrif (koraalrood met turquoise)', 'shell': '#e87060', 'accent': '#30c0b0',
             'body': '#383848', 'white': '#fff0e0', 'eye': '#f0e040'},
            {'naam': 'Kelpwoud (olijfgroen met amber)', 'shell': '#4a7838', 'accent': '#d0a840',
             'body': '#303828', 'white': '#e8f0d0', 'eye': '#f08030'},
            {'naam': 'Vaadhoo-strand (nachtblauw met lichtgevend plankton)', 'shell': ('#203470', DARK),
             'accent': '#40f0e0', 'body': '#182030', 'white': '#a0fff0', 'eye': '#40f0e0'},
            {'naam': 'Paua-schelp (pauwblauwgroen met paarse parelmoerglans)', 'shell': '#2a8898',
             'accent': '#b060d0', 'body': '#283040', 'white': '#e0f8f8', 'eye': '#f0f0a0'},
            {'naam': 'Verzonken schat (goud met turquoise zeeglas)', 'shell': ('#d8a830', GOLD),
             'accent': '#40d0c0', 'body': '#403828', 'white': '#fff8d0', 'eye': '#40d0c0'},
        ],
    },
    'oricorio_pau': {
        # Pa'u-stijl (hula): rok/kuif (crème), veren (lichtroze), lei (magenta), snavel/poten (roze).
        # Varianten zijn andere hulakostuums: de stijl blijft herkenbaar.
        'species': {
            'oricorio/pau': {'skirt': [1, 2, 3], 'body': [5, 6, 7], 'lei': [8, 11, 12], 'legs': [9, 10, 14]},
        },
        'variants': [
            {'naam': 'Ti-bladrok (groene ti-bladeren, gele ilima-lei)', 'skirt': '#88b850', 'body': '#f8d8c0',
             'lei': '#f0a820', 'legs': '#f0a080'},
            {'naam': 'Orchideeënlei (strogele rafia, paarse dendrobium)', 'skirt': '#d8b060', 'body': '#e8d0f0',
             'lei': '#9040c0', 'legs': '#e090c0'},
            {'naam': "Indigo pa'u-rok (bedrukt doek met plumeria-lei)", 'skirt': '#4060b8', 'body': '#f0e8f8',
             'lei': '#f0e070', 'legs': '#f0a0b0'},
            {'naam': 'Kukui-lei (bruine kapa-rok, zwartglanzende noten)', 'skirt': '#a07048', 'body': '#f0dcc8',
             'lei': ('#403840', DARK), 'legs': '#e09870'},
            {'naam': 'Siva afi (Samoaanse vuurdans: oranje rok, vuurrode lei)', 'skirt': '#f08028',
             'body': '#f8e8b8', 'lei': '#e02828', 'legs': '#f0c040'},
            {'naam': 'Moana (turquoise zeewierrok, koraal-lei)', 'skirt': '#30b0b0', 'body': '#f8e8d8',
             'lei': '#f07060', 'legs': '#f0b090'},
        ],
    },
    'oricorio_pom_pom': {
        # Pom-Pom-stijl (cheerleading): pompons (geel), lijf (lichtgeel), snavel/poten (roze).
        # Varianten zijn andere cheerleaderteams.
        'species': {
            'oricorio/pom_pom': {'pom': [1, 2, 7], 'body': [4, 5, 6], 'legs': [8, 9, 11]},
        },
        'variants': [
            {'naam': 'Dallas Cowboys Cheerleaders (blauw en zilver)', 'pom': '#2850a8', 'body': '#c8d0e0',
             'legs': '#f0a060'},
            {'naam': 'Bring It On (rode Toros-pompons, crème pakje)', 'pom': '#d82830', 'body': '#f0e0d0',
             'legs': '#f0a0b0'},
            {'naam': 'Lakers Girls (paars en goud)', 'pom': '#6838b0', 'body': ('#e8b830', GOLD),
             'legs': '#f08040'},
            {'naam': 'Seahawks (limegroen met marineblauw)', 'pom': '#88d030', 'body': '#405080',
             'legs': '#e0e0e8'},
            {'naam': 'Miami Dolphins (aqua en oranje)', 'pom': '#20b8b0', 'body': '#f09838', 'legs': '#f8e0c0'},
            {'naam': 'Elle Woods (glitterroze pompons, lichtroze pakje)', 'pom': '#f060a8', 'body': '#f8d0e8',
             'legs': '#f8f0f8'},
        ],
    },
    'oricorio_sensu': {
        # Sensu-stijl (nihon buyo): kimono (indigo), zoom/kuif (cyaan), lila binnenstof,
        # snavel/poten (roze). Varianten zijn andere kimono's.
        'species': {
            'oricorio/sensu': {'kimono': [7, 8, 9], 'trim': [1, 2, 3], 'lav': [4, 5], 'legs': [10, 11, 13],
                               '_base': {'kimono': 8}},
        },
        'variants': [
            {'naam': 'Furisode (karmijnrood met gouden zoom)', 'kimono': '#c02838', 'trim': ('#f0c040', GOLD),
             'lav': '#f8e0b0', 'legs': '#f0a0a0'},
            {'naam': 'Sakura-kimono (bloesemroze met groene zoom)', 'kimono': '#f0b8c8', 'trim': '#70b060',
             'lav': '#fff0f4', 'legs': '#c06080'},
            {'naam': 'Kuro-tomesode (zwart met goud en rode voering)', 'kimono': ('#504858', DARK),
             'trim': '#e0b040', 'lav': '#c03040', 'legs': '#f0a0b0'},
            {'naam': 'Momiji (herfstesdoorn: oranje met roodbruin)', 'kimono': '#e06020', 'trim': '#903020',
             'lav': '#f8d060', 'legs': '#f0b090'},
            {'naam': 'Uguisu (nachtegaalgroen met roze pruimenbloesem)', 'kimono': '#88a040', 'trim': '#f090b0',
             'lav': '#f8f0d0', 'legs': '#e0a0b0'},
            {'naam': 'Shiromuku (witte bruidskimono met rode zoom)', 'kimono': '#f0f0f8', 'trim': '#c82030',
             'lav': '#e0c060', 'legs': '#f09090'},
        ],
    },
}
