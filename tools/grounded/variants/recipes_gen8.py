"""Kleurvarianten Gen 8 (Galar). Formaat: zie recipes.py."""

ALBINO = {'l': 1.0}
DARK = {'l': 1.3}
GOLD = {'h': 0}

LINES = {
    'grookey': {
        # drumapen: lijf (Rillaboom: vacht), blad/haar, gezicht, bruin (oren/staart, stok, drumhout),
        # neus/handen (oranje), trommel (Rillaboom)
        'species': {
            'grookey': {'body': [4, 3, 1], 'face': [7, 5], 'brown': [9, 8, 6], 'nose': [14, 15, 13]},
            'thwackey': {'leaf': [3, 1], 'body': [5, 4], 'face': [6, 9, 14], 'brown': [8, 10, 7, 12, 15],
                         'nose': [11, 13]},
            'rillaboom': {'leaf': [3, 2, 1], 'body': [9, 5, 7], 'drum': [13, 6, 12], 'brown': [14, 15],
                          'nose': [10, 11]},
        },
        'variants': [
            {'naam': 'Mandril (olijfgrijs, blauwe snuit, rode neus, gele baard)', 'body': '#706850',
             'leaf': '#d8a830', 'face': '#4080d0', 'brown': '#4a3830', 'nose': '#e02828', 'drum': '#c8b8a0'},
            {'naam': 'Japanse sneeuwaap (grijswit met rood gezicht, sneeuw op de kruin)',
             'body': ('#c8c0b8', {'l': 1.2}), 'leaf': ('#e8f0f8', ALBINO), 'face': '#e05a5a', 'brown': '#6a5a50',
             'nose': '#d04040', 'drum': '#a07858'},
            {'naam': 'Kersenbloesem-bonsai (roze blad, donker hout)', 'body': '#8a6450', 'leaf': '#f0a0c0',
             'face': '#f8e0e0', 'brown': '#4a3028', 'nose': '#e06080', 'drum': '#f0d0d8'},
            {'naam': 'Goudstompneusaap (goudoranje met blauwe snuit)', 'body': '#e09030', 'leaf': '#4a3a30',
             'face': '#70a8e0', 'brown': '#8a4a20', 'nose': '#4070c0', 'drum': '#e8d0a0'},
            {'naam': 'Taiko no Tatsujin (Don-chan rood, Katsu-chan blauw)', 'body': '#d03030', 'leaf': '#3060d0',
             'face': '#f8f0e0', 'brown': '#3a2a28', 'nose': '#f0d040', 'drum': '#f8f0e0'},
            {'naam': 'Sun Wukong (de Apenkoning: goud met rood)', 'body': ('#e0b030', GOLD), 'leaf': '#c02828',
             'face': '#f8e0c0', 'brown': '#c02828', 'nose': '#e8a070', 'drum': '#c02828'},
        ],
    },
    'scorbunny': {
        # voetbalkonijnen: vacht, vuur (oren/voeten, Raboots trui, Cinderaces broek), geel (neus/oren),
        # shirt (Cinderace), broek (Raboot)
        'species': {
            'scorbunny': {'fur': [7, 6, 8], 'fire': [2, 3, 12, 1], 'yellow': [5, 9, 11]},
            'raboot': {'fur': [4, 2, 1], 'fire': [8, 9, 10], 'yellow': [5, 6], 'pants': [12, 13, 11]},
            'cinderace': {'fur': [4, 3, 1], 'fire': [8, 7, 9], 'yellow': [5, 10, 6, 14], 'shirt': [12, 13]},
        },
        'variants': [
            {'naam': 'Oranjegekte (Nederlands elftal: oranje, wit en blauw)', 'fur': '#f08a30', 'fire': '#2850b0',
             'yellow': '#f8f8f8', 'shirt': '#f8f8f8', 'pants': '#f0f0f0'},
            {'naam': 'Seleção canarinho (Brazilië: geel, groen, blauw)', 'fur': '#f0d040', 'fire': '#30a050',
             'yellow': '#2850c0', 'shirt': '#2850c0', 'pants': '#2850c0'},
            {'naam': 'Veldhaas (agouti met zwarte oorpunten)', 'fur': '#a88a68', 'fire': ('#3a2a24', DARK),
             'yellow': '#f0e0c0', 'shirt': '#f0e8d8', 'pants': '#5a4a38'},
            {'naam': 'Spookvuur (zwart konijn, cyaan vlammen)', 'fur': ('#4a4a58', DARK), 'fire': '#40d0f0',
             'yellow': '#c0f8ff', 'shirt': '#283050', 'pants': ('#20202a', DARK)},
            {'naam': 'Bugs Bunny (grijs met roze oren)', 'fur': '#9898a8', 'fire': '#f0a0b8', 'yellow': '#f8f8f8',
             'shirt': '#f8f8f8', 'pants': '#7a7a88'},
            {"naam": "Ballon d'Or (goud, witheet vuur, zwart tenue)", 'fur': ('#e0b030', GOLD), 'fire': '#f8f0d0',
             'yellow': '#f8f8f8', 'shirt': ('#2a2a30', DARK), 'pants': ('#2a2a30', DARK)},
        ],
    },
    'sobble': {
        # kameleon-spionnen: lijf, vin (kop), strepen, buik, handen (Drizzile), jas (Inteleon), oog
        'species': {
            'sobble': {'body': [9, 6, 5, 7], 'fin': [2, 3], 'stripe': [4, 1], 'belly': [12, 13, 8]},
            'drizzile': {'body': [5, 8, 6, 7], 'fin': [4, 3], 'stripe': [2, 1], 'belly': [12, 11],
                         'hands': [14, 9, 13]},
            'inteleon': {'body': [7, 8, 1, 5, 6], 'fin': [3, 4, 2], 'coat': [14, 13, 12], 'eye': [10]},
        },
        'variants': [
            {'naam': 'Pantherkameleon (rood met turquoise strepen)', 'body': '#d04030', 'fin': '#40c8c0',
             'stripe': '#2050a0', 'belly': '#f0d060', 'hands': '#40c0a0', 'coat': '#2a3a60', 'eye': '#f0d040'},
            {'naam': 'James Bond (smoking: zwart, wit overhemd, rode anjer)', 'body': ('#4a4e60', DARK),
             'fin': '#f0f0f0', 'stripe': '#c02828', 'belly': '#f8f8f8', 'hands': '#c02828',
             'coat': ('#26262c', DARK), 'eye': '#c02828'},
            {'naam': 'Jackson-kameleon (groen met gele kam)', 'body': '#40a040', 'fin': '#f0d030', 'stripe': '#1a5a30',
             'belly': '#c8e8a0', 'hands': '#3060c0', 'coat': '#5a4a30', 'eye': '#e03030'},
            {'naam': 'Axolotl (leucistisch roze, magenta kieuwen)', 'body': '#f0b0c0', 'fin': '#e04080',
             'stripe': '#c06080', 'belly': '#fff0f0', 'hands': '#e04080', 'coat': '#7a4a5a', 'eye': '#3a3a48'},
            {'naam': 'Ghillie-sluipschutter (camouflage)', 'body': '#6a7040', 'fin': '#8a7a50', 'stripe': '#3a4028',
             'belly': '#b0a878', 'hands': '#4a5a30', 'coat': '#4a4030', 'eye': '#e04020'},
            {'naam': 'Goldfinger (goud met zwart en rood)', 'body': ('#e0b030', GOLD), 'fin': '#f8f8f0',
             'stripe': '#a06a10', 'belly': '#f8f0c8', 'hands': '#c02828', 'coat': ('#2a2a30', DARK),
             'eye': '#c02828'},
        ],
    },
    'skwovet': {
        # eekhoorns: lijf (Greedent: roze vacht), staart (Greedent: staart en buik), lichte vacht/tanden,
        # wangen/neus
        'species': {
            'skwovet': {'body': [7, 6, 5], 'tail': [4, 3, 1], 'light': [10, 11, 12], 'cheek': [9, 8]},
            'greedent': {'body': [3, 4, 2], 'tail': [7, 6, 5], 'light': [11, 10, 13, 12], 'cheek': [9, 8]},
        },
        'variants': [
            {'naam': 'Grijze eekhoorn (grijs met zilveren staart)', 'body': '#8a8a90', 'tail': '#b8b8c0',
             'light': '#f0f0f0', 'cheek': '#c08060'},
            {'naam': 'Zwarte eekhoorn (melanistisch, oranje wangen)', 'body': ('#3a3438', DARK),
             'tail': ('#2a2628', DARK), 'light': '#8a8090', 'cheek': '#e07030'},
            {'naam': 'Indische reuzeneekhoorn (kastanjepaars, crème buik)', 'body': '#7a2848', 'tail': ('#2a1a24', DARK),
             'light': '#f0d8a8', 'cheek': '#f0a040'},
            {'naam': 'Albino (wit met roze)', 'body': ('#f0ece8', ALBINO), 'tail': ('#e8e0e0', ALBINO),
             'light': '#ffffff', 'cheek': '#f090a0'},
            {'naam': 'Ratatoskr (de bemoste eekhoorn uit Yggdrasil)', 'body': '#6a8048', 'tail': '#4a5a30',
             'light': '#d8e0b0', 'cheek': '#e0c040'},
            {'naam': 'Dagobert Duck (een geldpakhuis vol goud)', 'body': ('#e0b030', GOLD), 'tail': '#a87018',
             'light': '#f8f0c8', 'cheek': '#e04040'},
        ],
    },
    'rookidee': {
        # kraaien en ridders: verenkleed/harnas, kop/vleugels (olijf), buik (Rookidee geel), poten, oog
        'species': {
            'rookidee': {'body': [9, 4, 3], 'head': [2, 1], 'belly': [15, 14], 'legs': [5, 13, 11],
                         'eye': [10, 6]},
            'corvisquire': {'body': [5, 4, 3, 14], 'head': [2, 6, 1], 'legs': [11, 12], 'eye': [9, 8, 13]},
            'corviknight': {'body': [6, 1, 2, 5, 4, 10, 11, 12], 'legs': [9, 13], 'eye': [8, 7]},
        },
        'variants': [
            {'naam': 'Ekster (zwart met wit en blauwgroene glans)', 'body': ('#30343c', DARK), 'head': '#2a8080',
             'belly': '#f0f0f0', 'legs': '#3a3a40', 'eye': '#f0d040', 'corviknight:body': ('#24504e', DARK)},
            {'naam': 'Koperen harnas (koper met turquoise patina)', 'body': '#b06a3a', 'head': '#40a090',
             'belly': '#f0c890', 'legs': '#5a3a28', 'eye': '#40e0d0'},
            {'naam': 'Witte raaf (leucistisch, blauwe ogen)', 'body': ('#dce0ea', ALBINO), 'head': '#a0a8b8',
             'belly': '#f8f8f8', 'legs': '#8a8a98', 'eye': '#3080e0'},
            {'naam': 'Rode Ridder (karmijn met gouden ogen)', 'body': '#8a2030', 'head': '#3a1a20', 'belly': '#e0b040',
             'legs': '#3a2a2a', 'eye': '#f0c030'},
            {'naam': 'Glansspreeuw (Lamprotornis: smaragd en paars)', 'body': '#2a7a6a', 'head': '#5a3a8a',
             'belly': '#f08030', 'legs': '#2a2a30', 'eye': '#f08020'},
            {'naam': 'Odins raven Huginn en Muninn (gouden harnas)', 'body': ('#d8a830', GOLD), 'head': '#3050a0',
             'belly': '#f8f0d0', 'legs': '#6a4a20', 'eye': '#e02020'},
        ],
    },
    'blipbug': {
        # kevers en ufo's: schild (Blipbug: buik), stippen (Blipbug: lijf), gezicht, ogen
        'species': {
            'blipbug': {'shell': [9, 10, 12, 13, 11], 'spots': [3, 2, 1]},
            'dottler': {'shell': [6, 2, 7, 5, 14, 4], 'spots': [3, 1], 'face': [13, 9, 10], 'eye': [11, 12]},
            'orbeetle': {'shell': [4, 3, 1], 'spots': [5, 2], 'face': [9, 7, 10], 'eye': [15, 14]},
        },
        'variants': [
            {'naam': 'Zwart lieveheersbeestje (Exochomus: zwart met rode stippen)', 'shell': ('#34343c', DARK),
             'spots': '#d02828', 'face': '#f0e0a0', 'eye': '#40e0f0'},
            {'naam': 'Juweelkever (smaragd met goud)', 'shell': '#30a060', 'spots': '#d8b040', 'face': '#f08030',
             'eye': '#f040a0'},
            {'naam': 'Mars Attacks! (roze breinen, groene marsmannetjes)', 'shell': '#e8a0c0', 'spots': '#40b040',
             'face': '#50c050', 'eye': '#ff3030'},
            {'naam': 'Delfts blauw (wit porselein met blauwe stippen)', 'shell': ('#f0f0f0', ALBINO),
             'spots': '#2850a8', 'face': '#5a80c8', 'eye': '#2850a8'},
            {'naam': 'Tweeëntwintigstippelig lieveheersbeestje (citroengeel met zwart)', 'shell': '#f0e040',
             'spots': ('#2c2c34', DARK), 'face': '#f8f8f8', 'eye': '#e03030'},
            {'naam': 'Fabergé-ei (goud met robijn en saffier)', 'shell': ('#e0b030', GOLD), 'spots': '#c02040',
             'face': '#3060d0', 'eye': '#40f0d0'},
        ],
    },
    'nickit': {
        # vossen en dieven: vacht, donkere poten/snor, lichte vacht, ogen
        'species': {
            'nickit': {'body': [4, 6, 5], 'dark': [2, 1], 'light': [7, 8], 'eye': [9]},
            'thievul': {'body': [4, 6, 5], 'dark': [2, 1], 'light': [7, 8], 'eye': [9]},
        },
        'variants': [
            {'naam': 'Fennek (zandkleurig)', 'body': '#d8b080', 'dark': '#6a4a30', 'light': '#f8f0e0',
             'eye': '#5a3018'},
            {'naam': 'De Roze Panter (de diamant uit de film)', 'body': '#e070a0', 'dark': '#3a3a48',
             'light': '#f8f0f0', 'eye': '#f0c030'},
            {'naam': 'Kitsune (witte vos met rode markering)', 'body': ('#f0ece8', ALBINO), 'dark': '#c02020',
             'light': '#f8f0f0', 'eye': '#c02020'},
            {'naam': 'Melanistische vos (zwart met gouden ogen)', 'body': ('#3a3640', DARK),
             'dark': ('#1e1c22', DARK), 'light': '#9090a0', 'eye': '#f0c030'},
            {'naam': 'Aladdin (straatrat: paars vest, rode fez)', 'body': '#7a4a98', 'dark': '#c02828',
             'light': '#f0e0c0', 'eye': '#f0d040'},
            {'naam': 'Goudroof bij Gringotts (goud, zwarte poten, robijnen ogen)', 'body': ('#e0b030', GOLD),
             'dark': ('#2a2a30', DARK), 'light': '#f8f0c8', 'eye': '#c02028'},
        ],
    },
    'gossifleur': {
        # bloemen en katoen: bloemblaadjes (Eldegoss: bloem), rok (rood blad), groen blad, katoen, gezicht
        'species': {
            'gossifleur': {'petals': [2, 4, 5, 1], 'skirt': [9, 8, 7], 'leaves': [10, 11, 14], 'face': [6, 13, 12]},
            'eldegoss': {'cotton': [15, 3, 4, 2, 1], 'leaves': [5, 6, 9, 13, 14], 'petals': [12, 11, 10],
                         'face': [8]},
        },
        'variants': [
            {'naam': 'Korenbloem (blauw met paars)', 'petals': '#4070d8', 'skirt': '#5a3a90', 'leaves': '#3a8a50',
             'cotton': '#b8c8f0', 'face': '#f8f0d8'},
            {'naam': 'Hibiscus (Hawaï: rood met geel)', 'petals': '#e02840', 'skirt': '#f0c020', 'leaves': '#2a8a40',
             'cotton': '#f8e8a0', 'face': '#f8e8c0'},
            {'naam': 'Lavendelvelden van de Provence', 'petals': '#a080d0', 'skirt': '#6a4a90', 'leaves': '#7a9a70',
             'cotton': '#e0d0f0', 'face': '#f0e8f8'},
            {'naam': 'De zwarte tulp (Dumas en de tulpenmanie)', 'petals': ('#3a2440', DARK), 'skirt': '#7a2a4a',
             'leaves': '#3a6a3a', 'cotton': ('#4a3a58', DARK), 'face': '#c8a0d0'},
            {'naam': 'Suikerspin (kermis: roze en lichtblauw)', 'petals': '#f0a0c8', 'skirt': '#70b0f0',
             'leaves': '#a0e0c0', 'cotton': '#f8a8d0', 'face': '#fff0f8'},
            {'naam': 'Repelsteeltje (stro tot goud gesponnen)', 'petals': ('#e0b030', GOLD), 'skirt': '#c03030',
             'leaves': '#a08040', 'cotton': ('#e8c040', GOLD), 'face': '#f8f0d0'},
        ],
    },
    'wooloo': {
        # schapen: wol, gezicht/lijf (Dubwool grijs), poten/hoeven, hoorns (Dubwool), ogen, neus
        'species': {
            'wooloo': {'wool': [2, 4, 3, 1], 'face': [6, 9, 5, 15], 'legs': [10, 12, 8], 'eye': [11], 'nose': [13]},
            'dubwool': {'wool': [7, 8, 10, 5], 'face': [9, 6, 4], 'horn': [3, 1], 'legs': [12, 11], 'eye': [13],
                        'nose': [15], '_base': {'wool': 7}},
        },
        'variants': [
            {'naam': 'Drents heideschaap (strokleurige wol)', 'wool': '#c0a070', 'face': '#5a4838', 'legs': '#8a7a6a',
             'horn': '#d8c8a0', 'eye': '#e0d030', 'nose': '#c08070'},
            {'naam': 'Geverfd Schots heuvelschaap (felroze wol)', 'wool': '#f0a0c8', 'face': '#3a3038',
             'legs': '#6a5a68', 'horn': '#f0e0d0', 'eye': '#40b0e0', 'nose': '#e05080'},
            {'naam': 'Herdwick (leigrijze wol, witte kop)', 'wool': '#6a7480', 'face': '#e8e4e0',
             'legs': '#c8c4c0', 'horn': '#f0e8d0', 'eye': '#e09030', 'nose': '#d08080'},
            {'naam': 'Schaapjes tellen (nachtblauwe slaapwol, maangele ogen)', 'wool': '#8898d8', 'face': '#283058',
             'legs': '#404a78', 'horn': '#c8c8e8', 'eye': '#f0e040', 'nose': '#c080d0'},
            {'naam': 'Chia Pet (een schaap waar kiemgroen uit groeit)', 'wool': '#88c050', 'face': '#7a5030',
             'legs': '#a07850', 'horn': '#5a3a20', 'eye': '#f0e040', 'nose': '#e07060'},
            {'naam': 'Het Gulden Vlies (Jason en de Argonauten)', 'wool': ('#e8c040', GOLD), 'face': '#6a4020',
             'legs': '#8a6030', 'horn': '#f8f0d0', 'eye': '#e03030', 'nose': '#e08060'},
        ],
    },
    'chewtle': {
        # bijtschildpadden: hoorn, lijf (huid), schild, kaak/buik
        'species': {
            'chewtle': {'horn': [2, 4, 1], 'body': [6, 5, 3], 'shell': [13, 9, 10, 11, 12], 'jaw': [14, 15]},
            'drednaw': {'horn': [5, 3, 1, 4], 'body': [9, 12, 11, 10], 'shell': [8, 7, 6], 'jaw': [14, 15]},
        },
        'variants': [
            {'naam': 'Alligatorschildpad (modderolijf)', 'body': '#6a6a48', 'horn': '#a08a50', 'shell': '#3a3428',
             'jaw': '#c0b080'},
            {'naam': 'Karetschildpad (crème huid, amber schild)', 'body': '#d8c8a0', 'horn': '#3a3028',
             'shell': '#d08028', 'jaw': '#f8f0d8'},
            {'naam': 'Bowser (gele huid, groen schild, rood haar)', 'body': '#e8b040', 'horn': '#e03020',
             'shell': '#30a040', 'jaw': '#f8f0d0'},
            {'naam': 'Lavaschildpad (zwart gesteente, gloeiend rood)', 'body': ('#3a3036', DARK), 'horn': '#f05020',
             'shell': '#5a2018', 'jaw': '#f09040'},
            {'naam': 'Amethistschildpad (paars kristal)', 'body': '#9070c0', 'horn': '#e0c0f0', 'shell': '#4a2a6a',
             'jaw': '#e8d8f0'},
            {'naam': 'Kim Quy (de gouden schildpad uit de Vietnamese legende)', 'body': ('#d8b040', GOLD),
             'horn': '#c02828', 'shell': '#6a4a10', 'jaw': '#f8f0c8'},
        ],
    },
    'yamper': {
        # stroomhonden: vacht (Boltund: donker lijf), geel (bliksem), wit, tong, ogen
        'species': {
            'yamper': {'fur': [3, 4, 1], 'yellow': [7, 10, 11], 'white': [5, 6, 13], 'tongue': [12, 15],
                       'eye': [9, 8]},
            'boltund': {'fur': [9, 13, 15], 'yellow': [1, 3, 2, 8, 10, 7], 'white': [6, 11, 4], 'eye': [14]},
        },
        'variants': [
            {'naam': 'Shiba Inu (Doge: rossig met crème, rode bliksem)', 'fur': '#d88838', 'yellow': '#e04030',
             'white': '#f8f0e0', 'tongue': '#f08098', 'eye': '#3a2a20'},
            {'naam': 'Husky (grijs met ijsblauwe bliksem)', 'fur': '#707888', 'yellow': '#a0e0f8', 'white': '#f8f8f8',
             'tongue': '#f090a8', 'eye': '#40a0f0'},
            {'naam': '101 Dalmatiërs (wit met zwart)', 'fur': ('#e8e8e8', ALBINO), 'yellow': ('#2a2a30', DARK),
             'white': '#ffffff', 'tongue': '#f07090', 'eye': '#3a3a40'},
            {'naam': 'Scooby-Doo (bruin, blauwe halsband)', 'fur': '#a06830', 'yellow': '#3060c0', 'white': '#e0c8a0',
             'tongue': '#e06080', 'eye': '#f0d040'},
            {'naam': 'Tron (zwart met neoncyaan)', 'fur': ('#2c2c38', DARK), 'yellow': '#40e8f8', 'white': '#606880',
             'tongue': '#40e8f8', 'eye': '#40e8f8'},
            {'naam': 'Laika (de ruimtehond: nachtblauw met sterrengoud)', 'fur': ('#2a3060', DARK),
             'yellow': '#e0e8ff', 'white': '#a0a8d0', 'tongue': '#f0a0c0', 'eye': '#f0d040'},
        ],
    },
    'rolycoly': {
        # kolen: steen/kar (grijs), kool (zwart), gloed, (Rolycoly: oog)
        'species': {
            'rolycoly': {'stone': [1, 4, 3, 2], 'coal': [6, 9, 5, 7], 'ember': [12, 10]},
            'carkol': {'coal': [1, 4, 2, 3], 'ember': [5, 7], 'stone': [9, 10, 11, 13, 8]},
            'coalossal': {'coal': [4, 1, 3, 2], 'ember': [10, 11, 12, 13], 'stone': [7, 8, 9, 5, 14]},
        },
        'variants': [
            {'naam': 'Zwavel (geel met blauwe vlam)', 'stone': '#c8b040', 'coal': '#5a5020', 'ember': '#40a0f0'},
            {'naam': 'Kopermijn (malachiet met koperen gloed)', 'stone': '#40a070', 'coal': '#2a3a30',
             'ember': '#f08030'},
            {'naam': 'Hematiet (roestrood met gele gloed)', 'stone': '#8a4030', 'coal': '#3a2020', 'ember': '#f0d040'},
            {'naam': 'Diamant (kool onder druk: wit met ijsblauw vuur)', 'stone': ('#d8e8f0', ALBINO),
             'coal': '#5a7088', 'ember': '#40e0f0'},
            {'naam': 'Amethistgeode (paars met roze gloed)', 'stone': '#8060a8', 'coal': '#3a2848', 'ember': '#f060c0'},
            {'naam': 'Goudader (goud, witheet)', 'stone': ('#d8a830', GOLD), 'coal': '#4a3010', 'ember': '#f8f8f0'},
        ],
    },
    'applin': {
        # appeldraken: appel (Flapple: vleugels, Appletun: kop), groen (draak/lijf), taart/vruchtvlees
        'species': {
            'applin': {'apple': [10, 7, 9, 6, 8], 'green': [3, 2, 1], 'pie': [11, 12, 13]},
            'flapple': {'apple': [9, 2, 1, 13], 'green': [11, 5, 4], 'pie': [8, 10, 6, 7, 15, 12]},
            'appletun': {'apple': [4, 1, 12, 13], 'green': [6, 2, 5, 11], 'pie': [9, 7, 8, 10]},
        },
        'variants': [
            {'naam': 'Toffee-appel (karamel, kermis)', 'apple': '#c87830', 'green': '#7a4a28', 'pie': '#f0e0b0'},
            {'naam': 'Arkansas Black (bijna zwarte appel)', 'apple': ('#4a1a2a', DARK), 'green': '#2a5a30',
             'pie': '#d08040'},
            {'naam': 'Pink Lady (roze appel, lichtgroen blad)', 'apple': '#f080a8', 'green': '#90c060',
             'pie': '#f8e0c8'},
            {'naam': 'Gifappel van Sneeuwwitje (paars met gifgroen)', 'apple': '#7a3a9a', 'green': '#60e040',
             'pie': '#3a2a40'},
            {'naam': 'IJsappel (bevroren: ijsblauw)', 'apple': '#90b8f0', 'green': '#e0f0f8', 'pie': '#f0f8ff'},
            {'naam': 'Twistappel van Eris (goud met zilverblad)', 'apple': ('#e0b030', GOLD), 'green': '#c8d0d8',
             'pie': '#f8e8b0'},
        ],
    },
    'silicobra': {
        # zandslangen: lijf, licht (snuit/buik), zand(zak)/kraag, ogen
        'species': {
            'silicobra': {'body': [1, 4, 2], 'sand': [7, 8, 12], 'light': [6, 3, 5, 14, 13], 'eye': [11, 9]},
            'sandaconda': {'body': [1, 2, 4], 'sand': [5, 6], 'light': [10, 9, 7, 8], 'eye': [12, 11]},
        },
        'variants': [
            {'naam': 'Oase (turquoise water en palmgroen)', 'body': '#40a090', 'light': '#e8e0c0', 'sand': '#2a6060',
             'eye': '#f0c030'},
            {'naam': 'White Sands (witte gipswoestijn)', 'body': ('#e8e4dc', ALBINO), 'light': '#ffffff',
             'sand': '#b0a898', 'eye': '#e04040'},
            {'naam': 'Zwart vulkaanzand (IJsland)', 'body': ('#3a3a40', DARK), 'light': '#8a8a90',
             'sand': ('#1e1e24', DARK), 'eye': '#f0c030'},
            {'naam': 'Roze strand van Bermuda', 'body': '#e0a0a0', 'light': '#f8e0e0', 'sand': '#a05060',
             'eye': '#40b0e0'},
            {'naam': 'Shai-Hulud (Dune: okerkleurige zandworm, blauwe spice-ogen)', 'body': '#c08040',
             'light': '#e8c890', 'sand': '#6a3a20', 'eye': '#3080f0'},
            {'naam': 'Uraeus van de farao (goud en lapis lazuli)', 'body': ('#d8a830', GOLD), 'light': '#f8f0d0',
             'sand': '#2850a0', 'eye': '#e02020'},
        ],
    },
    'cramorant': {
        # zeevogels: verenkleed, buik, oog, poten. De snavel blijft geel: in de Gulping- en Gorging-vorm
        # delen Arrokuda en Pikachu de snavelindexen.
        'species': {
            'cramorant': {'body': [2, 3, 1], 'belly': [11, 12, 10], 'eye': [6, 9], 'legs': [13, 14]},
            'cramorant/gorging': {'body': [8, 9, 5], 'belly': [11, 12, 10], 'eye': [6], 'legs': [13, 7]},
            'cramorant/gulping': {'body': [10, 11, 6], 'belly': [7, 13, 12], 'eye': [9, 8], 'legs': [14, 15]},
        },
        'variants': [
            {'naam': 'Bruine pelikaan (grijsbruin, crème buik)', 'body': '#8a8278', 'belly': '#f0e8c8',
             'eye': '#f0f0f0', 'legs': '#3a3a3a'},
            {'naam': 'Roze pelikaan', 'body': '#f0b0c0', 'belly': '#fff0f0', 'eye': '#e04060', 'legs': '#e08080'},
            {'naam': 'Blauwvoetgent (bruin, felblauwe poten)', 'body': '#8a6040', 'belly': '#f8f8f8',
             'eye': '#f0e040', 'legs': '#40a0f0'},
            {'naam': 'Jan-van-gent (wit, ijsblauwe ogen)', 'body': ('#e8ecf0', ALBINO), 'belly': '#f8f8f8',
             'eye': '#60a0e0', 'legs': '#4a4a50'},
            {'naam': 'Fregatvogel (zwart met rode keelzak)', 'body': ('#303038', DARK), 'belly': '#e02020',
             'eye': '#60c0f0', 'legs': ('#202024', DARK)},
            {'naam': 'De gans met de gouden eieren', 'body': ('#e0b030', GOLD), 'belly': '#f8f0c0', 'eye': '#c02020',
             'legs': '#e08020'},
        ],
    },
    'arrokuda': {
        # snoeken en barracuda's: rug, buik, gele vin (Barraskewda: staart/onderkant), rode vinnen
        'species': {
            'arrokuda': {'body': [4, 5, 10], 'belly': [9, 7, 8], 'yellow': [6, 3, 1], 'red': [13, 14]},
            'barraskewda': {'body': [2, 7, 1, 12], 'belly': [8, 9], 'yellow': [11, 10], 'red': [4, 3, 6]},
        },
        'variants': [
            {'naam': 'Snoek (olijfgroen met gele vlekken)', 'body': '#6a7a40', 'belly': '#e8e0b0', 'yellow': '#d8c040',
             'red': '#d06030'},
            {'naam': 'Zilveren barracuda (zilvergrijs, zwarte vinnen)', 'body': '#8a9098', 'belly': '#f0f0f0',
             'yellow': '#c8d0d8', 'red': ('#2a2a30', DARK)},
            {'naam': 'Kohaku-koi (rood en wit)', 'body': '#e03828', 'belly': '#f8f8f8', 'yellow': '#f8f0f0',
             'red': '#f8f8f8'},
            {'naam': 'Goudmakreel (mahi-mahi: smaragd en geel)', 'body': '#30a060', 'belly': '#f0e040',
             'yellow': '#40c0e0', 'red': '#3070c0'},
            {'naam': 'Diepzeeroofvis (zwart met cyaan licht)', 'body': ('#2a2c38', DARK), 'belly': '#5a6080',
             'yellow': '#40f0e0', 'red': '#40f0e0'},
            {'naam': 'Aziatische arowana (de gouden geluksdraakvis)', 'body': ('#d8a830', GOLD), 'belly': '#f8f0c8',
             'yellow': '#e04030', 'red': '#e04030'},
        ],
    },
    'toxel': {
        # punkrockers: lijf (paars), buik (Toxel), stroom (Amped: geel, Low Key: lichtblauw; eigen kleur
        # per vorm), roze strepen, Toxels stekels
        'species': {
            'toxel': {'body': [4, 2, 1, 5], 'belly': [6, 7], 'spikes': [12, 10, 11], 'spark': [13]},
            'toxtricity': {'body': [7, 6, 4], 'spark': [2, 1, 3, 11], 'pink': [5, 12]},
            'toxtricity/low_key': {'body': [7, 5, 1], 'spark': [4, 3, 6, 11], 'pink': [2, 12]},
        },
        'variants': [
            {'naam': 'Iron Maiden (Eddie: grauw grijs met vuur)', 'body': '#7a8494', 'belly': '#d8d0c0',
             'spikes': '#4a5060', 'spark': '#f06020', 'toxtricity/low_key:spark': '#f0c040', 'pink': '#c03030'},
            {'naam': 'Ziggy Stardust (bleek met rode bliksemflits)', 'body': '#e0d8e8', 'belly': '#f8f8f8',
             'spikes': '#e06030', 'spark': '#e02828', 'toxtricity/low_key:spark': '#3080e0', 'pink': '#3080e0'},
            {'naam': 'Blauwe pijlgifkikker (kobalt met geel)', 'body': '#2058c8', 'belly': '#a0c8f0',
             'spikes': '#202838', 'spark': '#f0d830', 'toxtricity/low_key:spark': '#40e0f0', 'pink': '#202838'},
            {"naam": "Toxic (Britney Spears: gifgroen met magenta)", 'body': '#30a050', 'belly': '#d0f0c0',
             'spikes': '#e040c0', 'spark': '#e040c0', 'toxtricity/low_key:spark': '#c0f040', 'pink': '#e040c0'},
            {'naam': 'Hatsune Miku (turkoois met roze)', 'body': '#40b8b8', 'belly': '#f0f0f0', 'spikes': '#f070b0',
             'spark': '#f070b0', 'toxtricity/low_key:spark': '#c0f0f0', 'pink': '#f070b0'},
            {'naam': 'Daft Punk (zwart pak, gouden en zilveren helm)', 'body': ('#2c2c34', DARK),
             'belly': '#c8c8d0', 'spikes': '#d8a830', 'spark': ('#e0b030', GOLD),
             'toxtricity/low_key:spark': ('#d8dce4', ALBINO), 'pink': '#e02828'},
        ],
    },
    'sizzlipede': {
        # vuurduizendpoten: lijf (rood), vuur, donkere poten/segmenten
        'species': {
            'sizzlipede': {'red': [2, 4, 1], 'fire': [5, 8, 9], 'dark': [6, 7]},
            'centiskorch': {'red': [7, 8, 6, 10], 'fire': [1, 3, 2, 14, 13], 'dark': [4, 5, 9, 12, 15]},
        },
        'variants': [
            {'naam': 'Reuzenduizendpoot (Scolopendra: zwart met oranje poten)', 'red': ('#30303a', DARK),
             'fire': '#f08020', 'dark': '#c06020'},
            {'naam': 'Groen vuur (koper in de vlam)', 'red': '#40a050', 'fire': '#80f060', 'dark': '#2a3a28'},
            {'naam': 'Paarse lava', 'red': '#8040b0', 'fire': '#f060e0', 'dark': '#2a1a38'},
            {'naam': 'Witheet (geelwit vuur)', 'red': '#f0e0a0', 'fire': '#ffffff', 'dark': '#8a6a40'},
            {'naam': 'Zwavel van de Kawah Ijen (geel met blauw vuur)', 'red': '#e8d040', 'fire': '#40a0f0',
             'dark': '#5a5020'},
            {'naam': 'Hemelse drakendans (goud met jadegroen vuur)', 'red': ('#e0b030', GOLD), 'fire': '#40d0a0',
             'dark': '#6a2020'},
        ],
    },
    'clobbopus': {
        # vechtoctopussen: lijf, accent (Clobbopus oranje, Grapploct geel gezicht), donkere armen, oog
        'species': {
            'clobbopus': {'body': [12, 1, 2, 13], 'accent': [6, 5, 4], 'dark': [8, 7, 9], 'eye': [10, 11]},
            'grapploct': {'body': [4, 2, 1, 5], 'accent': [9, 8, 7], 'dark': [14, 11, 10], 'eye': [12, 6]},
        },
        'variants': [
            {'naam': 'Blauwgeringde octopus (geel met blauwe ringen)', 'body': '#e8c840', 'accent': '#2060e0',
             'dark': '#5a4020', 'eye': '#2060e0'},
            {'naam': 'Ursula (De kleine zeemeermin: lila met zwart)', 'body': '#9060c0', 'accent': '#e050a0',
             'dark': ('#2a2030', DARK), 'eye': '#f0d040'},
            {'naam': 'Dumbo-octopus (diepzeeroze)', 'body': '#f0a0b8', 'accent': '#c05080', 'dark': '#5a3050',
             'eye': '#3a3a48'},
            {'naam': 'Judo (witte gi, zwarte band)', 'body': ('#f0f0f0', ALBINO), 'accent': ('#2a2a2a', DARK),
             'dark': ('#2a2a2a', DARK), 'eye': '#c02020'},
            {'naam': 'Akuma (Street Fighter: donker met rood)', 'body': ('#3a3a48', DARK), 'accent': '#d02828',
             'dark': ('#1e1e26', DARK), 'eye': '#f04040'},
            {'naam': 'Kampioensriem (goud met rood)', 'body': ('#d8a830', GOLD), 'accent': '#c02828',
             'dark': '#3a2a10', 'eye': '#40c0f0'},
        ],
    },
    'sinistea': {
        # theeservies (echte en namaakvorm delen het palet): gouden rand, porselein, sierrand, bloemetjes, thee
        'species': {
            'sinistea': {'gold': [4, 3, 1], 'porcelain': [5], 'trim': [6, 7], 'flowers': [9, 10],
                         'tea': [13, 11, 12, 14, 15, 8]},
            'polteageist': {'gold': [1, 4], 'porcelain': [13, 7, 3], 'trim': [14, 10], 'flowers': [11, 12],
                            'tea': [9, 8, 6, 5]},
        },
        'variants': [
            {'naam': 'Japanse theeceremonie (raku-bruin, matcha)', 'porcelain': '#8a6040', 'trim': '#3a2818',
             'gold': '#c8b090', 'flowers': '#f0f0e0', 'tea': '#80c040'},
            {'naam': 'Delfts blauw (wit met blauw, amberkleurige Earl Grey)', 'porcelain': ('#f4f4f8', ALBINO),
             'trim': '#2850a8', 'flowers': '#2850a8', 'gold': '#c8d0e0', 'tea': '#c87830'},
            {'naam': 'Rozenbottelthee (crème porselein, robijnrode thee)', 'porcelain': '#f8f0e0', 'trim': '#c04070',
             'flowers': '#70b050', 'gold': '#e0b040', 'tea': '#c02040'},
            {'naam': 'Chai in een kulhad (terracotta, melkthee)', 'porcelain': '#c07050', 'trim': '#7a3a20',
             'flowers': '#f0d040', 'gold': '#e09030', 'tea': '#c8a070'},
            {'naam': 'Vlinderbloemthee in celadon (blauwe thee)', 'porcelain': '#a8d0b8', 'trim': '#4a7a60',
             'flowers': '#f0f0f0', 'gold': '#c0c8c0', 'tea': '#4050d0'},
            {'naam': 'Kintsugi (zwart, met goud gelijmd)', 'porcelain': ('#2c2c34', DARK), 'trim': ('#e0b030', GOLD),
             'gold': ('#e0b030', GOLD), 'flowers': '#e0b030', 'tea': '#c03030'},
        ],
    },
    'hatenna': {
        # heksen: haar (Hatterene ook de hoed), roze (Hatenna/Hattrem hoed, Hatterene lijf), wit (gezicht)
        'species': {
            'hatenna': {'hair': [2, 4, 1], 'pink': [9, 6, 5, 7], 'white': [8]},
            'hattrem': {'hair': [9, 10, 8, 12, 11], 'pink': [13, 4, 6, 1, 5], 'white': [2, 3]},
            'hatterene': {'hair': [5, 4, 2, 1], 'pink': [8, 13, 10, 14], 'white': [9, 6, 7, 11, 12]},
        },
        'variants': [
            {'naam': 'Lavendelheks (lila met mint)', 'hair': '#b090e0', 'pink': '#90d0b0', 'white': '#f8f0f8'},
            {'naam': 'Elphaba (Wicked: zwarte hoed, groene huid)', 'hair': ('#34343c', DARK), 'pink': '#50b050',
             'white': '#d0f0c0'},
            {'naam': 'Halloween (pompoenoranje met paars)', 'hair': '#f08020', 'pink': '#7a3a98', 'white': '#f8e8d0'},
            {'naam': 'Snoepheks van Hans en Grietje (peperkoek en suikerroze)', 'hair': '#a06830', 'pink': '#f070a0',
             'white': '#fff0f0'},
            {'naam': 'Scarlet Witch (rood en karmozijn)', 'hair': '#c02030', 'pink': '#7a1020', 'white': '#f0d0c0'},
            {'naam': 'Sterrenwichelaar (nachtblauw met goud)', 'hair': ('#283068', DARK), 'pink': ('#e0b030', GOLD),
             'white': '#f0e8c8'},
        ],
    },
    'impidimp': {
        # trollen: roze (huid), haar (paars; Grimmsnarl: hele lijf), groen (benen/huid), rode ogen
        'species': {
            'impidimp': {'pink': [1, 4, 2, 3, 12], 'hair': [6, 5, 7, 13], 'red': [8]},
            'morgrem': {'pink': [6, 2, 1], 'hair': [7, 3, 4, 5], 'green': [13, 12, 14], 'red': [8]},
            'grimmsnarl': {'hair': [5, 7, 3, 11], 'green': [2, 6, 1], 'pink': [13, 14], 'red': [8]},
        },
        'variants': [
            {'naam': 'Noorse trol (mos en steen)', 'hair': '#5a6a40', 'pink': '#a08870', 'green': '#7a7060',
             'red': '#f0c030'},
            {'naam': 'Aka-oni (rode duivel met gouden manen)', 'pink': '#d03028', 'hair': '#d89a30',
             'green': '#c87028', 'red': '#f0e040'},
            {'naam': 'De Grinch (groen met rood pak en witte bontrand)', 'pink': '#80c040', 'hair': '#d02828',
             'green': '#f8f8f8', 'red': '#f0e040'},
            {'naam': 'Pennywise (clownwit, oranjerood haar, zilveren pak)', 'hair': '#e05020',
             'pink': ('#f0f0f0', ALBINO), 'green': '#a8b0c0', 'red': '#f0e040',
             'grimmsnarl:hair': '#b0b8c8', 'grimmsnarl:green': '#e05020'},
            {'naam': 'Krampus (zwarte vacht, bruine huid)', 'hair': ('#2a2420', DARK), 'pink': '#7a5a48',
             'green': '#3a3028', 'red': '#e02020'},
            {'naam': 'Leprechaun (groen pak, pot met goud)', 'hair': '#2a8040', 'pink': '#f0c8a0',
             'green': ('#e0b030', GOLD), 'red': '#d04020'},
        ],
    },
    'milcery': {
        # room (Alcremie wordt bewust overgeslagen: die heeft 63 vormen)
        'species': {
            'milcery': {'cream': [3, 2, 1, 4]},
        },
        'variants': [
            {'naam': 'Aardbeienmelk', 'cream': '#f0a0b8'},
            {'naam': 'Chocolademelk', 'cream': ('#8a5a40', {'l': 1.2})},
            {'naam': 'Matcha latte', 'cream': '#a8c870'},
            {'naam': 'Bosbessenyoghurt', 'cream': '#a890d0'},
            {'naam': 'Blauwe-hawaiiaanse slush', 'cream': '#70c0f0'},
            {'naam': 'Zwarte-sesamijs', 'cream': ('#4a4448', DARK)},
        ],
    },
    'falinks': {
        # legioen: helm/schild (geel), kuif/schildhart (rood), wit, donker, ogen
        'species': {
            'falinks': {'gold': [4, 9, 10, 1], 'red': [3, 5], 'white': [12, 6], 'dark': [7, 11], 'eye': [8, 13]},
        },
        'variants': [
            {'naam': 'Terracottaleger (terracotta met grijsgroen)', 'gold': '#b86a48', 'red': '#6a7a70',
             'white': '#e0d0c0', 'dark': '#4a3a30', 'eye': '#e0c060'},
            {'naam': 'Britse koninklijke garde (rood met zwarte berenmuts)', 'gold': '#c02828',
             'red': ('#2a2a30', DARK), 'white': '#f8f8f8', 'dark': '#2a2a30', 'eye': '#3060c0'},
            {'naam': 'Stormtroopers (wit en zwart)', 'gold': ('#e8e8ec', ALBINO), 'red': ('#2a2a30', DARK),
             'white': '#ffffff', 'dark': '#2a2a30', 'eye': '#3a3a40'},
            {'naam': 'Zwitserse Garde (blauw en geel)', 'gold': '#2850b0', 'red': '#f0c020', 'white': '#f8f8f8',
             'dark': '#1a2050', 'eye': '#f0c020'},
            {'naam': 'Leger van Mordor (zwart ijzer, oranje oog)', 'gold': ('#3a3a40', DARK), 'red': '#f08020',
             'white': '#8a8a90', 'dark': '#1e1e24', 'eye': '#f08020'},
            {'naam': 'Paarse keizerlijke garde (purper met zilver)', 'gold': '#7a3a98', 'red': '#d8dce4',
             'white': '#f8f0ff', 'dark': '#3a1a50', 'eye': '#f0d040'},
        ],
    },
    'pincurchin': {
        # zee-egels: stekels, lijf, geel (tanden/ogen), stroompuntjes
        'species': {
            'pincurchin': {'spines': [6, 7, 5], 'body': [4, 2, 1], 'yellow': [9, 10, 11, 8], 'spark': [12, 13]},
        },
        'variants': [
            {'naam': 'Rode zee-egel', 'spines': '#a02828', 'body': '#c0a090', 'yellow': '#f0e0c0', 'spark': '#f0e040'},
            {'naam': 'Groene zee-egel', 'spines': '#4a7a3a', 'body': '#9a9a80', 'yellow': '#f0d040', 'spark': '#a0f040'},
            {'naam': 'Collector-zee-egel (wit met oranje)', 'spines': ('#e8e4dc', ALBINO), 'body': '#e09040',
             'yellow': '#f08020', 'spark': '#f08020'},
            {'naam': 'Paarse zee-egel (violet met roze stroom)', 'spines': '#7a3aa8', 'body': '#a090b0',
             'yellow': '#f0c040', 'spark': '#f060e0'},
            {'naam': 'Uni (sushi: oranje)', 'spines': '#e09020', 'body': '#6a4a30', 'yellow': '#f8e0a0',
             'spark': '#f8f0c0'},
            {'naam': 'Kroon-zee-egel (goud met robijn)', 'spines': ('#d8a830', GOLD), 'body': '#8a4a20',
             'yellow': '#e02040', 'spark': '#ffffff'},
        ],
    },
    'snom': {
        # ijsmotten: ijs (Snom: lijf, Frosmoth: vleugels), lijf/gezicht, ogen (Frosmoth)
        'species': {
            'snom': {'ice': [2, 1, 3, 4], 'body': [7, 8, 5]},
            'frosmoth': {'ice': [2, 3, 4, 1, 5], 'body': [8, 7, 9], 'eye': [10, 11, 12, 13]},
        },
        'variants': [
            {'naam': 'Noorderlicht (lila met mint)', 'ice': '#b0a0e8', 'body': '#80e0b0', 'eye': '#40f0a0'},
            {'naam': 'Citrienkristal (lichtgeel)', 'ice': '#f0e080', 'body': '#f8f8e0', 'eye': '#e09020'},
            {'naam': 'Rijp op rozen (roze ijskristal)', 'ice': '#f0b8d0', 'body': '#f8f0f8', 'eye': '#c04080'},
            {'naam': 'Zwart ijs (nachtblauw)', 'ice': ('#4a5068', DARK), 'body': '#a0b0d0', 'eye': '#60e0f0'},
            {'naam': 'Robijnijs (karmijn met wit)', 'ice': '#d04050', 'body': '#f8e8e8', 'eye': '#f0f0f0'},
            {'naam': 'Saffier met goud', 'ice': '#3050c0', 'body': ('#f0d040', GOLD), 'eye': '#f0d040'},
        ],
    },
    'stonjourner': {
        # megalieten: steen, donkere kopstenen/kruisen, aarde/mos onderaan, ogen
        'species': {
            'stonjourner': {'stone': [5, 7, 8, 6], 'dark': [2, 3, 1], 'dirt': [10, 12, 11], 'eye': [9]},
        },
        'variants': [
            {'naam': 'Zandsteen (Petra-rood)', 'stone': '#c07050', 'dark': '#6a3028', 'dirt': '#4a3a28', 'eye': '#f0e040'},
            {'naam': 'Bemost hunebed (Drenthe)', 'stone': '#7a8a60', 'dark': '#4a5a3a', 'dirt': '#3a6a30',
             'eye': '#f0f0c0'},
            {'naam': 'Moai van Paaseiland (tufsteen met rode pukao)', 'stone': '#5a5050', 'dark': '#a04030',
             'dirt': '#4a6a30', 'eye': '#f0f0f0'},
            {'naam': 'Carrara-marmer (wit met grijze aders)', 'stone': ('#e8e4e0', ALBINO), 'dark': '#8a8a90',
             'dirt': '#c8c0b0', 'eye': '#40a0e0'},
            {'naam': 'Obsidiaan met lavanaden', 'stone': ('#3a3440', DARK), 'dark': '#e05020', 'dirt': '#5a2018',
             'eye': '#f08020'},
            {'naam': 'El Dorado (goud met jade)', 'stone': ('#d8a830', GOLD), 'dark': '#3a8a5a', 'dirt': '#6a4a20',
             'eye': '#e02020'},
        ],
    },
    'eiscue': {
        # pinguïns met een ijsblok: ijs (blok/kop), lijf (zwart), snavel/poten
        'species': {
            'eiscue': {'ice': [2, 4, 5], 'body': [8, 7, 6], 'beak': [13, 11, 12]},
            'eiscue/noice_face': {'ice': [5, 3, 2], 'body': [9, 10, 8], 'beak': [13, 11, 12]},
        },
        'variants': [
            {'naam': 'Citroenijsje (keizerspinguïn: leigrijs met oranje snavel)', 'ice': '#f0e070',
             'body': '#3a4a5a', 'beak': '#f0a020'},
            {'naam': 'Munt-chocolade-ijs', 'ice': '#90e0b0', 'body': '#5a3a28', 'beak': '#f0d040'},
            {'naam': 'Druivenijsje (blauwe dwergpinguïn)', 'ice': '#a070d0', 'body': '#5070a0', 'beak': '#2a2a30'},
            {'naam': 'Colaijsje (Adéliepinguïn)', 'ice': '#8a4a28', 'body': ('#202028', DARK), 'beak': '#e04040'},
            {'naam': 'Blue raspberry-slush (rotspinguïn)', 'ice': '#3060e0', 'body': '#3a3a48', 'beak': '#e02020'},
            {'naam': 'Robijnen ijsblok (zwart met goud)', 'ice': '#c81838', 'body': ('#28242c', DARK),
             'beak': ('#e0b030', GOLD)},
        ],
    },
    'indeedee': {
        # psychische butlers (♂ en ♀): lijf, lichte vacht/gezicht, ogen
        'species': {
            'indeedee': {'body': [8, 4, 5, 1, 2, 13], 'light': [6, 7, 12], 'eye': [11, 9, 10]},
            'indeedee/f': {'body': [10, 3, 4, 1, 2, 13], 'light': [7, 8, 12], 'eye': [6, 9, 11]},
        },
        'variants': [
            {'naam': 'Geisha (rode kimono, wit gezicht)', 'body': '#c02838', 'light': '#f8f0f0', 'eye': '#2a2a30'},
            {'naam': 'Madame de Pompadour (roze)', 'body': '#e080a8', 'light': '#fff0f8', 'eye': '#40a0e0'},
            {'naam': 'Chinchilla (zilvergrijs)', 'body': '#8a8a98', 'light': '#f0f0f8', 'eye': '#2a2a30'},
            {'naam': 'Bollywood (saffraan met magenta)', 'body': '#e08020', 'light': '#f8e0f0', 'eye': '#e02080'},
            {'naam': 'Jade-Boeddha (jadegroen met goud)', 'body': '#40a070', 'light': '#e0f0d8', 'eye': '#e0b040'},
            {'naam': 'Maharadja (goud met robijn)', 'body': ('#d8a830', GOLD), 'light': '#f8f0d0', 'eye': '#c02040'},
        ],
    },
    'morpeko': {
        # hamsters met twee buien: stemming (vol: geel, Hangry: paars), bruin, donkere vacht, wangen
        'species': {
            'morpeko': {'mood': [7, 8], 'brown': [5, 2, 1], 'dark': [3, 4, 6], 'cheek': [11, 12]},
            'morpeko/hangry': {'mood': [4, 5, 10], 'dark': [3, 2, 1], 'cheek': [8]},
        },
        'variants': [
            {'naam': 'Snickers (je bent jezelf niet als je honger hebt)', 'mood': '#d89a40',
             'morpeko/hangry:mood': '#c02828', 'brown': '#6a3a20', 'dark': '#4a2a18', 'cheek': '#f06060'},
            {'naam': 'Russische dwerghamster (wit en grijs)', 'mood': ('#e8e4dc', ALBINO),
             'morpeko/hangry:mood': '#6a6a90', 'brown': '#8a8a90', 'dark': '#5a5a60', 'cheek': '#f090a0'},
            {'naam': 'Pac-Man-spookjes (Blinky rood, bang spookje blauw)', 'mood': '#e02020',
             'morpeko/hangry:mood': '#2040e0', 'brown': '#f8b0a0', 'dark': ('#1a1a60', DARK), 'cheek': '#f8f8f8'},
            {'naam': 'Matcha-mochi', 'mood': '#a0c870', 'morpeko/hangry:mood': '#2a6040', 'brown': '#f0e8d8',
             'dark': '#4a6a30', 'cheek': '#f0a0b0'},
            {'naam': 'Neapolitaans ijs (aardbei, vanille, chocolade)', 'mood': '#f0a0b0',
             'morpeko/hangry:mood': '#f8f0d8', 'brown': '#f8f0d8', 'dark': '#5a3020', 'cheek': '#e04060'},
            {'naam': 'Melkweg (nachtblauw met sterrenroze)', 'mood': '#f070c0', 'morpeko/hangry:mood': '#40e0f0',
             'brown': '#8090e0', 'dark': ('#202850', DARK), 'cheek': '#f0e040'},
        ],
    },
    'cufant': {
        # metalen olifanten: koper, patina (slurf/oren), slagtanden, accent (Copperajah teal, Cufant roze)
        'species': {
            'cufant': {'copper': [10, 8, 9, 7], 'patina': [6, 5, 1], 'tusk': [2, 4], 'accent': [14, 13]},
            'copperajah': {'copper': [6, 8, 5], 'patina': [7, 3, 2, 1], 'tusk': [10, 9, 14], 'accent': [13, 12, 11]},
        },
        'variants': [
            {'naam': 'IJzer met roest (grijs, roestoranje)', 'copper': '#8a8a90', 'patina': '#b05a28',
             'tusk': '#f0f0e8', 'accent': '#e07030'},
            {'naam': 'Holi-olifant (beschilderd: magenta en geel)', 'copper': '#d04090', 'patina': '#f0c020',
             'tusk': '#f8f8f8', 'accent': '#40c0e0'},
            {'naam': 'Geanodiseerd titanium (blauwpaars)', 'copper': '#5a6ac0', 'patina': '#c040a0',
             'tusk': '#f0f0f0', 'accent': '#f0d040'},
            {'naam': 'Witte olifant van Siam (zilver)', 'copper': ('#d8dce4', ALBINO), 'patina': '#8090a0',
             'tusk': '#f8f0d0', 'accent': '#40a0e0'},
            {'naam': 'Gietijzer (zwart met gloeiende naden)', 'copper': ('#3a3a42', DARK), 'patina': '#c04020',
             'tusk': '#a0a0a8', 'accent': '#f08020',
             'copperajah:patina': ('#3a3a42', DARK), 'copperajah:copper': '#c04020'},
            {'naam': 'Toetanchamon (goud met lapis lazuli)', 'copper': ('#e0b030', GOLD), 'patina': '#2850a0',
             'tusk': '#f8f0d0', 'accent': '#c02020'},
        ],
    },
    'fossils': {
        # Galar-fossielen (vier chimaera's uit twee helften): vogel (Zolt-boven), vis (Vish-boven),
        # draak (Draco-onder, rood) met groene schubben, ijs (Arcto-onder, wit) met blauwe vinnen
        'species': {
            'dracozolt': {'bird': [3, 4, 6, 2, 11], 'dragon': [7, 8, 5, 9, 10], 'scales': [12, 13, 14, 15]},
            'arctozolt': {'bird': [2, 5, 4, 1], 'ice': [9, 8, 10, 12, 7], 'fins': [11, 13, 14, 6]},
            'dracovish': {'fish': [4, 5, 2, 6], 'dragon': [3, 11, 12, 9, 15, 1], 'scales': [10, 8, 13, 14]},
            'arctovish': {'fish': [5, 4, 1, 8, 3], 'ice': [6, 7, 9], 'fins': [11, 12, 13, 10]},
        },
        'variants': [
            {'naam': 'Versteend fossiel (zandsteen en barnsteen)', 'bird': '#c8a070', 'fish': '#a08060',
             'dragon': '#8a5a40', 'scales': '#6a5040', 'ice': ('#e0d0b0', GOLD), 'fins': '#c08030'},
            {'naam': 'Barney (paars met groene buik)', 'bird': '#9050c0', 'fish': '#9050c0', 'dragon': '#90d050',
             'scales': '#7040a0', 'ice': '#b0e070', 'fins': '#9050c0'},
            {'naam': 'Koraalrif (koraalrood met turquoise)', 'bird': '#f07050', 'fish': '#f07050', 'dragon': '#40c0b0',
             'scales': '#2a8080', 'ice': '#f8e0d0', 'fins': '#f07050'},
            {'naam': 'Godzilla (antraciet met blauw atoomvuur)', 'bird': ('#3a3c44', DARK),
             'fish': ('#3a3c44', DARK), 'dragon': '#4a4c54', 'scales': ('#2a2c30', DARK), 'ice': '#5a5c64',
             'fins': '#40c0f0'},
            {'naam': 'Albino (wit met roze en zilver)', 'bird': ('#f0f0e8', ALBINO), 'fish': ('#e8eef4', ALBINO),
             'dragon': '#f0c8d0', 'scales': '#c8d0d8', 'ice': ('#ffffff', GOLD), 'fins': '#a0b0c0'},
            {'naam': 'Gouden chimaera (goud met robijn en saffier)', 'bird': ('#e0b030', GOLD), 'fish': ('#e0b030', GOLD),
             'dragon': '#c02030', 'scales': '#2850b0', 'ice': ('#f8f0d0', GOLD), 'fins': '#2850b0'},
        ],
    },
    'duraludon': {
        # wolkenkrabbers: metaal (lijf), blauwe accenten (kop/armen), rode ogen, gele oogjes
        'species': {
            'duraludon': {'metal': [9, 15, 8, 12, 5, 11], 'blue': [14, 10, 2, 1], 'red': [3, 13], 'yellow': [6, 7]},
        },
        'variants': [
            {'naam': 'Vrijheidsbeeld (groene kopatina)', 'metal': '#60b098', 'blue': '#2a6050', 'red': '#e05030',
             'yellow': '#f0d040'},
            {'naam': 'Tokyo Tower (rood en wit)', 'metal': '#e03028', 'blue': '#f8f8f8', 'red': '#f0d040',
             'yellow': '#f0d040'},
            {'naam': 'Darth Vader-staal (zwart, rood licht)', 'metal': ('#3a3c48', DARK), 'blue': ('#202028', DARK),
             'red': '#f02020', 'yellow': '#f02020'},
            {'naam': 'Bouwkraan (geel met zwart)', 'metal': '#f0c020', 'blue': ('#2a2a30', DARK), 'red': '#e04020',
             'yellow': '#f8f8f8'},
            {'naam': 'Barbie Dreamhouse (roze)', 'metal': '#f0a0c8', 'blue': '#c04080', 'red': '#40c0f0',
             'yellow': '#40c0f0'},
            {'naam': 'Ishtarpoort van Babylon (lapis lazuli met goud)', 'metal': '#2850a8', 'blue': ('#e0b030', GOLD),
             'red': '#f0f0f0', 'yellow': '#f0f0f0'},
        ],
    },
    'dreepy': {
        # spookstraaljagers: spooklijf/staart, donkere romp, roze vinnen, gele ogen, lichtbruin (Dreepy-houders)
        'species': {
            'dreepy': {'ghost': [7, 6, 4, 1, 13], 'pink': [8, 9, 12, 3, 5], 'yellow': [11, 10]},
            'drakloak': {'dark': [1, 4, 6], 'ghost': [11, 12, 2, 13, 5], 'pink': [7, 9, 8], 'yellow': [10],
                         'tan': [14, 15]},
            'dragapult': {'dark': [2, 1, 4], 'ghost': [12, 7, 15, 8, 14], 'pink': [5, 6, 9], 'yellow': [10],
                          'tan': [11, 13]},
        },
        'variants': [
            {'naam': 'Camouflage-straaljager (olijf en zand)', 'ghost': '#a8b070', 'dark': '#4a5030', 'pink': '#e0c080',
             'yellow': '#f04020', 'tan': '#c0a070'},
            {'naam': 'Blue Angels (marineblauw met geel)', 'dark': '#203080', 'ghost': '#80b0f0', 'pink': '#f0d040',
             'yellow': '#f0f0f0', 'tan': '#f0d040'},
            {'naam': 'Casper het vriendelijke spookje (wit met lichtblauw)', 'ghost': ('#e8f0f8', ALBINO),
             'dark': '#9aa4b8', 'pink': '#80c0f0', 'yellow': '#3a6ab0', 'tan': '#f0f0f0'},
            {'naam': 'Halloween (oranje spook, paarse romp)', 'ghost': '#f0a040', 'dark': '#4a2a68', 'pink': '#80e040',
             'yellow': '#f0f040', 'tan': '#f8d0a0'},
            {'naam': 'De Rode Baron (Fokker-rood)', 'dark': '#a02028', 'ghost': '#f09070', 'pink': '#2a2a30',
             'yellow': '#f0f0f0', 'tan': '#f0e0c0'},
            {'naam': 'Apollo (goudfolie van de maanlander)', 'dark': ('#d8a830', GOLD), 'ghost': '#f8e8a0',
             'pink': '#3060d0', 'yellow': '#c02020', 'tan': '#f8f0d0'},
        ],
    },
    'zacian': {
        # heldenwolven (ook de gekroonde vormen): blauw (Zacians vacht, Zamazenta's manen), rood (Zacians manen,
        # Zamazenta's lijf), lichtbruin (Zacians poten/snuit), zwaard/schild (goud), grijs (Zamazenta)
        'species': {
            'zacian': {'blue': [3, 4, 1], 'red': [5, 9, 12], 'tan': [7, 6, 11]},
            'zacian/crowned_sword': {'gold': [2, 3, 1], 'blue': [7, 5, 6], 'red': [8, 9, 12], 'tan': [10, 11, 15]},
            'zamazenta': {'blue': [2, 4, 1], 'red': [8, 7, 6], 'grey': [5, 9]},
            'zamazenta/crowned_shield': {'blue': [2, 3, 1], 'gold': [6, 7, 5, 10], 'red': [9, 11, 8],
                                         'grey': [14, 15]},
        },
        'variants': [
            {'naam': 'Sif (Dark Souls: grijze wolf met nachtblauwe mantel)', 'blue': '#8a8c98', 'red': '#3a3a70',
             'tan': '#d0c8c0', 'gold': '#c8ccd8', 'grey': '#a8a8b0'},
            {'naam': 'Fenrir (zwart met bloedrood)', 'blue': ('#34343c', DARK), 'red': '#c02030', 'tan': '#8a8a90',
             'gold': '#a0a8b8', 'grey': '#5a5a60',
             'zamazenta:blue': '#c02030', 'zamazenta:red': ('#34343c', DARK),
             'zamazenta/crowned_shield:blue': '#c02030', 'zamazenta/crowned_shield:red': ('#34343c', DARK)},
            {'naam': 'De Groene Ridder (Sir Gawain)', 'blue': '#3a8a50', 'red': '#c8a040', 'tan': '#e0d0b0',
             'gold': '#d0d4d8', 'grey': '#a0b0a0'},
            {'naam': 'Koninklijk purper en goud', 'blue': '#6a3aa0', 'red': '#f0c020', 'tan': '#f0e0c0',
             'gold': '#f0c020', 'grey': '#c0b0d0'},
            {'naam': 'Sköll en Hati (de wolven die zon en maan najagen)', 'blue': '#e08030', 'red': '#f8f0c0',
             'tan': '#f8e0b0', 'gold': '#f8f8f8', 'grey': '#e0c080'},
            {'naam': 'Tiangou (de hemelhond: wit met goud)', 'blue': ('#f0ece4', ALBINO), 'red': ('#e0b030', GOLD),
             'tan': '#f8f0e0', 'gold': ('#e0b030', GOLD), 'grey': '#c0b8a8'},
        ],
    },
    'eternatus': {
        # kosmische draak (ook Eternamax): schild (paars), kern/stekels (rood)
        'species': {
            'eternatus': {'shell': [7, 1, 2, 9], 'core': [8, 4, 5, 6, 10, 11], 'pink': [12, 14, 13]},
            'eternatus/eternamax': {'shell': [1, 2, 9, 10], 'core': [7, 8, 12, 11, 13, 14], 'pink': [4, 5, 6]},
        },
        'variants': [
            {'naam': 'Zwart gat (zwart met oranje accretieschijf)', 'shell': ('#2a2830', DARK), 'core': '#f0a020',
             'pink': '#f0e040'},
            {'naam': 'Blauwe superreus (diepblauw met cyaan)', 'shell': '#304890', 'core': '#60e0f0', 'pink': '#f0f0f0'},
            {'naam': 'Kryptoniet (groen gloeiend)', 'shell': '#2a4030', 'core': '#60f060', 'pink': '#c0f0a0'},
            {'naam': 'Zonnevlam (karmijn met geel)', 'shell': '#802020', 'core': '#f0e040', 'pink': '#f8f8c0'},
            {'naam': 'Sterrenstof (zilver met violet)', 'shell': '#b0b4c8', 'core': '#8040e0', 'pink': '#e0c0f8'},
            {'naam': 'Gouden komeet (goud met witte staart)', 'shell': ('#d8a830', GOLD), 'core': '#f8f8f0',
             'pink': '#40c0f0'},
        ],
    },
    'kubfu': {
        # vechtberen (beide Urshifu-stijlen): vacht, witte vacht, donkere vacht/riemen, goud (ogen/klauwen)
        'species': {
            'kubfu': {'fur': [3, 2, 1], 'white': [6, 7, 4], 'dark': [9, 13, 8], 'gold': [10, 11, 12]},
            'urshifu': {'fur': [5, 6, 1], 'white': [4, 7, 10], 'dark': [9, 8, 2], 'gold': [12, 13, 11]},
            'urshifu/rapid_strike': {'fur': [3, 2, 1], 'white': [11, 8, 13], 'dark': [9, 5, 6],
                                     'gold': [12, 10, 7]},
        },
        'variants': [
            {'naam': 'Reuzenpanda (wit met zwarte poten, bamboegroene ogen)', 'fur': ('#e8e8e8', ALBINO),
             'white': '#f8f8f8', 'dark': ('#202024', DARK), 'gold': '#40a040'},
            {'naam': 'Kodiakbeer (bruin, honinggoud)', 'fur': '#8a5a38', 'kubfu:fur': '#c09068', 'white': '#e0c8a0',
             'dark': '#3a2418', 'gold': '#f0c040'},
            {'naam': 'Shaolin-monnik (saffraan en rood)', 'fur': '#e08a20', 'white': '#f8e8c8', 'dark': '#a02020',
             'gold': '#f0d040'},
            {'naam': 'Bruce Lee (Game of Death: geel pak met zwarte strepen)', 'fur': '#f0c820', 'white': '#f8f0c0',
             'dark': ('#202024', DARK), 'gold': '#e03020'},
            {'naam': 'Waterstijl (diepblauw met cyaan)', 'fur': '#2a4a90', 'kubfu:fur': '#6080c0', 'white': '#a0e0f0',
             'dark': '#182040', 'gold': '#40e0f0'},
            {'naam': 'Gouden Boeddha (goud met jade)', 'fur': ('#d8a830', GOLD), 'white': '#f8f0d0', 'dark': '#2a8050',
             'gold': '#40c080'},
        ],
    },
    'zarude': {
        # junglebewakers (ook Dada): vacht, lianen, grijze tekening, cape (Dada)
        'species': {
            'zarude': {'fur': [6, 3, 1], 'vine': [13, 7, 9], 'grey': [10, 11, 4, 5]},
            'zarude/dada': {'fur': [4, 3, 1], 'vine': [15, 14, 10], 'grey': [12, 13, 6, 7, 5], 'cape': [11, 8]},
        },
        'variants': [
            {'naam': 'Orang-oetan (roodbruin met mos)', 'fur': '#a04a20', 'vine': '#6a8a30', 'grey': '#e0a070',
             'cape': '#3060a0'},
            {'naam': 'Sneeuwvlok (de albino gorilla van Barcelona)', 'fur': ('#e8e4e0', ALBINO), 'vine': '#40a050',
             'grey': '#f8c0b0', 'cape': '#c02020'},
            {'naam': 'Doodsliaan (paarse vacht, bloedrode lianen)', 'fur': '#5a3a80', 'vine': '#c03040',
             'grey': '#c0a0e0', 'cape': '#40c080'},
            {'naam': 'Tropische nacht (nachtblauw met lichtgevende lianen)', 'fur': '#2a3a6a', 'vine': '#40f0d0',
             'grey': '#90a0d0', 'cape': '#f0c040'},
            {'naam': 'Kersenbloesemliaan (grijs met roze)', 'fur': '#7a7880', 'vine': '#f0a0c0', 'grey': '#f0e0e8',
             'cape': '#a03060'},
            {'naam': 'Hanuman (de apengod: goud met rode lendendoek)', 'fur': ('#d8a830', GOLD), 'vine': '#40a060',
             'grey': '#f8e8c0', 'cape': '#c02828'},
        ],
    },
    'regieleki': {
        # elektrische titaan: lijf (geel), kern/ringen (blauw), stippen
        'species': {
            'regieleki': {'body': [4, 2, 5, 1, 11], 'core': [8, 9, 7, 10], 'dots': [6]},
        },
        'variants': [
            {'naam': 'Cyaan plasma (cyaan met paars)', 'body': '#40d0f0', 'core': '#6030a0', 'dots': '#f040a0'},
            {'naam': 'The Flash (rood met geel)', 'body': '#e03028', 'core': '#f0d040', 'dots': '#f8f8f8'},
            {'naam': 'Witte vonk (wit met ijsblauw)', 'body': ('#f0f0f8', ALBINO), 'core': '#3060d0', 'dots': '#40e0f0'},
            {'naam': 'Zonsondergangstroom (oranje met paars)', 'body': '#f08020', 'core': '#5a2a90', 'dots': '#f8f080'},
            {'naam': 'Paarse bliksem (Raiden)', 'body': '#9050e0', 'core': '#f0f0f0', 'dots': '#f0e040'},
            {'naam': 'Printplaat (pcb-groen met gouden banen)', 'body': '#2a7a40', 'core': ('#e0b030', GOLD),
             'dots': '#f04040'},
        ],
    },
    'regidrago': {
        # draaktitaan: lijf, drakenkop (rood), stippen
        'species': {
            'regidrago': {'body': [4, 3, 1, 9, 5], 'head': [10, 7, 6, 14, 8], 'dots': [12, 11, 13]},
        },
        'variants': [
            {'naam': 'Bronzen draak (brons met turquoise)', 'body': '#a07040', 'head': '#40c0b0', 'dots': '#f0e040'},
            {'naam': 'Y Ddraig Goch (de rode draak van Wales, met groen)', 'body': '#c02828', 'head': '#30a040',
             'dots': '#f8f8f8'},
            {'naam': 'Witte draak (wit met blauw)', 'body': ('#d8dce8', ALBINO), 'head': '#4080e0', 'dots': '#f04040'},
            {'naam': 'Bahamut (zwart met paarsblauw vuur)', 'body': ('#2c2c38', DARK), 'head': '#8050f0',
             'dots': '#40f0f0'},
            {'naam': 'Jadedraak (jade met goud)', 'body': '#40a080', 'head': '#e0b040', 'dots': '#c02828'},
            {'naam': 'King Ghidorah (goud met rood)', 'body': ('#d8a830', GOLD), 'head': '#c02828', 'dots': '#40e0f0'},
        ],
    },
    'calyrex': {
        # de koning en zijn rossen (Calyrex, Glastrier, Spectrier en beide rijvormen): kroon (groen), mantel,
        # ogen, ijsros (lijf + ijs), spookros (lijf + manen + staart)
        'species': {
            'calyrex': {'crown': [4, 6, 3], 'robe': [10, 11], 'eye': [5, 12, 13]},
            'glastrier': {'icebody': [8, 4, 7], 'ice': [5, 3, 2, 1]},
            'spectrier': {'ghostbody': [1, 3], 'mane': [5, 4, 6, 9], 'tail': [7, 8]},
            'calyrex/ice': {'crown': [8, 6, 3], 'robe': [14, 13], 'eye': [7, 15], 'icebody': [12, 9, 4],
                            'ice': [10, 5, 2, 1]},
            'calyrex/shadow': {'crown': [6, 3, 1], 'robe': [12, 11], 'ghostbody': [7, 2], 'mane': [4, 13, 14],
                               'tail': [10, 9]},
        },
        'variants': [
            {'naam': 'Herfstkoning (oranjerode bladerkroon, amberijs, vos)', 'crown': '#d06020', 'robe': '#8a5a40',
             'eye': '#40a040', 'icebody': '#c8a070', 'ice': '#c08040', 'ghostbody': '#4a3028', 'mane': '#e08030',
             'tail': '#f0d8a0'},
            {'naam': 'Kersenbloesemkeizer (sakura)', 'crown': '#f0a0c0', 'robe': '#a07890', 'eye': '#40a060',
             'icebody': '#f8e0e8', 'ice': '#e080a8', 'ghostbody': '#5a3048', 'mane': '#f070a0', 'tail': '#f8e0e8'},
            {'naam': 'Elfenkoning Oberon (maanzilver met indigo)', 'crown': '#a0a8c0', 'robe': '#4a4a70',
             'eye': '#f0d040', 'icebody': '#8a90b8', 'ice': '#e0e8ff', 'ghostbody': '#2a2a48', 'mane': '#c0c8f0',
             'tail': '#f0f0ff'},
            {'naam': 'Paddenstoelkoning (rood met wit)', 'crown': '#d02828', 'robe': '#f0e0c0', 'eye': '#3060d0',
             'icebody': '#f8f0e0', 'ice': '#d02828', 'ghostbody': '#5a1a1a', 'mane': '#e03030', 'tail': '#f8f8f8'},
            {'naam': 'Dullahan (de hoofdloze ruiter: zwart met groen spookvuur)', 'crown': ('#2c2c34', DARK),
             'robe': '#3a3a40', 'eye': '#40f070', 'icebody': '#7a8a80', 'ice': '#40f070',
             'ghostbody': ('#1e1e24', DARK), 'mane': '#40f070', 'tail': '#80a090'},
            {'naam': 'De Zonnekoning (Lodewijk XIV: goud en koningsblauw)', 'crown': ('#e0b030', GOLD),
             'robe': '#2840a0', 'eye': '#c02020', 'icebody': '#f8f0d8', 'ice': ('#e0b030', GOLD),
             'ghostbody': '#2840a0', 'mane': ('#e0b030', GOLD), 'tail': '#f8f0d8'},
        ],
    },
    'enamorus': {
        # liefdesgodin (ook Therian): wolk, roze, karmijn, mauve (lijf/haar), geel
        'species': {
            'enamorus': {'cloud': [1, 2, 3], 'pink': [5, 6, 7], 'crimson': [9, 10, 15], 'mauve': [12, 13, 14],
                         'yellow': [8]},
            'enamorus/therian': {'cloud': [13, 11, 2], 'pink': [9, 10, 6], 'mauve': [7, 1], 'crimson': [5, 4, 3],
                                 'yellow': [8]},
        },
        'variants': [
            {'naam': 'De geboorte van Venus (Botticelli: zeegroen en perzik)', 'pink': '#80c8b0', 'crimson': '#e0a080',
             'mauve': '#c8a890', 'cloud': '#f8f0e8', 'yellow': '#f0d040'},
            {'naam': 'Primavera (lentegroen met lila)', 'pink': '#a8d070', 'crimson': '#a070c0', 'mauve': '#5a7a40',
             'cloud': '#f8f8e0', 'yellow': '#f0a0c0'},
            {'naam': 'Onweerswolk (stormgrijs met paarse bliksem)', 'cloud': '#7a8090', 'pink': '#9070c0',
             'crimson': '#4a3a80', 'mauve': '#3a3a50', 'yellow': '#f0f040'},
            {'naam': 'Zonsondergang (oranje en violet)', 'pink': '#f0a040', 'crimson': '#d04060', 'mauve': '#6a3a70',
             'cloud': '#f8d8b0', 'yellow': '#f8f8c0'},
            {'naam': 'Selene (de maangodin: nachtblauw met zilver)', 'pink': '#a0a8d8', 'crimson': '#3a4a90',
             'mauve': ('#2a2a48', DARK), 'cloud': '#c8d0e8', 'yellow': '#f0f0f0'},
            {'naam': 'Freya (goud met rood)', 'pink': ('#e8b840', GOLD), 'crimson': '#c02030', 'mauve': '#8a5a20',
             'cloud': '#f8f0d0', 'yellow': '#c02030'},
        ],
    },
}
