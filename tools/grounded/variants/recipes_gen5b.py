"""Kleurvarianten Gen 5, tweede helft (Unova: Minccino t/m Genesect, plus Basculegion
en de vormen van de Unova-legendaries). Zie AGENT_BRIEF.md en keuring_gen5b.md."""

ALBINO = {'l': 1.0}
DARK = {'l': 1.3}

LINES = {
    'minccino': {
        # chinchilla's (echte kleurmutaties) en een sprookje
        'species': {
            'minccino': {'fur': [2, 5, 1], 'tips': [3, 4], 'ears': [7, 8, 9, 10, 11], '_base': {'fur': 5}},
            'cinccino': {'fur': [4, 3, 5], 'fluff': [9, 2, 1], 'ears': [6, 8]},
        },
        'variants': [
            {'naam': 'Violet chinchilla (lavendelgrijs)', 'fur': '#a898c0', 'tips': '#f0e0f8', 'fluff': '#e8d8f8',
             'ears': '#8848a8'},
            {'naam': 'Ebony-chinchilla (antraciet, zilveren pluim)', 'fur': ('#585460', {'l': 1.2}), 'tips': '#c8c8d8',
             'fluff': '#b8b8c8', 'ears': '#a03048'},
            {'naam': 'Wilson-wit (witte chinchilla, roze oren)', 'fur': ('#e8e4e4', ALBINO), 'tips': '#f8f8f8',
             'fluff': ('#f0eef0', ALBINO), 'ears': '#f07890'},
            {'naam': 'Syrische goudhamster (goudoranje, wit)', 'fur': '#d89038', 'tips': '#f8f0e0',
             'fluff': '#f8f4ec', 'ears': '#b04828'},
            {'naam': 'Sjaal van de Vierde Doctor (Doctor Who: roest, mosterd, paars)', 'fur': ('#703c70', {'l': 1.2}),
             'tips': '#f0c850', 'fluff': '#e0b848', 'ears': '#c05828'},
            {'naam': 'Assepoester (zilverblauwe baljurk, gouden koets)', 'fur': '#90b8e0', 'tips': '#f8f8ff',
             'fluff': ('#d8f0f8', {'l': 1.2}), 'ears': '#f0c040'},
        ],
    },
    'gothita': {
        # gothic lolita-stijlen (Harajuku)
        'species': {
            'gothita': {'dress': [2, 1], 'bows': [6, 5, 4], 'face': [7, 8, 9], 'eyes': [10, 11], 'mouth': [12, 13]},
            'gothorita': {'dress': [5, 6], 'bows': [4, 3, 2], 'face': [8, 7], 'eyes': [9, 10], 'mouth': [11, 12]},
            'gothitelle': {'dress': [5, 2, 1], 'bows': [7, 6, 4], 'face': [10, 8, 9], 'eyes': [11, 12],
                           'mouth': [13, 14]},
        },
        'variants': [
            {'naam': 'Sweet Lolita (roze jurk, witte strikken)', 'dress': '#d878a8', 'bows': '#f8f0f8',
             'face': '#f8d0d8', 'eyes': '#c03070', 'mouth': '#e85878'},
            {'naam': 'Classic Lolita (bordeaux en crème)', 'dress': ('#6a1830', DARK), 'bows': '#f0e0c0',
             'face': '#e8c0a8', 'eyes': '#8a5020', 'mouth': '#c04040'},
            {'naam': 'Sailor Lolita (marineblauw met wit)', 'dress': ('#203878', DARK), 'bows': '#f0f4f8',
             'face': '#f0c8c8', 'eyes': '#d03030', 'mouth': '#e06060'},
            {'naam': 'Shiro Lolita (wit, zwarte strikken)', 'dress': ('#e0dce8', ALBINO), 'bows': ('#3a3a48', DARK),
             'face': '#d8d0e0', 'eyes': '#303040', 'mouth': '#d06080'},
            {'naam': 'Wa Lolita (kimono: rood en goud)', 'dress': '#b02028', 'bows': '#e8c040', 'face': '#f8e0c8',
             'eyes': '#202020', 'mouth': '#d03030'},
            {'naam': 'Aristocrat (Mana-sama: dieppaars en zilver)', 'dress': ('#3a1858', DARK),
             'bows': '#c8c8d8', 'face': '#b098d0', 'eyes': '#e03050', 'mouth': '#8030a0'},
        ],
    },
    'solosis': {
        # microscopie: kleuringen en een petrischaaltje
        'species': {
            'solosis': {'gel': [2, 1, 13, 3], 'inner': [6, 11, 15, 5], 'organel': [10, 9, 8], 'nucleus': [14, 12]},
            'duosion': {'gel': [2, 4, 1, 8, 9], 'inner': [5, 6, 3], 'nucleus': [10, 11]},
            'reuniclus': {'gel': [3, 2, 1, 4, 15], 'inner': [6, 5], 'organel': [11, 12], 'nucleus': [9, 10, 14, 13]},
        },
        'variants': [
            {'naam': 'Gramkleuring (kristalviolet)', 'gel': '#8048b8', 'inner': '#e0d0f0', 'organel': '#f0a0c8',
             'nucleus': '#402080'},
            {'naam': 'Gram-negatief (safranine-roze)', 'gel': '#e06890', 'inner': '#f8d8e0', 'organel': '#f8e070',
             'nucleus': '#a02040'},
            {'naam': 'Ziehl-Neelsen (methyleenblauw, fuchsine kern)', 'gel': '#3888c8', 'inner': '#e0f0f8',
             'organel': '#f070c0', 'nucleus': '#d01878'},
            {'naam': 'Agar in een petrischaal (amber)', 'gel': '#d8a048', 'inner': '#f8e8c0', 'organel': '#f8f8e8',
             'nucleus': '#c84020'},
            {'naam': 'Donkerveldmicroscopie (licht op zwart)', 'gel': ('#e0e8f0', ALBINO), 'inner': ('#303848', DARK),
             'organel': '#f8e870', 'nucleus': '#60e8f8'},
            {'naam': 'Colloïdaal goud (Faraday: robijnrode gel)', 'gel': '#b81838', 'inner': '#f8d8a0',
             'organel': ('#e8b830', {'h': 0}), 'nucleus': '#f8e060'},
        ],
    },
    'ducklett': {
        # eenden en zwanen
        'species': {
            'ducklett': {'body': [3, 4, 1, 2], 'down': [11, 6, 12], 'beak': [10, 8, 9]},
            'swanna': {'body': [3, 5, 1, 2], 'chest': [12, 13, 11, 14], 'beak': [9, 10, 15], 'legs': [6, 8]},
        },
        'variants': [
            {'naam': 'Odile, de zwarte zwaan (Zwanenmeer; rode snavel)', 'body': ('#383840', {'l': 1.5}),
             'down': '#8a8a98', 'chest': '#e8e8f0', 'beak': '#d82830', 'legs': '#202020',
             'ducklett:body': ('#484858', {'l': 1.4})},
            {'naam': 'Mandarijneend (oranje, teal)', 'body': '#e89048', 'down': '#30a090', 'chest': '#30a090',
             'beak': '#e83838', 'swanna:body': '#f8e0c0', 'legs': '#e08030'},
            {'naam': 'Wilde eend (groene kop, bruine borst)', 'body': '#3a8a50', 'down': '#8a5a38', 'chest': '#8a5a38',
             'beak': '#e8c030', 'swanna:body': '#58a068', 'legs': '#e07020'},
            {'naam': 'Badeendje (geel, oranje snavel)', 'body': '#f8d830', 'down': '#f0b818', 'chest': '#f8e870',
             'beak': '#f07818', 'legs': '#f07818'},
            {'naam': 'Flamingo (roze, zwarte snavelpunt)', 'body': '#f090a8', 'down': '#e06088', 'chest': '#f8c8d0',
             'beak': '#383038', 'legs': '#e85878'},
            {'naam': 'Cygnus (sterrenbeeld Zwaan: nachtblauw met sterren)', 'body': ('#283878', DARK),
             'down': '#f8f0c0', 'chest': '#f8f0c0', 'beak': '#e8c040', 'legs': '#182040'},
        ],
    },
    'vanillite': {
        # ijssmaken; het ijs eronder wordt saus of hoorntje
        'species': {
            'vanillite': {'cream': [3, 5, 6, 1, 2], 'ice': [7, 8, 9, 13, 14], 'face': [12, 11, 10]},
            'vanillish': {'cream': [2, 5, 11, 1, 3], 'ice': [8, 6, 7, 12, 13], 'face': [10, 9]},
            'vanilluxe': {'cream': [3, 2, 8, 1, 4, 14], 'ice': [7, 9, 6, 11, 10], 'face': [13, 12]},
        },
        'variants': [
            {'naam': 'Aardbei (roze ijs, aardbeiensaus)', 'cream': '#f8c0d0', 'ice': '#d83048', 'face': '#901830'},
            {'naam': 'Chocolade met wafel', 'cream': ('#8a5838', {'l': 0.9}), 'ice': '#e0b060', 'face': '#402010'},
            {'naam': 'Pistache (met nootjes)', 'cream': '#c8e0a0', 'ice': '#80a048', 'face': '#486020'},
            {'naam': 'Ube (paars Filipijns ijs)', 'cream': '#c8a8e8', 'ice': '#6838a8', 'face': '#402070'},
            {'naam': 'Zwart sesamijs met rode bonen (anko)', 'cream': ('#585058', {'l': 1.2}), 'ice': '#904050',
             'face': '#f0e8e0'},
            {'naam': 'Golden Opulence Sundae (bladgoud, $1000)', 'cream': ('#f0d058', {'h': 0}), 'ice': '#f8f0d8',
             'face': '#8a5810'},
        ],
    },
    'emolga': {
        # vliegende eekhoorns en buideldieren
        'species': {
            'emolga': {'fur': [3, 1, 2], 'white': [8, 6, 11], 'yellow': [9, 5, 7, 15], 'cheeks': [14, 13, 12]},
        },
        'variants': [
            {'naam': 'Suikereekhoorn (blauwgrijs, crème)', 'fur': ('#687080', {'l': 1.2}), 'white': '#f8f0d8',
             'yellow': '#383840', 'cheeks': '#e8a0a8'},
            {'naam': 'Minun-kleuren (blauw, blauwe wangen)', 'fur': ('#3868c0', {'l': 1.2}),
             'white': '#f8f8f0', 'yellow': '#80c8f8', 'cheeks': '#3888e0'},
            {'naam': 'Reuzenvliegeekhoorn (roodbruin, oranje)', 'fur': ('#a83820', {'l': 1.2}), 'white': '#f0d8b8',
             'yellow': '#f08020', 'cheeks': '#f8c8b0'},
            {'naam': 'Albino (rode ogen, roze accenten)', 'fur': ('#d8d4dc', ALBINO), 'white': ('#f8f8f8', ALBINO),
             'yellow': '#f0a0b8', 'cheeks': '#e04858'},
            {'naam': 'Tron (zwart met cyaan gloed)', 'fur': ('#282838', {'l': 1.5}), 'white': '#405068',
             'yellow': '#30e8f8', 'cheeks': '#30e8f8'},
            {'naam': 'Raijin (goud met paarse bliksem)', 'fur': ('#c89020', {'h': 0}), 'white': '#f8f0c8',
             'yellow': '#9048e0', 'cheeks': '#e04870'},
        ],
    },
    'karrablast': {
        # ridders (Escavalier draagt Shelmets helm; Karrablast krijgt de kleur van de pluim)
        'species': {
            'karrablast': {'helm': [3, 1, 2, 4], 'armour': [8, 7], 'face': [11, 10, 14], 'eyes': [12], 'shine': [6, 9]},
            'escavalier': {'helm': [3, 1, 2], 'armour': [5, 6, 7, 8], 'face': [11, 10, 13], 'eyes': [9],
                           'shine': [14, 15]},
        },
        'variants': [
            {'naam': 'De Groene Ridder (Gawain-legende)', 'helm': '#3a8838', 'armour': '#b08850', 'face': '#d8e070',
             'eyes': '#e83020', 'shine': '#a0e080', 'karrablast:armour': '#6a5030'},
            {'naam': 'De Zwarte Prins (zwart harnas, gouden pluim)', 'helm': '#e0b030', 'armour': ('#48505a', {'l': 1.4}),
             'face': '#e0b030', 'eyes': '#e03030', 'shine': '#f8e070', 'karrablast:helm': ('#383840', {'l': 1.5}),
             'karrablast:armour': '#e0b030'},
            {'naam': 'Lancelot (azuur en zilver)', 'helm': '#2850c0', 'armour': '#d8dce8', 'face': '#f0f0f8',
             'eyes': '#30a0f0', 'shine': '#80c8f8', 'karrablast:helm': '#e8e8f0', 'karrablast:armour': '#2850c0'},
            {'naam': 'Tempelier (wit met rood kruis)', 'helm': ('#e8e4e0', ALBINO), 'armour': '#a07850',
             'face': '#d82828', 'eyes': '#202020', 'shine': '#d82828', 'karrablast:armour': '#d82828'},
            {'naam': 'Karel de Grote (keizerspurper en goud)', 'helm': '#6a2890', 'armour': ('#d0a030', {'h': 0}),
             'face': '#f8e8a0', 'eyes': '#e03030', 'shine': '#c080f0', 'karrablast:armour': '#d0a030'},
            {'naam': 'Gold Saint (Saint Seiya: goud harnas)', 'helm': ('#d8a020', {'h': 0}),
             'armour': ('#f0d868', {'h': 0}), 'face': '#f8f0c0', 'eyes': '#30c0f8', 'shine': '#30c0f8',
             'karrablast:armour': '#f8f0c0'},
        ],
    },
    'shelmet': {
        # Teenage Mutant Ninja Turtles: Shelmet in zijn schild, Accelgor met de bandana
        'species': {
            'shelmet': {'shell': [5, 2, 1, 3], 'rim': [8, 7], 'face': [12, 10, 9, 11], 'mouth': [15, 13]},
            'accelgor': {'face': [2, 3, 1], 'wraps': [11, 10, 9], 'green': [6, 7], 'brown': [5, 8]},
        },
        'variants': [
            {'naam': 'Michelangelo (oranje bandana)', 'shell': '#98a840', 'rim': '#e0c070', 'face': '#f08020',
             'wraps': '#58a048', 'green': '#c89058', 'brown': '#8a5a30', 'mouth': '#c84020'},
            {'naam': 'Donatello (paarse bandana)', 'shell': '#7a6a40', 'rim': '#c8a070', 'face': '#8040b8',
             'wraps': '#489848', 'green': '#a07848', 'brown': '#6a4828', 'mouth': '#e070c0'},
            {'naam': 'Leonardo (blauwe bandana)', 'shell': '#38784a', 'rim': '#b8c088', 'face': '#2860c8',
             'wraps': '#50a050', 'green': '#c08048', 'brown': '#704c28', 'mouth': '#60c0f0'},
            {'naam': 'Raphael (rode bandana)', 'shell': '#4a5848', 'rim': '#a08048', 'face': '#c81818',
             'wraps': '#3a8840', 'green': '#a87040', 'brown': '#603818', 'mouth': '#f8a040'},
            {'naam': 'Splinter (rattenbruin, kastanje kimono)', 'shell': '#8a6040', 'rim': '#d8b890', 'face': '#d8b0a0',
             'wraps': '#7a3820', 'green': '#f0d0c0', 'brown': '#4a2818', 'mouth': '#f090a0'},
            {'naam': 'Shredder (zilveren lemmeten, paarse cape)', 'shell': '#c0c8d8', 'rim': '#5a2878', 'face': '#d8dce8',
             'wraps': ('#3a2050', DARK), 'green': '#c02828', 'brown': '#202028', 'mouth': '#c02828'},
        ],
    },
    'foongus': {
        # Foongus doet zich voor als Poké Ball: dus Poké Ball-soorten
        'species': {
            'foongus': {'cap': [4, 2, 1], 'band': [5, 6], 'body': [8, 7, 10], 'mouth': [11, 9]},
            'amoonguss': {'cap': [8, 7, 10], 'band': [5, 2, 13], 'body': [4, 6, 1, 9], 'mouth': [11, 12]},
        },
        'variants': [
            {'naam': 'Great Ball (blauw met rode strepen)', 'cap': '#3060d0', 'band': ('#8a2828', {'l': 1.2}),
             'body': '#f0f0f0', 'mouth': '#e04848'},
            {'naam': 'Ultra Ball (zwart met geel)', 'cap': '#e8c030', 'band': ('#303038', {'l': 1.4}),
             'body': '#d8d8e0', 'mouth': '#f0d870'},
            {'naam': 'Net Ball (turkoois net)', 'cap': '#30a8b0', 'band': ('#2a4858', {'l': 1.2}), 'body': '#f0f8f8',
             'mouth': '#78d8e0'},
            {'naam': 'Premier Ball (wit met rode rand)', 'cap': ('#f0ecec', ALBINO), 'band': '#c82830',
             'body': '#f8f0e8', 'mouth': '#e04848'},
            {'naam': 'Dusk Ball (nachtgroen met rood)', 'cap': '#287838', 'band': ('#202820', DARK), 'body': '#c84838',
             'mouth': '#f0d040'},
            {'naam': 'Master Ball (paars met roze bollen)', 'cap': '#7838b8', 'band': ('#382050', DARK),
             'body': '#f0e8f8', 'mouth': '#f070b8'},
        ],
    },
    'frillish': {
        # kwallen (geldt voor mannetje en vrouwtje: een skin vervangt de kleur)
        'species': {
            'frillish': {'body': [6, 5, 1], 'frill': [4, 3], 'eyes': [8, 9]},
            'jellicent': {'body': [7, 6, 5, 1], 'frill': [9, 2, 4, 8], 'eyes': [10]},
        },
        'variants': [
            {'naam': 'Kompaskwal (karamel met bruin)', 'body': '#c08850', 'frill': '#f8e8d0', 'eyes': '#702818'},
            {'naam': 'Spiegeleikwal (eigeel en eiwit)', 'body': '#f0c030', 'frill': '#f8f8f0', 'eyes': '#c06010'},
            {'naam': 'Parelkwal (Pelagia noctiluca: paars)', 'body': '#9050c0', 'frill': '#e8c8f0', 'eyes': '#f8d040'},
            {'naam': 'Leeuwenmanen (rood-oranje)', 'body': '#d84828', 'frill': '#f8d8a8', 'eyes': '#f8f070'},
            {'naam': 'Kristalkwal (Aequorea: groen licht in het donker)', 'body': ('#283840', {'l': 1.4}),
             'frill': '#70f098', 'eyes': '#70f098'},
            {'naam': 'Gouden kwal (Jellyfish Lake, Palau)', 'body': ('#d8a830', {'h': 0}), 'frill': '#f8f0c0',
             'eyes': '#e04020'},
        ],
    },
    'alomomola': {
        # maanvissen en andere oceaanreuzen; de verpleegster van de zee
        'species': {
            'alomomola': {'body': [7, 2, 10, 3, 1, 5, 6], 'shine': [9, 8], 'eye': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Mola mola (zilvergrijs)', 'body': '#a0a8b8', 'shine': '#f0f4f8', 'eye': '#283850'},
            {'naam': 'Opah (koningsvis: rood met zilver)', 'body': '#c83828', 'shine': '#f0e8e8', 'eye': '#f0c030'},
            {'naam': 'Operatiegroen (chirurgenkleding)', 'body': '#70b8a0', 'shine': '#e8f8f0', 'eye': '#204838'},
            {'naam': 'Dory (blauwe doktersvis)', 'body': '#3868d0', 'shine': '#f8e050', 'eye': '#202040'},
            {'naam': 'Diepzee (zwart, gloeiend oog)', 'body': ('#383848', {'l': 1.4}), 'shine': '#80d0f8',
             'eye': '#80f0f8'},
            {'naam': 'Gouden hart', 'body': ('#e0b038', {'h': 0}), 'shine': '#f8f0d0', 'eye': '#c02840'},
        ],
    },
    'joltik': {
        # spinnen
        'species': {
            'joltik': {'fur': [2, 4, 1, 10], 'eyes': [9, 5, 8]},
            'galvantula': {'fur': [7, 6, 10], 'body': [1, 3, 2], 'legs': [9], 'eyes': [8, 11]},
        },
        'variants': [
            {'naam': 'Pauwspin (Maratus: blauw, oranje, rood)', 'fur': '#3878d8', 'body': '#f08830', 'legs': '#c02828',
             'eyes': '#30c8f0'},
            {'naam': 'Zwarte weduwe (zwart met rood)', 'fur': ('#383440', {'l': 1.4}), 'body': '#c81820',
             'legs': '#202020', 'eyes': '#e83030'},
            {'naam': 'Goliath-vogelspin (bruin, roze haar)', 'fur': '#8a5a3a', 'body': '#d89098', 'legs': '#4a3020',
             'eyes': '#e8c0a0'},
            {'naam': 'Roodknievogelspin (zwart en oranje)', 'fur': '#e86818', 'body': ('#303038', DARK),
             'legs': '#f0a040', 'eyes': '#e8e0d0'},
            {'naam': 'Groene lynxspin (lime)', 'fur': '#88d048', 'body': '#e8e870', 'legs': '#c04040',
             'eyes': '#3a8028'},
            {'naam': 'Spider-Man (rood en blauw)', 'fur': '#d82028', 'body': '#2850c0', 'legs': '#202848',
             'eyes': '#f0f0f8'},
        ],
    },
    'ferroseed': {
        # metalen en stekelige vruchten (Ferroseed is een bolster)
        'species': {
            'ferroseed': {'metal': [7, 5, 4, 8, 10], 'spikes': [2, 6, 1], 'eyes': [12, 11]},
            'ferrothorn': {'metal': [6, 4, 1, 3], 'spikes': [8, 7, 5], 'eyes': [11, 10]},
        },
        'variants': [
            {'naam': 'Koper met kopergroen (patina)', 'metal': '#c07040', 'spikes': '#40b0a0', 'eyes': '#f0e060'},
            {'naam': 'Tamme kastanje (bruine bolster)', 'metal': '#8a5a30', 'spikes': '#a8a040', 'eyes': '#f0d8a0'},
            {'naam': 'Durian (geelgroene stekels)', 'metal': '#c0b850', 'spikes': '#587018', 'eyes': '#f0f0b0'},
            {'naam': 'Ramboetan (rood met groene haren)', 'metal': '#c02830', 'spikes': '#78b030', 'eyes': '#f8f0d0'},
            {'naam': 'Zeemijn (zwart, rode lampjes)', 'metal': ('#404048', {'l': 1.4}), 'spikes': '#c82020',
             'eyes': '#f83030'},
            {'naam': 'Goud met smaragd', 'metal': ('#d8b040', {'h': 0}), 'spikes': '#108858', 'eyes': '#f8f8f8'},
        ],
    },
    'klink': {
        # tandwielen en machines
        'species': {
            'klink': {'gear': [4, 3, 1, 6, 10], 'core': [9, 8]},
            'klang': {'gear': [5, 4], 'gear2': [6, 1, 2], 'band': [10, 13], 'core': [9, 12, 8, 11]},
            'klinklang': {'gear': [5, 4], 'gear2': [6, 1, 2], 'band': [10, 13], 'core': [9, 12, 8, 11],
                          'red': [15, 14]},
        },
        'variants': [
            {'naam': 'Steampunk (messing en koper)', 'gear': '#d8b058', 'gear2': '#b06838', 'band': '#704830',
             'core': '#40c890', 'red': '#40c890', 'klink:gear': '#c87840'},
            {'naam': 'Gietijzer met roest', 'gear': ('#5a5a62', {'l': 1.3}), 'gear2': '#b05828', 'band': '#c05820',
             'core': '#e8a030', 'red': '#f0d050', 'klink:gear': ('#5a4a44', {'l': 1.3})},
            {'naam': 'Meccano (rode en groene platen)', 'gear': '#d03030', 'gear2': '#389048', 'band': '#e8c040',
             'core': '#e8c040', 'red': '#3060c8'},
            {'naam': 'Geanodiseerd aluminium (paars en cyaan)', 'gear': '#a060e0', 'gear2': '#30a8c8',
             'band': '#5040a0', 'core': '#f070c0', 'red': '#f8e060'},
            {'naam': 'RX-78 Gundam (wit, blauw, rood, geel)', 'gear': ('#f0f0f8', ALBINO), 'gear2': '#3050b0',
             'band': '#e0c030', 'core': '#e8c020', 'red': '#d02828'},
            {'naam': 'Gouden zakhorloge (blauwe saffier)', 'gear': ('#e8c050', {'h': 0}),
             'gear2': ('#b88828', {'h': 0}), 'band': '#f0e0a0', 'core': '#2858d0', 'red': '#2858d0'},
        ],
    },
    'tynamo': {
        # murenen en sidderalen
        'species': {
            'tynamo': {'body': [3, 1, 6, 2, 4], 'spots': [10, 9], 'mouth': [8, 7, 11]},
            'eelektrik': {'body': [6, 5], 'belly': [3, 1, 2], 'mouth': [9, 8, 7], 'spots': [11, 10]},
            'eelektross': {'body': [3, 1, 2, 4], 'belly': [10, 7, 6], 'mouth': [11, 12], 'spots': [9, 8]},
        },
        'variants': [
            {'naam': 'Lintmurene (koningsblauw met gele vinnen)', 'body': '#2848c0', 'belly': '#f0d030', 'mouth': '#f8e070',
             'spots': '#f8f070', 'tynamo:body': '#7898e8'},
            {'naam': 'Echte sidderaal (bruingrijs, oranje buik)', 'body': ('#4a4038', {'l': 1.3}), 'belly': '#e89040',
             'mouth': '#e8c098', 'spots': '#f0a040', 'tynamo:body': '#a89070'},
            {'naam': 'Drakenmurene (oranjerood met witte vlekken)', 'body': '#c84020', 'belly': '#f8d8b0',
             'mouth': '#f8e0c8', 'spots': '#f8f8f0', 'tynamo:body': '#f09070'},
            {'naam': 'Zebramurene (zwart en wit)', 'body': ('#383840', {'l': 1.5}), 'belly': '#e8e8f0',
             'mouth': '#d84050', 'spots': '#f8f8f8', 'tynamo:body': ('#e0e0e8', ALBINO), 'tynamo:spots': '#383840'},
            {'naam': 'Diepzee-bioluminescentie (violet met roze lichtjes)', 'body': '#5030a0', 'belly': '#c0a8f0',
             'mouth': '#f070c0', 'spots': '#f880e0', 'tynamo:body': '#b8a0f0'},
            {'naam': 'Goudstaartmurene', 'body': ('#c89830', {'h': 0}), 'belly': '#f8f0d0', 'mouth': '#d04030',
             'spots': '#f8f8e0', 'tynamo:body': ('#e8c060', {'h': 0}), 'tynamo:spots': '#e06020'},
        ],
    },
    'elgyem': {
        # buitenaardsen uit de popcultuur
        'species': {
            'elgyem': {'head': [3, 4, 1, 2], 'suit': [7, 6], 'eyes': [10, 8], 'lights': [12, 11, 13, 14]},
            'beheeyem': {'head': [4, 2, 1, 3], 'suit': [6], 'band': [8, 7, 14], 'feet': [9, 11, 10],
                         'lights': [13, 12]},
        },
        'variants': [
            {'naam': 'Little Green Men (klassieke marsmannetjes)', 'head': '#88c848', 'suit': '#3a6028',
             'eyes': '#202020', 'band': '#e83030', 'feet': '#d0f0a0', 'lights': '#e83030'},
            {'naam': "Na'vi (Avatar: blauw met gele ogen)", 'head': '#4878c8', 'suit': '#283868', 'eyes': '#f0d030',
             'band': '#f0d030', 'feet': '#a8c8f0', 'lights': '#f070c0'},
            {'naam': 'Mars Attacks! (roze hersenen, groene huid)', 'head': '#e898b0', 'suit': '#58a048',
             'eyes': '#202020', 'band': '#58a048', 'feet': '#f0d0d8', 'lights': '#f8f040'},
            {'naam': 'De rode planeet (Marszand)', 'head': '#c05830', 'suit': '#603020', 'eyes': '#f8c040',
             'band': '#f8c040', 'feet': '#e8a878', 'lights': '#f8e080'},
            {'naam': 'Men in Black (zwart pak, neuralyzer-licht)', 'head': ('#404048', {'l': 1.4}),
             'suit': ('#282830', DARK), 'eyes': '#f0f0f0', 'band': '#f0f0f0', 'feet': '#f0f0f0',
             'lights': '#f8f8ff'},
            {'naam': 'Silver Surfer (chroom)', 'head': ('#c8d0d8', {'l': 1.5}), 'suit': '#8890a0', 'eyes': '#3060c0',
             'band': '#3060c0', 'feet': '#f8f8ff', 'lights': '#60c0f8'},
        ],
    },
    'litwick': {
        # vlamkleuren uit de scheikunde, en een beroemde kandelaar
        'species': {
            'litwick': {'flame': [2, 1, 3, 4], 'wax': [8, 7, 6, 9], 'eyes': [11, 10]},
            'lampent': {'flame': [5, 8, 7], 'metal': [2, 3], 'glass': [4, 11, 6], 'eyes': [10, 9]},
            'chandelure': {'flame': [2, 1, 3], 'metal': [5, 6], 'glass': [7, 9], 'eyes': [10]},
        },
        'variants': [
            {'naam': 'Boriumvlam (groen)', 'flame': '#38c050', 'wax': '#e8f0d8', 'metal': ('#2a3a30', DARK),
             'glass': '#d8f0d8', 'eyes': '#f8f070'},
            {'naam': 'Strontiumvlam (scharlaken)', 'flame': '#e83020', 'wax': '#f8e8e0', 'metal': ('#4a1828', DARK),
             'glass': '#f8d8e0', 'eyes': '#f8e8a0'},
            {'naam': 'Gasvlam (blauw)', 'flame': '#2878f0', 'wax': '#d8e8f8', 'metal': ('#1c2848', DARK),
             'glass': '#c8e0f8', 'eyes': '#f8f8f8'},
            {'naam': 'Ectoplasma (roze spookvlam, zwarte kaars)', 'flame': '#f070d0', 'wax': ('#484450', {'l': 1.4}),
             'metal': ('#382838', DARK), 'glass': '#f8d0f0', 'eyes': '#80f0f0'},
            {'naam': 'Magnesiumfakkel (witheet, zilver)', 'flame': ('#e8f0f8', ALBINO), 'wax': '#c0c8d8',
             'metal': '#a0a8b8', 'glass': '#f0f8ff', 'eyes': '#30a0f0'},
            {'naam': 'Lumière (Belle en het Beest: goud, warme vlam)', 'flame': '#f8b030', 'wax': '#f8f0d8',
             'metal': ('#c89028', {'h': 0}), 'glass': '#f8e8b0', 'eyes': '#c03020'},
        ],
    },
    'axew': {
        # beroemde draken
        'species': {
            'axew': {'skin': [6, 7, 15], 'tusk': [4, 1, 3, 2], 'jaw': [12, 13, 14], 'eyes': [8, 11]},
            'fraxure': {'skin': [3, 4, 1], 'plate': [5, 6, 9, 12, 14], 'tusk': [8, 7, 11, 13, 15]},
            'haxorus': {'skin': [9, 10, 6, 7], 'plate': [4, 8, 11], 'tusk': [3, 1, 5]},
        },
        'variants': [
            {'naam': 'Smaug (roodgoud, op zijn goudschat)', 'skin': '#b83020', 'plate': '#e0b048', 'tusk': '#f0d060',
             'jaw': '#f0d8a0', 'eyes': '#f0d060'},
            {'naam': 'Spyro (paars met gouden hoorns)', 'skin': '#8048c8', 'plate': '#e8c048', 'tusk': '#f0d060',
             'jaw': '#f0e0a0', 'eyes': '#30a030'},
            {'naam': 'Chinese jadedraak (jade, wit jade, rood)', 'skin': '#40a078', 'plate': '#e8ecd8', 'tusk': '#c83028',
             'jaw': '#e8ecd8', 'eyes': '#e8c030'},
            {'naam': 'Viserion (Game of Thrones: roomwit en goud)', 'skin': ('#e8e0d0', ALBINO), 'plate': '#d0a050',
             'tusk': '#b87038', 'jaw': '#f0d8a0', 'eyes': '#e8a020'},
            {'naam': 'Saphira (Eragon: saffierblauw, ivoren hoorns)', 'skin': '#2858c0', 'plate': '#90c0f0',
             'tusk': '#f0ece0', 'jaw': '#b0d8f8', 'eyes': '#30c0f0'},
            {'naam': 'Mechagodzilla (chroom, gele bijlen)', 'skin': ('#b8c0d0', {'l': 1.3}),
             'plate': ('#485060', DARK), 'tusk': '#f8c020', 'jaw': '#505868', 'eyes': '#f8e030'},
        ],
    },
    'cubchoo': {
        # beren (Cubchoo's snotbel en Beartics baard worden mee-ijs)
        'species': {
            'cubchoo': {'fur': [3, 1, 2, 13, 14], 'belly': [9, 12, 11, 8], 'snot': [7, 6, 10, 5]},
            'beartic': {'fur': [3, 2, 1], 'snot': [9, 7, 8, 5], 'nose': [6, 10], 'mouth': [12, 11]},
        },
        'variants': [
            {'naam': 'Grizzly (bruin met honing)', 'fur': '#9a6840', 'belly': '#d8b890', 'snot': '#f0b840',
             'nose': '#3a2818', 'mouth': '#e07080'},
            {'naam': 'Zwarte beer (zwart, wit ijs)', 'fur': ('#3a3640', {'l': 1.5}), 'belly': '#888090',
             'snot': '#e0f0f8', 'nose': '#c8a888', 'mouth': '#e07080'},
            {'naam': 'Troetelbeertje (Hartjesbeer: roze, rode hartjes)', 'fur': '#f0a8c0', 'belly': '#f8e8f0',
             'snot': '#e03050', 'nose': '#e03050', 'mouth': '#f8d0e0'},
            {'naam': 'Gletsjerbeer (blauwgrijs, Alaska)', 'fur': '#607090', 'belly': '#c8d0e0', 'snot': '#c8f0f8',
             'nose': '#283048', 'mouth': '#e07080'},
            {'naam': 'Gummibeertje (groen met rood)', 'fur': '#68c048', 'belly': '#c8f0a0', 'snot': '#e83040',
             'nose': '#2a6020', 'mouth': '#f8e040'},
            {'naam': 'Winnie de Poeh (honinggoud, rood shirt)', 'fur': ('#e8b030', {'h': 0}), 'belly': '#d02828',
             'snot': '#d02828', 'nose': '#5a3018', 'mouth': '#d02828'},
        ],
    },
    'cryogonal': {
        # edelstenen
        'species': {
            'cryogonal': {'body': [2, 1, 6, 4, 7], 'facet': [10, 9, 8, 5], 'chain': [12, 11, 13, 14]},
        },
        'variants': [
            {'naam': 'Amethist', 'body': '#8048b8', 'facet': '#e0c8f8', 'chain': '#c890f0'},
            {'naam': 'Smaragd', 'body': '#20a060', 'facet': '#b8f0c8', 'chain': '#60e090'},
            {'naam': 'Robijn', 'body': '#c01838', 'facet': '#f8b8c8', 'chain': '#f86080'},
            {'naam': 'Citrien', 'body': ('#d8a020', {'h': 0}), 'facet': ('#f8f0b0', {'h': 0}), 'chain': '#f8d050'},
            {'naam': 'Zwart ijs (obsidiaan met cyaan glans)', 'body': ('#303040', {'l': 1.4}), 'facet': '#60d8f0',
             'chain': '#60d8f0'},
            {'naam': 'Opaal (melkwit met regenboogglans)', 'body': ('#d8e0f0', {'l': 1.4}), 'facet': '#f8d0f0',
             'chain': '#60e0b0'},
        ],
    },
    'stunfisk': {
        # platvissen en modder
        'species': {
            'stunfisk': {'body': [9, 7, 6, 5, 8], 'marks': [2, 1, 3, 10], 'lips': [15, 14, 13], 'eyes': [12, 11]},
        },
        'variants': [
            {'naam': 'Schol (grijsbruin met oranje vlekken)', 'body': '#a09078', 'marks': '#f07820', 'lips': '#e8d0b0',
             'eyes': '#f0f0f0'},
            {'naam': 'Pauwbot (zandbeige met blauwe vlekken)', 'body': '#d8c098', 'marks': '#3878d0', 'lips': '#a08060',
             'eyes': '#f0f0f0'},
            {'naam': 'Veenmoeras (mosgroen, oranje vlekken)', 'body': '#6a8848', 'marks': '#e8a030', 'lips': '#c8c890',
             'eyes': '#f8f0c0'},
            {'naam': 'Albino platvis (rode ogen)', 'body': ('#ece4dc', ALBINO), 'marks': '#f8d0d8', 'lips': '#f0b8b8',
             'eyes': '#e83040'},
            {'naam': 'Teerput (zwart met cyaan bliksem)', 'body': ('#403c44', {'l': 1.4}), 'marks': '#40e0f8',
             'lips': '#706870', 'eyes': '#f8f8f8'},
            {'naam': 'Pikachu-platvis (geel met rode wangen)', 'body': '#f0c838', 'marks': '#d82828', 'lips': '#8a5020',
             'eyes': '#f8f8f8'},
        ],
    },
    'stunfisk_galar': {
        # berenklemmen en vleesetende planten (Galar: Ground/Steel)
        'species': {
            'stunfisk/galar': {'body': [4, 1, 2], 'jaw': [8, 5, 9, 10, 15], 'lips': [6, 7], 'mouth': [14, 13, 12]},
        },
        'variants': [
            {'naam': 'Roestige berenklem', 'body': '#8a4a28', 'jaw': '#c08060', 'lips': '#f0c040', 'mouth': '#702020'},
            {'naam': 'Venusvliegenval (groen met rode bek)', 'body': '#3a7030', 'jaw': '#a8c870', 'lips': '#d83040',
             'mouth': '#f080a0'},
            {'naam': 'Koper met patina', 'body': '#a86038', 'jaw': '#e0b090', 'lips': '#40c0b0', 'mouth': '#305858'},
            {'naam': 'Gietijzer (zwart met rode lippen)', 'body': ('#38383c', {'l': 1.4}), 'jaw': '#808088',
             'lips': '#e02828', 'mouth': '#f8d040'},
            {'naam': 'Legercamouflage (kaki en zand)', 'body': '#5a6038', 'jaw': '#c8b080', 'lips': '#8a7040',
             'mouth': '#4a3020'},
            {'naam': 'Gouden klem met robijnen lippen', 'body': ('#c09028', {'h': 0}), 'jaw': '#f0e0a0',
             'lips': '#c01838', 'mouth': '#601020'},
        ],
    },
    'mienfoo': {
        # Kung Fu Panda: de Furious Five en hun meesters
        'species': {
            'mienfoo': {'fur': [2, 5, 3, 1, 4], 'limbs': [9, 7, 11, 12]},
            'mienshao': {'fur': [6, 5, 4], 'limbs': [9, 8, 7], 'tuft': [12, 2, 1], 'eyes': [10, 11]},
        },
        'variants': [
            {'naam': 'Tigress (oranje met zwart en rood)', 'fur': '#f09038', 'limbs': ('#383038', DARK),
             'tuft': '#c82828', 'eyes': '#f0c030'},
            {'naam': 'Monkey (goudbruin, donkerbruin)', 'fur': '#c8a068', 'limbs': '#5a3820', 'tuft': '#e8d0a0',
             'eyes': '#f0c030'},
            {'naam': 'Mantis (helgroen)', 'fur': '#98d860', 'limbs': '#307828', 'tuft': '#e8f070', 'eyes': '#202020'},
            {'naam': 'Po de panda (wit en zwart)', 'fur': ('#f0f0f0', ALBINO), 'limbs': ('#34343c', {'l': 1.5}),
             'tuft': '#e8c040', 'eyes': '#30a030'},
            {'naam': 'Meester Shifu (rode panda)', 'fur': '#c05028', 'limbs': '#382018', 'tuft': '#f0e0c8',
             'eyes': '#3060c0'},
            {'naam': 'De Drakenkrijger (goud met rood)', 'fur': ('#e8c040', {'h': 0}), 'limbs': '#c02020',
             'tuft': '#f8f0c0', 'eyes': '#c02020'},
        ],
    },
    'druddigon': {
        # kaiju uit de Godzilla-films
        'species': {
            'druddigon': {'body': [4, 3, 2], 'head': [7, 6, 5, 11], 'yellow': [9], 'belly': [12, 13],
                          'claws': [8, 10]},
        },
        'variants': [
            {'naam': 'Megalon (zilver met gouden kop)', 'body': '#9098b0', 'head': '#d8a828', 'yellow': '#e83030',
             'belly': '#c8c8d0', 'claws': '#f0f0e0'},
            {'naam': 'Rodan (roodbruin, oranje kop)', 'body': '#8a3820', 'head': '#f08830', 'yellow': '#f8e060',
             'belly': '#e0b080', 'claws': '#f0e8d0'},
            {'naam': 'Godzilla (houtskool, blauwe atoomgloed)', 'body': ('#484850', {'l': 1.4}), 'head': '#40a0f0',
             'yellow': '#a0f0ff', 'belly': '#686870', 'claws': '#d8d8e0'},
            {'naam': 'Anguirus (zandbeige, bruine stekels)', 'body': '#c0a070', 'head': '#6a4828', 'yellow': '#f0c040',
             'belly': '#f0e0c0', 'claws': '#f8f8f0'},
            {'naam': 'Destoroyah (karmijn en paars)', 'body': '#5a2878', 'head': '#d02838', 'yellow': '#f8e040',
             'belly': '#a070c0', 'claws': '#f0d0f0'},
            {'naam': 'King Ghidorah (goud, rode vleugels)', 'body': ('#d8a830', {'h': 0}), 'head': '#c02020',
             'yellow': '#f8f0c0', 'belly': '#f0e0a0', 'claws': '#f8f8f0'},
        ],
    },
    'golett': {
        # golems en reuzenbeelden
        'species': {
            'golett': {'body': [3, 5, 4, 6, 1, 2, 8], 'bands': [11, 12, 10], 'eyes': [9, 13, 14]},
            'golurk': {'body': [7, 6, 5, 3, 2, 1], 'bands': [12, 13, 11], 'eyes': [8, 10, 9]},
        },
        'variants': [
            {'naam': 'Terracottaleger (gebakken klei, brons)', 'body': '#c07050', 'bands': '#806840',
             'eyes': '#f0e0b0'},
            {'naam': 'Abu Simbel (zandsteen, lapis lazuli)', 'body': '#d0b078', 'bands': '#3060a8', 'eyes': '#40c0f0'},
            {'naam': 'Grieks marmer (wit met goud)', 'body': ('#e0dcd8', {'l': 1.2}), 'bands': '#d0a040',
             'eyes': '#5080d0'},
            {'naam': 'Basalt (zwart met cyaan ogen)', 'body': ('#444450', {'l': 1.4}), 'bands': '#808898',
             'eyes': '#40e0f8'},
            {'naam': 'Tetsujin 28 / Gigantor (blauw met rood)', 'body': '#3858a8', 'bands': '#c82828',
             'eyes': '#f8e050'},
            {'naam': 'Kolos van Rhodos (brons en goud)', 'body': ('#b08030', {'h': 0}), 'bands': ('#e8c858', {'h': 0}),
             'eyes': '#f04020'},
        ],
    },
    'pawniard': {
        # Alice in Wonderland: de kaartsoldaten en de schaakstukken achter de spiegel
        'species': {
            'pawniard': {'red': [3, 5, 1], 'blade': [4, 7, 6], 'body': [9, 11, 8], 'eyes': [10, 12]},
            'bisharp': {'red': [10, 11, 8], 'blade': [6, 9, 7, 2], 'body': [12, 13, 14], 'gold': [4, 3, 1]},
        },
        'variants': [
            {'naam': 'Klaverensoldaat (groen en zwart)', 'red': '#2a8a40', 'blade': '#d8e0e0', 'body': ('#2c3430', DARK),
             'gold': '#e0c040', 'eyes': '#f0d040'},
            {'naam': 'Schoppensoldaat (zwart en zilver)', 'red': ('#383840', {'l': 1.5}), 'blade': '#e8e8f0',
             'body': '#687080', 'gold': '#c8ccd8', 'eyes': '#e03030'},
            {'naam': 'Ruitensoldaat (oranje, ivoor)', 'red': '#f08020', 'blade': '#f0e8d8', 'body': '#5a3828',
             'gold': '#f8d878', 'eyes': '#f8f0a0'},
            {'naam': 'De Witte Koningin (wit en ijszilver)', 'red': ('#e8e8f0', ALBINO), 'blade': '#a8c8e8',
             'body': '#7880a0', 'gold': '#c0c8d8', 'eyes': '#3060c0'},
            {'naam': 'De Cheshire Kat (roze en paars)', 'red': '#d058b8', 'blade': '#f0b0e0', 'body': '#503068',
             'gold': '#f8f070', 'eyes': '#f8f070'},
            {'naam': 'De Gouden Koning (goud, paars, robijn)', 'red': ('#e0b030', {'h': 0}), 'blade': '#f8f0d0',
             'body': '#4a2868', 'gold': '#c82038', 'eyes': '#c82038'},
        ],
    },
    'bouffalant': {
        # afrokapsels en runderen
        'species': {
            'bouffalant': {'afro': [2, 1], 'body': [6, 5, 4, 7], 'horns': [8, 10, 9, 11], 'hooves': [13, 14, 12]},
        },
        'variants': [
            {'naam': 'Zongebleekte surfer (blonde afro)', 'afro': '#e8c870', 'body': '#8a6040', 'horns': '#f8f0e0',
             'hooves': '#584838'},
            {'naam': 'Ronald McDonald (rode afro, geel pak)', 'afro': '#d82820', 'body': '#e8c040', 'horns': '#f8f8f8',
             'hooves': '#c02020'},
            {'naam': 'Purple Haze (Jimi Hendrix)', 'afro': '#6a2898', 'body': '#5a4038', 'horns': '#f0d8f8',
             'hooves': '#302838'},
            {'naam': 'Schotse hooglander (gember)', 'afro': '#c86020', 'body': '#a05030', 'horns': '#f0e0c0',
             'hooves': '#3a2820'},
            {'naam': 'Discokoning (discobal-afro, wit pak)', 'afro': ('#c0c8d8', {'l': 1.3}),
             'body': ('#e8e4e0', ALBINO), 'horns': '#f8d048', 'hooves': '#8890a0'},
            {'naam': 'Het gouden kalf', 'afro': ('#b08020', {'h': 0}), 'body': ('#e0b840', {'h': 0}),
             'horns': '#f8f0c0', 'hooves': '#806018'},
        ],
    },
    'rufflet': {
        # adelaars op nationale vlaggen (Braviary is de Amerikaanse zeearend)
        'species': {
            'rufflet': {'body': [1, 10, 11, 14], 'white': [6, 7, 3, 5], 'plume': [9, 8], 'beak': [12, 13]},
            'braviary': {'plume': [3, 2, 1], 'body': [6, 12, 5], 'white': [8, 11, 9, 7], 'beak': [14, 13, 10],
                         'tips': [15]},
        },
        'variants': [
            {'naam': 'Bundesadler (Duitsland: zwart, rood, goud)', 'plume': '#e8b830', 'body': ('#34343c', {'l': 1.5}),
             'white': '#d83028', 'beak': '#e8b830', 'tips': '#d83028'},
            {'naam': 'Mexico (steenarend: bruin, groen, wit)', 'plume': '#208848', 'body': '#7a5030',
             'white': '#f0ece0', 'beak': '#e8c040', 'tips': '#c82828'},
            {'naam': 'Zambia (oranje arend op groen)', 'plume': '#e06818', 'body': '#2a7a38', 'white': '#f0a050',
             'beak': '#f8d040', 'tips': '#202020'},
            {'naam': 'Polen (witte adelaar met gouden kroon)', 'plume': '#e8c040', 'body': ('#e0e0e8', ALBINO),
             'white': '#f8f8f8', 'beak': '#e8c040', 'tips': '#d82838'},
            {'naam': 'Egypte (adelaar van Saladin: goud en zwart)', 'plume': ('#383438', DARK),
             'body': ('#d0a030', {'h': 0}), 'white': '#f8f4e8', 'beak': '#c82828', 'tips': '#202020'},
            {'naam': 'Kazachstan (gouden steppe-arend op hemelsblauw)', 'plume': '#f0c838', 'body': '#38a8e0',
             'white': '#f8e8a0', 'beak': '#f0c838', 'tips': '#f0c838'},
        ],
    },
    'braviary_hisui': {
        # mythische vogels (Hisui: Psychic/Flying; moderne sprite)
        'species': {
            'braviary/hisui': {'head': [9, 13, 12], 'body': [11, 14], 'mask': [10, 5, 2, 8], 'beak': [7, 1, 3]},
        },
        'variants': [
            {'naam': 'Roc (Duizend-en-een-nacht: zandbruin en wit)', 'head': '#e0c8a0', 'body': '#6a4828',
             'mask': '#30a0a0', 'beak': '#f0d060'},
            {'naam': 'Hō-ō (Japanse feniks: rood en goud)', 'head': '#e05838', 'body': '#802028', 'mask': '#f0c838',
             'beak': '#f8e070'},
            {'naam': 'Simurgh (Perzisch: turkoois)', 'head': '#78d0c8', 'body': '#205860', 'mask': '#e870a0',
             'beak': '#f0d060'},
            {'naam': 'Quetzalcoatl (gevederde slang: groen en rood)', 'head': '#58b860', 'body': '#205830',
             'mask': '#e03030', 'beak': '#f0c030'},
            {'naam': 'Garuda (goud met rood)', 'head': ('#e8c050', {'h': 0}), 'body': '#a02820', 'mask': '#30a0d0',
             'beak': '#f8f0c0'},
            {'naam': 'Thunderbird (totempaal: blauw, rood, geel)', 'head': '#4878d0', 'body': '#283058',
             'mask': '#e03020', 'beak': '#f8d020'},
        ],
    },
    'vullaby': {
        # gieren, en Día de los Muertos
        'species': {
            'vullaby': {'feathers': [1, 3], 'skin': [5, 6, 4], 'bones': [12, 11, 13], 'fluff': [10, 9]},
            'mandibuzz': {'feathers': [2, 12], 'chest': [13, 14], 'skin': [7, 8, 6], 'bones': [4, 5, 3],
                          'fluff': [11, 15]},
        },
        'variants': [
            {'naam': 'Lammergier (roestoranje borst, leigrijs)', 'feathers': ('#4a4e58', {'l': 1.3}),
             'chest': '#e08838', 'skin': '#f0e0c8', 'bones': '#f8f0e0', 'fluff': '#e08838'},
            {'naam': 'Koningsgier (crème, oranje-paarse kop)', 'feathers': '#d8d0b8', 'chest': '#f0ece0',
             'skin': '#f09040', 'bones': '#a060c0', 'fluff': '#383038'},
            {'naam': 'Himalayagier (zandbeige, blauwe kop)', 'feathers': '#a88858', 'chest': '#e0d0a8',
             'skin': '#a8c8e8', 'bones': '#f0ece0', 'fluff': '#f0ece0'},
            {'naam': 'Calavera (Día de los Muertos: paars, goudsbloem)', 'feathers': '#5a2878', 'chest': '#e85898',
             'skin': '#f8f0f0', 'bones': '#f89820', 'fluff': '#40b0c0'},
            {'naam': 'De Boze Heks van het Westen (groen gezicht)', 'feathers': ('#302830', {'l': 1.5}),
             'chest': '#504858', 'skin': '#68b848', 'bones': '#c8b8e0', 'fluff': '#504858'},
            {'naam': 'Goudgier (goud met zilveren botten)', 'feathers': ('#c89830', {'h': 0}), 'chest': '#f0d878',
             'skin': '#e8b0a0', 'bones': '#d0d8e8', 'fluff': '#f0e0a8'},
        ],
    },
    'heatmor': {
        # miereneters en vlamkleuren (Heatmor is een gasbrander)
        'species': {
            'heatmor': {'body': [4, 1, 2], 'stripes': [5, 3, 10], 'flame': [7, 6, 11]},
        },
        'variants': [
            {'naam': 'Reuzenmiereneter (grijs, zwarte streep met witte rand)', 'body': '#908880',
             'stripes': ('#383438', DARK), 'flame': '#f0f0f0'},
            {'naam': 'Zijdemiereneter (goudgeel met oranje)', 'body': '#d8b060', 'stripes': '#e06820',
             'flame': '#f8f0b0'},
            {'naam': 'Aardvarken met blauwe gasvlam', 'body': '#c0a098', 'stripes': '#3070e0', 'flame': '#80e8f8'},
            {'naam': 'Gietijzeren kachel (gloeiend rood)', 'body': ('#484448', {'l': 1.4}), 'stripes': '#e02818',
             'flame': '#f8a030'},
            {'naam': 'Kopervlam (groen vuur)', 'body': '#806848', 'stripes': '#30a840', 'flame': '#b8f070'},
            {'naam': 'Feniks (goud met karmijn)', 'body': ('#d8a838', {'h': 0}), 'stripes': '#c01838',
             'flame': '#f8f8e0'},
        ],
    },
    'durant': {
        # mieren
        'species': {
            'durant': {'helm': [3, 2, 1], 'body': [4, 5, 6, 7], 'eyes': [9, 8]},
        },
        'variants': [
            {'naam': 'Rode bosmier (roodbruin, zwart)', 'helm': '#b05030', 'body': ('#3a3030', {'l': 1.2}),
             'eyes': '#f8d040'},
            {'naam': 'Honingpotmier (amber)', 'helm': '#e8a838', 'body': '#5a3818', 'eyes': '#202020'},
            {'naam': 'Groenkopmier (metaalgroen)', 'helm': '#48b060', 'body': '#3a3828', 'eyes': '#f0d030'},
            {'naam': 'Blauwe metaalmier (Polyrhachis)', 'helm': '#4878d8', 'body': '#202840', 'eyes': '#f05030'},
            {'naam': 'Kogelmier (zwart met bronsglans)', 'helm': ('#6a5040', {'l': 1.4}), 'body': ('#302824', DARK),
             'eyes': '#e8c040'},
            {'naam': 'Midas-mier (goud)', 'helm': ('#e8c050', {'h': 0}), 'body': '#806020', 'eyes': '#c02020'},
        ],
    },
    'deino': {
        # hydra's en driekoppige monsters
        'species': {
            'deino': {'body': [2, 4, 1, 12], 'fur': [7, 6, 5], 'pink': [11, 10, 9, 8]},
            'zweilous': {'body': [2, 3, 1], 'fur': [5, 6, 7], 'pink': [10, 11, 8]},
            'hydreigon': {'body': [4, 2, 1], 'fur': [10, 9, 8], 'pink': [6, 5, 7, 11, 12]},
        },
        'variants': [
            {'naam': 'Bloedmaan (karmijn vacht, gouden accenten)', 'body': ('#3a2a30', {'l': 1.2}), 'fur': '#b02030',
             'pink': '#e8b030'},
            {'naam': 'Amethisthydra (paarse vacht, turkoois)', 'body': ('#302838', {'l': 1.2}), 'fur': '#7038b0',
             'pink': '#40d0c0'},
            {'naam': 'Sneeuwhydra (ijswit vacht, ijsblauw)', 'body': '#58607a', 'fur': '#e0ecf8', 'pink': '#50b0f0'},
            {'naam': 'Negatief (wit lijf, zwarte vacht)', 'body': ('#d8d8e0', {'l': 1.3}), 'fur': ('#303038', DARK),
             'pink': '#e03080'},
            {'naam': 'Cerberus (Hades: zwart met oranje vlammen)', 'body': ('#383030', {'l': 1.2}), 'fur': '#f07818',
             'pink': '#f8d040'},
            {'naam': 'Hydra-sterrenbeeld (nachtblauw met sterwit)', 'body': ('#20284a', {'l': 1.2}), 'fur': '#f0f0d8',
             'pink': '#e8c040'},
        ],
    },
    'larvesta': {
        # sterren en zonnen (Volcarona is de zon van Unova)
        'species': {
            'larvesta': {'horns': [3, 2, 1], 'fluff': [6, 9, 7, 5], 'body': [14, 12, 13], 'eyes': [10, 11]},
            'volcarona': {'wings': [2, 1, 3], 'flame': [6], 'fluff': [9, 8, 7], 'body': [13, 14, 15, 12],
                          'eyes': [11, 10]},
        },
        'variants': [
            {'naam': 'Blauwe reus (Rigel: blauw vuur)', 'horns': '#3070e0', 'wings': '#2858c8', 'flame': '#60c8f8',
             'fluff': '#e8f0f8', 'body': '#283868', 'eyes': '#f8f8f8'},
            {'naam': 'Zonsverduistering (zwart met gouden corona)', 'horns': ('#383440', {'l': 1.5}),
             'wings': ('#383440', {'l': 1.5}), 'flame': '#f0f0f8', 'fluff': '#c8c8d8', 'body': '#202028',
             'eyes': '#f8f8f8'},
            {'naam': 'Groene flits (bij zonsondergang)', 'horns': '#38a848', 'wings': '#30984a', 'flame': '#b8f060',
             'fluff': '#f0f8e0', 'body': '#2a5830', 'eyes': '#f0e040'},
            {'naam': 'Witte dwerg (wit en ijsblauw)', 'horns': ('#e0e8f0', ALBINO), 'wings': ('#e0e8f0', ALBINO),
             'flame': '#90d8f8', 'fluff': '#c8d8e8', 'body': '#80b8e0', 'eyes': '#3070d0'},
            {'naam': 'Noorderlicht (paars met groen)', 'horns': '#8040c0', 'wings': '#7038b8', 'flame': '#50e090',
             'fluff': '#e0d0f8', 'body': '#30a080', 'eyes': '#50e090'},
            {'naam': 'Eos, de rozenvingerige dageraad (roze en perzik)', 'horns': '#f090a8', 'wings': '#f090a8',
             'flame': '#f8d0a0', 'fluff': '#fff0f0', 'body': '#c06878', 'eyes': '#f8e070'},
        ],
    },
    'cobalion': {
        # paardenvachten (Athos, de edele musketier)
        'species': {
            'cobalion': {'body': [8, 12, 6], 'horns': [4, 2, 1], 'mane': [13, 11], 'face': [7, 9, 5, 14, 15]},
        },
        'variants': [
            {'naam': 'Vos (kastanje met blonde manen)', 'body': '#b84820', 'mane': '#f0d8a0', 'horns': '#f0e8d8',
             'face': '#5a3020'},
            {'naam': 'Fries (zwart met zilveren manen)', 'body': ('#34343c', {'l': 1.5}), 'mane': '#c0c8d8',
             'horns': '#d0a040', 'face': '#585860'},
            {'naam': 'Palomino (goud met witte manen)', 'body': '#e0b048', 'mane': '#f8f8f0', 'horns': '#a07850',
             'face': '#906838'},
            {'naam': 'Schimmel (wit-grijs)', 'body': ('#c8c8d0', {'l': 1.2}), 'mane': '#f8f8f8', 'horns': '#6a6a78',
             'face': '#9898a0'},
            {'naam': 'Aardbeischimmel (roze-grijs, rode manen)', 'body': '#c08880', 'mane': '#8a3830',
             'horns': '#f0e0c8', 'face': '#7a5048'},
            {'naam': 'Paard van Troje (hout met brons)', 'body': '#a07040', 'mane': '#5a3418', 'horns': '#c89040',
             'face': '#6a4420'},
        ],
    },
    'terrakion': {
        # gesteenten (Porthos, de sterke musketier)
        'species': {
            'terrakion': {'body': [5, 7, 6], 'mane': [2, 4, 3], 'tan': [10, 12, 13, 14], 'horn': [9, 8]},
        },
        'variants': [
            {'naam': 'Roze graniet (zwarte spikkels)', 'body': '#b88880', 'mane': '#403038',
             'tan': '#e8d0c8', 'horn': '#f0f0f0'},
            {'naam': 'Basalt (zwart met gloeiende hoorn)', 'body': ('#4a4850', {'l': 1.4}), 'mane': '#282830',
             'tan': '#787480', 'horn': '#f8d030'},
            {'naam': 'Uluru (rode rots)', 'body': '#c05830', 'mane': '#602818', 'tan': '#e8a070', 'horn': '#f0e0b0'},
            {'naam': 'Marmer (wit met grijze aders)', 'body': ('#e0e0e8', {'l': 1.2}), 'mane': '#686878',
             'tan': '#f8f8f8', 'horn': '#3070c0'},
            {'naam': 'Malachiet (groen gestreept)', 'body': '#3a9a60', 'mane': '#1a4830', 'tan': '#90d8a8',
             'horn': '#e8c040'},
            {'naam': 'Lapis lazuli (blauw met pyrietgoud)', 'body': '#2848a0', 'mane': '#182858', 'tan': '#e0c050',
             'horn': '#e0c050'},
        ],
    },
    'virizion': {
        # bladeren en seizoenen (Aramis, de sierlijke musketier)
        'species': {
            'virizion': {'body': [4, 3, 1, 2], 'horns': [8, 12, 10], 'cream': [11, 13, 14], 'face': [7, 6]},
        },
        'variants': [
            {'naam': 'Esdoornherfst (oranje, rode hoorns)', 'body': '#e07828', 'horns': '#c02020', 'cream': '#f8e8c0',
             'face': '#6a4030'},
            {'naam': 'Hulst (donkergroen, bessenrode hoorns)', 'body': '#2a6838', 'horns': '#d02020', 'cream': '#f0f0e0',
             'face': '#203020'},
            {'naam': 'Ginkgo (goudgeel, groene hoorns)', 'body': '#e8c838', 'horns': '#58a030', 'cream': '#f8f8e0',
             'face': '#6a5828'},
            {'naam': 'Berijpt (ijswit en blauw)', 'body': ('#d8e8f0', ALBINO), 'horns': '#4888e0', 'cream': '#f8f8ff',
             'face': '#607080'},
            {'naam': 'Rode beuk (purper, roze hoorns)', 'body': '#7a2848', 'horns': '#f088b0', 'cream': '#e8c8d8',
             'face': '#3a2030'},
            {'naam': 'Zilverspar (blauwgroen, zilveren hoorns)', 'body': '#4a8890', 'horns': '#d0d8e0',
             'cream': '#e0f0f0', 'face': '#304850'},
        ],
    },
    'keldeo': {
        # My Little Pony (D'Artagnan is nog een veulen)
        'species': {
            'keldeo': {'mane': [4, 3, 1], 'tail': [12, 11, 15], 'navy': [10, 8, 6], 'legs': [7, 9, 5]},
            'keldeo/resolute': {'mane': [8, 6], 'tail': [3, 11], 'navy': [7, 5, 10], 'legs': [12, 13, 15],
                                'horn': [4]},
        },
        'variants': [
            {'naam': 'Applejack (oranje met blonde manen)', 'mane': '#f0d070', 'tail': '#f09838', 'navy': '#a05020',
             'legs': '#f0c890', 'horn': '#c03028'},
            {'naam': 'Fluttershy (geel met roze manen)', 'mane': '#f0a0c8', 'tail': '#f8e070', 'navy': '#d07898',
             'legs': '#f8f0c0', 'horn': '#80c0f0'},
            {'naam': 'Twilight Sparkle (lavendel, donkerblauwe manen)', 'mane': '#303878', 'tail': '#c8a0e8',
             'navy': '#e04890', 'legs': '#e0d0f0', 'horn': '#e04890'},
            {'naam': 'Rarity (wit met paarse manen)', 'mane': '#6a3898', 'tail': ('#e8e8f0', ALBINO),
             'navy': '#8048b0', 'legs': '#f8f8f8', 'horn': '#60b0f0'},
            {'naam': 'Pinkie Pie (roze met felroze manen)', 'mane': '#e03890', 'tail': '#f0a8d0', 'navy': '#b02870',
             'legs': '#f8d8e8', 'horn': '#60c8f0'},
            {'naam': 'Prinses Luna (nachtblauw, sterrenmanen)', 'mane': '#80b0f0', 'tail': '#283068',
             'navy': ('#181838', DARK), 'legs': '#4048a0', 'horn': '#e8e0f8'},
        ],
    },
    'reshiram': {
        # vuur en yin-yang (Reshiram: waarheid, het witte vuur)
        'species': {
            'reshiram': {'body': [5, 4, 2, 1, 6], 'parts': [9, 10, 8], 'eyes': [7], 'flame': [12, 11, 13]},
        },
        'variants': [
            {'naam': 'Yin (zwart met blauwe vlam)', 'body': ('#484858', {'l': 1.3}), 'parts': '#2860c0',
             'eyes': '#e83030', 'flame': '#30a0f8'},
            {'naam': 'Zonsondergang (perzik met karmijn vuur)', 'body': '#f0c0a0', 'parts': '#c04050',
             'eyes': '#3060c0', 'flame': '#c81838'},
            {'naam': 'Blauw vuur (ijsblauw lijf)', 'body': '#a8c8f0', 'parts': '#3058b0', 'eyes': '#f8f8f8',
             'flame': '#3888f8'},
            {'naam': 'Witgoud (crème met gouden vlam)', 'body': ('#f0e8d0', ALBINO), 'parts': '#c09838',
             'eyes': '#c03020', 'flame': '#f0c030'},
            {'naam': 'Amethistvuur (lila met paarse vlam)', 'body': '#c8b0e8', 'parts': '#6838a8', 'eyes': '#f0c030',
             'flame': '#9040e0'},
            {'naam': 'Ho-Oh-kleuren (rood, goud, groen)', 'body': '#d84838', 'parts': '#f0c040', 'eyes': '#30a040',
             'flame': '#40c050'},
        ],
    },
    'zekrom': {
        # bliksem en yin-yang (Zekrom: idealen, de zwarte bliksem)
        'species': {
            'zekrom': {'body': [1, 3, 8, 7], 'glow': [6, 5, 2], 'eyes': [11, 10]},
        },
        'variants': [
            {'naam': 'Yang (wit met rode bliksem)', 'body': ('#d8d8e0', {'l': 1.6}), 'glow': '#e83030',
             'eyes': '#3060d0'},
            {'naam': 'Stormnacht (marineblauw, gele bliksem)', 'body': ('#283868', {'l': 1.2}), 'glow': '#f8e040',
             'eyes': '#f8e040'},
            {'naam': 'Bloedonweer (bordeauxzwart, rode gloed)', 'body': ('#4a2028', {'l': 1.2}), 'glow': '#f84040',
             'eyes': '#f8f040'},
            {'naam': 'Gammastraling (Hulk: paars met groen)', 'body': ('#4a3070', {'l': 1.2}), 'glow': '#60f060',
             'eyes': '#60f060'},
            {'naam': 'Raiden (gunmetal met oranje bliksem)', 'body': ('#505868', {'l': 1.3}), 'glow': '#f89030',
             'eyes': '#f0f0f0'},
            {'naam': 'Zeus (goud met witte bliksem)', 'body': ('#c09028', {'h': 0, 'l': 1.2}), 'glow': '#f8f8f8',
             'eyes': '#3060d0'},
        ],
    },
    'kyurem': {
        # ijs in alle kleuren (ook Zwarte en Witte Kyurem)
        'species': {
            'kyurem': {'ice': [7, 3, 1, 2, 4], 'body': [10, 5, 8], 'eyes': [6, 12, 11]},
            'kyurem/black': {'ice': [2, 4, 7], 'body': [6, 1, 9], 'gray': [5, 8, 14], 'glow': [10, 11],
                             'eyes': [12, 13]},
            'kyurem/white': {'ice': [1, 2, 8], 'white': [3, 11, 12], 'gray': [5, 7, 6], 'glow': [9, 10, 13, 15],
                             'eyes': [14]},
        },
        'variants': [
            {'naam': 'Amethistijs (paars ijs)', 'ice': '#b090e0', 'body': '#686078', 'gray': '#787088',
             'white': '#f0e8f8', 'glow': '#e050c0', 'eyes': '#f0e040'},
            {'naam': 'Vuur en ijs (lava-oranje ijs, basalt)', 'ice': '#f09048', 'body': ('#484448', {'l': 1.3}),
             'gray': '#686468', 'white': '#f8e0c8', 'glow': '#f8d040', 'eyes': '#f83020'},
            {'naam': 'Smaragdijs (groen)', 'ice': '#80d898', 'body': '#587060', 'gray': '#6a8070', 'white': '#e8f8ec',
             'glow': '#30c060', 'eyes': '#f8f0a0'},
            {'naam': 'Aardbeiensorbet (roze ijs)', 'ice': '#f8a8c0', 'body': '#907080', 'gray': '#a08890',
             'white': '#fff0f4', 'glow': '#e83868', 'eyes': '#60c8f0'},
            {'naam': 'Zwart ijs (donker met cyaan glans)', 'ice': '#40c8e0', 'body': ('#303038', DARK),
             'gray': '#484850', 'white': '#a8b0c0', 'glow': '#40f0f8', 'eyes': '#f83030'},
            {'naam': 'Gouden ijs (goud en wit)', 'ice': ('#f0d060', {'h': 0}), 'body': '#908058', 'gray': '#a09068',
             'white': '#fff8e0', 'glow': '#f09020', 'eyes': '#c02020'},
        ],
    },
    'genesect': {
        # mecha (de Drive-kleurvormen krijgen geen varianten)
        'species': {
            'genesect': {'body': [3, 2, 1], 'light': [5, 9], 'cannon': [7, 8, 6], 'eyes': [11, 12, 10]},
        },
        'variants': [
            {'naam': 'Zaku II (groen, roze mono-oog)', 'body': '#5a8a48', 'light': '#a8c890', 'cannon': '#4a5a40',
             'eyes': '#f060a0'},
            {'naam': 'Evangelion Unit-00 (blauw met wit)', 'body': '#3060c0', 'light': '#f0f0f8', 'cannon': '#e8e8f0',
             'eyes': '#f04040'},
            {'naam': 'Bumblebee (geel met zwart)', 'body': '#e8c030', 'light': '#f8f0b0', 'cannon': ('#383840', DARK),
             'eyes': '#40c0f0'},
            {'naam': 'Tron (zwart met cyaan lichtlijnen)', 'body': ('#303040', {'l': 1.4}), 'light': '#40e8f8',
             'cannon': '#40e8f8', 'eyes': '#f8f8f8'},
            {'naam': 'RoboCop (zilver)', 'body': ('#a8b0c0', {'l': 1.3}), 'light': '#e8eef8', 'cannon': '#505868',
             'eyes': '#f03030'},
            {'naam': 'Unicorn Gundam (wit met rood psychoframe)', 'body': ('#e8e8f0', {'l': 1.3}), 'light': '#f04050',
             'cannon': '#d8a830', 'eyes': '#30d070'},
        ],
    },
    'basculegion': {
        # zielvuur en geestenvissen (mannetje roze, vrouwtje blauw; moderne sprites)
        'species': {
            'basculegion': {'spirit': [2, 3, 1, 14, 13], 'body': [6, 7, 8], 'fins': [10, 9, 11]},
            'basculegion/f': {'spirit': [5, 1, 3, 14], 'body': [9, 6, 7], 'fins': [10, 8, 11]},
        },
        'variants': [
            {'naam': 'Dwaallicht (groen spookvuur)', 'spirit': '#50d060', 'body': '#4a5040', 'fins': '#c0d0b0'},
            {'naam': 'Blauwe vlam van de Styx (indigo)', 'spirit': '#4050d8', 'body': '#40445a',
             'fins': '#d8d8f0'},
            {'naam': 'Bloedmaan (rood)', 'spirit': '#d82828', 'body': '#4a3838', 'fins': '#c8a8a8'},
            {'naam': 'Lantaarnvis (mannetje geel licht, vrouwtje roze)', 'spirit': '#f0d030', 'body': '#3a4458',
             'fins': '#a8b8d0', 'basculegion/f:spirit': '#f06090'},
            {'naam': 'Día de los Muertos (goudsbloem-oranje)', 'spirit': '#f08818', 'body': '#4a2a58',
             'fins': '#e0b0f0'},
            {'naam': 'De Vliegende Hollander (zilvergrijs met cyaan vuur)', 'spirit': '#40e0f0', 'body': '#808890',
             'fins': '#f0f4f8', 'basculegion/f:spirit': ('#f0f4ff', {'l': 1.3})},
        ],
    },
    'landorus': {
        # aarde en oogst
        'species': {
            'landorus': {'cloud': [3, 4, 14], 'body': [8, 7, 9], 'tail': [15, 12, 11, 1], 'marks': [6, 5, 13],
                         'eyes': [10]},
            'landorus/therian': {'cloud': [7, 8, 6], 'body': [11, 12, 10], 'tail': [4, 1, 5], 'marks': [3, 13, 9],
                                 'eyes': [14]},
        },
        'variants': [
            {'naam': 'Vulkanische aarde (zwart met rood)', 'body': ('#484040', {'l': 1.3}), 'tail': '#302828',
             'marks': '#e03020', 'cloud': '#c8c0c0', 'eyes': '#f8d030'},
            {'naam': 'Rijstveld (jonggroen met wolken)', 'body': '#80c050', 'tail': '#5a7838', 'marks': '#e8d060',
             'cloud': '#f8f8f0', 'eyes': '#f8d030'},
            {'naam': 'Blauwe klei (blauwgrijs)', 'body': '#7088a8', 'tail': '#485868', 'marks': '#c06048',
             'cloud': '#e0e8f0', 'eyes': '#f8e070'},
            {'naam': 'Krijt (wit, okerbruine tekening)', 'body': ('#e8e4dc', ALBINO), 'tail': '#a89880',
             'marks': '#c07830', 'cloud': '#c8c8d0', 'eyes': '#c02020'},
            {'naam': 'Lavendelveld (Provence)', 'body': '#9070c8', 'tail': '#5a6838', 'marks': '#e8d870',
             'cloud': '#f0ecf8', 'eyes': '#f8e070'},
            {'naam': 'Gouden oogst (rijpe tarwe)', 'body': ('#e0b030', {'h': 0}), 'tail': '#a07028', 'marks': '#c03020',
             'cloud': '#f8f0d0', 'eyes': '#30a040'},
        ],
    },
    'meloetta': {
        # Vocaloids (ook in Pirouette-vorm)
        'species': {
            'meloetta': {'hair': [6, 5, 7], 'body': [4, 2, 1], 'notes': [11, 8], 'accent': [14]},
            'meloetta/pirouette': {'hair': [7, 5, 6, 8], 'body': [3, 4, 1], 'accent': [13, 11, 12]},
        },
        'variants': [
            {'naam': 'Kagamine Rin (blond, matrozenpakje)', 'hair': '#f0d040', 'body': '#9898a8', 'notes': '#f09020',
             'accent': '#f09020'},
            {'naam': 'KAITO (blauw haar, witte jas)', 'hair': '#3060d0', 'body': '#c8c8d8', 'notes': '#3060d0',
             'accent': '#3060d0'},
            {'naam': 'Megurine Luka (roze haar, zwart en goud)', 'hair': '#f090b0', 'body': ('#383040', {'l': 1.3}),
             'notes': '#e8c040', 'accent': '#e8c040'},
            {'naam': 'MEIKO (bruinrood haar, rood pak)', 'hair': '#8a3020', 'body': '#b02828', 'notes': '#f0a040',
             'accent': '#f0a040'},
            {'naam': 'Kamui Gakupo (paars haar, witte kimono)', 'hair': '#8050c0', 'body': '#d8d0e8', 'notes': '#8050c0',
             'accent': '#e0c040'},
            {'naam': 'Hatsune Miku (turkoois haar, grijs, roze das)', 'hair': '#30c8c0', 'body': '#585868',
             'notes': '#e83070', 'accent': '#e83070'},
        ],
    },
    'thundurus': {
        # onweer en bliksemverschijnselen
        'species': {
            'thundurus': {'cloud': [2, 3, 1], 'body': [9, 7], 'spots': [6, 5, 8], 'tail': [13, 12, 10],
                          'claws': [14], 'eyes': [11]},
            'thundurus/therian': {'cloud': [2, 5, 1], 'body': [10, 8, 9], 'spots': [7, 6, 4], 'tail': [14, 13],
                                  'eyes': [12, 11]},
        },
        'variants': [
            {'naam': 'Red sprite (rode bliksem boven de wolken)', 'body': '#e04838', 'spots': '#5838a0',
             'tail': ('#3a2830', {'l': 1.2}), 'claws': '#f0c040', 'cloud': '#e8e0e8', 'eyes': '#f8e040'},
            {'naam': 'Bolbliksem (oranjegeel)', 'body': '#f0a830', 'spots': '#c05018', 'tail': ('#3a3028', {'l': 1.2}),
             'claws': '#f8f0d0', 'cloud': '#f0ece0', 'eyes': '#c02020'},
            {'naam': 'Stormwolk (leigrijs met gele bliksem)', 'body': '#686e80', 'spots': '#f8e040',
             'tail': ('#282830', DARK), 'claws': '#f8e040', 'cloud': '#a8acb8', 'eyes': '#f8e040'},
            {'naam': 'Witte flits (wit en cyaan)', 'body': ('#e0ecf8', {'l': 1.3}), 'spots': '#30c8f0',
             'tail': '#586078', 'claws': '#80e0f8', 'cloud': '#f8f8ff', 'eyes': '#3060d0'},
            {'naam': 'Sint-Elmusvuur (violet met cyaan)', 'body': '#8050d0', 'spots': '#40e8f0',
             'tail': ('#302840', DARK), 'claws': '#e0c8f8', 'cloud': '#e8e0f8', 'eyes': '#40e8f0'},
            {'naam': 'Zeus (goud en wit)', 'body': ('#e0b838', {'h': 0}), 'spots': '#f8f8f0', 'tail': '#806028',
             'claws': '#f8f8f0', 'cloud': '#f8f4e0', 'eyes': '#3060d0'},
        ],
    },
    'tornadus': {
        # beroemde winden
        'species': {
            'tornadus': {'cloud': [2, 4, 1], 'body': [8, 7, 10], 'tail': [5, 9, 6], 'tan': [13, 14, 12], 'eyes': [11]},
            'tornadus/therian': {'cloud': [6, 7, 5], 'body': [9, 11, 8], 'tail': [3, 1, 2], 'tan': [12, 13, 10],
                                 'eyes': [14]},
        },
        'variants': [
            {'naam': 'Sirocco (woestijnrood, zandstorm)', 'body': '#c05030', 'tail': '#d8b070', 'tan': '#704020',
             'cloud': '#f0e0c8', 'eyes': '#f8e040'},
            {'naam': 'Mistral (koud blauw)', 'body': '#3870c0', 'tail': '#a0b8e8', 'tan': '#d8d0b8', 'cloud': '#f0f4f8',
             'eyes': '#f0c030'},
            {'naam': 'Harmattan (stoffig okergeel)', 'body': '#c8a040', 'tail': '#806030', 'tan': '#f0e0b0',
             'cloud': '#e8dcc8', 'eyes': '#c02020'},
            {'naam': 'Bora (ijzige valwind: wit en ijsblauw)', 'body': ('#d8e8f0', {'l': 1.3}), 'tail': '#a8d0e8',
             'tan': '#90a8c0', 'cloud': '#f8f8ff', 'eyes': '#3060d0'},
            {'naam': 'Santa Ana (zonsondergang: roze en oranje)', 'body': '#f08868', 'tail': '#d84888',
             'tan': '#f8d080', 'cloud': '#f8e0e0', 'eyes': '#f8f040'},
            {'naam': 'Aeolus (god van de winden: goud met witte wind)', 'body': ('#e0b838', {'h': 0}),
             'tail': '#f0e8c0', 'tan': '#58a8e8', 'cloud': '#f0f8ff', 'eyes': '#3060d0'},
        ],
    },
}
