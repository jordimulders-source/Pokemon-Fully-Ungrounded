"""Kleurvarianten Gen 9 (Paldea, Kitakami, Blueberry). Formaat: zie recipes.py."""

ALBINO = {'l': 1.0}
DARK = {'l': 1.3}
GOLD = {'h': 0}

LINES = {
    'sprigatito': {
        # goochelkatten: vacht (licht), masker/cape (donkergroen), ogen/bloem (roze), bloemsteel en
        # capevoering (Meowscarada, felgroen)
        'species': {
            'sprigatito': {'fur': [5, 6, 7], 'mask': [3, 2, 1], 'eyes': [9, 10, 12, 11]},
            'floragato': {'fur': [5, 4, 7, 6], 'mask': [1, 2, 8], 'eyes': [10, 11, 12]},
            'meowscarada': {'mask': [1, 5, 3, 2], 'fur': [13, 10], 'eyes': [7, 8, 6], 'stem': [11, 9, 12]},
        },
        'variants': [
            {'naam': 'Japanse esdoorn (herfst: oranje vacht, rood masker)', 'fur': '#e8b070', 'mask': '#b03024',
             'eyes': '#f0d040', 'stem': '#6a3a20'},
            {'naam': 'Lavendelveld (lila met honinggele ogen)', 'fur': '#c8b4e0', 'mask': '#6a4a9a', 'eyes': '#f0c838',
             'stem': '#4a7a50'},
            {'naam': 'Hanami (sakura-roze, kersenhout)', 'fur': '#f8d0dc', 'mask': '#d86090', 'eyes': '#40a060',
             'stem': '#6a3a30'},
            {'naam': 'Monets waterlelies (blauwgroen, roze bloem)', 'fur': '#a8d0dc', 'mask': '#2c6a70', 'eyes': '#f080b0',
             'stem': '#e0d050'},
            {'naam': 'Le Chat Noir (zwarte goochelaarskat, bordeaux cape)', 'fur': ('#4a4a58', DARK),
             'mask': ('#7a2034', DARK), 'eyes': '#f0d040', 'stem': '#c02838'},
            {'naam': 'Klimt, De Kus (bladgoud met groen en rozen)', 'fur': ('#e8c858', GOLD), 'mask': '#1c5a44',
             'eyes': '#e03050', 'stem': '#c89828'},
        ],
    },
    'fuecoco': {
        # vuurkrokodillen (Skeledirge = Día de los Muertos): lijf (rood), kop/buik (crème),
        # vuur, rugstekels (geel), mond, klauwen; Skeledirge: schedel, vuurvogel, paarse ogen
        'species': {
            'fuecoco': {'body': [11, 8, 4], 'cream': [7, 9, 5], 'flame': [2, 1], 'spikes': [3, 13], 'mouth': [6],
                        'claws': [15, 10]},
            'crocalor': {'body': [9, 12, 11], 'cream': [4, 7, 6], 'flame': [3, 2, 1], 'spikes': [10],
                         'claws': [8, 13]},
            'skeledirge': {'body': [9, 11, 10], 'cream': [5, 3, 1], 'flame': [4, 6, 7, 2], 'eyes': [12],
                           'claws': [14, 13, 15]},
        },
        'variants': [
            {'naam': 'Gilamonster (zwart met oranje kralen)', 'body': ('#4a3c40', DARK), 'cream': '#f0a868',
             'flame': '#f07020', 'spikes': '#f07020', 'mouth': '#f0a868', 'claws': '#3a3034', 'eyes': '#f07020'},
            {'naam': 'Calavera de azúcar (roze suikerschedel, turkoois vuur)', 'body': '#e070a8', 'cream': '#f8f0e8',
             'flame': '#30c8c8', 'spikes': '#f0d040', 'mouth': '#30c8c8', 'claws': '#7a3a68', 'eyes': '#30c8c8'},
            {'naam': 'Kopervlam (groen vuur, mosgroen lijf)', 'body': '#3a7a48', 'cream': '#e8f0c8', 'flame': '#50e060',
             'spikes': '#c0e040', 'mouth': '#e08070', 'claws': '#2c3a30', 'eyes': '#c0e040'},
            {'naam': 'Albino krokodil (wit, rode ogen, roze vuur)', 'body': ('#e8dcd4', ALBINO), 'cream': '#f8f4f0',
             'flame': '#f080a0', 'spikes': '#f0b0b8', 'mouth': '#e04050', 'claws': '#a89890', 'eyes': '#e02838'},
            {'naam': 'Mariachi (zwart pak, zilveren knopen, rood vuur)', 'body': ('#34343e', DARK), 'cream': '#c8ccd8',
             'flame': '#e02828', 'spikes': '#d8dce8', 'mouth': '#e02828', 'claws': '#a0a4b0', 'eyes': '#f0d040'},
            {'naam': 'Quetzalcoatl (jade gevederde slang met goud)', 'body': '#1c8a70', 'cream': '#f0d878',
             'flame': '#40c0f0', 'spikes': ('#e0b030', GOLD), 'mouth': '#e04040', 'claws': ('#e0b030', GOLD),
             'eyes': '#e04040'},
        ],
    },
    'quaxly': {
        # dansende eenden: kuif/veren (blauw, ook Quaquavals waterdruppels), lijf (wit),
        # pak (Quaquaval, donkerblauw), kam (rood), snavel/poten
        'species': {
            'quaxly': {'hair': [2, 3, 1, 4, 9], 'body': [7, 5, 8, 10], 'beak': [12, 13, 11]},
            'quaxwell': {'hair': [4, 2, 1, 3, 5, 6], 'body': [11, 10, 8], 'beak': [9, 12, 13]},
            'quaquaval': {'hair': [2, 3, 1], 'suit': [8, 9, 7], 'body': [6, 5, 10], 'crest': [12, 11, 13],
                          'beak': [14, 15]},
        },
        'variants': [
            {'naam': 'Wilde eend (groene kop, bruin pak)', 'hair': '#2a8a50', 'body': '#d0c8b8', 'suit': '#6a5040',
             'crest': '#f0f0e8', 'beak': '#e8c030'},
            {'naam': 'Flamenco (rood met zwart pak)', 'hair': '#d02838', 'body': '#f8f0e8', 'suit': ('#34343c', DARK),
             'crest': '#f0d040', 'beak': '#f0d040'},
            {'naam': 'Mandarijneend (oranje, groenblauw pak, paarse kam)', 'hair': '#e88030', 'body': '#f0e8e0', 'suit': '#2c6a5a',
             'crest': '#7a4ab0', 'beak': '#e04030'},
            {'naam': 'Badeendje (geel met oranje snavel)', 'hair': '#f0d030', 'body': '#f8f0b8', 'suit': '#f0a020',
             'crest': '#f07020', 'beak': '#f07020'},
            {'naam': 'Zwanenmeer (zwarte zwaan, witte tutu)', 'hair': ('#3a3a46', DARK), 'body': '#c8c8d4',
             'suit': '#e8e8f0', 'crest': '#e02838', 'beak': '#e02838'},
            {'naam': 'Carnaval van Rio (paarse veren, goud, smaragd)', 'hair': '#8040c0', 'body': '#f8f0c8',
             'suit': ('#e0b030', GOLD), 'crest': '#20b060', 'beak': '#f0d040'},
        ],
    },
    'lechonk': {
        # varkens: lijf, snuit/hoeven/staart (roze), bruine wangen/slagtanden (Lechonk), ogen/goud
        'species': {
            'lechonk': {'body': [3, 4, 1], 'pink': [11, 10, 12], 'face': [7, 6, 5], 'gold': [9]},
            'oinkologne': {'body': [7, 4, 3, 5, 2, 1], 'pink': [10, 8, 6], 'gold': [9, 13], '_base': {'body': 7}},
            'oinkologne/f': {'body': [5, 7, 4, 3, 2, 1], 'pink': [11, 8, 6], 'gold': [9, 13]},
        },
        'variants': [
            {'naam': 'Mangalica (blond wolvarken)', 'body': '#d8c8a0', 'pink': '#e89898', 'face': '#a87850',
             'gold': '#6a4a30'},
            {'naam': 'Sneeuwbal (Animal Farm: wit varken, roze snuit)', 'body': ('#ecece6', ALBINO), 'pink': '#f090a8',
             'face': '#d8ccc0', 'gold': '#3a8ad0'},
            {'naam': 'Eau de Lavande (Oinkolognes eigen parfum)', 'body': '#a890c8', 'pink': '#f0d040', 'face': '#e8d8f8',
             'gold': '#f0d040'},
            {'naam': 'Tamworth (gemberrood landvarken)', 'body': '#c06830', 'pink': '#f0b090', 'face': '#f0c890',
             'gold': '#40a040'},
            {'naam': 'Delfts blauw spaarvarken (porselein)', 'body': '#a8c0e8', 'pink': '#24409a',
             'face': '#3050a8', 'gold': '#3050a8'},
            {'naam': 'Koning Midas (alles wat hij aanraakt wordt goud)', 'body': ('#d8a830', GOLD), 'pink': '#c03040',
             'face': '#f8e8a0', 'gold': '#c03040'},
        ],
    },
    'tarountula': {
        # spinnen: zijdebal (Tarountula), gezichtsplaat (Spidops), poten (geel/bruin), lijf/voeten (groen)
        'species': {
            'tarountula': {'silk': [2, 3, 1], 'legs': [7, 6, 5], 'body': [13, 12, 11]},
            'spidops': {'body': [4, 2, 1, 6], 'legs': [11, 8, 7, 12], 'silk': [14, 13]},
        },
        'variants': [
            {'naam': 'Gouden wielwebspin (gouden zijde)', 'silk': '#f0d070', 'body': '#5a4a30', 'legs': '#e0b828'},
            {'naam': 'Pauwspin (blauw en oranje balts)', 'silk': '#a8d4f0', 'body': '#2c60c0', 'legs': '#f08020'},
            {'naam': 'Krabspin op een roos (roze en wit)', 'silk': '#f8d8e8', 'body': '#e888b0', 'legs': '#f8f0f0'},
            {'naam': 'Spider-Man (rood en blauw, wit web)', 'silk': '#e8e8f0', 'body': '#d02828', 'legs': '#2048b0'},
            {'naam': 'Zwarte weduwe (rode zandloper)', 'silk': ('#4a4a54', DARK), 'body': ('#34343c', DARK),
             'legs': '#d02828'},
            {'naam': 'Groenblauwe vogelspin (cobalt poten, oranje achterlijf)', 'silk': '#f0a040', 'body': '#2a8aa0',
             'legs': '#2050c0'},
        ],
    },
    'nymble': {
        # sprinkhanen: lijf, lichte delen (Nymbles gezicht/poten, Lokix' blauwgrijze armen), ogen/accent (oranje)
        'species': {
            'nymble': {'body': [1, 2, 4, 3], 'face': [6, 7, 11], 'accent': [10, 8, 9]},
            'lokix': {'body': [8, 1, 9, 3, 4], 'face': [7, 6, 5], 'accent': [10, 11, 12]},
        },
        'variants': [
            {'naam': 'Woestijnsprinkhaan (zandkleur, oranje)', 'body': '#b09468', 'face': '#e8d8b0', 'accent': '#f06820'},
            {'naam': 'Kamen Rider Ichigo (groen, zilver, rode ogen)', 'body': '#2a7a48', 'face': '#c8ccd8',
             'accent': '#e02828'},
            {'naam': 'Regenbooggrashopper (rood, blauw en geel)', 'body': '#c82828', 'face': '#2858c0',
             'accent': '#f0d040'},
            {'naam': 'Roze sabelsprinkhaan (erytrisme)', 'body': '#e080a8', 'face': '#f8e0ec', 'accent': '#f8f0a0'},
            {'naam': 'De Joker (paars pak, groen haar)', 'body': '#6a3a9a', 'face': '#40b048', 'accent': '#f0d040'},
            {'naam': 'Jade gelukskrekel (Chinese krekelkooi, goud)', 'body': '#40a878', 'face': ('#d8b040', GOLD),
             'accent': '#e03040'},
        ],
    },
    'pawmi': {
        # elektrische hamsters: vacht (oranje), crème (snuit/buik/staart), kussentjes (geel), oren (teal)
        'species': {
            'pawmi': {'fur': [6, 7, 10, 4, 1], 'cream': [12, 13, 5, 9], 'pads': [8], 'ears': [3, 2]},
            'pawmo': {'fur': [5, 6, 9, 1], 'cream': [12, 10, 4], 'pads': [8, 7], 'ears': [3, 2]},
            'pawmot': {'fur': [2, 3, 1, 5], 'cream': [11, 12], 'pads': [10], 'ears': [6, 7]},
        },
        'variants': [
            {'naam': 'Russische dwerghamster (zilvergrijs, roze kussentjes)', 'fur': '#a8a8b4', 'cream': '#f4f4f4',
             'pads': '#f0a0b0', 'ears': '#5070c0'},
            {'naam': 'Chocoladehamster (cacao, paarse kussentjes)', 'fur': '#6a4030', 'cream': '#f0d8b0',
             'pads': '#b050c0', 'ears': '#f0d040'},
            {'naam': 'Pikachu-cosplay (geel, rode wangen)', 'fur': '#f0cc30', 'cream': '#f8f0c8', 'pads': '#e03030',
             'ears': ('#3a3a40', DARK)},
            {'naam': 'Sonic (blauw met crème buik)', 'fur': '#3068d0', 'cream': '#f0d8b0', 'pads': '#f0d040',
             'ears': '#e03030'},
            {'naam': 'Stroomstoring (zwart met cyaan bliksem)', 'fur': ('#3a3a44', DARK), 'cream': '#a8a8b8',
             'pads': '#40e0f0', 'ears': '#40e0f0'},
            {'naam': 'Hulk (groen met paarse broek)', 'fur': '#50a040', 'cream': '#e0f0c0', 'pads': '#8040b0',
             'ears': '#8040b0'},
        ],
    },
    'tandemaus': {
        # muizen: vacht (wit, basis = wit), pootjes/oren (blauw). Maushold-vier deelt het palet van Maushold.
        'species': {
            'tandemaus': {'body': [2, 5, 6, 7, 1, 3], 'paws': [9, 10, 8], '_base': {'body': 2}},
            'maushold': {'body': [2, 4, 6, 1], 'paws': [8, 9], '_base': {'body': 2}},
        },
        'variants': [
            {'naam': 'Huismuis (grijs, roze pootjes)', 'body': '#b4b4c0', 'paws': '#f0a0b0'},
            {'naam': 'Jerry (oker, crème pootjes)', 'body': '#d8a868', 'paws': '#f8e0c0'},
            {'naam': 'Goudse kaas (geel, oranje korst)', 'body': '#f0d468', 'paws': '#f07020'},
            {'naam': 'Mickey Mouse (zwart, rode broek)', 'body': ('#50505c', DARK), 'paws': '#e02828'},
            {'naam': 'Suikermuis (roze fondant)', 'body': '#f0b0c8', 'paws': '#f8f4f4'},
            {'naam': 'De Rat van de Chinese dierenriem (goud met rood)', 'body': ('#e0b840', GOLD), 'paws': '#d02828'},
        ],
    },
    'fidough': {
        # broodhonden: korst, deeg (licht)
        'species': {
            'fidough': {'crust': [4, 5, 2, 6], 'dough': [8, 3, 7, 1]},
            'dachsbun': {'crust': [8, 7, 3, 1, 6], 'dough': [9, 10, 2, 4], '_base': {'crust': 8}},
        },
        'variants': [
            {'naam': 'Pumpernickel (donker roggebrood)', 'crust': '#5a3a28', 'dough': '#a87858'},
            {'naam': 'Meloenpan met matcha (groen)', 'crust': '#7aa848', 'dough': '#f0f0c8'},
            {'naam': 'Ube-broodje (Filipijns paars)', 'crust': '#7a4aa0', 'dough': '#dcc4f0'},
            {'naam': 'Houtskoolbrood (zwarte bamboe)', 'crust': ('#3c3c44', DARK), 'dough': '#a8a8b0'},
            {'naam': 'Aardbeien-melkbrood (roze)', 'crust': '#e080a0', 'dough': '#f8e8f0'},
            {'naam': 'Red velvet (rood met roomkaas)', 'crust': '#a82034', 'dough': '#f8f4f0'},
        ],
    },
    'smoliv': {
        # olijfbomen: blad, olijven (Smolivs kopje), lijf/gezicht, stam (Arboliva)
        'species': {
            'smoliv': {'body': [10, 11, 9, 12], 'leaves': [8, 7, 6], 'olive': [2, 3, 1, 4]},
            'dolliv': {'leaves': [7, 9, 2, 1, 3], 'olive': [6, 5, 4], 'body': [10, 11, 12, 14]},
            'arboliva': {'leaves': [1, 6, 3, 4, 2], 'olive': [9, 7, 8], 'body': [12, 10, 11], 'trunk': [14, 13, 15]},
        },
        'variants': [
            {'naam': 'Tapenade (zwarte olijven, donker blad)', 'leaves': '#2c5a38', 'olive': ('#3a3440', DARK),
             'body': '#b8b890', 'trunk': '#4a3a30'},
            {'naam': 'Kalamata (aubergine-paarse olijven)', 'leaves': '#4a7a38', 'olive': '#4a2040', 'body': '#6a3058',
             'trunk': '#6a5038'},
            {'naam': 'Kersenboom in bloei (roze blad, kersen)', 'leaves': '#f0a0c0', 'olive': '#c02040', 'body': '#f8e8f0',
             'trunk': '#5a3030'},
            {'naam': 'Herfstgaard (oranje blad, roodbruine vruchten)', 'leaves': '#e08830', 'olive': '#7a2a20',
             'body': '#f0d8a0', 'trunk': '#5a3a28'},
            {'naam': 'Sinaasappelboom van Valencia', 'leaves': '#1e5a2c', 'olive': '#f08a20', 'body': '#f8f0c0',
             'trunk': '#7a5a3a'},
            {'naam': "Athena's olijfboom (zilver blad, gouden olijven, marmer)", 'leaves': '#c0c8c8',
             'olive': ('#e0b030', GOLD), 'body': '#f8f8f0', 'trunk': '#9a9aa4'},
        ],
    },
    'squawkabilly': {
        # papegaaien (besluit Jordi): de vier verenkleden zijn vormen en krijgen dezelfde zes skins.
        # De vormen hebben geen eigen sprite (telling 0): de eerste index van een groep is de basis.
        'species': {
            'squawkabilly': {'body': [7, 4, 5], 'belly': [12, 6], 'crest': [2, 1], 'beak': [10, 8, 13, 9, 14]},
            'squawkabilly/blue': {'body': [7, 4, 5], 'belly': [12, 6], 'crest': [2, 1], 'beak': [10, 8, 13, 9, 14]},
            'squawkabilly/yellow': {'body': [7, 4, 5], 'belly': [12, 6], 'crest': [2, 1], 'beak': [10, 8, 13, 9, 14]},
            'squawkabilly/white': {'body': [7, 4, 5], 'belly': [12, 6], 'crest': [2, 1], 'beak': [10, 8, 13, 9, 14]},
        },
        'variants': [
            {'naam': 'Kea (bronsgroen met oranje oksels)', 'body': '#7a7a3a', 'belly': '#e86020', 'crest': '#3a4a28',
             'beak': '#5a5a60'},
            {'naam': 'Galah (roze kaketoe, grijze vleugels)', 'body': '#a8a8b4', 'belly': '#f088a8', 'crest': '#f8c8d8',
             'beak': '#f0e8e0'},
            {'naam': 'Oostelijke rosella (rode kop, geel, witte wangen)', 'body': '#e8c030', 'belly': '#f8f8f0',
             'crest': '#d02828', 'beak': '#e8e0c8'},
            {'naam': 'Geelvleugelara (rood, goud en blauw)', 'body': '#d02028', 'belly': '#f0c020', 'crest': '#2050c0',
             'beak': '#e8e0d0'},
            {'naam': 'Regenbooglori (oranje borst, blauwe kop)', 'body': '#f07020', 'belly': '#f0d840', 'crest': '#3048c0',
             'beak': '#e02828'},
            {'naam': "Banks' zwarte kaketoe (zwart met rode staartband)", 'body': ('#3a3a44', DARK), 'belly': '#d83028',
             'crest': ('#2a2a32', DARK), 'beak': '#a8a8b0'},
        ],
    },
    'nacli': {
        # zoutrotsen: zout (wit), gesteente (bruin), ogen (oranje)
        'species': {
            'nacli': {'salt': [2, 8, 4, 1], 'rock': [6, 3, 5, 9], 'eyes': [11, 10]},
            'naclstack': {'salt': [7, 6, 3, 8], 'rock': [4, 1, 2, 9, 5], 'eyes': [12, 13]},
            'garganacl': {'salt': [3, 2, 1, 4, 15], 'rock': [7, 10, 9, 6, 13, 5, 14], 'eyes': [11, 12],
                          '_base': {'rock': 7}},
        },
        'variants': [
            {'naam': 'Zwart lavazout van Hawaï', 'salt': ('#50505a', DARK), 'rock': '#a07050', 'eyes': '#f04020'},
            {'naam': 'Roze Himalayazout', 'salt': '#f0b8c4', 'rock': '#7a4a40', 'eyes': '#f0d040'},
            {'naam': 'Blauw Perzisch zout (sylviet)', 'salt': '#a8c8f0', 'rock': '#5a6070', 'eyes': '#f0d040'},
            {'naam': 'Gerookt zout (hickory)', 'salt': '#c8a070', 'rock': '#4a3020', 'eyes': '#f08020'},
            {'naam': 'Amethistgeode', 'salt': '#b080e0', 'rock': '#4a4048', 'eyes': '#f0f0f0'},
            {'naam': 'Pyriet (kattengoud)', 'salt': ('#e0c040', GOLD), 'rock': '#5a5a64', 'eyes': '#e03030'},
        ],
    },
    'charcadet': {
        # vuurridders: rood (Charcadet/Armarouge), goud harnas (Armarouge), kling (Ceruledge), pantser
        # (Ceruledge), vuur, vlampunt, houtskoollijf
        'species': {
            'charcadet': {'red': [5, 4, 6], 'coal': [9, 8, 11], 'fire': [10, 12], 'tip': [2, 1, 3]},
            'armarouge': {'gold': [5, 4, 15, 12, 13], 'red': [2, 1, 6], 'tip': [3], 'coal': [9, 8]},
            'ceruledge': {'blade': [5, 3, 4], 'armor': [7, 6, 8, 13], 'tip': [1, 2, 14], 'coal': [9, 11]},
        },
        'variants': [
            {'naam': 'Green Lantern (smaragd vuur)', 'red': '#2a8a50', 'gold': '#b8e040', 'blade': '#50e080',
             'armor': '#1c5a3a', 'fire': '#60f080', 'tip': '#f0f0a0', 'coal': '#2c3a30'},
            {'naam': 'IJsvuur (Frozen: wit en cyaan)', 'red': '#5aa0d8', 'gold': '#d8ecf8', 'blade': '#e0f4ff',
             'armor': '#3a70b0', 'fire': '#80e0f0', 'tip': '#ffffff', 'coal': '#3a4458'},
            {'naam': 'Doctor Strange (blauw tuniek, rode mantel)', 'red': '#c02028', 'gold': '#3050b0',
             'blade': '#d02838', 'armor': '#2a3a80', 'fire': '#f0d040', 'tip': '#40e0a0', 'coal': '#2c2c3a',
             'charcadet:red': '#3050b0'},
            {'naam': 'Obsidiaan en lava', 'red': ('#3a3440', DARK), 'gold': '#f06020', 'blade': '#f08020',
             'armor': ('#2c2830', DARK), 'fire': '#f04010', 'tip': '#f0d040', 'coal': '#1c1c20',
             'armarouge:gold': ('#4a4450', DARK), 'armarouge:red': '#f04010'},
            {'naam': 'Sakura-ronin (roze en wit)', 'red': '#e070a0', 'gold': '#f8e0e8', 'blade': '#f8c0d8',
             'armor': '#7a2a50', 'fire': '#f0a0c0', 'tip': '#ffffff', 'coal': '#4a3040'},
            {'naam': "Jeanne d'Arc (zilver harnas, Franse lelie)", 'red': '#2848a8', 'gold': '#d8dce8',
             'blade': '#e8ecf4', 'armor': '#2848a8', 'fire': ('#f0c830', GOLD), 'tip': ('#f0c830', GOLD),
             'coal': '#4a4a58'},
        ],
    },
    'tadbulb': {
        # elektrische kikkers: lijf (Bellibolt, teal), licht (Tadbulbs lamp, Bellibolts gele navels),
        # grijs (Tadbulbs kop/staart, Bellibolts buik), oranje (staartpunt, mond, poten)
        'species': {
            'tadbulb': {'light': [3, 2, 6, 4, 1, 8], 'grey': [13, 9, 11, 10], 'orange': [12, 14, 15]},
            'bellibolt': {'body': [9, 8, 13, 10], 'grey': [4, 14, 7], 'light': [11, 15], 'orange': [1, 3, 2, 5]},
        },
        'variants': [
            {'naam': 'Neonreclame (roze lijf, cyaan licht)', 'body': '#d84090', 'light': '#40e8f0', 'grey': '#4a4058',
             'orange': '#f0f040'},
            {'naam': 'Blauwe pijlgifkikker (Dendrobates azureus)', 'body': '#2858c8', 'light': '#90e8f8',
             'grey': '#2c3a60', 'orange': '#f8f8f8'},
            {'naam': 'Aardbeikikker (rood, blauwe poten)', 'body': '#d02828', 'light': '#f0d040', 'grey': '#4a3a40',
             'orange': '#2858c0'},
            {'naam': 'Gouden pad van Monteverde (oranje)', 'body': '#f08020', 'light': '#f8e060', 'tadbulb:light': '#f07818', 'grey': '#6a4a30',
             'orange': '#e04030'},
            {'naam': 'Vuurvliegje (zwart lijf, lime licht)', 'body': ('#3a3a44', DARK), 'light': '#c0f040',
             'grey': '#5a5a40', 'orange': '#f08020'},
            {'naam': 'Teslaspoel (paars plasma, koper)', 'body': '#6a3ab0', 'light': '#e0b0ff', 'grey': '#b07040',
             'orange': '#d0a040'},
        ],
    },
    'wattrel': {
        # stormvogels: lijf (zwart), geel, buik (blauwgrijs), snavel/poten
        'species': {
            'wattrel': {'body': [3, 2], 'yellow': [9, 7, 12], 'belly': [14, 13, 15], 'beak': [11, 8, 10]},
            'kilowattrel': {'body': [3, 2], 'yellow': [5, 4, 13], 'belly': [15, 14], 'beak': [12, 11, 7]},
        },
        'variants': [
            {'naam': 'Jan-van-gent (wit, gele kop)', 'body': ('#e8e8ec', ALBINO), 'yellow': '#f0d878', 'belly': '#c8d0e0',
             'beak': '#7090b0'},
            {'naam': 'Blauwvoetgent (bruin, blauwe poten)', 'body': '#7a5a40', 'yellow': '#f0f0e8', 'belly': '#d8c8b0',
             'beak': '#40a0e0'},
            {'naam': 'Paarse bliksem (cyaan strepen)', 'body': '#4a2a80', 'yellow': '#40e0f0', 'belly': '#a080e0',
             'beak': '#f040a0'},
            {'naam': 'Kardinaal (rood met oranje snavel)', 'body': '#c02028', 'yellow': '#f0c030', 'belly': '#e87070',
             'beak': '#f08020'},
            {'naam': 'Onweerswolk (leigrijs, wit licht)', 'body': '#6a7480', 'yellow': '#f0f8ff', 'belly': '#b0b8c8',
             'beak': '#f0d040'},
            {'naam': 'Thunderbird (turkoois, rood en goud)', 'body': '#209090', 'yellow': '#e03030', 'belly': '#f0f0e0',
             'beak': ('#f0c030', GOLD)},
        ],
    },
    'maschiff': {
        # maffiahonden: lijf, manen (Maschiffs gele kraag, Mabosstiffs grijze kuif), donker masker/vacht, ogen
        'species': {
            'maschiff': {'body': [9, 10, 3], 'mane': [11, 7, 6], 'mask': [4, 2, 1], 'eyes': [8, 13, 5]},
            'mabosstiff': {'body': [9, 10, 12], 'mane': [2, 3, 4], 'mask': [1, 8], 'eyes': [11, 13]},
        },
        'variants': [
            {'naam': 'Rottweiler (zwart met tan)', 'body': ('#3e383c', DARK), 'mane': '#c07838', 'mask': '#a86a30',
             'eyes': '#f0d040'},
            {'naam': 'Blauwe dobermann (blauwgrijs met roest)', 'body': '#5a6478', 'mane': '#c06830', 'mask': '#3a4050',
             'eyes': '#f0d040'},
            {'naam': 'Shiba inu (vos-rood met crème)', 'body': '#d08040', 'mane': '#f8f0e0', 'mask': '#f0e0c8',
             'eyes': '#3a2a20'},
            {'naam': 'Weimaraner (zilvergrijs, amberogen)', 'body': '#a8a8b0', 'mane': '#dcdce4', 'mask': '#6a6a78',
             'eyes': '#f0a030'},
            {'naam': 'Peaky Blinders (grijsgroen tweed, petten)', 'body': '#5a6450', 'mane': '#c8b890', 'mask': '#2c3028',
             'eyes': '#40a0e0'},
            {'naam': 'De Peetvader (gouden ketting, zwart)', 'body': ('#d8b040', GOLD), 'mane': '#f8f0d0',
             'mask': '#3a3030', 'eyes': '#e02828'},
        ],
    },
    'shroodle': {
        # graffitimaki's: lijf (donker), arm/kop (blauwgrijs), crème (kuif/staart), gezicht (mint), verf
        'species': {
            'shroodle': {'body': [6, 7, 1], 'blue': [10, 8, 5], 'cream': [2, 4], 'face': [9, 12], 'paint': [14]},
            'grafaiai': {'body': [5, 6], 'blue': [10, 11], 'cream': [4, 3, 1], 'face': [8, 9, 7], 'paint': [13, 12],
                         'paint2': [14, 15], '_base': {'body': 6, 'face': 9}},
        },
        'variants': [
            {'naam': 'Ringstaartmaki (grijs, oranje ogen)', 'body': '#7a7a80', 'blue': '#3a3a40', 'cream': '#f0f0e8',
             'face': '#f0a030', 'paint': '#e02828', 'paint2': '#f0d040'},
            {'naam': 'Banksy (zwart-wit stencil met rood)', 'body': ('#e4e4e4', ALBINO), 'blue': '#34343c',
             'cream': '#d02828', 'face': '#d02828', 'paint': '#d02828', 'paint2': '#34343c'},
            {'naam': 'Neongraffiti (lime en magenta)', 'body': '#3a8a30', 'blue': '#2a4a20', 'cream': '#e040c0',
             'face': '#f0f040', 'paint': '#40e0f0', 'paint2': '#f040a0'},
            {'naam': 'Vingerdier (aye-aye: bruin, oranje ogen)', 'body': '#5a4a3a', 'blue': '#8a7a6a', 'cream': '#c8b8a0',
             'face': '#f0b030', 'paint': '#40c040', 'paint2': '#e06020'},
            {'naam': 'Keith Haring (rood, geel en blauw)', 'body': '#d82828', 'blue': '#2850c0', 'cream': '#f0d040',
             'face': '#f0f0f0', 'paint': '#f0d040', 'paint2': '#2850c0'},
            {'naam': 'Dalí (bordeaux met goud, surrealistisch blauw)', 'body': '#7a1830', 'blue': ('#d8b040', GOLD),
             'cream': '#f8f0d8', 'face': '#40b0e0', 'paint': '#f0d040', 'paint2': '#40b0e0'},
        ],
    },
    'bramblin': {
        # tuimelkruid: takken, binnenkant (rood), punten (Brambleghast), ogen
        'species': {
            'bramblin': {'twig': [3, 4, 1, 2], 'inner': [8, 7, 5, 12], 'eyes': [9, 10, 11]},
            'brambleghast': {'twig': [8, 7, 3, 4], 'inner': [11, 10, 9], 'tips': [2, 6, 1], 'eyes': [13]},
        },
        'variants': [
            {'naam': 'Zilverdistel', 'twig': '#a8a8a8', 'inner': '#6a6a78', 'tips': '#d0d0e0', 'eyes': '#40c0f0'},
            {'naam': 'Woestijnzonsondergang (oranje en roze)', 'twig': '#e09040', 'inner': '#e05070', 'tips': '#f0d040',
             'eyes': '#f0f040'},
            {'naam': 'Doornenhaag met rozen (Doornroosje)', 'twig': '#4a7a30', 'inner': '#d02848', 'tips': '#f0a0c0',
             'eyes': '#f0d040'},
            {'naam': 'Berijpte wilgentenen', 'twig': ('#e0e4ec', ALBINO), 'inner': '#90a0c0', 'tips': '#c0d8f0',
             'eyes': '#3070e0'},
            {'naam': 'Dwaallicht (zwarte takken, groen spookvuur)', 'twig': ('#3a3a40', DARK), 'inner': '#40d060',
             'tips': '#a0f080', 'eyes': '#c0f040'},
            {'naam': 'Gouden tuimelkruid (Western)', 'twig': ('#e0b030', GOLD), 'inner': '#8a3020', 'tips': '#f8f0c0',
             'eyes': '#e02828'},
        ],
    },
    'toedscool': {
        # paddenstoelkwallen: hoed, stippen/rand (geel), poten/tentakels, vlekken (Toedscruel)
        'species': {
            'toedscool': {'cap': [4, 3, 1, 2], 'spots': [6, 7, 5], 'legs': [11, 9, 12]},
            'toedscruel': {'cap': [7, 4, 1, 2], 'patch': [3, 5], 'spots': [6, 15, 14], 'legs': [12, 10, 11]},
        },
        'variants': [
            {'naam': 'Vliegenzwam (rood, witte stippen)', 'cap': '#d02828', 'spots': '#f8f8f0', 'legs': ('#e4e0d8', {'l': 1.6}),
             'patch': ('#ece8e0', {'l': 1.5})},
            {'naam': 'Toadsworth (witte hoed met bruine stippen, paars vest)', 'cap': ('#e4dccc', {'l': 1.5}), 'spots': '#8a5a30',
             'legs': '#7a4aa0', 'patch': '#8a5a30'},
            {'naam': 'Blauwe parasolzwam (Entoloma hochstetteri)', 'cap': '#3060c8', 'spots': '#a0d0f0',
             'legs': '#c8d8f0', 'patch': '#80b0f0'},
            {'naam': 'Amethistzwam (paars)', 'cap': '#8050b0', 'spots': '#e0c8f0', 'legs': '#c8b8d8', 'patch': '#c090e0'},
            {'naam': 'Inktzwam (zwart druipend)', 'cap': ('#3a3a44', DARK), 'spots': '#a0a0b0', 'legs': '#e8e8e8',
             'patch': '#5a5a68'},
            {'naam': 'Spookzwam (groen bioluminescent)', 'cap': '#204838', 'spots': '#80ff80', 'legs': '#c0f0c0',
             'patch': '#60e080'},
        ],
    },
    'klawf': {
        # klifkrab: schild (rood), rug (crème), ogen, poten/scharen (donker), blos
        'species': {
            'klawf': {'red': [9, 2, 7], 'cream': [12, 11, 10], 'eyes': [5, 4], 'dark': [6, 3, 1, 15], 'blush': [13, 14]},
        },
        'variants': [
            {'naam': 'Blauwe zwemkrab (Callinectes)', 'red': '#3060b0', 'cream': '#d8e0f0', 'eyes': '#f0d040',
             'dark': '#2a3a50', 'blush': '#f08020'},
            {'naam': 'Kokoskrab (paarsblauw)', 'red': '#6a4aa8', 'cream': '#d0b8e0', 'eyes': '#f8f8f8', 'dark': '#3a2a50',
             'blush': '#f0a0c0'},
            {'naam': 'Halloweenkrab (zwart, oranje, paars)', 'red': ('#3a3440', DARK), 'cream': '#f08020',
             'eyes': '#f0d040', 'dark': '#6a3a90', 'blush': '#f08020'},
            {'naam': 'Spookkrab (zandwit)', 'red': '#e0d4c0', 'cream': '#f8f0e0', 'eyes': '#3a3a40', 'dark': '#a89880',
             'blush': '#f0b0a0'},
            {'naam': 'Kingler (paletwissel: oranjerood met beige scharen)', 'red': '#e05828', 'cream': '#f0d8a8',
             'eyes': '#202020', 'dark': ('#d8b890', {'l': 1.3}), 'blush': '#f0a080'},
            {'naam': 'Sterrenbeeld Kreeft (nachtblauw met goud)', 'red': '#283068', 'cream': ('#e0c050', GOLD),
             'eyes': '#f0f0ff', 'dark': '#14183a', 'blush': '#f0f0ff'},
        ],
    },
    'capsakid': {
        # pepers: lijf, blad/steel, peper (Scovillains rode kop, Capsakids oranje), zaadjes/crème
        'species': {
            'capsakid': {'body': [7, 9, 8, 10], 'leaf': [13, 4, 1], 'seed': [3, 5, 2], 'pepper': [12]},
            'scovillain': {'body': [8, 6, 14, 13, 12, 15], 'leaf': [3, 4, 1], 'pepper': [7, 5, 9, 11], '_base': {'pepper': 7, 'leaf': 3}},
        },
        'variants': [
            {'naam': 'Habanero (oranje en geel)', 'body': '#e87818', 'leaf': '#3a8a30', 'pepper': '#f0c020', 'seed': '#f8e8c0',
             'scovillain:pepper': '#e87818', 'scovillain:leaf': '#f0c828', 'scovillain:body': '#3a8a30'},
            {'naam': 'Carolina Reaper (dieprood, gele angel)', 'body': '#a01818', 'leaf': '#2a6a28', 'pepper': '#f0d040',
             'seed': '#f0d8b0', 'scovillain:pepper': '#b01818', 'scovillain:leaf': '#b01818', 'scovillain:body': '#2a7a28'},
            {'naam': 'Banaanpeper (geel)', 'body': '#f0d040', 'leaf': '#4a8a30', 'pepper': '#f08020', 'seed': '#f8f8d0',
             'scovillain:pepper': '#f0e070', 'scovillain:leaf': '#d8e060', 'scovillain:body': '#7aa030'},
            {'naam': 'Gedroogde Mexicaanse chilis (ancho en guajillo)', 'body': '#6a2418', 'leaf': '#4a5a28',
             'pepper': '#8a2a18', 'seed': '#d8b890', 'scovillain:pepper': '#6a1c14', 'scovillain:leaf': '#8a3418',
             'scovillain:body': '#5a3a24'},
            {'naam': 'Black Pearl (zwarte sierpeper, rood)', 'body': ('#3a3440', DARK), 'leaf': '#5a4a60',
             'pepper': '#d02828', 'seed': '#f0d0d0'},
            {'naam': 'Ghost pepper (spookwit met paars vuur)', 'body': ('#d4ccdc', {'l': 1.6}), 'leaf': '#8050b0',
             'pepper': '#a040e0', 'seed': '#c0a0e0'},
        ],
    },
    'rellor': {
        # scarabeeën: bal (mest/psychische bol), patroon (oranje/rood), lijf
        'species': {
            'rellor': {'ball': [2, 4, 1, 3, 13], 'pattern': [6, 12], 'body': [7, 9, 5, 10, 11, 14, 15]},
            'rabsca': {'ball': [1, 2, 3], 'pattern': [4, 6, 7, 8, 14, 15], 'body': [11, 10, 12, 13]},
        },
        'variants': [
            {'naam': 'Groene juweelkever (Chrysina)', 'ball': '#3aa060', 'pattern': '#e0d050', 'body': '#206040'},
            {'naam': 'Lieveheersbeestje', 'ball': '#d02828', 'pattern': ('#2c2c34', DARK), 'body': ('#3a3a44', DARK)},
            {'naam': 'Toetanchamons scarabee (lapis, goud, carneool)', 'ball': '#2848a0', 'pattern': ('#e0b030', GOLD),
             'body': '#8a3a20'},
            {'naam': 'Zonnegod Ra (oranje zonneschijf)', 'ball': '#f08020', 'pattern': '#f0e060', 'body': '#c03020'},
            {'naam': 'Nevel (zwart met cyaan, roze poten)', 'ball': ('#2a2040', DARK), 'pattern': '#40e0f0', 'body': '#f060c0'},
            {'naam': 'Zilveren scarabee (Chrysina limbata, chroom)', 'ball': ('#d0d4e0', {'l': 1.2}), 'pattern': '#40c0f0',
             'body': '#5a5a68'},
        ],
    },
    'flittle': {
        # psychische loopvogels: lijf (geel/oranje), wit (veren, kop), accent (Flittles roze ring,
        # Espathras paarse veren), poten, ogen
        'species': {
            'flittle': {'body': [7, 5, 4], 'white': [2, 3, 1], 'accent': [12, 11, 13], 'feet': [15, 14], 'eyes': [8, 10]},
            'espathra': {'body': [9, 10, 8, 11, 12], 'white': [3, 2, 1], 'accent': [6, 7], 'feet': [14, 13, 15],
                         'eyes': [5]},
        },
        'variants': [
            {'naam': 'Emoe (grijsbruin, blauwe nek)', 'body': '#8a7a68', 'white': '#c8c0b0', 'accent': '#3a6ac0',
             'feet': '#5a5048', 'eyes': '#f08020'},
            {'naam': 'Pauw (blauw, groen en goud)', 'body': '#2060a0', 'white': '#40b080', 'accent': '#f0c030',
             'feet': '#a0a0a8', 'eyes': '#40e0a0'},
            {'naam': 'Kasuaris (zwartblauw, rode lel)', 'body': '#30304a', 'white': '#40a0e0', 'accent': '#e02828',
             'feet': '#7a7a80', 'eyes': '#f08020'},
            {'naam': 'Lavalamp (paars met roze en mint)', 'body': '#9040c0', 'white': '#f0c0e0', 'accent': '#40e0c0',
             'feet': '#f0d040', 'eyes': '#f040a0'},
            {'naam': 'Albino struisvogel (wit, roze huid)', 'body': ('#ecebe6', ALBINO), 'white': '#d8d4e0',
             'accent': '#f0a0b0', 'feet': '#f0b0b0', 'eyes': '#e03030'},
            {'naam': 'Horus (lapis en goud)', 'body': '#2848a0', 'white': ('#e0b030', GOLD), 'accent': '#30a0a0',
             'feet': ('#e0b030', GOLD), 'eyes': '#40e0f0'},
        ],
    },
    'tinkatink': {
        # smidsfeeën: huid (roze), haar/crème, hamer (metaal), ogen
        'species': {
            'tinkatink': {'pink': [7, 5, 11, 12], 'cream': [3, 2, 1], 'hammer': [6, 8, 9, 10, 13], 'eyes': [15]},
            'tinkatuff': {'pink': [15, 11, 10, 9], 'cream': [3, 2, 1], 'hammer': [8, 6, 7, 5, 12], 'eyes': [14]},
            'tinkaton': {'pink': [14, 11, 13, 12], 'cream': [3, 2, 1], 'hammer': [10, 8, 6, 7, 9], 'eyes': [15]},
        },
        'variants': [
            {'naam': 'Smidsvuur (oranje gloed, houtskoolhamer)', 'pink': '#e86030', 'cream': '#f8e0c8',
             'hammer': '#5a5a64', 'eyes': '#f0d040'},
            {'naam': 'Mjölnir (Thor: blauw, zilveren hamer)', 'pink': '#5080d0', 'cream': '#f0e8d8', 'hammer': '#a8acb8',
             'eyes': '#f0d040'},
            {'naam': 'Harley Quinn (rood en zwart, mallet)', 'pink': '#d02838', 'cream': '#f8f0f0',
             'hammer': ('#3a3a44', DARK), 'eyes': '#3070e0'},
            {'naam': 'Munt en roségoud', 'pink': '#60c0a0', 'cream': '#f0f8f0', 'hammer': '#e0a090', 'eyes': '#8040a0'},
            {'naam': 'Gothic (zwart, wit en bloedrode hamer)', 'pink': ('#4a3a50', DARK), 'cream': '#e8e0f0',
             'hammer': '#a01830', 'eyes': '#e02838'},
            {'naam': 'Hephaistos (bronzen huid, gouden hamer)', 'pink': '#b06a40', 'cream': '#f0d8b0',
             'hammer': ('#e0b030', GOLD), 'eyes': '#40c0f0'},
        ],
    },
    'wiglett': {
        # lintalen: lijf (Wiglett wit, Wugtrio rood), mond/ogen, zand/rots
        'species': {
            'wiglett': {'body': [3, 2, 1], 'mouth': [9, 6, 7, 8], 'rock': [12, 13, 11, 10]},
            'wugtrio': {'body': [1, 5, 3, 2], 'rock': [11, 13, 10, 12], 'mouth': [7, 8, 9]},
        },
        'variants': [
            {'naam': "Oranje lintaal (Taylor's garden eel)", 'body': '#f08030', 'mouth': '#f8f0e0', 'rock': '#c8b890'},
            {'naam': 'Groene murene (Gymnothorax funebris)', 'body': '#2a7a48', 'mouth': '#f0e060', 'rock': '#c8c0a0'},
            {'naam': 'Zebramurene (chocoladebruin, crème)', 'body': '#7a4a30', 'mouth': '#f0e0c0', 'rock': '#506040'},
            {'naam': 'Koraaltuin (roze aal, paars koraal)', 'body': '#f090c0', 'mouth': '#e04080', 'rock': '#8050b0'},
            {'naam': 'Zwartwitte zeeslang', 'body': ('#3a3a44', DARK), 'mouth': '#f0f0f0', 'rock': '#d0d4dc'},
            {'naam': 'Hydrothermale bron (goud op basalt)', 'body': ('#e0b030', GOLD), 'mouth': '#e03020',
             'rock': ('#34343c', DARK)},
        ],
    },
    'bombirdier': {
        # ooievaar: veren (wit), donkere vleugels, rood (snavel, keelzak, poten)
        'species': {
            'bombirdier': {'body': [9, 11, 12, 8, 4, 5], 'dark': [1, 3], 'red': [6, 7, 2]},
        },
        'variants': [
            {'naam': 'Maraboe (leigrijs, roze keelzak)', 'body': '#6a6a78', 'dark': '#3a3a40', 'red': '#f0a0b0'},
            {'naam': 'Schoenbekooievaar (blauwgrijs)', 'body': '#7a8aa0', 'dark': '#3a4458', 'red': '#d0c070'},
            {'naam': 'Rode ibis (zwarte vleugelpunten)', 'body': '#e04830', 'dark': ('#2c2c34', DARK), 'red': '#3a3434'},
            {'naam': 'Kraamooievaar (babyblauw en roze)', 'body': '#a8c8f0', 'dark': '#f0a0c0', 'red': '#f8f0f0'},
            {'naam': 'Gier (zwart, kale rode kop)', 'body': ('#3a3a40', DARK), 'dark': '#f0e8d8', 'red': '#d03028'},
            {'naam': 'Gouden ooievaar (robijnen snavel)', 'body': ('#e0b840', GOLD), 'dark': '#6a4a20', 'red': '#c02040'},
        ],
    },
    'finizen': {
        # dolfijnhelden: lijf, buik, wangen, ogen; Palafin-held: pak (donkerblauw)
        'species': {
            'finizen': {'body': [4, 2, 1, 3, 13, 15, 14], 'belly': [5, 6], 'cheek': [10, 12, 11], 'eyes': [7]},
            'palafin': {'body': [4, 2, 1, 3, 13, 15, 14], 'belly': [5, 6], 'cheek': [10, 12, 11], 'eyes': [7]},
            'palafin/hero': {'body': [3, 2, 1, 10], 'suit': [5, 8, 6, 7], 'belly': [11, 12], 'cheek': [13, 14]},
        },
        'variants': [
            {'naam': 'Roze Amazonedolfijn (boto)', 'body': '#e8a0b0', 'belly': '#f8e8ec', 'suit': '#c05078',
             'cheek': '#e04060', 'eyes': '#3a3a40'},
            {'naam': 'Orka (zwart en wit)', 'body': ('#3a3a44', DARK), 'belly': '#f4f4f4', 'suit': ('#2a2a30', DARK),
             'cheek': '#e03040', 'eyes': '#f0f0f0'},
            {'naam': 'The Flash (rood en geel)', 'body': '#d02828', 'belly': '#f0d040', 'suit': '#a01818',
             'cheek': '#f0d040', 'eyes': '#f0d040'},
            {'naam': 'Vaporwave-dolfijn (mint en paars)', 'body': '#60e0c0', 'belly': '#f0f0ff', 'suit': '#8040c0',
             'cheek': '#f060c0', 'eyes': '#8040c0'},
            {'naam': 'Ultraman (zilver en rood, gouden ogen)', 'body': '#c8ccd8', 'belly': '#f8f8f8', 'suit': '#c02028',
             'cheek': '#f0d040', 'eyes': '#f0d040'},
            {'naam': 'Wonder Woman (goud met rood en blauw)', 'body': ('#e0b030', GOLD), 'belly': '#f8f0d0',
             'suit': '#c02028', 'cheek': '#c02028', 'eyes': '#2050c0'},
        ],
    },
    'varoom': {
        # motorblokken: metaal, donker chassis, uitlaat (paars), lampjes (geel)
        'species': {
            'varoom': {'metal': [7, 5, 8, 6], 'dark': [1, 3, 4, 14], 'purple': [10, 12, 9], 'yellow': [11, 13]},
            'revavroom': {'metal': [7, 11, 13, 12, 6], 'dark': [1, 2, 4, 3], 'purple': [8, 9, 10], 'yellow': [14, 15]},
        },
        'variants': [
            {'naam': 'Rosso Corsa (Ferrari-rood)', 'metal': ('#d40c0c', {'h': 0}), 'dark': '#3a3a40', 'purple': '#f0d040',
             'yellow': '#f0d040'},
            {'naam': 'Gulf Racing (lichtblauw en oranje)', 'metal': '#90c8e8', 'dark': '#3a4a5a', 'purple': '#f08020',
             'yellow': '#f08020'},
            {'naam': 'Roestbak (roest en zeegroen)', 'metal': '#a86030', 'dark': '#4a3a30', 'purple': '#60a090',
             'yellow': '#e0c070'},
            {'naam': 'Mercedes F1 (wit en zilver, petrolgroen)', 'metal': ('#dce0e4', {'l': 1.5}), 'dark': ('#1c1c22', DARK),
             'purple': '#00c0a8', 'yellow': '#00c0a8'},
            {'naam': 'Lamborghini-groen', 'metal': '#80d020', 'dark': '#2c2c34', 'purple': '#3a3a40', 'yellow': '#f0f0f0'},
            {'naam': 'Gouden lowrider (candy-goud, kersenrood)', 'metal': ('#e0b030', GOLD), 'dark': '#5a1828',
             'purple': '#e02840', 'yellow': '#f8f0d0'},
        ],
    },
    'cyclizar': {
        # fietshagedis: lijf, zadel/kop (donkergroen), donkere poten, oranje accent
        'species': {
            'cyclizar': {'body': [9, 10, 13], 'saddle': [1, 2, 3, 4], 'dark': [12, 11, 14], 'accent': [6]},
        },
        'variants': [
            {'naam': 'Kraaghagedis (zandbruin, oranje)', 'body': '#c0a070', 'saddle': '#7a5a38', 'dark': '#4a3a30',
             'accent': '#f06020'},
            {'naam': 'Basilisk (blauwgroen)', 'body': '#40a0a0', 'saddle': '#20606a', 'dark': '#283a48',
             'accent': '#f0d040'},
            {'naam': 'Vespa (mint scooter, crème zadel)', 'body': '#a8e0c8', 'saddle': ('#c8b890', {'l': 1.5}), 'dark': '#5a5a60',
             'accent': '#e02828'},
            {'naam': 'Ducati Panigale (rood, zwart zadel)', 'body': '#d02828', 'saddle': ('#34343c', DARK),
             'dark': '#3a3a40', 'accent': '#f0f0f0'},
            {'naam': 'Harley-Davidson (zwart, chroom en oranje)', 'body': ('#3a3a44', DARK), 'saddle': '#c8ccd8',
             'dark': '#1c1c22', 'accent': '#f08020'},
            {'naam': 'Tron-lightcycle (neoncyaan op zwart)', 'body': '#40e0f0', 'saddle': ('#202830', DARK),
             'dark': ('#1c2028', DARK), 'accent': '#f0f0ff'},
        ],
    },
    'orthworm': {
        # treinworm: lijf (rood), metaal (grijs), buik, stekels (blauw), ogen
        'species': {
            'orthworm': {'body': [3, 2, 1, 5], 'metal': [7, 8, 6], 'belly': [11, 10], 'spikes': [14, 15],
                         'mouth': [13, 12], 'eyes': [9]},
        },
        'variants': [
            {'naam': 'Regenworm (pierroze)', 'body': '#e0a0a0', 'metal': '#8a7a70', 'belly': '#f8e0d0', 'spikes': '#c04060',
             'mouth': '#7a3040', 'eyes': '#f0f0f0'},
            {'naam': 'Stoomlocomotief (zwart met messing)', 'body': ('#3a3a44', DARK), 'metal': ('#d0a840', GOLD),
             'belly': '#a03028', 'spikes': '#d0a840', 'mouth': '#601820', 'eyes': '#f0d040'},
            {'naam': 'Shinkansen (wit met blauwe streep)', 'body': '#f0f0f4', 'metal': '#a0a8b8', 'belly': '#e0e4ec',
             'spikes': '#2048b0', 'mouth': '#2048b0', 'eyes': '#2048b0'},
            {'naam': 'Zandworm van Dune (zand, oranje kristal)', 'body': '#d0b080', 'metal': '#7a6a50', 'belly': '#f0e0c0',
             'spikes': '#f08020', 'mouth': '#6a4a30', 'eyes': '#3070e0'},
            {'naam': 'Orient-Express (nachtblauw met goud)', 'body': '#203878', 'metal': ('#d8b040', GOLD),
             'belly': '#f0e8d0', 'spikes': '#c02838', 'mouth': '#101c40', 'eyes': '#f0d040'},
            {'naam': 'De gouden spoorspijker (goud op zwart)', 'body': ('#d8b040', GOLD), 'metal': ('#34343c', DARK),
             'belly': '#f8f0d0', 'spikes': '#c02838', 'mouth': '#6a4a10', 'eyes': '#c02838'},
        ],
    },
    'glimmet': {
        # giftige kristallen: kristal (blauw), paars (Glimmets lijf, Glimmoras bloembladen), kern, ogen
        'species': {
            'glimmet': {'crystal': [1, 4, 3, 2], 'purple': [10, 12, 11, 13], 'core': [6, 7, 5, 14], 'eyes': [8]},
            'glimmora': {'crystal': [6, 7, 4, 3, 8, 1, 5], 'purple': [11, 10, 9], 'core': [12, 13, 14], 'eyes': [15]},
        },
        'variants': [
            {'naam': 'Robijn', 'crystal': '#d02040', 'purple': '#f0a0b0', 'core': '#4a3040', 'eyes': '#f0f0f0'},
            {'naam': 'Smaragd', 'crystal': '#20a060', 'purple': '#e0d070', 'core': '#2c4038', 'eyes': '#f0d040'},
            {'naam': 'Keizerstopaas (oranje)', 'crystal': '#f09030', 'purple': '#a05030', 'core': '#4a3a30',
             'eyes': '#40e0f0'},
            {'naam': 'Opaal (melkwit met regenboogglans)', 'crystal': ('#d4e0e8', {'l': 1.6}), 'purple': '#f0a0d0',
             'core': '#90b0c8', 'eyes': '#40d0a0'},
            {'naam': 'Obsidiaan met gifgroen', 'crystal': ('#34343e', DARK), 'purple': '#80f040', 'core': '#1c1c24',
             'eyes': '#80f040'},
            {'naam': 'Watermeloentoermalijn (roze en groen)', 'crystal': '#f070a0', 'purple': '#40b060',
             'core': '#305030', 'eyes': '#f8f0f0'},
        ],
    },
    'greavard': {
        # spookhonden: lijf (grijze grafsteen), laken/witte vacht, kaarsvlam (Greavard), lap (Houndstone), mond
        'species': {
            'greavard': {'body': [8, 3, 2, 9], 'sheet': [13, 12, 14], 'flame': [7, 6, 10, 5], 'mouth': [1, 4]},
            'houndstone': {'body': [4, 9, 1, 11], 'sheet': [7, 12, 3], 'cloth': [5, 8, 2, 10]},
        },
        'variants': [
            {'naam': 'Terracotta urn (blauw kaarslicht)', 'body': '#c06a40', 'sheet': '#f0d8c0', 'flame': '#40c0f0',
             'cloth': '#3a5a80', 'mouth': '#a03030'},
            {'naam': 'Mosbegroeid graf', 'body': '#7a9070', 'sheet': '#c8d8b0', 'flame': '#c0f040', 'cloth': '#4a6a30',
             'mouth': '#a04040'},
            {'naam': 'Zero (Nightmare Before Christmas: wit, oranje neus)', 'body': ('#e4e6ee', ALBINO),
             'sheet': '#ffffff', 'flame': '#f08020', 'cloth': '#f08020', 'mouth': '#c04050'},
            {'naam': 'Roze marmeren engelengraf', 'body': '#d8b0b8', 'sheet': '#f8eef0', 'flame': '#f0d040',
             'cloth': '#a04060', 'mouth': '#a03050'},
            {'naam': 'Hellehond (zwart, groen spookvuur)', 'body': ('#3a3a44', DARK), 'sheet': '#6a6a78',
             'flame': '#40f060', 'cloth': '#30a050', 'mouth': '#40f060'},
            {'naam': 'Faraograf (lapis met goud)', 'body': '#3050a0', 'sheet': '#c8d4f0', 'flame': ('#f0c030', GOLD),
             'cloth': ('#e0b030', GOLD), 'mouth': '#c02838'},
        ],
    },
    'flamigo': {
        # flamingo: lijf (roze), vleugelpunten (magenta), hals/poten (grijs-wit), snavel, ogen
        'species': {
            'flamigo': {'body': [14, 5, 1, 4], 'magenta': [2, 11], 'neck': [3, 9, 12], 'beak': [7, 10],
                        'eyes': [8, 13]},
        },
        'variants': [
            {'naam': 'Zwarte flamingo (melanisme, Cyprus)', 'body': ('#3a3a44', DARK), 'magenta': '#d03070',
             'neck': '#a0a0a8', 'beak': '#f0a0b0', 'eyes': '#f0d040'},
            {'naam': 'Witte lepelaar (gele borst)', 'body': ('#ecebe8', ALBINO), 'magenta': '#f0d050', 'neck': '#d8d0c8',
             'beak': '#3a3a40', 'eyes': '#e03030'},
            {'naam': 'Blauwe reiger', 'body': '#7a90b0', 'magenta': '#2c3a58', 'neck': '#e0e4ec', 'beak': '#f0c030',
             'eyes': '#f0d040'},
            {'naam': 'Shaolin-kraanvogel (oranje en rood gewaad)', 'body': '#f08020', 'magenta': '#c02020',
             'neck': '#f0d040', 'beak': '#3a3a40', 'eyes': '#f0f0f0'},
            {'naam': 'Purperkoet (paars en blauw, rode snavel)', 'body': '#5a40a0', 'magenta': '#3060c0',
             'neck': '#a090d0', 'beak': '#e03030', 'eyes': '#f0d040'},
            {'naam': 'Miami Vice (mint en neonroze)', 'body': '#60d8c0', 'magenta': '#f060a0', 'neck': '#f8f8f8',
             'beak': '#f060a0', 'eyes': '#f0d040'},
        ],
    },
    'cetoddle': {
        # ijswalvissen: wit, grijze huid, roze (oren/wangen), hoorn/poten (Cetitan)
        'species': {
            'cetoddle': {'white': [3, 4], 'grey': [5, 1, 2], 'pink': [6, 7]},
            'cetitan': {'white': [2], 'grey': [5, 1, 3], 'pink': [4, 6, 7], 'horn': [12, 9, 11, 10]},
        },
        'variants': [
            {'naam': 'Narwal (gevlekt grijs, ivoren hoorn)', 'white': '#c8ccd8', 'grey': '#6a7488', 'pink': '#40a0c0',
             'horn': '#f0ecd8'},
            {'naam': 'Wolharige mammoet (roodbruin)', 'white': '#c09068', 'grey': '#7a4a30', 'pink': '#f0e0c0',
             'horn': '#f0e8d0'},
            {'naam': 'Gletsjerblauw', 'white': '#c8ecf8', 'grey': '#5aa0d0', 'pink': '#3060c0', 'horn': '#e0f8ff'},
            {'naam': 'Pêche Melba (perzik met frambozen)', 'white': '#f8d0b0', 'grey': '#e08070', 'pink': '#c02848',
             'horn': '#f8f0e0'},
            {'naam': 'Noorderlicht (groen en paars)', 'white': '#a0f0c8', 'grey': '#6040a0', 'pink': '#f060c0',
             'horn': '#40e0a0'},
            {'naam': 'Kerstman (rood met wit bont)', 'white': '#d02838', 'grey': '#801820', 'pink': '#f8f8f8',
             'horn': '#f8f8f8'},
        ],
    },
    'veluza': {
        # filetvis: lijf (zilvergrijs), vinnen (roze, ook de paarse vlekjes), mond
        'species': {
            'veluza': {'body': [7, 8, 5, 9, 6, 12], 'fins': [4, 2, 1, 11], 'mouth': [13, 14]},
        },
        'variants': [
            {'naam': 'Zalmfilet (oranjeroze)', 'body': '#f09070', 'fins': '#e05030', 'mouth': '#f8f0e0'},
            {'naam': 'Blauwvintonijn (blauwzwart, gele vinnen)', 'body': '#3a4a70', 'fins': '#f0d040', 'mouth': '#e04040'},
            {'naam': 'Barracuda (zilver, zwarte vinnen)', 'body': '#c8ccd0', 'fins': ('#2c2c34', DARK), 'mouth': '#e04040'},
            {'naam': 'Kohaku-koi (wit met rood)', 'body': ('#ecebe8', ALBINO), 'fins': '#e03020', 'mouth': '#e03020'},
            {'naam': 'Diepzee-zwaardvis (indigo met cyaan)', 'body': '#3a3070', 'fins': '#40e0f0', 'mouth': '#40e0f0'},
            {'naam': 'Goudvis (kingyo)', 'body': ('#e0b030', GOLD), 'fins': '#e04030', 'mouth': '#f8f0f0'},
        ],
    },
    'dondozo': {
        # reuzenmeerval: rug (lichtblauw), flanken (donkerblauw), buik/snorharen
        'species': {
            'dondozo': {'top': [6, 7, 10, 5], 'dark': [11, 9, 8, 12], 'belly': [2, 3, 1]},
        },
        'variants': [
            {'naam': 'Albino meerval (rozewit)', 'top': ('#ece0e0', ALBINO), 'dark': '#c8a0a8', 'belly': '#f8f0f0'},
            {'naam': 'Groene snoekbaars (olijf)', 'top': '#6a8a40', 'dark': '#3a5028', 'belly': '#e8e0c0'},
            {'naam': 'Moddermeerval (bruin)', 'top': '#8a6a48', 'dark': '#4a3a28', 'belly': '#d8c8b0'},
            {'naam': 'Diepzee-hengelaar (paarse gloed)', 'top': '#7a4ab0', 'dark': '#3a2060', 'belly': '#e0d0f0'},
            {'naam': 'Orka-meerval (zwart en wit)', 'top': ('#3a3a44', DARK), 'dark': ('#1c1c24', DARK), 'belly': '#f0f0f0'},
            {'naam': 'Showa-koi (rood, zwart en wit)', 'top': '#d02820', 'dark': ('#2c2c34', DARK), 'belly': '#f8f8f8'},
        ],
    },
    'tatsugiri': {
        # sushi-draakjes. Oordeel: de drie vormen (curly/droopy/stretchy) zijn vormen, net als Squawkabilly;
        # ze krijgen dezelfde zes sushi-skins (lijf, buik, rijst/bord). Ogen blijven wit.
        'species': {
            'tatsugiri': {'body': [2, 4, 1, 3], 'belly': [6, 8, 7], 'rice': [14, 12, 13]},
            'tatsugiri/droopy': {'body': [2, 4, 1, 3], 'rice': [7, 8, 6]},
            'tatsugiri/stretchy': {'body': [2, 4, 1, 6, 3], 'rice': [12, 10, 11]},
        },
        'variants': [
            {'naam': 'Saba (makreel, zilverblauw)', 'body': '#6a88b0', 'belly': '#e0e8f0', 'rice': '#f8f8f0'},
            {'naam': 'Unagi (paling met teriyakisaus)', 'body': '#5a3a28', 'belly': '#c08850', 'rice': '#f8f4e8'},
            {'naam': 'Kappamaki (komkommer op nori)', 'body': '#4aa050', 'belly': '#d0f0b0', 'rice': ('#3a3a40', DARK)},
            {'naam': 'Ikasumi (inktvisinkt, zwart)', 'body': ('#3e3e48', DARK), 'belly': '#a0a0b0', 'rice': '#f8f8f0'},
            {'naam': 'Ube-mochi (paars)', 'body': '#8050b0', 'belly': '#e0c8f0', 'rice': '#f8f0f8'},
            {'naam': 'Kinpaku (bladgoud op zwart lakbord)', 'body': ('#e0b830', GOLD), 'belly': '#f8f0c0',
             'rice': ('#2c2c34', DARK)},
        ],
    },
    'kingambit': {
        # 'ijzeren koning' (eigen recept, Pawniard/Bisharp zijn van een andere agent): harnas, goud (kroon/
        # schouders), rood (cape, kraag), witte kling (gezicht)
        'species': {
            'kingambit': {'armor': [8, 12], 'gold': [4, 5, 7], 'red': [10, 13, 11, 9, 6, 14, 15], 'blade': [3, 1]},
        },
        'variants': [
            {'naam': 'Witte schaakkoning (zilver, koningsblauw)', 'armor': '#a8acb8', 'gold': '#e8e8f0', 'red': '#3050b0',
             'blade': '#f8f8f8'},
            {'naam': 'Shogun (rood lakharnas met goud)', 'armor': '#8a1820', 'gold': '#f0c030', 'red': ('#2c2c34', DARK),
             'blade': '#f0f0f0'},
            {'naam': 'Korinthisch brons (kopergroen en brons)', 'armor': '#3a7a68', 'gold': '#c08040', 'red': '#e0e0e8',
             'blade': '#f0f0f0'},
            {'naam': 'Byzantijnse keizer (purper, goud, smaragd)', 'armor': '#4a2a6a', 'gold': '#e0b040',
             'red': '#40c0a0', 'blade': '#f0f0f0'},
            {'naam': 'De Nachtkoning (ijsblauw)', 'armor': '#5a8ab0', 'gold': '#c8e8f8', 'red': '#40e0ff',
             'blade': '#e8f8ff'},
            {'naam': 'Zonnekoning Lodewijk XIV (goud met koningsblauw)', 'armor': ('#e0b840', GOLD), 'gold': '#2848a0',
             'red': '#2848a0', 'blade': '#fffcf0'},
        ],
    },
    'frigibax': {
        # ijsdraken: lijf, ijs (rugvin, Baxcaliburs kling), geel (ogen/klauwen), rood (Baxcaliburs klauwen)
        'species': {
            'frigibax': {'body': [6, 8, 7, 1, 10, 11], 'ice': [14, 15, 12], 'yellow': [5, 4, 3, 2]},
            'arctibax': {'body': [8, 10, 2, 5, 3], 'ice': [13, 14, 12, 9, 4], 'yellow': [7, 6, 1]},
            'baxcalibur': {'body': [6, 11, 5], 'ice': [4, 7, 2, 3], 'yellow': [9, 8], 'red': [14, 13, 12]},
        },
        'variants': [
            {'naam': 'Nachtdraak (zwart met cyaan ijs)', 'body': ('#3a3a46', DARK), 'ice': '#60e0f0', 'yellow': '#f0f040',
             'red': '#40e0f0'},
            {'naam': 'Smaragdgletsjer', 'body': '#2a6a5a', 'ice': '#a0f0d0', 'yellow': '#f0d040', 'red': '#e04040'},
            {'naam': 'Sneeuwwitte draak (blauwe ogen)', 'body': ('#d4d8e4', {'l': 1.6}), 'ice': '#80c0f0',
             'yellow': '#3060d0', 'red': '#d02838'},
            {'naam': 'Amethistgrot', 'body': '#4a3a7a', 'ice': '#d0a0f0', 'yellow': '#f0d040', 'red': '#f060a0'},
            {'naam': 'Vuur en ijs (rode draak, ijsblauwe vinnen)', 'body': '#a02028', 'ice': '#a0e0f8',
             'yellow': '#f0d040', 'red': '#f08020'},
            {'naam': 'Excalibur (koningsblauw met gouden kling)', 'body': '#283070', 'ice': ('#e0b840', GOLD),
             'yellow': '#f8f8f8', 'red': '#c02028'},
        ],
    },
    'gimmighoul': {
        # schatkist en munten: goud (kistbeslag, munten, Gholdengo), fluweel (rood), spookje (grijs)
        'species': {
            'gimmighoul': {'gold': [8, 4, 2, 13, 9], 'velvet': [3, 7, 1], 'ghost': [14, 5, 10, 11, 6, 15],
                           '_base': {'ghost': 14}},
            'gimmighoul/roaming': {'gold': [4, 2, 1, 5], 'ghost': [8, 3, 6, 9]},
            'gholdengo': {'gold': [8, 11, 10, 9, 5, 7, 1, 2, 6], 'ghost': [4, 14, 12], 'velvet': [3],
                          '_base': {'ghost': 14}},
        },
        'variants': [
            {'naam': 'Zilverschat (sterling, blauw fluweel)', 'gold': ('#c8ccd8', {'l': 1.2}), 'velvet': '#2848a0',
             'ghost': '#98a8c8'},
            {'naam': 'Koperen centen (groen fluweel)', 'gold': '#c06838', 'velvet': '#2a6a50', 'ghost': '#b8a8a0'},
            {'naam': 'Jadeschat (rood fluweel)', 'gold': '#40a878', 'velvet': '#c02838', 'ghost': '#a0c0b0'},
            {'naam': 'Roségoud', 'gold': '#e0a090', 'velvet': '#5a3a60', 'ghost': '#c0a8c0'},
            {'naam': 'Vervloekt Azteeks goud (Pirates of the Caribbean)', 'gold': '#7a8a50', 'velvet': '#2c3a2c',
             'ghost': '#a0f0c0'},
            {'naam': 'Amethistgoud (paarse spookschat)', 'gold': '#a060d0', 'velvet': '#f0c030', 'ghost': '#a890c0'},
        ],
    },
    'great_tusk': {
        # oer-Donphan: lijf (paars), onderlijf (grijsblauw), slagtanden, rode tekening, ogen
        'species': {
            'great_tusk': {'body': [4, 1, 11], 'lower': [10, 14], 'tusks': [15, 12, 7], 'red': [6, 8, 3, 5, 2],
                           'eyes': [9]},
        },
        'variants': [
            {'naam': 'Oermammoet (roodbruin, oranje)', 'body': '#7a4a30', 'lower': '#c09068', 'tusks': '#f0e8d0',
             'red': '#f0a030', 'eyes': '#f0f0f0'},
            {'naam': 'Basalt (grijs, oranje tekening)', 'body': '#4a4a52', 'lower': '#8a8a92', 'tusks': '#f0e0c0',
             'red': '#f08020', 'eyes': '#f0d040'},
            {'naam': 'Grotschildering van Lascaux (oker en houtskool)', 'body': '#b06a30', 'lower': '#e0b070',
             'tusks': '#3a3030', 'red': '#7a2018', 'eyes': '#f0f0e0'},
            {'naam': 'IJstijd (ijsblauw en wit)', 'body': '#b8d0e8', 'lower': '#e8f0f8', 'tusks': '#f8f8f8',
             'red': '#3070d0', 'eyes': '#3070d0'},
            {'naam': 'Fossiel in zandsteen (barnsteen)', 'body': '#c0a880', 'lower': '#e0d0b0', 'tusks': '#8a7058',
             'red': '#e09020', 'eyes': '#e09020'},
            {'naam': 'Maya-obsidiaan met jade', 'body': ('#2c2c38', DARK), 'lower': '#3a5a50', 'tusks': '#40c080',
             'red': '#40c080', 'eyes': '#f0d040'},
        ],
    },
    'scream_tail': {
        # oer-Jigglypuff: vacht (roze), staart/oren (donkerroze), ogen (geel)
        'species': {
            'scream_tail': {'body': [2, 3, 1], 'tail': [6, 8, 4, 5], 'eyes': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Holenbeer (bruin)', 'body': '#c0a080', 'tail': '#7a4a30', 'eyes': '#f0d040'},
            {'naam': 'Yeti (wit met blauw)', 'body': ('#e8ecf4', ALBINO), 'tail': '#6080c0', 'eyes': '#f08020'},
            {'naam': 'Rode oker (Neanderthaler-verf)', 'body': '#e0a070', 'tail': '#a03020', 'eyes': '#3a2018'},
            {'naam': 'Pastelmint', 'body': '#c0f0d8', 'tail': '#40a080', 'eyes': '#f060a0'},
            {'naam': 'De Schreeuw (Munch: oranje lucht, blauw)', 'body': '#f0a040', 'tail': '#3050a0', 'eyes': '#3a3a40'},
            {'naam': 'Sterrennacht als nachtmerrie (zwartblauw, bloedrode staart, gloeiende ogen)', 'body': ('#262a50', DARK),
             'tail': '#a01020', 'eyes': '#ff2828'},
        ],
    },
    'brute_bonnet': {
        # oer-Amoonguss: hoed (rood), lijf (bruin), stippen (wit), mos (groen)
        'species': {
            'brute_bonnet': {'cap': [4, 7], 'brown': [2, 6, 15], 'spots': [5, 3], 'moss': [10, 9, 8],
                             'eyes': [11, 13, 14, 12]},
        },
        'variants': [
            {'naam': 'Gele vliegenzwam (Amanita flavoconia)', 'cap': '#f0c030', 'brown': '#6a4a28', 'spots': '#f8f0e0',
             'moss': '#a0b040', 'eyes': '#e04040'},
            {'naam': 'Psilocybe (karamel met blauwe kneuzing)', 'cap': '#c08040', 'brown': '#5a3a28', 'spots': '#e0d8c0',
             'moss': '#4070c0', 'eyes': '#40c0f0'},
            {'naam': 'Berkenzwam met korstmos', 'cap': '#e8e4dc', 'brown': '#8a8a80', 'spots': '#3a3a40',
             'moss': '#a0b8a0', 'eyes': '#e04040'},
            {'naam': 'Bloedende tandzwam (wit met bloeddruppels)', 'cap': '#c81828', 'brown': '#e0d8d0',
             'spots': '#f8f8f8', 'moss': '#b8b0a8', 'eyes': '#c81828'},
            {'naam': 'Lichtgevende Mycena (groen licht in donker bos)', 'cap': '#80f080', 'brown': ('#2c3830', DARK),
             'spots': '#c0ffc0', 'moss': '#1c2c24', 'eyes': '#c0ffc0'},
            {'naam': 'Truffel met bladgoud', 'cap': ('#e0b030', GOLD), 'brown': '#3a2a24', 'spots': '#f8f0d0',
             'moss': '#6a5a40', 'eyes': '#e0b030'},
        ],
    },
    'flutter_mane': {
        # oer-Misdreavus: lijf (teal), haar (paars), rode parels/ogen, nekpunten, gele ogen
        'species': {
            'flutter_mane': {'body': [7, 10, 9, 8], 'hair': [4, 2, 1], 'red': [11, 6, 5], 'tips': [12, 13],
                             'eyes': [15, 14]},
        },
        'variants': [
            {'naam': 'Banshee (bleekgrijs met bloedrood)', 'body': '#7a8088', 'hair': '#c8c8d8', 'red': '#a01828',
             'tips': '#a8b0b8', 'eyes': '#f0f0f0'},
            {'naam': 'Mismagius-hoed (paars en roze)', 'body': '#4a2a6a', 'hair': '#e070b0', 'red': '#f0d040',
             'tips': '#8050a0', 'eyes': '#f0d040'},
            {'naam': 'Bloedroos (rozenrood met roze haar)', 'body': '#7a1830', 'hair': '#f080a0', 'red': '#f0d040',
             'tips': '#c04060', 'eyes': '#f0d040'},
            {'naam': 'Zwarte weduwe met parels', 'body': ('#2c2c34', DARK), 'hair': '#e8e0f0', 'red': '#c02848',
             'tips': '#5a5a68', 'eyes': '#c02848'},
            {'naam': 'Onryō (wit kimono, zwart haar)', 'body': '#d8d0d8', 'hair': ('#2c2c34', DARK), 'red': '#c02020',
             'tips': '#f0f0f0', 'eyes': '#c02020'},
            {'naam': 'Morgenrood (oranje met gouden haar)', 'body': '#d07040', 'hair': ('#f0c040', GOLD),
             'red': '#f0f0f0', 'tips': '#f0a060', 'eyes': '#40c0f0'},
        ],
    },
    'slither_wing': {
        # oer-Volcarona: vleugels (rood), geel, witte vacht, blauw (borst/poten), groene vlekjes
        'species': {
            'slither_wing': {'red': [6, 7, 1], 'yellow': [3, 2], 'fur': [9, 10, 8], 'blue': [12, 11],
                             'green': [4, 14, 15, 13]},
        },
        'variants': [
            {'naam': 'Atlasvlinder (roestbruin, crème)', 'red': '#a85a30', 'yellow': '#f0e0b0', 'fur': '#e8d8c0',
             'blue': '#3a2a20', 'green': '#f0c070'},
            {'naam': 'Maanvlinder (lichtgroen)', 'red': '#80d090', 'yellow': '#f0e080', 'fur': '#f0f8e8',
             'blue': '#a04060', 'green': '#e0f0a0'},
            {'naam': 'Blauwe morpho', 'red': '#2070e0', 'yellow': '#40e0f0', 'fur': '#d8e0f0', 'blue': ('#2c2c34', DARK),
             'green': '#60f0f0'},
            {'naam': 'Rouwmantel (zwart met gele rand)', 'red': ('#3a2a30', DARK), 'yellow': '#f0e060', 'fur': '#c8c0c0',
             'blue': '#4060d0', 'green': '#f0e060'},
            {'naam': 'Roze esdoornmot', 'red': '#f080b0', 'yellow': '#f0e050', 'fur': '#f8f0f0', 'blue': '#d04080',
             'green': '#f8c0d8'},
            {'naam': 'Feniks (wit vuur met goud)', 'red': ('#e8e4f0', {'l': 1.2}), 'yellow': ('#f0c030', GOLD),
             'fur': '#f8f0e0', 'blue': '#e04020', 'green': '#f08030'},
        ],
    },
    'sandy_shocks': {
        # oer-Magneton van ijzerzand: zand (donker), magneten (blauw), ogen (geel), punten (rood)
        'species': {
            'sandy_shocks': {'body': [1, 3, 7], 'blue': [11, 9, 6, 8, 12, 13, 10], 'yellow': [14, 15], 'red': [5, 4]},
        },
        'variants': [
            {'naam': 'Woestijnzand (oker met turkoois)', 'body': '#b08850', 'blue': '#40b0b0', 'yellow': '#f0f0f0',
             'red': '#e04030'},
            {'naam': 'Hoefijzermagneet (rood en zilver)', 'body': '#5a5a64', 'blue': '#d02828', 'yellow': '#f0f0f0',
             'red': '#c8ccd8'},
            {'naam': 'Malachiet', 'body': '#2c4a3a', 'blue': '#40c070', 'yellow': '#f0d040', 'red': '#e06020'},
            {'naam': 'Fulguriet (bliksemglas in zand)', 'body': '#8a7a60', 'blue': '#e0f0e0', 'yellow': '#40e0f0',
             'red': '#f0a030'},
            {'naam': 'Magnetiet met paars plasma', 'body': ('#2c2c34', DARK), 'blue': '#a060f0', 'yellow': '#f040c0',
             'red': '#40e0f0'},
            {'naam': 'Pyriet (kattengoud)', 'body': '#5a4a30', 'blue': ('#e0c040', GOLD), 'yellow': '#e03030',
             'red': '#f0f0f0'},
        ],
    },
    'roaring_moon': {
        # oer-Salamence: vleugels (rood), lijf (blauw), geel/lila accenten
        'species': {
            'roaring_moon': {'red': [5, 6, 2], 'body': [10, 9, 13, 14, 3], 'yellow': [7, 8]},
        },
        'variants': [
            {'naam': 'Zwarte draak met oranje vleugels', 'body': ('#34343e', DARK), 'red': '#f08020', 'yellow': '#f0d040'},
            {'naam': 'Smaragddraak (gouden vleugels)', 'body': '#2a8a60', 'red': '#e0c040', 'yellow': '#f0f0f0'},
            {'naam': 'Paarse koningsdraak', 'body': '#6a4ab0', 'red': '#f0c030', 'yellow': '#40e0f0'},
            {'naam': 'Witte draak met blauwe vleugels', 'body': ('#e4e8f0', ALBINO), 'red': '#3060c0', 'yellow': '#40e0f0'},
            {'naam': 'Bloedmaan (karmozijn met zwarte vleugels)', 'body': '#8a1828', 'red': ('#34343c', DARK),
             'yellow': '#f04040'},
            {'naam': 'King Ghidorah (goud met rood)', 'body': ('#e0b030', GOLD), 'red': '#a01828', 'yellow': '#f0f0f0'},
        ],
    },
    'walking_wake': {
        # oer-Suicune: lijf (paars), manen/kuif (blauw), rood, oranje kuifpunten
        'species': {
            'walking_wake': {'body': [7, 8, 1, 12], 'blue': [9, 10, 2, 14], 'red': [4], 'orange': [5, 6]},
        },
        'variants': [
            {'naam': 'Moeraskrokodil (groen)', 'body': '#4a7a40', 'blue': '#90c0a0', 'red': '#f0d040', 'orange': '#e06020'},
            {'naam': 'Raikou-kleuren (geel met paarse manen)', 'body': '#d8a830', 'blue': '#6040a0', 'red': '#40c0f0',
             'orange': '#f0f0f0'},
            {'naam': 'Entei-kleuren (bruin met crème manen)', 'body': '#8a5030', 'blue': '#e8d8c0', 'red': '#f0c030',
             'orange': '#e04020'},
            {'naam': 'Suicune-kleuren (blauw met lila manen)', 'body': '#4a7ad0', 'blue': '#a080e0', 'red': '#f0f0f0',
             'orange': '#c03040'},
            {'naam': 'Inktzwart water (cyaan manen)', 'body': ('#34343e', DARK), 'blue': '#40e0f0', 'red': '#f04060',
             'orange': '#f0f0f0'},
            {'naam': 'Ho-Oh (rood met goud en groen)', 'body': '#c02828', 'blue': ('#e0b030', GOLD), 'red': '#30b060',
             'orange': '#f0f0f0'},
        ],
    },
    'gouging_fire': {
        # oer-Entei: manen (goud), lijf (oranjebruin), grijs (kraag/staart), rood, groen
        'species': {
            'gouging_fire': {'mane': [4, 5, 2, 1], 'body': [13, 15, 14], 'grey': [8, 6, 7], 'red': [12, 11],
                             'green': [9, 10]},
        },
        'variants': [
            {'naam': 'Zwart vuur (zwarte manen, rood lijf)', 'mane': ('#3a3440', DARK), 'body': '#8a2020', 'grey': '#a0a0a8',
             'red': '#f06020', 'green': '#f0d040'},
            {'naam': 'Blauw vuur', 'mane': '#4080e0', 'body': '#2a3a6a', 'grey': '#c8d0e0', 'red': '#40e0f0',
             'green': '#f0f0f0'},
            {'naam': 'Raikou-kleuren (paarse manen, geel lijf)', 'mane': '#7050b0', 'body': '#d8a830', 'grey': '#e0e0e8',
             'red': '#40c0f0', 'green': '#f0f0f0'},
            {'naam': 'Witheet', 'mane': ('#f0ecf0', {'l': 1.2}), 'body': '#c08060', 'grey': '#8a8a90', 'red': '#f0d040',
             'green': '#40c0f0'},
            {'naam': 'Kopervuur (groen)', 'mane': '#40c060', 'body': '#3a5030', 'grey': '#a0b0a0', 'red': '#e0f040',
             'green': '#f06020'},
            {'naam': 'Ho-Oh (rode manen, goud lijf)', 'mane': '#d83028', 'body': ('#f0c040', GOLD), 'grey': '#f8f0e0',
             'red': '#30b060', 'green': '#f0c040'},
        ],
    },
    'raging_bolt': {
        # oer-Raikou: wolk (paars), lijf (geel), wit, rood, blauw, kop (grijs)
        'species': {
            'raging_bolt': {'cloud': [8, 7, 4], 'yellow': [10, 9, 5], 'white': [6, 12, 11], 'red': [13], 'blue': [14, 15],
                            'grey': [1]},
        },
        'variants': [
            {'naam': 'Onweerswolk (zilvergrijs)', 'cloud': '#7a8090', 'yellow': '#f0d040', 'white': '#f0f0f0',
             'red': '#e06020', 'blue': '#40c0f0', 'grey': '#3a3a44'},
            {'naam': 'Roze zonsopgang', 'cloud': '#f0a0c0', 'yellow': '#f08040', 'white': '#f8f0e8', 'red': '#c02848',
             'blue': '#f0f040', 'grey': '#5a4048'},
            {'naam': 'Suicune-kleuren (blauwe wolk, cyaan lijf)', 'cloud': '#5070d0', 'yellow': '#60e0e0',
             'white': '#f0f8ff', 'red': '#a050e0', 'blue': '#f0f0f0', 'grey': '#3a4060'},
            {'naam': 'Tornado (groene storm)', 'cloud': '#4a7a5a', 'yellow': '#c0e040', 'white': '#e8f0e0',
             'red': '#f06020', 'blue': '#80f0c0', 'grey': '#3a4a40'},
            {'naam': 'Zwarte wolk, rode bliksem', 'cloud': ('#3a3a46', DARK), 'yellow': '#d02828', 'white': '#c8c8d0',
             'red': '#f0f0f0', 'blue': '#f04040', 'grey': '#2c2c34'},
            {'naam': 'Zeus (witgouden wolk, blauwe bliksem)', 'cloud': ('#f0ecf8', {'l': 1.2}), 'yellow': ('#e0b030', GOLD),
             'white': '#ffffff', 'red': '#3060d0', 'blue': '#40c0f0', 'grey': '#8a8a98'},
        ],
    },
    'iron_treads': {
        # robot-Donphan: lijf (donker), lichtstrepen (rood), metaal (grijs)
        'species': {'iron_treads': {'body': [3, 1, 5, 6, 2], 'lights': [8, 9, 10, 4], 'metal': [11, 7, 13, 14]}},
        'variants': [
            {'naam': 'Tron (cyaan neon)', 'body': ('#2a2a36', DARK), 'lights': '#40e0f0', 'metal': '#3a4a68'},
            {'naam': 'Bulldozer (Caterpillar-geel)', 'body': '#3a3a3e', 'lights': '#f08020', 'metal': '#e8b820'},
            {'naam': 'Evangelion Unit-01 (paars en lime)', 'body': '#4a2a70', 'lights': '#80f040', 'metal': '#7a5ab0'},
            {'naam': 'Stormtrooper (wit met blauwe lampjes)', 'body': '#c8c8d0', 'lights': '#3070e0', 'metal': '#f0f0f8'},
            {'naam': 'British racing green met goud', 'body': '#1c3a28', 'lights': '#f0c030', 'metal': '#3a6a48'},
            {'naam': 'Roségoud met mintlicht', 'body': '#5a3a48', 'lights': '#40e0c0', 'metal': '#e0a090'},
        ],
    },
    'iron_bundle': {
        # robot-Delibird: rood (zak/lijf), grijs-wit, geel (snavel/poten), blauw (ogen/stuwers)
        'species': {'iron_bundle': {'red': [4, 5, 6, 2], 'grey': [11, 3, 14, 15], 'yellow': [8, 7], 'blue': [10, 13, 9]}},
        'variants': [
            {'naam': 'Pinguïnbot (zwart en wit, oranje)', 'red': ('#3a3a44', DARK), 'grey': '#c8ccd0', 'yellow': '#f08020',
             'blue': '#40e0f0'},
            {'naam': 'IJskoud (blauw met oranje ogen)', 'red': '#3060c0', 'grey': '#d0e0f0', 'yellow': '#f0f0f0',
             'blue': '#f08020'},
            {'naam': 'De Grinch (groen met rood)', 'red': '#50a030', 'grey': '#d8e0c8', 'yellow': '#d02828',
             'blue': '#d02828'},
            {'naam': 'Kerstbal (roze en zilver)', 'red': '#e070b0', 'grey': '#e0e0e8', 'yellow': '#c0c8d8',
             'blue': '#a050e0'},
            {'naam': 'Krampus (zwartrood, bloedrode ogen)', 'red': '#5a1018', 'grey': '#4a4a54', 'yellow': '#c0a080',
             'blue': '#f04040'},
            {'naam': 'Gouden kerstster', 'red': ('#e0b030', GOLD), 'grey': '#f0ece0', 'yellow': '#c02028',
             'blue': '#2050c0'},
        ],
    },
    'iron_hands': {
        # robot-Hariyama: lijf (grijs), donker (broek/romp, blauw), handen (goud)
        'species': {'iron_hands': {'body': [10, 5, 12, 13], 'blue': [2, 4, 9, 1, 3], 'gold': [8, 7, 6, 14]}},
        'variants': [
            {'naam': 'Bouwkraan (staal en oranje)', 'body': '#8a8a92', 'blue': '#3a3a40', 'gold': '#f08020'},
            {'naam': 'Mazinger Z (staal, rood en blauw)', 'body': '#a0a8b8', 'blue': '#c02028', 'gold': '#3050c0'},
            {'naam': 'Yokozuna (huidkleur, zwarte mawashi, wit touw)', 'body': '#e0c8a8', 'blue': ('#2c2c34', DARK),
             'gold': '#f8f8f8'},
            {'naam': 'Gipsy Danger (Pacific Rim: blauwstaal, oranje reactor)', 'body': '#4a6a90', 'blue': '#2a3a58',
             'gold': '#f06020'},
            {'naam': 'Roze bokshandschoenen', 'body': '#f0b0c8', 'blue': '#c04070', 'gold': '#f8f0f8'},
            {'naam': 'Kampioensgordel (goud met rood)', 'body': ('#e0b030', GOLD), 'blue': '#c02028', 'gold': '#f8f0f0'},
        ],
    },
    'iron_jugulis': {
        # robot-Hydreigon: lijf (zwart), magenta, blauw
        'species': {'iron_jugulis': {'body': [3, 7, 1, 2, 6], 'magenta': [12, 11, 5, 13], 'blue': [10, 9, 4, 8, 15]}},
        'variants': [
            {'naam': 'F-14 Tomcat (grijs, rood en geel)', 'body': '#6a7080', 'magenta': '#d02828', 'blue': '#f0d040'},
            {'naam': 'Batwing (zwart met geel)', 'body': ('#2c2c34', DARK), 'magenta': '#f0c020', 'blue': '#f0f0f0'},
            {'naam': 'Stealthbommenwerper (nachtzichtgroen)', 'body': '#3a4038', 'magenta': '#60f060', 'blue': '#a0f0a0'},
            {'naam': 'Blue Angels (marineblauw met geel)', 'body': '#2840a0', 'magenta': '#f0c020', 'blue': '#f0f0f0'},
            {'naam': 'De Rode Baron (rood met wit)', 'body': '#a01818', 'magenta': '#f0f0f0', 'blue': ('#2c2c34', DARK)},
            {'naam': 'Gouden draak (King Ghidorah-robot)', 'body': ('#d8a830', GOLD), 'magenta': '#c02028',
             'blue': '#40c0f0'},
        ],
    },
    'iron_moth': {
        # robot-Volcarona: zonnevleugels (oranje), rood, lijf (donker), metaal, blauw
        'species': {'iron_moth': {'wings': [9, 7, 5, 10], 'red': [8, 6], 'body': [2, 3, 1], 'metal': [12, 4, 15],
                                  'blue': [11, 14]}},
        'variants': [
            {'naam': 'Gasbrander (blauwe vlam)', 'wings': '#3070e0', 'red': '#80e0f0', 'body': '#2c2c38', 'metal': '#c0c4d0',
             'blue': '#f08020'},
            {'naam': 'Uraniumreactor (gifgroen)', 'wings': '#80e030', 'red': '#2a8a30', 'body': '#2c3428', 'metal': '#b8c0b0',
             'blue': '#f0f040'},
            {'naam': 'Paars plasma', 'wings': '#a050e0', 'red': '#f060c0', 'body': '#2c2838', 'metal': '#c0b8d0',
             'blue': '#40e0f0'},
            {'naam': 'Neonroze', 'wings': '#f060a0', 'red': '#a02060', 'body': '#3a2c34', 'metal': '#d8c8d0',
             'blue': '#f0f040'},
            {'naam': 'Zwarte zon (zwart met gouden corona)', 'wings': ('#3a3440', DARK), 'red': ('#f0c030', GOLD),
             'body': '#1c1c22', 'metal': '#5a5a60', 'blue': '#f0c030'},
            {'naam': 'Spiegelchroom (zilver, roze en cyaan)', 'wings': ('#d0d4e0', {'l': 1.2}), 'red': '#f060a0',
             'body': '#3a3a44', 'metal': '#7a7a88', 'blue': '#40e0f0'},
        ],
    },
    'iron_thorns': {
        # robot-Tyranitar: lijf (groen), kristallen (teal), donker metaal
        'species': {'iron_thorns': {'body': [8, 10, 3, 11], 'crystal': [12, 9, 14], 'grey': [5, 2, 1, 4, 6, 7]}},
        'variants': [
            {'naam': 'Mechagodzilla (zilverstaal, gele kristallen)', 'body': '#a0a8b8', 'crystal': '#f0c030',
             'grey': '#3a3a44'},
            {'naam': 'Destoroyah (paarse kaiju, rode kristallen)', 'body': '#6a3a8a', 'crystal': '#f04060', 'grey': '#2c2034'},
            {'naam': 'Godzilla (atoomblauw op zwartgroen)', 'body': '#3a4a40', 'crystal': '#40c0f0', 'grey': '#2c2c30'},
            {'naam': 'Shin Godzilla (gloeiend rood)', 'body': '#a02820', 'crystal': '#f08020', 'grey': '#2c2020'},
            {'naam': 'RX-78 Gundam (wit, rood en blauw)', 'body': '#e4e4ec', 'crystal': '#c02028', 'grey': '#2848a0'},
            {'naam': 'Kolos van Rhodos (brons met turkoois)', 'body': ('#c08040', GOLD), 'crystal': '#40e0c0',
             'grey': '#4a3a28'},
        ],
    },
    'iron_valiant': {
        # robot-Gardevoir/Gallade: groen, wit, roze (hoorn/kling), donker
        'species': {'iron_valiant': {'green': [5, 6, 7, 2], 'white': [15, 14, 9, 10, 11], 'pink': [8, 4, 12]}},
        'variants': [
            {'naam': 'IJszwaard (blauw met cyaan)', 'green': '#3060b0', 'white': '#f0f0f8', 'pink': '#40e0f0'},
            {'naam': 'Zwarte ridder (zwart met paars)', 'green': ('#34343e', DARK), 'white': '#a0a0b0', 'pink': '#a050e0'},
            {'naam': 'Rode lotus (rood met goud)', 'green': '#b02030', 'white': '#f8f0e0', 'pink': '#f0c030'},
            {'naam': 'Lavendel en jade', 'green': '#a080d0', 'white': '#f8f8ff', 'pink': '#40c0a0'},
            {'naam': 'Sakura-samoerai (roze, wit, zwart)', 'green': '#f0a0c0', 'white': '#f8f8f8',
             'pink': ('#34343c', DARK)},
            {'naam': 'Paladijn (goud en wit, blauwe kling)', 'green': ('#e0b030', GOLD), 'white': '#f8f8f8',
             'pink': '#3060d0'},
        ],
    },
    'iron_leaves': {
        # robot-Virizion: lijf (groen), rood (hoorn/knieën), grijs metaal. Thema: de Zwaarden van Gerechtigheid.
        'species': {'iron_leaves': {'green': [8, 9, 3, 11, 1, 2], 'red': [7, 6, 14], 'grey': [5, 4, 10, 13]}},
        'variants': [
            {'naam': 'Herfstblad (oranje, geel)', 'green': '#d07030', 'red': '#f0d040', 'grey': '#6a5040'},
            {'naam': 'Cobalion-kleuren (blauw met goud)', 'green': '#3a6ab0', 'red': '#f0c030', 'grey': '#5a6070'},
            {'naam': 'Terrakion-kleuren (grijs met oranje)', 'green': '#8a8070', 'red': '#f08020', 'grey': '#4a4038'},
            {'naam': 'Keldeo-kleuren (crème, rood en blauw)', 'green': '#f0e0c0', 'red': '#d02838', 'grey': '#3060c0'},
            {'naam': 'Cyberblad (zwart met neonlime)', 'green': ('#2c2c34', DARK), 'red': '#c0f040', 'grey': '#40e0a0'},
            {'naam': 'Gouden lauwerkrans (Olympisch)', 'green': ('#e0b030', GOLD), 'red': '#f8f8f8', 'grey': '#8a6a20'},
        ],
    },
    'iron_boulder': {
        # robot-Terrakion: pantser (grijs), lijf (donkerbruin), oranje, rood. Thema: de Zwaarden van Gerechtigheid.
        'species': {'iron_boulder': {'armor': [10, 8, 6, 7], 'body': [3, 2, 4, 5], 'orange': [11, 9, 12],
                                     'red': [15, 14, 13]}},
        'variants': [
            {'naam': 'Cobalion-kleuren (blauw staal)', 'armor': '#6a88b8', 'body': '#2a3858', 'orange': '#f0d040',
             'red': '#40c0f0'},
            {'naam': 'Virizion-kleuren (groen met roze)', 'armor': '#90d0a0', 'body': '#2c5a3c', 'orange': '#f080a0',
             'red': '#e03050'},
            {'naam': 'Roze graniet', 'armor': '#d0a8a8', 'body': ('#2c2c30', DARK), 'orange': '#f0f0f0', 'red': '#c02838'},
            {'naam': 'Lavarots (zwart met rood)', 'armor': '#5a5a64', 'body': '#3a2020', 'orange': '#f04018',
             'red': '#f0c030'},
            {'naam': 'Maansteen (wit met blauw)', 'armor': ('#e8ecf4', ALBINO), 'body': '#3a4868', 'orange': '#80c0f0',
             'red': '#4060d0'},
            {'naam': 'Gulden Vlies (gouden ram)', 'armor': ('#e0b030', GOLD), 'body': '#5a3a20', 'orange': '#f8f8f0',
             'red': '#c02028'},
        ],
    },
    'iron_crown': {
        # robot-Cobalion: kristallijf (teal), goud, grijs metaal
        'species': {'iron_crown': {'teal': [12, 10, 9, 11, 1, 2, 3], 'gold': [5, 8, 6], 'grey': [7, 13, 14, 15]}},
        'variants': [
            {'naam': 'Robijnen koning (zilveren kroon)', 'teal': '#c02040', 'gold': '#e0e0e8', 'grey': '#5a5a64'},
            {'naam': 'Smaragden koning', 'teal': '#20a060', 'gold': '#e0c040', 'grey': '#4a5a50'},
            {'naam': 'Amethisten koning', 'teal': '#8050c0', 'gold': '#f0f0f0', 'grey': '#5a5068'},
            {'naam': 'Diamanten koning (ijswit)', 'teal': ('#d8f0f8', ALBINO), 'gold': '#80c0f0', 'grey': '#9098a8'},
            {'naam': 'Onyx (zwart met rood licht)', 'teal': ('#2c2c34', DARK), 'gold': '#e02828', 'grey': '#5a5a64'},
            {'naam': 'Zonnekroon (goud met koningsblauw)', 'teal': ('#e0b030', GOLD), 'gold': '#2848a0', 'grey': '#f0f0f0'},
        ],
    },
    'koraidon': {
        # oer-motorhagedis: rood lijf, witte veren/staart, grijs, blauw (borst/kraag), roze punten
        'species': {'koraidon': {'red': [7, 6, 1], 'white': [15, 13], 'grey': [4, 2], 'blue': [9, 10, 3],
                                 'pink': [12, 11]}},
        'variants': [
            {'naam': 'Miraidon-kleuren (paars met geel)', 'red': '#5a48a8', 'white': '#c8c6e4', 'grey': '#2d2f60',
             'blue': '#f0e020', 'pink': '#40c0f0'},
            {'naam': 'Kawasaki-racer (groen, zwart, geel)', 'red': '#3aa040', 'white': '#f0f0f0', 'grey': '#3a3a40',
             'blue': ('#2c2c34', DARK), 'pink': '#f0e020'},
            {'naam': 'Woestijnhagedis (zandoker)', 'red': '#c09050', 'white': '#f0e0c0', 'grey': '#5a4a38',
             'blue': '#7a4a30', 'pink': '#e06020'},
            {'naam': 'KTM (oranje met zwart)', 'red': '#f07818', 'white': '#f8f0e8', 'grey': '#4a4a50', 'blue': '#3a3a44',
             'pink': '#f0f0f0'},
            {'naam': 'Chopper (zwart met rode kraag)', 'red': ('#3a3a46', DARK), 'white': '#c8c8d0', 'grey': '#5a5a64',
             'blue': '#c02028', 'pink': '#f0d040'},
            {'naam': 'Azteekse zonnesteen (goud met turkoois)', 'red': ('#e0b030', GOLD), 'white': '#f8f0d8',
             'grey': '#6a5a40', 'blue': '#30a090', 'pink': '#c02028'},
        ],
    },
    'miraidon': {
        # toekomst-motordraak: paars lijf, lichtpaars, blauwe randen, geel licht
        'species': {'miraidon': {'body': [5, 2, 6], 'light': [11, 12, 9, 3], 'edges': [7, 8], 'yellow': [4, 14]}},
        'variants': [
            {'naam': 'Koraidon-kleuren (rood, wit en blauw)', 'body': '#d83838', 'light': '#e8e6e2', 'edges': '#1830b1',
             'yellow': '#f0f0f0'},
            {'naam': 'Tron (zwart met cyaan)', 'body': ('#2c2c38', DARK), 'light': '#5a5a74', 'edges': '#40e0f0',
             'yellow': '#40e0f0'},
            {'naam': 'Zilverpijl (zilver met cyaan)', 'body': '#a0a4b0', 'light': '#e0e4ec', 'edges': '#3a3a44',
             'yellow': '#40c0f0'},
            {'naam': 'Synthwave (zuurstokroze)', 'body': '#e04090', 'light': '#f8b0d0', 'edges': '#40e0f0',
             'yellow': '#f0f040'},
            {'naam': 'Groene bliksem', 'body': '#2a8a40', 'light': '#a0e0a0', 'edges': '#f0f040', 'yellow': '#f0f040'},
            {'naam': 'Gouden racer (rode lichten)', 'body': ('#d8a830', GOLD), 'light': '#f8f0d0', 'edges': '#c02028',
             'yellow': '#c02028'},
        ],
    },
    'wo_chien': {
        # Schatten van het Verderf (seizoenen + vloek + brons): bladeren, schelp, hout/tabletten, mos
        'species': {'wo_chien': {'leaves': [5, 9, 1, 10, 15], 'shell': [6, 2, 12], 'wood': [8, 4, 13], 'moss': [7, 3],
                                 'eyes': [11]}},
        'variants': [
            {'naam': 'Herfst (roestrood blad)', 'leaves': '#c05020', 'shell': '#5a4030', 'wood': '#c0a070',
             'moss': '#6a6050', 'eyes': '#f0d040'},
            {'naam': 'Lente (kersenbloesem)', 'leaves': '#f0a0c0', 'shell': '#5a3a3a', 'wood': '#e0c8b0', 'moss': '#a08090',
             'eyes': '#40c060'},
            {'naam': 'Winter (berijpt)', 'leaves': '#d0e0e8', 'shell': '#4a5060', 'wood': '#a8b0c0', 'moss': '#80909a',
             'eyes': '#40a0f0'},
            {'naam': 'Jade en lakwerk', 'leaves': '#40a080', 'shell': '#8a2020', 'wood': '#d0a040', 'moss': '#2c5040',
             'eyes': '#f0d040'},
            {'naam': 'De vloek (zwart met paars)', 'leaves': '#4a2a5a', 'shell': ('#2c2c30', DARK), 'wood': '#5a4a50',
             'moss': '#3a3040', 'eyes': '#c060f0'},
            {'naam': 'Shang-brons (goud met patina)', 'leaves': ('#c08a40', GOLD), 'shell': '#3a6a5a', 'wood': '#4a9a80',
             'moss': '#2c4a40', 'eyes': '#e03030'},
        ],
    },
    'chien_pao': {
        # Schatten van het Verderf: vacht (wit), ijs (blauw), zwaarden (donker), accent
        'species': {'chien_pao': {'fur': [5, 6, 7], 'ice': [4, 9, 1, 3, 2], 'dark': [12, 11], 'accent': [10, 13]}},
        'variants': [
            {'naam': 'Sabeltandtijger (oranje)', 'fur': '#e0a060', 'ice': '#f8f0e0', 'dark': '#3a3030', 'accent': '#f0f0f0'},
            {'naam': 'Zwarte panter met ijs', 'fur': ('#3e3e48', DARK), 'ice': '#60c0e0', 'dark': '#1c1c24',
             'accent': '#60f0f0'},
            {'naam': 'Sneeuwluipaard (grijs, donker ijs)', 'fur': '#c8c4c0', 'ice': '#6a6a70', 'dark': '#2c2c30',
             'accent': '#80c0e0'},
            {'naam': 'Herfsttijger (rood)', 'fur': '#c04830', 'ice': '#f8d0b0', 'dark': '#3a2020', 'accent': '#f0d040'},
            {'naam': 'Bloedige sneeuw (wit met karmozijn)', 'fur': '#f0e8e8', 'ice': '#c02838', 'dark': '#4a1018',
             'accent': '#f04060'},
            {'naam': 'Jadetijger met goud', 'fur': '#80c8a0', 'ice': ('#e0b030', GOLD), 'dark': '#1c4a30',
             'accent': '#c02838'},
        ],
    },
    'ting_lu': {
        # Schatten van het Verderf: schaal (teal), lijf (bruin), rood
        'species': {'ting_lu': {'shell': [5, 2, 11], 'body': [4, 6, 9, 10, 13, 14, 1], 'red': [3, 7, 8]}},
        'variants': [
            {'naam': 'Herfst (oranje schaal)', 'shell': '#c06a20', 'body': '#5a4030', 'red': '#f0d040'},
            {'naam': 'Lente (kersenbloesem)', 'shell': '#e090b0', 'body': '#6a4a40', 'red': '#40a060'},
            {'naam': 'Winter (sneeuwwit)', 'shell': '#d0dce8', 'body': '#6a6070', 'red': '#3070c0'},
            {'naam': 'Jade en lakwerk', 'shell': '#40a080', 'body': '#8a2828', 'red': '#f0c030'},
            {'naam': 'De vloek (paars met zwart)', 'shell': '#4a2a5a', 'body': ('#2c2830', DARK), 'red': '#a050e0'},
            {'naam': 'Shang-brons (goud met patina)', 'shell': ('#c08a40', GOLD), 'body': '#3a5a50', 'red': '#40c0a0'},
        ],
    },
    'chi_yu': {
        # Schatten van het Verderf: vuur (rood en oranje), lijf (groen kraal)
        'species': {'chi_yu': {'red': [2, 1, 3, 8], 'orange': [5, 7, 6], 'body': [11, 9, 14, 12, 10]}},
        'variants': [
            {'naam': 'Lithiumvlam (roze)', 'red': '#c02070', 'orange': '#f080c0', 'body': '#2a3a50'},
            {'naam': 'Groen spookvuur', 'red': '#208040', 'orange': '#80f060', 'body': '#40204a'},
            {'naam': 'Kaliumvlam (paars)', 'red': '#6020a0', 'orange': '#d080f0', 'body': '#205040'},
            {'naam': 'Magnesium (wit vuur)', 'red': '#8a8a98', 'orange': ('#f0f0f8', {'l': 1.2}), 'body': '#3a3a40'},
            {'naam': 'Zwart vuur met rode kraal', 'red': ('#2c2028', DARK), 'orange': '#6a4a5a', 'body': '#c02028'},
            {'naam': 'Chinese gelukskarper (rood, goud, blauw)', 'red': '#c02028', 'orange': ('#f0c030', GOLD),
             'body': '#2050c0'},
        ],
    },
    'dipplin': {
        # appeldraken (eigen recept, Applin & co. zijn van een andere agent): appel, draakje (groen), siroop/crème
        'species': {
            'dipplin': {'apple': [5, 6, 4, 1, 10], 'dragon': [7, 11, 3, 2, 8], 'cream': [9, 13]},
            'hydrapple': {'apple': [6, 8, 5, 2, 11, 7, 9, 15], 'dragon': [10, 13, 4, 3], 'cream': [12, 14]},
        },
        'variants': [
            {'naam': 'Granny Smith (groene appel, rood draakje)', 'apple': '#80c040', 'dragon': '#c04030',
             'cream': '#f0e8a0'},
            {'naam': 'Pink Lady (roze appel)', 'apple': '#f0a0b0', 'dragon': '#5a8a30', 'cream': '#f8f0e0'},
            {'naam': 'Toffee-appel (karamel)', 'apple': '#c07028', 'dragon': '#3a7a30', 'cream': '#f8e0a0'},
            {'naam': 'Zwarte diamant (Tibetaanse appel)', 'apple': ('#3a2840', DARK), 'dragon': '#6a9a40',
             'cream': '#e0c0e0'},
            {'naam': 'De gifappel van Sneeuwwitje (paars)', 'apple': '#7a2a90', 'dragon': '#40c040', 'cream': '#d0f080'},
            {'naam': 'Zilveren appels van de maan (Yeats)', 'apple': ('#d0d4e0', {'l': 1.2}), 'dragon': '#3a7a68',
             'cream': '#e0e8ff'},
        ],
    },
    'poltchageist': {
        # theespoken: thee (matcha), kom/ketel (wit), donker (schaduw), goud/hout
        'species': {
            'poltchageist': {'tea': [10, 2, 11, 12], 'cup': [7, 13, 14], 'dark': [5, 4], 'gold': [8, 15, 1, 3]},
            'sinistcha': {'tea': [6, 7, 3, 10, 12], 'cup': [15, 13], 'gold': [8, 11, 5, 4]},
        },
        'variants': [
            {'naam': 'Hojicha (geroosterde thee)', 'tea': '#a06a38', 'cup': '#f0e8d8', 'dark': '#3a2a24', 'gold': '#c08040'},
            {'naam': 'Sakura-thee (roze)', 'tea': '#f0a0b8', 'cup': '#f8f0f0', 'dark': '#4a3038', 'gold': '#d0b060'},
            {'naam': 'Vlinderbloemthee (blauw)', 'tea': '#3060c0', 'cup': '#f0f0f8', 'dark': '#2a2a40', 'gold': '#c0a0e0'},
            {'naam': 'Earl Grey in Wedgwood-blauw', 'tea': '#c8b090', 'cup': '#a8c0e0', 'dark': '#3a3040', 'gold': '#f0f0f0'},
            {'naam': 'Vermiljoen lakwerk met gifpaarse thee', 'tea': '#7030a0', 'cup': '#c02838', 'dark': '#1c1c22',
             'gold': '#80f040'},
            {'naam': 'Kintsugi (zwarte raku-kom met gouden naden)', 'tea': '#50a040', 'cup': ('#3a3a40', DARK),
             'dark': '#1c1c22', 'gold': ('#f0c030', GOLD)},
        ],
    },
    'okidogi': {
        # de Trouwe Drie (Okidogi, Munkidori, Fezandipiti) in één recept: donker lijf, tweede kleur
        # (groen/blauw/oranje), mochi-ketting (magenta), goud
        'species': {
            'okidogi': {'dark': [3, 6, 1], 'second': [8, 4, 2], 'chain': [7, 10, 5], 'gold': [9]},
            'munkidori': {'dark': [1, 2, 3], 'second': [5, 6, 10], 'chain': [8, 7, 4], 'gold': [11, 12]},
            'fezandipiti': {'dark': [2, 6, 1], 'second': [7, 4, 3], 'chain': [11, 8, 5], 'gold': [10, 9],
                            'white': [12, 14]},
        },
        'variants': [
            {'naam': 'Kibidango (Momotaro: rijstwit en perzik)', 'dark': '#6a5a50', 'second': '#f0e8d0',
             'chain': '#f8a088', 'gold': '#f0d040', 'white': '#f8f0e0'},
            {'naam': 'Pecharunts gifmochi (gifgroen met paars)', 'dark': '#2c3428', 'second': '#a050e0',
             'chain': '#80f040', 'gold': '#f040a0', 'white': '#d0f0c0'},
            {'naam': 'Oni (rode demon, blauwe ketting)', 'dark': '#8a2020', 'second': '#f0c090', 'chain': '#3060d0',
             'gold': '#f0d040', 'white': '#f8f0e0'},
            {'naam': 'Porseleinen wachters (wit en indigo)', 'dark': '#c8c8d0', 'second': '#5a5a68', 'chain': '#2840a0',
             'gold': '#e03030', 'white': '#f8f8ff'},
            {'naam': 'Nachtwacht (indigo met zilver)', 'dark': '#20244a', 'second': '#4060c0', 'chain': '#c8ccd8',
             'gold': '#f0f0f0', 'white': '#c8ccd8'},
            {'naam': 'Gouden schatbewakers (goud en jade)', 'dark': '#3a3020', 'second': '#40a070',
             'chain': ('#e0b030', GOLD), 'gold': '#40c080', 'white': '#f8f0d0'},
        ],
    },
    'ogerpon': {
        # oni-meisje van Kitakami. Basis + drie maskers (Wellspring, Hearthflame, Cornerstone) delen dezelfde
        # zes thema's: blad/cape, donker lijf, hout (riem/stok), bloemen. Het masker (en bij de maskervormen
        # de cape in maskerkleur) blijft staan: dat is wat de vorm is. Tera-vormen overgeslagen.
        'species': {
            'ogerpon': {'leaf': [8, 6, 14, 7, 2], 'dark': [1, 4], 'wood': [5, 10], 'flower': [9, 11]},
            'ogerpon/wellspring': {'leaf': [5, 2], 'dark': [1, 3], 'wood': [4], 'flower': [6, 7]},
            'ogerpon/hearthflame': {'leaf': [8, 3], 'dark': [1, 4], 'wood': [7], 'flower': [9]},
            'ogerpon/cornerstone': {'leaf': [7, 3, 8], 'wood': [6], 'flower': [9, 10]},
        },
        'variants': [
            {'naam': 'Japanse esdoorn (herfst)', 'leaf': '#d86830', 'dark': '#3a2a24', 'wood': '#6a4030',
             'flower': '#f0d040'},
            {'naam': 'Sakura', 'leaf': '#f0a0c0', 'dark': '#4a3038', 'wood': '#8a5a40', 'flower': '#f8f0f0'},
            {'naam': 'Sneeuw op dennen (winterbes)', 'leaf': '#d8e8f0', 'dark': '#3a4048', 'wood': '#7a6a5a',
             'flower': '#e04050'},
            {'naam': 'Ginkgo (goudgeel blad)', 'leaf': '#e8c830', 'dark': '#3a3424', 'wood': '#6a5030', 'flower': '#f08020'},
            {'naam': 'Oni-nacht (paars blad)', 'leaf': '#6a40a0', 'dark': ('#1c1c24', DARK), 'wood': '#4a3040',
             'flower': '#f040a0'},
            {'naam': 'Shuten-dōji (bloedrode oni met goud)', 'leaf': '#a01828', 'dark': '#2c1c1c', 'wood': '#c08a40',
             'flower': ('#f0c030', GOLD)},
        ],
    },
    'archaludon': {
        # stalen brug (eigen recept, Duraludon is van een andere agent): staal (lila), blauw, rood, gele punten
        'species': {'archaludon': {'steel': [10, 12, 7, 8, 9], 'blue': [13, 11, 6, 14], 'red': [4, 1],
                                   'yellow': [5, 3, 15]}},
        'variants': [
            {'naam': 'Golden Gate (oranjerood staal)', 'steel': '#d05030', 'blue': '#3a3a44', 'red': '#f0d040',
             'yellow': '#f0f0f0'},
            {'naam': 'Cortenstaal (roest)', 'steel': '#a06038', 'blue': '#3a2a24', 'red': '#40a0a0', 'yellow': '#e0c070'},
            {'naam': 'Vaporwave-brug (roze en cyaan)', 'steel': '#f0a0c8', 'blue': '#3a90b0', 'red': '#f0f040',
             'yellow': '#ffffff'},
            {'naam': 'Vrijheidsbeeld (kopergroen patina)', 'steel': '#70b8a0', 'blue': '#2a5a50', 'red': '#c08040',
             'yellow': '#f0d040'},
            {'naam': 'Gietijzer met lava', 'steel': '#4a4a54', 'blue': '#1c1c24', 'red': '#f05020', 'yellow': '#f08020'},
            {'naam': 'Cầu Vàng (de Gouden Brug van Đà Nẵng)', 'steel': ('#e0b030', GOLD), 'blue': '#5a4a3a',
             'red': '#c02838', 'yellow': '#f8f8f0'},
        ],
    },
    'terapagos': {
        # tera-schildpad, alle drie de vormen (normaal, Terastal, Stellar): lijf (blauw), kristal (teal/groen),
        # warme accenten
        'species': {
            'terapagos': {'body': [4, 2, 1, 13], 'crystal': [9, 11, 14, 10, 3], 'accent': [5, 6, 7, 8],
                          '_base': {'crystal': 9}},
            'terapagos/terastal': {'body': [5, 4, 6], 'crystal': [10, 12, 11], 'accent': [2, 3, 7, 8, 14, 9]},
            'terapagos/stellar': {'body': [4, 2, 8, 9, 3], 'crystal': [11, 13, 15], 'accent': [7, 14, 12, 6, 5, 10],
                                  '_base': {'crystal': 11}},
        },
        'variants': [
            {'naam': 'Robijn-tera', 'body': '#8a2030', 'crystal': '#f06070', 'accent': '#f0d040'},
            {'naam': 'Smaragd-tera', 'body': '#1c5a40', 'crystal': '#60e0a0', 'accent': '#f080c0'},
            {'naam': 'Amethist-tera', 'body': '#4a2a70', 'crystal': '#c080f0', 'accent': '#f0d040'},
            {'naam': 'Opaal (melkwit met roze glans)', 'body': '#b8bcd0', 'crystal': '#f0c0e0', 'accent': '#40c0f0'},
            {'naam': 'Onyx (zwart met zilverkristal)', 'body': ('#2c2c34', DARK), 'crystal': '#b0b0c8', 'accent': '#f04060'},
            {'naam': 'Zonnekristal (goud op brons)', 'body': '#6a3a20', 'crystal': ('#f0c030', GOLD), 'accent': '#f0f0f0'},
        ],
    },
    'pecharunt': {
        # gifmochi-meester: lijf (paars), schelp (donkergrijs), magenta (randen), roze (perzik)
        'species': {'pecharunt': {'body': [10, 8, 7, 11], 'shell': [2, 5], 'magenta': [4, 14, 3, 6, 15], 'pink': [9]}},
        'variants': [
            {'naam': 'Perzik (momo)', 'body': '#e08070', 'shell': '#5a4038', 'magenta': '#f0c060', 'pink': '#f8d0b0'},
            {'naam': 'Matcha-mochi', 'body': '#4a8a40', 'shell': '#3a3a30', 'magenta': '#e070a0', 'pink': '#d0f0b0'},
            {'naam': 'Bramen en zilver', 'body': '#3a2a5a', 'shell': '#a0a0b0', 'magenta': '#40c0f0', 'pink': '#c0e0f0'},
            {'naam': 'Sakuramochi (roze en wit)', 'body': '#f0a0c0', 'shell': '#e8e8ec', 'magenta': '#c02860',
             'pink': '#ffffff'},
            {'naam': 'Zwart gif (neongroen)', 'body': ('#2c2c34', DARK), 'shell': '#4a4a54', 'magenta': '#80f040',
             'pink': '#c0f080'},
            {'naam': 'Perzik der onsterfelijkheid (Sun Wukong: goud en rood)', 'body': ('#e0b030', GOLD),
             'shell': '#6a2020', 'magenta': '#e03030', 'pink': '#f8f0c0'},
        ],
    },
}
