"""Kleurvarianten, generatie 4 (Sinnoh). Formaat: zie recipes.py."""

ALBINO = {'l': 1.0}
DARK = {'l': 1.3}

LINES = {
    'turtwig': {
        # bladeren, huid, schild (Torterra: lijf), gele kaak/korst, rotsen (Torterra)
        'species': {
            'turtwig': {'leaves': [1, 2, 3], 'body': [7, 9, 10, 11], 'shell': [4, 6, 8], 'yellow': [12, 13]},
            'grotle': {'leaves': [1, 2, 3], 'body': [10, 11, 12], 'shell': [5, 6, 7], 'yellow': [8, 9]},
            'torterra': {'leaves': [1, 2, 3, 12], 'rocks': [5, 6, 7, 8, 13], 'shell': [9, 10, 11]},
        },
        'variants': [
            {'naam': 'Herfstesdoorn (rood blad, zandsteen)', 'leaves': '#d04820', 'body': '#9a8048',
             'shell': '#6a4020', 'yellow': '#f0a030', 'rocks': '#b08868'},
            {'naam': 'Kersenbloesem (Japanse tuin)', 'leaves': '#f0a0c0', 'body': '#b8a088',
             'shell': '#5a3038', 'yellow': '#f8e0e8', 'rocks': '#d8d0c8'},
            {'naam': 'Galápagosreuzenschildpad (lavarots)', 'leaves': '#285828', 'body': '#88887a',
             'shell': ('#4a4844', DARK), 'yellow': '#c0b498', 'rocks': ('#3c3c48', DARK)},
            {'naam': 'Winterbos (sneeuw op de takken)', 'leaves': '#e0ecf0', 'body': '#7890a8',
             'shell': '#5c5268', 'yellow': '#b8d8f0', 'rocks': '#98c8e8'},
            {'naam': 'Jacaranda (paarse bloesem)', 'leaves': '#9058d0', 'body': '#6a8c70',
             'shell': '#7a4830', 'yellow': '#e0c8f0', 'rocks': '#b8a8c8'},
            {'naam': 'Yggdrasil (gouden wereldboom, smaragd)', 'leaves': ('#e8b828', {'h': 0}), 'body': '#309068',
             'shell': '#704018', 'yellow': '#f8f0a0', 'rocks': '#40b8a0'},
        ],
    },
    'chimchar': {
        # vacht, crème (gezicht/buik/borst), vlam, rode wangen, blauw masker (Monferno/Infernape), goud
        'species': {
            'chimchar': {'fur': [1, 2, 3, 4], 'cream': [6, 7, 8], 'flame': [9, 14, 15], 'marks': [10, 11]},
            'monferno': {'fur': [2, 5, 7, 8], 'cream': [3, 4, 6], 'flame': [1], 'gold': [14], 'mask': [9, 10]},
            'infernape': {'fur': [1, 10, 11], 'cream': [12, 13, 14], 'flame': [6, 7, 15], 'gold': [4, 5, 9],
                          'mask': [2, 8]},
        },
        'variants': [
            {'naam': 'Ringstaartmaki (grijs, gele vlam)', 'fur': '#7c7a80', 'cream': '#f0eee4', 'flame': '#f8d040',
             'marks': '#383838', 'gold': '#e8e8f0', 'mask': '#303038'},
            {'naam': 'Blauw vuur (gasbrander)', 'fur': '#4c3024', 'cream': '#c8b090', 'flame': '#3080f0',
             'marks': '#40c0e8', 'gold': '#a8c8e0', 'mask': '#20b8c8'},
            {'naam': 'Goudkopleeuwaapje (rood vuur)', 'fur': '#e8a020', 'cream': '#f8e8c0', 'flame': '#d82020',
             'marks': '#8a2010', 'gold': '#f8f0c0', 'mask': '#3a3040'},
            {'naam': 'Wildfire (groen vuur, Game of Thrones)', 'fur': '#3c443a', 'cream': '#a8b49c', 'flame': '#40e040',
             'marks': '#20a030', 'gold': '#c8c060', 'mask': '#206030'},
            {'naam': 'Javaanse lutung (zwart, oranje vuur)', 'fur': ('#34343c', DARK), 'cream': '#9898a8',
             'flame': '#f08020', 'marks': '#f0a020', 'gold': '#c0c0c8', 'mask': '#e06818'},
            {'naam': 'Hanuman (wit en goud: zijn brandende staart zette Lanka in vuur)', 'fur': ('#d8cab0', {'l': 1.4}),
             'cream': '#f0d070', 'flame': '#e83018', 'marks': '#d02040', 'gold': ('#e8b020', {'h': 0}),
             'mask': '#c02838'},
        ],
    },
    'piplup': {
        # lijf, lichtblauw (wangen/buik/mantelrand), wit, snavel/kroon/voeten
        'species': {
            'piplup': {'body': [1, 2, 3, 4], 'light': [5, 9, 15], 'white': [6, 7, 8], 'beak': [11, 12, 13, 14]},
            'prinplup': {'body': [6, 7], 'light': [8, 9, 10, 12, 14], 'white': [11, 13], 'beak': [1, 2, 3, 4]},
            'empoleon': {'body': [6, 9], 'light': [7, 8, 10, 12], 'white': [11], 'beak': [1, 2, 3, 4]},
        },
        'variants': [
            {'naam': 'Koningspinguïn (oranje halsvlek)', 'body': '#3c4450', 'light': '#f09030', 'white': '#f4f0e8',
             'beak': '#e86818'},
            {'naam': 'Rotspinguïn (rode snavel, gele kuif)', 'body': '#2c2c34', 'light': '#9898a8',
             'white': '#f0f0f0', 'beak': '#d02828'},
            {'naam': 'Napoleon (groen uniform, rode sjerp, gouden epauletten)', 'body': '#2a5038', 'light': '#c83030',
             'white': '#f4f0e0', 'beak': '#e8c040'},
            {'naam': 'Byzantijnse keizer (purper en goud)', 'body': '#5a2c80', 'light': '#c088e0',
             'white': '#f0e0f8', 'beak': ('#e8b020', {'h': 0})},
            {'naam': 'IJsberg', 'body': '#88b8d8', 'light': '#d8f0f8', 'white': '#f8f8f8', 'beak': '#b8c8d8'},
            {'naam': 'Club Penguin (rood, gouden kroon)', 'body': '#b02028', 'light': '#f07070',
             'white': '#f8f0e0', 'beak': ('#f0c020', {'h': 0})},
        ],
    },
    'starly': {
        # donker verenkleed, grijze vleugels/buik, wit, snavel/poten, kuif (Staraptor)
        'species': {
            'starly': {'dark': [1], 'grey': [3, 11, 12, 13], 'white': [5, 6, 7], 'beak': [8, 9, 10]},
            'staravia': {'dark': [1, 2, 11], 'grey': [4, 10], 'white': [5, 6], 'beak': [7, 8, 9]},
            'staraptor': {'dark': [1, 4], 'grey': [2, 7, 8, 9], 'white': [10, 11], 'beak': [12, 13, 14],
                          'crest': [5, 6]},
        },
        'variants': [
            {'naam': 'Spreeuw in zomerkleed (groen-paarse glans, gele snavel)', 'dark': '#2a4038', 'grey': '#5c4468',
             'white': '#e8e0c8', 'beak': '#e8c020', 'crest': '#9040c0'},
            {'naam': 'Driekleurige glansspreeuw (Lamprotornis superbus)', 'dark': '#2060a0', 'grey': '#d87028',
             'white': '#f4f0f0', 'beak': '#404040', 'crest': '#30b0d0'},
            {'naam': 'Roze spreeuw', 'dark': ('#2c2830', DARK), 'grey': '#e098b0', 'white': '#f8dce4',
             'beak': '#f0a0a0', 'crest': '#e06090'},
            {'naam': 'Balispreeuw (wit, blauw gezicht)', 'dark': ('#a8a8b4', {'l': 1.5}), 'grey': ('#dcdce4', {'l': 1.5}), 'white': '#f8f8f8',
             'beak': '#d8c070', 'crest': '#3080e0'},
            {'naam': 'Ekster (zwart-wit met blauwe glans)', 'dark': ('#24242a', DARK), 'grey': '#2c58a8',
             'white': '#f4f4f4', 'beak': '#505058', 'crest': '#3070d0'},
            {'naam': 'Quetzal (smaragd met rode borst, heilige vogel van de Maya)', 'dark': '#20985a', 'grey': '#c02030',
             'white': '#f0ecd0', 'beak': '#f0d040', 'crest': '#40d880'},
        ],
    },
    'bidoof': {
        # vacht, crème gezicht/buik, donkere snuit/staart
        'species': {
            'bidoof': {'body': [1, 2, 3], 'cream': [6, 7], 'dark': [9]},
            'bibarel': {'body': [1, 2, 4], 'cream': [5, 6], 'dark': [9, 12]},
        },
        'variants': [
            {'naam': 'Zwarte bever (melanistisch)', 'body': ('#3c3430', DARK), 'cream': '#a89880', 'dark': '#201c1c'},
            {'naam': 'Goudhamster', 'body': '#e0a040', 'cream': '#f8f0e0', 'dark': '#a06030'},
            {'naam': 'Grijze eekhoorn', 'body': '#808088', 'cream': '#f0f0e8', 'dark': '#505058'},
            {'naam': 'Rode eekhoorn', 'body': '#c04818', 'cream': '#f8e0c0', 'dark': '#702810'},
            {'naam': 'Bemoste moerasbever', 'body': '#6a7a40', 'cream': '#d0d8a0', 'dark': '#3a4a28'},
            {'naam': 'God Bidoof (Arceus-wit met goud)', 'body': '#e4e4dc', 'cream': '#f0d060', 'dark': '#b08828'},
        ],
    },
    'kricketot': {
        # rood (Kricketot: jasje, Kricketune: lijf), donker lijf, geel/crème (snor, kraag), bruin
        'species': {
            'kricketot': {'red': [7, 8, 9], 'body': [1, 2, 3], 'yellow': [5, 6, 10], 'brown': [11, 12]},
            'kricketune': {'red': [1, 2, 3], 'body': [5, 6, 8], 'yellow': [9, 10, 11, 12, 13]},
        },
        'variants': [
            {'naam': 'Groene sabelsprinkhaan', 'red': '#40a040', 'body': '#4c5838', 'yellow': '#d0e070',
             'brown': '#506028'},
            {'naam': 'Paarse boomkrekel', 'red': '#7040a0', 'body': '#403848', 'yellow': '#e0d0f0',
             'brown': '#503070'},
            {'naam': 'Blauwvleugelsprinkhaan', 'red': '#3070d0', 'body': '#5c5864', 'yellow': '#c0d0f0',
             'brown': '#304878'},
            {'naam': 'Japie Krekel (groen met zwarte slipjas)', 'red': ('#2c2c34', DARK), 'body': '#5a9a40',
             'yellow': '#e8c040', 'brown': '#c03028'},
            {'naam': 'Holenkrekel (bleek, blind)', 'red': '#e0d0c0', 'body': '#a8a098', 'yellow': '#f8f0e0',
             'brown': '#b09880'},
            {'naam': 'Chinese gelukskrekel (goud op lak)', 'red': ('#d8a020', {'h': 0}), 'body': '#782020',
             'yellow': '#f8e8a0', 'brown': '#a01818'},
        ],
    },
    'shinx': {
        # blauwe vacht, donkere manen/lijf, gele sterren/ringen, ogen
        'species': {
            'shinx': {'blue': [1, 2, 3], 'dark': [11, 12], 'yellow': [4, 6, 7], 'eyes': [9, 10]},
            'luxio': {'blue': [8, 9, 10], 'dark': [5, 6, 7], 'yellow': [1, 2, 3], 'eyes': [12, 13]},
            'luxray': {'blue': [8, 9, 12], 'dark': [4, 5, 7], 'yellow': [1, 2, 6], 'eyes': [10, 11]},
        },
        'variants': [
            {'naam': 'Euraziatische lynx', 'blue': '#a88a68', 'dark': '#4c4038', 'yellow': '#ece4d4',
             'eyes': '#40a040'},
            {'naam': 'Witte tijger (blauwe sterren)', 'blue': ('#e0e0e8', {'l': 1.4}), 'dark': ('#303038', DARK),
             'yellow': '#4890f0', 'eyes': '#183890'},
            {'naam': 'Pink Panther', 'blue': '#e890b0', 'dark': '#a04870', 'yellow': '#f8f0f0', 'eyes': '#e8c030'},
            {'naam': 'Garfield (oranje kater met zwarte strepen)', 'blue': '#e87424', 'dark': ('#3a2418', DARK),
             'yellow': '#f8f0d0', 'eyes': '#f8f8f8'},
            {'naam': 'Tron (zwart, cyaan, oranje)', 'blue': '#30d8f0', 'dark': ('#1c1c28', DARK), 'yellow': '#f08020',
             'eyes': '#f08020'},
            {'naam': 'Raijin (rode donderdemon)', 'blue': '#c83028', 'dark': ('#283028', DARK), 'yellow': '#f0d040',
             'eyes': '#f0d040'},
        ],
    },
    'cranidos': {
        # blauwe schedel, grijs lijf, witte stekels
        'species': {
            'cranidos': {'head': [4, 6, 7, 11], 'body': [8, 9, 10, 12], 'spikes': [1, 2, 3]},
            'rampardos': {'head': [5, 6, 8, 9], 'body': [7, 10, 11, 12], 'spikes': [1, 2, 4]},
        },
        'variants': [
            {'naam': 'Pachycephalosaurus (museumreconstructie: groen en bruin)', 'head': '#4a8040',
             'body': '#7a6850', 'spikes': '#e8e0c8'},
            {'naam': 'Dikhoornschaap (ram)', 'head': '#a07850', 'body': '#c8b8a0', 'spikes': '#f0e8d8'},
            {'naam': 'Komeetinslag (gloeiende kop, zwart lijf)', 'head': '#f07818', 'body': ('#3c3a3a', DARK),
             'spikes': '#f0c040'},
            {'naam': 'IJstijd (diepgevroren fossiel)', 'head': '#90c0e8', 'body': '#e0e4ec', 'spikes': '#f8f8f8'},
            {'naam': 'Amethistgeode', 'head': '#8040c0', 'body': '#605870', 'spikes': '#e0d0f8'},
            {'naam': 'Toetanchamon (goud en lapis lazuli)', 'head': ('#e0b030', {'h': 0}), 'body': '#2c4ca0',
             'spikes': '#f4f0e0'},
        ],
    },
    'shieldon': {
        # schild/kop, lichte schildrand, okerkleurig lijf/vensters
        'species': {
            'shieldon': {'shield': [1, 2], 'light': [4, 5], 'tan': [7, 8, 9, 11]},
            'bastiodon': {'shield': [1, 3, 5, 6], 'light': [2], 'tan': [7, 8, 9]},
        },
        'variants': [
            {'naam': 'Triceratops (groen schild, oker)', 'shield': '#4a6a40', 'light': '#a0b890', 'tan': '#d8b878'},
            {'naam': 'Kasteel van baksteen', 'shield': '#8a3a28', 'light': '#d8a088', 'tan': '#e8d8b0'},
            {'naam': 'Ridderharnas (gepoetst zilver, blauw wapen)', 'shield': '#a8b0c0', 'light': '#f0f4f8',
             'tan': '#5070b0'},
            {'naam': 'Jade (keizerlijk China)', 'shield': '#2a8060', 'light': '#a0e0c0', 'tan': '#e0c060'},
            {'naam': 'Obsidiaan met gloeiende lava', 'shield': ('#2c2a32', DARK), 'light': '#e05020',
             'tan': '#f0a030'},
            {'naam': 'Captain America-schild', 'shield': '#2850a0', 'light': '#f0f0f0', 'tan': '#c02828'},
        ],
    },
    'combee': {
        # honing (geel), oranje (Combee-rand, Vespiquens rok), vleugels, zwart lijf, rode edelsteen
        'species': {
            'combee': {'honey': [7, 8, 9, 10, 12, 13], 'orange': [6, 11], 'wings': [3, 4, 5], 'dark': [2]},
            'vespiquen': {'honey': [6, 8, 9], 'orange': [11, 13, 14], 'wings': [1, 2, 5, 15], 'dark': [4, 7],
                          'jewel': [10, 12]},
        },
        'variants': [
            {'naam': 'Boekweithoning (donkere honing)', 'honey': '#8a4a18', 'orange': '#40200c',
             'wings': '#e8e0d0', 'dark': '#302020', 'jewel': '#f0c040'},
            {'naam': 'Orchideebij (smaragdgroene metaalglans)', 'honey': '#30a060', 'orange': '#2070a0',
             'wings': '#d0f0e8', 'dark': '#204038', 'jewel': '#f0d040'},
            {'naam': 'Koninginnengelei (crème)', 'honey': '#f0e8c8', 'orange': '#e8b8a0', 'wings': '#f8f8f8',
             'dark': '#706860', 'jewel': '#e05080'},
            {'naam': 'Paarse houtbij', 'honey': '#7040a8', 'orange': '#402860', 'wings': '#c8b8e8',
             'dark': '#28203a', 'jewel': '#f0c030'},
            {'naam': 'Goudwesp (Chrysis: metaalrood en blauw)', 'honey': '#c02838', 'orange': '#2050c0',
             'wings': '#e0e0f0', 'dark': '#203060', 'jewel': '#30d0f0'},
            {'naam': 'Kristalhoning (diamant)', 'honey': '#a8e0f0', 'orange': '#3060c0', 'wings': '#ffffff',
             'dark': '#283048', 'jewel': '#e03070'},
        ],
    },
    'pachirisu': {
        # blauwe vacht, witte vacht, gele wangen
        'species': {
            'pachirisu': {'blue': [1, 2, 3], 'white': [4, 5, 7, 8], 'cheeks': [9, 11]},
        },
        'variants': [
            {'naam': 'Vliegende eekhoorn (grijsbruin)', 'blue': '#8a7868', 'white': '#f0e8dc', 'cheeks': '#f0d060'},
            {'naam': 'Emolga-kleuren (zwart, wit, geel)', 'blue': ('#34343c', DARK), 'white': '#f4f4f0',
             'cheeks': '#f8d030'},
            {'naam': 'Muntchocolade', 'blue': '#60c8a8', 'white': '#f0fff8', 'cheeks': '#7a4a30'},
            {'naam': 'Plusle-rood', 'blue': '#d02838', 'white': '#fff4f0', 'cheeks': '#f8d030'},
            {'naam': 'Aurora (paars met cyaan wangen)', 'blue': '#8060d0', 'white': '#e8e0f8', 'cheeks': '#60e0f0'},
            {'naam': 'Pikachu-kloon (geel, rode wangen, bruine streep)', 'blue': '#a06030', 'white': '#f8d850',
             'cheeks': '#e03030'},
        ],
    },
    'buizel': {
        # oranje vacht, crème, gele zwemband, blauwe vinnen
        'species': {
            'buizel': {'orange': [1, 2, 3, 14], 'cream': [6, 8], 'float': [12, 13], 'fins': [5, 7]},
            'floatzel': {'orange': [1, 2, 3, 14], 'cream': [5, 6], 'float': [7, 9, 11], 'fins': [12, 13]},
        },
        'variants': [
            {'naam': 'Zeeotter (donkerbruin, crème kop)', 'orange': '#5a3a28', 'cream': '#e8dcc0',
             'float': '#c89040', 'fins': '#4070a0'},
            {'naam': 'Hermelijn in winterkleed', 'orange': ('#c4c4d0', {'l': 1.8}), 'cream': ('#f8f8f0', {'l': 1.3}), 'float': ('#b8c4d4', {'l': 1.3}),
             'fins': '#34343c'},
            {'naam': 'Reddingsboei (rood en wit)', 'orange': '#c82828', 'cream': '#f8f0e8', 'float': '#f4f4f4',
             'fins': '#f0a020'},
            {'naam': 'Tropische lagune (turquoise, koraal)', 'orange': '#30a8b0', 'cream': '#f0e8d0',
             'float': '#f08070', 'fins': '#f0d040'},
            {'naam': 'Zwarte nerts', 'orange': ('#302828', DARK), 'cream': '#a09088', 'float': '#c0a050',
             'fins': '#60c0e0'},
            {'naam': 'Kawauso (Japanse otter-yokai: paars met jade)', 'orange': '#704898', 'cream': '#e8d8f0',
             'float': '#f0c040', 'fins': '#40d0c0'},
        ],
    },
    'cherubi': {
        # kers/bloemblad (roze), bladeren, gesloten paarse kelk (Cherrim), geel gezicht (zonvorm)
        'species': {
            'cherubi': {'pink': [7, 8, 9, 10, 12], 'leaves': [1, 2, 4, 5]},
            'cherrim': {'pink': [1, 2, 3, 5], 'leaves': [6, 7, 8, 9], 'purple': [10, 11, 12, 13]},
            'cherrim/sunshine': {'pink': [1, 2, 3, 5, 6, 7, 8], 'face': [9, 10, 11], 'leaves': [12, 13]},
        },
        'variants': [
            {'naam': 'Rainier-kers (geel met blos)', 'pink': '#f0c040', 'leaves': '#4a8a3a', 'purple': '#c06830',
             'face': '#f8e8c0'},
            {'naam': 'Morel (zwarte kers)', 'pink': '#5a1828', 'leaves': '#3a6030', 'purple': ('#2c1c30', DARK),
             'face': '#e8c0d0'},
            {'naam': 'Witte sakura (Shirotae)', 'pink': ('#dcc0cc', {'l': 1.6}), 'leaves': '#80b060', 'purple': '#c8a8c0',
             'face': '#f8d0e0'},
            {'naam': 'Kruisbes', 'pink': '#90c040', 'leaves': '#3a6028', 'purple': '#507020', 'face': '#f0f0a0'},
            {'naam': 'Herfstkers (rood met oranje blad)', 'pink': '#c02020', 'leaves': '#d07020',
             'purple': '#702818', 'face': '#f0b040'},
            {'naam': 'Maanbloem (nachtblauw met zilver)', 'pink': '#283870', 'leaves': '#3a7890',
             'purple': ('#141c40', DARK), 'face': '#e0e8f8'},
        ],
    },
    'drifloon': {
        # ballonlijf, lichte onderkant (Drifblim), wolkje, geel kruis/handen, rode vlekjes
        'species': {
            'drifloon': {'body': [5, 6, 7, 8, 9], 'puff': [1, 2, 3], 'yellow': [10, 11, 12]},
            'drifblim': {'body': [5, 6, 7, 8], 'light': [13, 14], 'puff': [1, 2, 3], 'yellow': [10, 11, 12],
                         'red': [9, 15]},
        },
        'variants': [
            {'naam': 'Pennywise-ballon (IT)', 'body': '#c82028', 'light': '#e86068', 'puff': '#f4f4f4',
             'yellow': '#f0d040', 'red': '#303030'},
            {'naam': 'Up (Pixar: blauwe ballon)', 'body': '#3070d0', 'light': '#80b0f0', 'puff': '#f8f8f8',
             'yellow': '#f8a020', 'red': '#f0d040'},
            {'naam': 'Kauwgombel', 'body': '#f080b0', 'light': '#f8c0d8', 'puff': '#f8f0f8', 'yellow': '#60c0e0',
             'red': '#a03070'},
            {'naam': 'Oudejaarsballon (zwart met goud)', 'body': ('#2e2e38', DARK), 'light': '#606070',
             'puff': '#f0d050', 'yellow': '#f0d040', 'red': '#e04040'},
            {'naam': 'Dwaallicht (cyaan gloed)', 'body': '#40c0c0', 'light': '#a0f0e8', 'puff': '#e0fff8',
             'yellow': '#f0f8a0', 'red': '#3060c0'},
            {'naam': "Jack-o'-lantern (oranje met groen steeltje)", 'body': '#e87018', 'light': '#f8b040',
             'puff': '#4a8a30', 'yellow': '#f8e040', 'red': '#402010'},
        ],
    },
    'buneary': {
        # bruine vacht, crème pluis, roze oren/neus
        'species': {
            'buneary': {'brown': [4, 5, 7, 12], 'cream': [1, 2, 3], 'pink': [8, 9, 10]},
            'lopunny': {'brown': [4, 5, 6], 'cream': [1, 2, 8, 10], 'pink': [7, 9, 12]},
        },
        'variants': [
            {'naam': 'Hollander (zwart-wit konijn)', 'brown': ('#34343c', DARK), 'cream': '#f4f4f0', 'pink': '#f0a0b0'},
            {'naam': 'Chinchilla-konijn (blauwgrijs)', 'brown': '#7a7a88', 'cream': '#d8d0e0', 'pink': '#e080a0'},
            {'naam': 'Paaseitje (mint)', 'brown': '#50b090', 'cream': '#f0f8e8', 'pink': '#f0a0b0'},
            {'naam': 'Albino (rode ogen)', 'brown': ('#e4e0dc', ALBINO), 'cream': '#f8f4ec', 'pink': '#e04060'},
            {'naam': 'Maanhaas (Japanse mochi-maan: nachtblauw met goud)', 'brown': '#2c3c70', 'cream': '#f0d870',
             'pink': '#f0f0f0'},
            {'naam': 'Jaar van het Konijn (rood en goud)', 'brown': '#b82828', 'cream': ('#f0c040', {'h': 0}),
             'pink': '#f8e8a0'},
        ],
    },
    'glameow': {
        # vacht, wit, roze oren, paarse oren/staart (Purugly), ogen
        'species': {
            'glameow': {'body': [6, 7, 8, 11], 'white': [3, 4, 5], 'pink': [9, 10, 12], 'eyes': [13, 14]},
            'purugly': {'body': [4, 5, 7, 9], 'purple': [2, 3], 'white': [10, 14, 15], 'pink': [6, 8],
                        'eyes': [12, 13]},
        },
        'variants': [
            {'naam': 'Rode kater', 'body': '#d07830', 'white': '#f8f0e0', 'pink': '#f090a0', 'purple': '#a04018',
             'eyes': '#40a040'},
            {'naam': 'Heksenkat (zwart, gele ogen)', 'body': ('#303038', DARK), 'white': '#8888a0', 'pink': '#9050c0',
             'purple': '#6030a0', 'eyes': '#f0d020'},
            {'naam': 'Siamees (donkere punten, blauwe ogen)', 'body': '#d8c8a8', 'white': '#f8f0e0', 'pink': '#e0a0a0',
             'purple': '#4a3020', 'eyes': '#3080f0'},
            {'naam': 'Kat van Cheshire', 'body': '#c060b0', 'white': '#f0d0f0', 'pink': '#f0e060',
             'purple': '#602878', 'eyes': '#f0e060'},
            {'naam': 'Doraemon (blauw-wit, rode neus, gouden belletje)', 'body': '#2890e0', 'white': '#f8f8f8',
             'pink': '#e02030', 'purple': '#f0d020', 'eyes': '#303030'},
            {'naam': 'Hello Kitty (wit met rode strik)', 'body': '#e4e4ea', 'white': '#f8f8f8', 'pink': '#f04090',
             'purple': '#f04090', 'eyes': '#303030'},
        ],
    },
    'stunky': {
        # vacht, rugstreep, oranje neus/ogen
        'species': {
            'stunky': {'fur': [1, 3, 7], 'stripe': [4, 5, 6], 'orange': [8, 9]},
            'skuntank': {'fur': [1, 2, 3, 5], 'stripe': [6, 7, 8], 'orange': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Gewoon stinkdier (zwart-wit)', 'fur': ('#2c2c34', DARK), 'stripe': '#f4f4f0', 'orange': '#e04040'},
            {'naam': 'Gifgroen (giftig afval)', 'fur': '#3a6030', 'stripe': '#c0f040', 'orange': '#f040c0'},
            {'naam': 'Rode panda', 'fur': '#a04018', 'stripe': '#f0e8d8', 'orange': '#303030'},
            {'naam': 'Vuilnisbelt (bruin met groene walm)', 'fur': '#5a4a30', 'stripe': '#c8b070', 'orange': '#90f040'},
            {'naam': 'Zwavel (geel met zwarte streep)', 'fur': ('#c8a020', {'h': 0}), 'stripe': '#3a3228',
             'orange': '#e04020'},
            {'naam': 'Kosmische nevel (blauw met roze streep)', 'fur': '#203880', 'stripe': '#f080c0',
             'orange': '#f0f040'},
        ],
    },
    'bronzor': {
        # metaal, lichte band (Bronzong), ogen/ornamenten
        'species': {
            'bronzor': {'metal': [1, 2, 3, 4, 8], 'eyes': [6, 7]},
            'bronzong': {'metal': [1, 2, 3, 4, 6, 10], 'band': [7, 8, 9], 'eyes': [11, 12]},
        },
        'variants': [
            {'naam': 'Gepolijst brons', 'metal': '#a86830', 'band': '#e0c890', 'eyes': '#40d0c0'},
            {'naam': 'Gietijzer (Japanse tetsubin)', 'metal': ('#3a3a42', DARK), 'band': '#a0a0a8', 'eyes': '#e04020'},
            {'naam': 'Amethist', 'metal': '#7848b0', 'band': '#e0d0f0', 'eyes': '#f0d040'},
            {'naam': 'Zilveren tempelbel', 'metal': '#a8b0c0', 'band': '#f0f4f8', 'eyes': '#3080e0'},
            {'naam': 'Roségoud', 'metal': '#d08878', 'band': '#f8e0d8', 'eyes': '#c02040'},
            {'naam': 'Liberty Bell in goud', 'metal': ('#d0a030', {'h': 0}), 'band': '#f8f0c0', 'eyes': '#c02030'},
        ],
    },
    'chatot': {
        # kop/staart, wit, snavel/wangen, blauwe vleugels, geel, groen
        'species': {
            'chatot': {'dark': [1, 2, 3], 'white': [5, 6], 'pink': [7, 8], 'blue': [9, 10, 11], 'yellow': [12, 13],
                       'green': [14]},
        },
        'variants': [
            {'naam': 'Afrikaanse grijze roodstaart', 'dark': '#6c6c74', 'white': '#d8d8e0', 'pink': '#d02020',
             'blue': '#8a8a94', 'yellow': '#c02020', 'green': '#404048'},
            {'naam': 'Geelvleugelara (rood, geel, blauw)', 'dark': '#c02020', 'white': '#f0f0e0', 'pink': '#383838',
             'blue': '#2860c0', 'yellow': '#f0c030', 'green': '#30a040'},
            {'naam': 'Geelkuifkaketoe', 'dark': '#e0e0e4', 'white': '#f8f8f8', 'pink': '#404048', 'blue': '#f0e8c0',
             'yellow': '#f0d030', 'green': '#f0d030'},
            {'naam': 'Agapornis (groen met roze kop)', 'dark': '#40a040', 'white': '#f0a090', 'pink': '#e04040',
             'blue': '#3070c0', 'yellow': '#f0e040', 'green': '#20a0c0'},
            {'naam': 'Zonparkiet (geel en oranje)', 'dark': '#f0a020', 'white': '#f8e060', 'pink': '#303030',
             'blue': '#30a050', 'yellow': '#f06020', 'green': '#3060c0'},
            {'naam': 'Gouden plaat (muzieknoot in goud en zwart)', 'dark': '#c09030', 'white': '#f8f0c0',
             'pink': '#c02030', 'blue': ('#303034', DARK), 'yellow': '#f8f8f8', 'green': '#c02030'},
        ],
    },
    'spiritomb': {
        # paarse wervel, groene zielen, gele ogen, sluitsteen
        'species': {
            'spiritomb': {'purple': [1, 2, 10, 11], 'green': [3, 6, 7, 9], 'yellow': [4, 5],
                          'stone': [12, 13, 14, 15]},
        },
        'variants': [
            {'naam': 'Blauw spookvuur', 'purple': '#4060c0', 'green': '#40d0e0', 'yellow': '#f0f8f8', 'stone': '#808890'},
            {'naam': 'Bloedmaan', 'purple': '#a02030', 'green': '#f0a030', 'yellow': '#f8f040', 'stone': '#604040'},
            {'naam': 'Ectoplasma (Slimer)', 'purple': '#50a040', 'green': '#c0f040', 'yellow': '#f0f0a0',
             'stone': '#606850'},
            {'naam': 'Rook en as', 'purple': '#707078', 'green': '#c0c0c8', 'yellow': '#e04040', 'stone': '#504840'},
            {'naam': 'Zwart gat (paarse ogen)', 'purple': ('#2c2838', DARK), 'green': '#7040c0', 'yellow': '#e070f0',
             'stone': '#383040'},
            {'naam': '108 gouden zielen (hitodama)', 'purple': ('#d0a030', {'h': 0}), 'green': '#f8e8a0',
             'yellow': '#ffffff', 'stone': '#a08060'},
        ],
    },
    'gible': {
        # lijf, buik (rood), accent (Gibles vinvlekken, de gele ster), klauwen/stekels blijven wit
        'species': {
            'gible': {'body': [1, 2, 3, 4], 'accent': [6, 9], 'belly': [13, 14]},
            'gabite': {'body': [1, 2, 3, 4, 5, 6], 'belly': [10, 11, 13], 'accent': [8, 9]},
            'garchomp': {'body': [1, 3, 4, 6], 'belly': [12, 13, 14, 15], 'accent': [2, 5]},
        },
        'variants': [
            {'naam': 'Grote witte haai (grijs, witte buik)', 'body': '#707888', 'belly': '#e8e8ec', 'accent': '#c02030'},
            {'naam': 'Bloedrode draak (rood, crème buik)', 'body': '#a02828', 'belly': '#f0c890', 'accent': '#f0d040'},
            {'naam': 'Westerse draak (groen met gouden buik)', 'body': '#3a7a40', 'belly': '#f0c040',
             'accent': '#c02020'},
            {'naam': 'Megalodon-fossiel (botwit)', 'body': ('#c8bca8', {'l': 1.5}), 'belly': ('#806048', {'l': 1.3}), 'accent': '#303030'},
            {'naam': 'Alduin (zwarte draak met lava)', 'body': ('#2e2a32', DARK), 'belly': '#e05010',
             'accent': '#f0d040'},
            {'naam': 'King Ghidorah (goud)', 'body': ('#d0a030', {'h': 0}), 'belly': '#b02030', 'accent': '#f8f0c0'},
        ],
    },
    'riolu': {
        # blauwe aura-vacht, zwart, crème borst (Lucario), geel (Riolu)
        'species': {
            'riolu': {'blue': [2, 3, 4], 'black': [5, 6], 'cream': [10, 11]},
            'lucario': {'blue': [1, 2, 4], 'black': [5, 6, 7], 'cream': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Zilvervos', 'blue': '#a0a0b0', 'black': ('#303038', DARK), 'cream': '#f4f4f4'},
            {'naam': 'Rode vos-aura', 'blue': '#c83020', 'black': '#383030', 'cream': '#f0e0c0'},
            {'naam': 'Groene aura (jade)', 'blue': '#30a050', 'black': '#404040', 'cream': '#e0f0a0'},
            {'naam': 'Shiba Inu', 'blue': '#e08030', 'black': '#f0e8d8', 'cream': '#f8f0e0'},
            {'naam': 'Paarse aura (meditatie)', 'blue': '#8048c8', 'black': '#383040', 'cream': '#e0d0f0'},
            {'naam': 'Sakura-aura (roze)', 'blue': '#f080b0', 'black': '#504050', 'cream': '#fff0f8'},
        ],
    },
    'hippopotas': {
        # zandkleur, bruin (Hippopotas: kop) / donker (Hippowdon), zandhoop, roze snuit/bek
        'species': {
            'hippopotas': {'tan': [6, 7, 8, 9], 'dark': [1, 3, 4], 'pink': [12, 13, 14]},
            'hippowdon': {'dark': [1, 2, 9], 'tan': [5, 6, 13], 'sand': [14, 15], 'pink': [4, 7, 11, 12]},
        },
        'variants': [
            {'naam': 'Nijlpaard (grijs-roze)', 'tan': '#9a8890', 'dark': '#5a4850', 'pink': '#f0a0a8', 'sand': '#d8c090'},
            {'naam': 'Uluru (rode woestijn)', 'tan': '#c86030', 'dark': '#6a2818', 'pink': '#f0c080', 'sand': '#d87040'},
            {'naam': 'Zwart vulkaanzand (IJsland)', 'tan': '#606068', 'dark': ('#2a2a30', DARK), 'pink': '#e07080',
             'sand': '#505058'},
            {'naam': 'White Sands (gipsduinen)', 'tan': '#e4e0d4', 'dark': '#8a8478', 'pink': '#f0b0b8',
             'sand': '#f0ece0'},
            {'naam': 'Moerasnijlpaard (bemost)', 'tan': '#6a8a40', 'dark': '#3a4a28', 'pink': '#e8d060',
             'sand': '#8a7040'},
            {'naam': 'Fantasia-nijlpaard (roze tutu)', 'tan': '#f0a0c0', 'dark': '#8a4878', 'pink': '#c02060',
             'sand': '#f8d8e8'},
        ],
    },
    'skorupi': {
        # pantser, witte scharen/klauwen, ogen/edelstenen
        'species': {
            'skorupi': {'body': [4, 6, 7, 9, 10], 'white': [1, 2, 5, 8], 'cyan': [11, 12]},
            'drapion': {'body': [1, 2, 4, 5, 6, 7, 13], 'white': [10, 11, 12], 'cyan': [8, 9]},
        },
        'variants': [
            {'naam': 'Keizerschorpioen (zwart, groen onder UV)', 'body': ('#2e2e36', DARK), 'white': '#a0a8a8',
             'cyan': '#40f0a0'},
            {'naam': 'Schorsschorpioen (bruin)', 'body': '#8a6030', 'white': '#e0c890', 'cyan': '#b8f048'},
            {'naam': 'Bleke woestijnschorpioen', 'body': '#d8d0c0', 'white': '#f8f8f0', 'cyan': '#303030'},
            {'naam': 'Blacklight (cyaan met magenta)', 'body': '#30c0c0', 'white': '#e0fff8', 'cyan': '#a010b0'},
            {'naam': 'Gifgroen', 'body': '#50a030', 'white': '#e0f0b0', 'cyan': '#a01020'},
            {'naam': 'Scorpion King (goud, lapis)', 'body': ('#d0a030', {'h': 0}), 'white': '#f8f0c0',
             'cyan': '#203890'},
        ],
    },
    'croagunk': {
        # lijf, zwarte armen, witte band, wangen/keelzak, gele ogen
        'species': {
            'croagunk': {'body': [1, 3, 4, 15], 'dark': [5, 6], 'white': [12, 13, 14], 'sac': [9, 10, 11],
                         'yellow': [7, 8]},
            'toxicroak': {'body': [1, 3, 4, 13], 'dark': [5, 6], 'white': [11, 12, 15], 'sac': [9, 10, 14],
                          'yellow': [7, 8]},
        },
        'variants': [
            {'naam': 'Roodoogmakikikker (groen, blauwe flanken)', 'body': '#40a040', 'dark': '#2050a0',
             'white': '#f0f0e0', 'sac': '#f08020', 'yellow': '#e02020'},
            {'naam': 'Muay Thai (rode broek, gouden band)', 'body': '#c02828', 'dark': '#303030', 'white': '#f0f0f0',
             'sac': '#f0d040', 'yellow': '#f0f0f0'},
            {'naam': 'Mantella (zwart met oranje)', 'body': ('#303034', DARK), 'dark': '#e07020', 'white': '#c0c0c0',
             'sac': '#f0a020', 'yellow': '#f0d040'},
            {'naam': 'Glaskikker', 'body': '#a8e0a0', 'dark': '#609060', 'white': '#f8f8f0', 'sac': '#f0a0a0',
             'yellow': '#303030'},
            {'naam': 'Kauwgom (roze, cyaan keelzak)', 'body': '#e080b0', 'dark': '#603050', 'white': '#f8f0f8',
             'sac': '#40c0e0', 'yellow': '#f0f040'},
            {'naam': 'Kampioensgordel (goud met bordeaux)', 'body': ('#d0a030', {'h': 0}), 'dark': '#802020',
             'white': '#f8f0d0', 'sac': '#c02020', 'yellow': '#f8f8f8'},
        ],
    },
    'carnivine': {
        # kop, bladeren, bek, gele kraag
        'species': {
            'carnivine': {'head': [1, 2, 4], 'leaves': [3, 9, 11], 'mouth': [7, 8, 10], 'collar': [12, 13, 14]},
        },
        'variants': [
            {'naam': 'Dracula (zwarte vliegenval)', 'head': ('#383038', DARK), 'leaves': '#2a3a28', 'mouth': '#c02030',
             'collar': '#a0a0a8'},
            {'naam': 'Zonnedauw (Drosera)', 'head': '#d07848', 'leaves': '#a04030', 'mouth': '#f8f0f0',
             'collar': '#f0f0f0'},
            {'naam': 'Blauweregen', 'head': '#a8b0f0', 'leaves': '#405090', 'mouth': '#f040a0', 'collar': '#f0e060'},
            {'naam': 'Herfstplant', 'head': '#e0a040', 'leaves': '#805020', 'mouth': '#c02020', 'collar': '#f0e0a0'},
            {'naam': 'Spookplant (Monotropa)', 'head': '#e4e4dc', 'leaves': '#a8a8b0', 'mouth': '#c03040',
             'collar': '#d0d0d8'},
            {'naam': 'Piranha Plant (Mario)', 'head': '#d82020', 'leaves': '#30a030', 'mouth': '#f8f8f8',
             'collar': '#f8f8f8'},
        ],
    },
    'finneon': {
        # lichte schubben, donkere rug, roze lichtvlekken
        'species': {
            'finneon': {'light': [1, 2, 4, 6], 'dark': [3, 10, 11], 'pink': [7, 8, 9]},
            'lumineon': {'light': [1, 3, 4, 5], 'dark': [6, 7], 'pink': [8, 9]},
        },
        'variants': [
            {'naam': 'Zeegras (groen, gele lichtjes)', 'light': '#80d080', 'dark': '#2a6040', 'pink': '#f0e060'},
            {'naam': 'Koi (wit met rood)', 'light': '#f4f0ec', 'dark': '#d03020', 'pink': '#303030'},
            {'naam': 'Gele doktersvis', 'light': '#f0e040', 'dark': '#c0a020', 'pink': '#f8f8f8'},
            {'naam': 'Diepzee-lantaarnvis (zwart, cyaan lichtjes)', 'light': ('#4a4a5c', DARK),
             'dark': ('#181824', DARK), 'pink': '#40f0f0'},
            {'naam': 'Paarse kempvis (betta)', 'light': '#9050d0', 'dark': '#401870', 'pink': '#f0a0f0'},
            {'naam': 'Sluierstaartgoudvis', 'light': ('#f0a020', {'h': 0}), 'dark': '#c04010', 'pink': '#f8f0e0'},
        ],
    },
    'snover': {
        # sneeuw, naalden/bladeren, stam, paarse accenten (Abomasnow)
        'species': {
            'snover': {'snow': [1, 2, 3, 5], 'leaves': [6, 7, 8, 9], 'trunk': [10, 11, 12]},
            'abomasnow': {'leaves': [1, 2, 4], 'snow': [5, 6, 7, 8, 12], 'purple': [9, 10, 11]},
        },
        'variants': [
            {'naam': 'Esdoorn in de eerste sneeuw', 'leaves': '#d06020', 'trunk': '#5a3020', 'purple': '#c02020'},
            {'naam': 'Sakura in de sneeuw', 'leaves': '#f0a0c0', 'trunk': '#4a3038', 'purple': '#e04080'},
            {'naam': 'Blauwspar (Picea pungens)', 'leaves': '#6090b0', 'trunk': '#706860', 'purple': '#f0d040'},
            {'naam': 'Yeti (vuile sneeuw, mos)', 'snow': '#d0c0a8', 'leaves': '#506030', 'trunk': '#3a2a20',
             'purple': '#40a0e0'},
            {'naam': 'IJskoningin (ijsblauw met violet)', 'snow': '#c0e0f8', 'leaves': '#7050c0', 'trunk': '#90b0d8',
             'purple': '#f0f8ff'},
            {'naam': 'Lothlórien (gouden blad, zilveren stam)', 'leaves': ('#e0b030', {'h': 0}), 'snow': '#f8f4e8',
             'trunk': '#c0c0c8', 'purple': '#30a060'},
        ],
    },
    'rotom': {
        # Het oranje lijf is in elke vorm hetzelfde en wisselt per variant; de plasma-aura
        # bepaalt de vorm (zoals Arceus' typekleur) en wisselt alleen bij de basisvorm.
        'species': {
            'rotom': {'body': [3, 4, 5, 6], 'aura': [1, 2, 12]},
            'rotom/fan': {'body': [5, 6, 7, 8]},
            'rotom/frost': {'body': [3, 4, 5, 6]},
            'rotom/heat': {'body': [5, 6, 7, 8]},
            'rotom/mow': {'body': [3, 4, 5, 6]},
            'rotom/wash': {'body': [3, 4, 5, 6]},
        },
        'variants': [
            {'naam': 'Jaren-50-koelkast (crème, wit plasma)', 'body': '#e8dcc0', 'aura': '#e8eef8'},
            {'naam': 'Smeg-retro (mintgroen, roze plasma)', 'body': '#88c8a8', 'aura': '#f0a0c0'},
            {'naam': 'Roestvrij staal (blauw plasma)', 'body': '#a0a8b4', 'aura': '#40a0f0'},
            {'naam': 'Mat zwart premium (rood plasma)', 'body': ('#34343c', DARK), 'aura': '#f04040'},
            {'naam': 'Barbie-keuken (roze, cyaan plasma)', 'body': '#f080b8', 'aura': '#90e8f0'},
            {'naam': 'Fabergé (verguld, paars plasma)', 'body': ('#d0a030', {'h': 0}), 'aura': '#9040e0'},
        ],
    },
    'uxie': {
        # meertrio: kop, lijf/staarten, edelstenen
        'species': {
            'uxie': {'head': [1, 2, 3, 4], 'body': [10, 11, 13], 'gem': [6, 9]},
            'mesprit': {'head': [2, 3, 4, 5], 'body': [8, 10, 11], 'gem': [6, 12]},
            'azelf': {'head': [1, 2, 3, 9], 'body': [10, 11, 13], 'gem': [5, 6, 7]},
        },
        'variants': [
            {'naam': 'Trioruil (elk de kleur van een ander), groene edelsteen', 'uxie:head': '#5890c0',
             'mesprit:head': '#e8b860', 'azelf:head': '#e870a8', 'body': '#a8b8d8', 'gem': '#30c060'},
            {'naam': 'Maanzilver', 'head': '#c4ccd8', 'body': '#6a7088', 'gem': '#4080f0'},
            {'naam': 'Jade-boeddha', 'head': '#40a070', 'body': '#d8e8d8', 'gem': '#f0c030'},
            {'naam': 'Obsidiaan en vuur', 'head': ('#3a3442', DARK), 'body': '#7a7080', 'gem': '#f06020'},
            {'naam': 'Sterrenstof (nachtblauw, gele sterren)', 'head': '#283878', 'body': '#4a5888', 'gem': '#f0e060'},
            {'naam': 'Drie juwelen (robijn, saffier, smaragd op goud)', 'uxie:head': '#c02030',
             'mesprit:head': '#3050d0', 'azelf:head': '#20a050', 'body': ('#e0c060', {'h': 0}), 'gem': '#f8f8f8'},
        ],
    },
    'dialga': {
        # blauw pantser, staal (grijs/wit), hartdiamant
        'species': {
            'dialga': {'blue': [5, 6, 8, 9, 10, 15], 'steel': [1, 3, 4, 7, 12], 'gem': [14]},
            'dialga/origin': {'blue': [1, 2, 5, 6, 7, 9, 11, 14, 15], 'steel': [3, 8, 10], 'gem': [12]},
        },
        'variants': [
            {'naam': 'Bronzen staande klok', 'blue': '#7a4a20', 'steel': '#d8c090', 'gem': '#40c0a0'},
            {'naam': 'Karmozijnen uurwerk (rood met goud)', 'blue': '#8a1c28', 'steel': '#e0c070',
             'gem': '#f8f0a0'},
            {'naam': 'Amethist-uurwerk', 'blue': '#6040a0', 'steel': '#d8c8f0', 'gem': '#40e0f0'},
            {'naam': 'Zilveren chronograaf', 'blue': '#7c8494', 'steel': '#e0e4ec', 'gem': '#2050f0'},
            {'naam': 'Primal Dialga (Mystery Dungeon: zwart met oranje gloed)', 'blue': ('#2a2a30', DARK),
             'steel': '#5a5a64', 'gem': '#f08020'},
            {'naam': 'Gouden zandloper', 'blue': ('#c89830', {'h': 0}), 'steel': '#f8f0c8', 'gem': '#3060f0'},
        ],
    },
    'palkia': {
        # parelwit, paarse banden, donkere platen/poten, parels
        'species': {
            'palkia': {'pearl': [2, 3, 4, 5, 6, 11], 'purple': [8, 9], 'dark': [1, 7, 10], 'gem': [13, 15]},
            'palkia/origin': {'pearl': [3, 5, 6], 'purple': [1, 9, 11, 12], 'dark': [2, 4, 7], 'gem': [13, 14, 15]},
        },
        'variants': [
            {'naam': 'Zwarte Tahiti-parel (groene glans)', 'pearl': ('#5a5868', DARK), 'purple': '#40a080',
             'dark': '#2c2c34', 'gem': '#f0f0f0'},
            {'naam': 'Maanparel (zilver met blauw)', 'pearl': '#c8ccd8', 'purple': '#3050c0', 'dark': '#505868',
             'gem': '#f0f0f0'},
            {'naam': 'Lavalamp (oranje en rood)', 'pearl': '#f0b080', 'purple': '#d03020', 'dark': '#704030',
             'gem': '#f0f040'},
            {'naam': 'Ruimtenevel (indigo met roze)', 'pearl': '#4a4a90', 'purple': '#f070c0', 'dark': '#24244a',
             'gem': '#f0f0a0'},
            {'naam': 'Jade', 'pearl': '#c0e8c8', 'purple': '#208050', 'dark': '#405848', 'gem': '#f0d040'},
            {'naam': 'Parelmoer (cyaan en magenta weerschijn)', 'pearl': '#e8f0f8', 'purple': '#20c0e0',
             'dark': '#8060a0', 'gem': '#f040c0'},
        ],
    },
    'giratina': {
        # donker lijf, grijze buik/poten, gouden pantser, rode strepen
        'species': {
            'giratina': {'dark': [2, 8, 14], 'grey': [10, 11], 'gold': [3, 5, 7, 9, 13], 'red': [1, 4, 6]},
            'giratina/origin': {'dark': [1, 2, 7, 15], 'grey': [11, 12], 'gold': [6, 8, 9, 10, 13],
                                'red': [3, 4, 5]},
        },
        'variants': [
            {'naam': 'Verscheurde Wereld (groen met paars)', 'dark': '#2a4038', 'grey': '#80a090', 'gold': '#60e0a0',
             'red': '#a040e0'},
            {'naam': 'Hellevuur', 'dark': '#3a1c18', 'grey': '#a07060', 'gold': '#f07020', 'red': '#f8e040'},
            {'naam': 'Spookpaars (cyaan strepen)', 'dark': '#3a2a58', 'grey': '#a090c0', 'gold': '#e0c8f0',
             'red': '#40e0f0'},
            {'naam': 'Albinogeest (wit lijf, rode strepen)', 'dark': '#c4c4cc', 'grey': '#f0f0f4', 'gold': '#e8d8a0',
             'red': '#e03040'},
            {'naam': 'Zwart gat (zilveren pantser)', 'dark': ('#1c1c22', DARK), 'grey': '#505058', 'gold': '#e4e4ec',
             'red': '#c01010'},
            {'naam': 'Keizerlijk (bordeaux met goud, cyaan strepen)', 'dark': '#601828', 'grey': '#e0b0c0',
             'gold': '#f0d860', 'red': '#30c0f0'},
        ],
    },
    'heatran': {
        # lijf, staal, gloeiende vlekken, ogen
        'species': {
            'heatran': {'body': [1, 2, 3], 'steel': [5, 6, 7, 10, 12], 'glow': [8, 9], 'eyes': [13, 14]},
        },
        'variants': [
            {'naam': 'Kawah Ijen (blauw vuur)', 'body': '#283c78', 'steel': '#a0a8b8', 'glow': '#40c0f0',
             'eyes': '#40c0f0'},
            {'naam': 'Kopervuur (groen)', 'body': '#305a40', 'steel': '#c8b090', 'glow': '#60f080', 'eyes': '#60f080'},
            {'naam': 'Obsidiaan', 'body': ('#2c2a32', DARK), 'steel': '#707078', 'glow': '#f0a020', 'eyes': '#f04020'},
            {'naam': 'Witheet', 'body': '#e0d0c0', 'steel': '#f0f0f0', 'glow': '#f8f060', 'eyes': '#f08020'},
            {'naam': 'Paarse magma', 'body': '#5a2878', 'steel': '#9090a8', 'glow': '#e060f0', 'eyes': '#f0e040'},
            {'naam': 'Gesmolten goud', 'body': '#a07020', 'steel': ('#e0b840', {'h': 0}), 'glow': '#f8f8f8',
             'eyes': '#30a0f0'},
        ],
    },
    'regigigas': {
        # lijf, gouden banden, mos, donkere delen
        'species': {
            'regigigas': {'body': [8, 11, 12], 'gold': [1, 3, 4], 'moss': [2, 6, 7], 'dark': [9, 10, 15]},
        },
        'variants': [
            {'naam': 'Jadetempel (groene banden, gouden mos)', 'body': '#e0e8d8', 'gold': '#40a070',
             'moss': '#e8c040', 'dark': '#2a4038'},
            {'naam': 'Zwart graniet met zilver', 'body': '#686870', 'gold': '#d0d4e0', 'moss': '#3a6040',
             'dark': '#2a2a30'},
            {'naam': 'Regice-ijs', 'body': '#d0e8f8', 'gold': '#70b0e0', 'moss': '#f4f8ff', 'dark': '#305078'},
            {'naam': 'Regirock-lava', 'body': '#a89488', 'gold': '#e05020', 'moss': '#403028', 'dark': '#5a3020'},
            {'naam': 'Kersenbloesem (mos wordt bloesem)', 'body': '#f4f0f0', 'gold': '#b07858', 'moss': '#f0a0c0',
             'dark': '#5a4058'},
            {'naam': 'Regieleki (donker met geel en cyaan)', 'body': '#4a5262', 'gold': '#f0e040', 'moss': '#40e0f0',
             'dark': '#202430'},
        ],
    },
    'cresselia': {
        # maansikkel (goud), roze linten, blauw lijf
        'species': {
            'cresselia': {'moon': [1, 3, 4, 5], 'pink': [6, 7, 8, 9, 10], 'blue': [12, 13, 14]},
        },
        'variants': [
            {'naam': 'Zilveren sikkel', 'moon': '#c8ccd8', 'pink': '#7080c0', 'blue': '#e4e4f0'},
            {'naam': 'Bloedmaan', 'moon': '#c03020', 'pink': '#601828', 'blue': '#f0a080'},
            {'naam': 'Oogstmaan', 'moon': '#f09030', 'pink': '#a04818', 'blue': '#f8d8a0'},
            {'naam': 'Nieuwe maan (donker)', 'moon': '#4a5060', 'pink': ('#24284a', DARK), 'blue': '#6070a0'},
            {'naam': 'Blauwe maan', 'moon': '#80b0f0', 'pink': '#3050c0', 'blue': '#c0e0f8'},
            {'naam': 'Kaguya-hime (maanprinses: wit met rood)', 'moon': '#f4ece0', 'pink': '#c02040',
             'blue': '#ececf4'},
        ],
    },
    'manaphy': {
        # blauw lijf, gele antennes/ogen (Manaphy), rode edelsteen
        'species': {
            'phione': {'blue': [1, 2, 3, 5, 6, 7, 8], 'gem': [12, 13, 14]},
            'manaphy': {'blue': [1, 2, 3, 5, 6, 7], 'yellow': [8, 9], 'gem': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Zeeanemoon (roze)', 'blue': '#f080a8', 'yellow': '#f0f060', 'gem': '#40c0e0'},
            {'naam': 'Zeewier (smaragd)', 'blue': '#40b070', 'yellow': '#f0d040', 'gem': '#e03030'},
            {'naam': 'Koraalrif (oranje, witte ogen)', 'blue': '#f08030', 'yellow': '#f8f8f8', 'gem': '#3070e0'},
            {'naam': 'Diepzee (nachtblauw met gloed)', 'blue': '#283070', 'yellow': '#40f0e0', 'gem': '#f040f0'},
            {'naam': 'Parel', 'blue': '#e4e4ee', 'yellow': '#f0d0e0', 'gem': '#3080f0'},
            {'naam': 'Zeekoning (goud met robijn)', 'blue': ('#e0b030', {'h': 0}), 'yellow': '#f8f8f8',
             'gem': '#c02040'},
        ],
    },
    'darkrai': {
        # donker lijf, witte pluim, rode kraag, cyaan oog
        'species': {
            'darkrai': {'body': [3, 5], 'plume': [1, 2, 6], 'collar': [7, 8, 12], 'eye': [9, 10]},
        },
        'variants': [
            {'naam': 'Smeulende nachtmerrie (rookgrijs met oranje gloed)', 'body': '#585860', 'plume': '#f0a040',
             'collar': '#f06020', 'eye': '#f0d040'},
            {'naam': 'Wit spook (negatief)', 'body': '#c4c4cc', 'plume': '#3a3a44', 'collar': '#c02030',
             'eye': '#c02030'},
            {'naam': 'Bloednacht (rood lijf, zwarte kraag)', 'body': '#601818', 'plume': '#e0a0a0', 'collar': '#2a2a2a',
             'eye': '#f0f040'},
            {'naam': 'Bosgeest (donkergroen, groene vlam)', 'body': '#1c3828', 'plume': '#a0e0b0', 'collar': '#40f060',
             'eye': '#f0f040'},
            {'naam': 'Kosmische nachtmerrie (nachtblauw, cyaan)', 'body': '#18204a', 'plume': '#80c0f0',
             'collar': '#40f0f0', 'eye': '#f040f0'},
            {'naam': 'Gouden droom (Cresselia-kleuren)', 'body': ('#c8a040', {'h': 0}), 'plume': '#f0d0f0',
             'collar': '#c058a0', 'eye': '#5068b0'},
        ],
    },
    'shaymin': {
        # gras, bloem, witte vacht, gele stipjes (landvorm)
        'species': {
            'shaymin': {'grass': [1, 2, 3, 11, 13, 14], 'flower': [5, 6, 12], 'white': [8, 9, 15], 'dots': [4]},
            'shaymin/sky': {'grass': [1, 2, 3, 10, 11], 'white': [4, 5, 7, 8], 'flower': [12, 13, 14]},
        },
        'variants': [
            {'naam': 'Lavendelveld', 'grass': '#90a880', 'flower': '#9060d0', 'white': '#f0f0f8', 'dots': '#f8f8f8'},
            {'naam': 'Zonnebloem', 'grass': '#507a28', 'flower': '#f0c020', 'white': '#f8f0d8', 'dots': '#704010'},
            {'naam': 'Herfstveld', 'grass': '#c08030', 'flower': '#c02028', 'white': '#f0e8d8', 'dots': '#f0d040'},
            {'naam': 'Korenbloem', 'grass': '#a0c060', 'flower': '#3060e0', 'white': '#f0f4f8', 'dots': '#f8f8f8'},
            {'naam': 'Edelweiss (sneeuwveld)', 'grass': '#b8ccd8', 'flower': '#f8f8f0', 'white': '#e0e8f0',
             'dots': '#f0d040'},
            {'naam': 'Klimt (goud met lapis)', 'grass': ('#c8a030', {'h': 0}), 'flower': '#2860c0', 'white': '#f8f0d0',
             'dots': '#c02020'},
        ],
    },
    'burmy': {
        # alleen de plantmantel (zand- en afvalmantel zijn zelf al kleurvormen); Mothim: vleugels
        'species': {
            'burmy': {'cloak': [6, 7, 8], 'body': [2, 3, 4]},
            'wormadam': {'cloak': [5, 7, 9, 10, 11, 12], 'body': [2, 3, 4]},
            'mothim': {'wings': [1, 2, 3, 4, 5, 7], 'body': [8, 9, 10, 11, 12, 13]},
        },
        'variants': [
            {'naam': 'Esdoornblad', 'cloak': '#b84820', 'body': '#6a5a50', 'wings': '#d04020'},
            {'naam': 'Blauwgroen mos', 'cloak': '#2a7a70', 'body': '#4a5868', 'wings': '#40a090'},
            {'naam': 'Lunamot (lichtgroen)', 'cloak': '#a8e090', 'body': '#d8e0d0', 'wings': '#b8f0a0'},
            {'naam': 'Lavendelmot', 'cloak': '#8060b0', 'body': '#605870', 'wings': '#a080d0'},
            {'naam': 'Sneeuwmantel (witte mot)', 'cloak': '#e4eaee', 'body': '#808898', 'wings': '#f0f0f8'},
            {'naam': 'Keizerlijke zijde (gouden cocon, paars lijf, zijdeblauwe vleugels)',
             'cloak': ('#d8b040', {'h': 0}), 'body': '#6040a0', 'wings': '#2090c0'},
        ],
    },
    'shellos': {
        # zeenaaktslakken. Westen (roze/bruin) en oosten (blauw/groen) houden elk een eigen paar kleuren.
        'species': {
            'shellos': {'main': [1, 3, 4, 5, 6, 7, 15], 'rim': [8, 9, 11], 'lower': [12, 13, 14]},
            'shellos/east': {'emain': [5, 6, 7, 8], 'rim': [9, 10, 11], 'elower': [12, 13, 14]},
            'gastrodon': {'back': [1, 3, 4, 5], 'main': [12, 13, 14], 'rim': [7, 8, 9]},
            'gastrodon/east': {'eback': [1, 3, 4, 5], 'emain': [12, 13, 14], 'rim': [7, 8, 9]},
        },
        'variants': [
            {'naam': 'Spaanse danseres (west) / Flabellina (oost, oranje)', 'main': '#b81830', 'lower': '#f8e8e0',
             'back': '#801820', 'rim': '#f0d040', 'emain': '#f08030', 'elower': '#f8f0e0', 'eback': '#803818'},
            {'naam': 'Citroennaaktslak (west) / Smaragdzeeslak Elysia (oost)', 'main': '#f0d040', 'lower': '#f8f8e8',
             'back': '#a07020', 'rim': '#404040', 'emain': '#40b050', 'elower': '#c0e8a0', 'eback': '#205030'},
            {'naam': 'Paarse zeehaas (west) / Turkooise zeeslak (oost)', 'main': '#8048b0', 'lower': '#e0d0f0',
             'back': '#3a2050', 'rim': '#f0a020', 'emain': '#30c0c0', 'elower': '#f0f0e0', 'eback': '#206070'},
            {'naam': 'Albino', 'main': '#f0e4ea', 'lower': '#f8f8f8', 'back': '#c8c0c0', 'rim': '#f0d0d8',
             'emain': '#e4eaf2', 'elower': '#f4f8f4', 'eback': '#b8c4c0'},
            {'naam': 'Zwarte zeeslak met oranje rand', 'main': ('#34343c', DARK), 'lower': '#686068',
             'back': ('#24242a', DARK), 'rim': '#f07020', 'emain': ('#2c3448', DARK), 'elower': '#506070',
             'eback': ('#1e2430', DARK)},
            {'naam': 'Regenboognaaktslak (Chromodoris)', 'main': '#7040e0', 'lower': '#f8f8f8', 'back': '#f08020',
             'rim': '#f0f040', 'emain': '#f040a0', 'elower': '#f8f0f8', 'eback': '#30c0e0'},
        ],
    },
    'arceus': {
        # Alleen het lijf (wit/grijs, bij elk type gelijk) wisselt; het wiel, de hoeven en de
        # buik dragen de typekleur van de plaat en blijven. Elke typemap krijgt precies
        # dezelfde lijfkleur, zodat de variant meegaat als de plaat wisselt.
        'species': dict(
            [('arceus', {'body': [2, 1, 4, 5], '_base': {'body': 2}})] +
            [('arceus/' + t, {'body': [2, 1, 4, 5], '_base': {'body': 2}}) for t in (
                'bug', 'dark', 'dragon', 'electric', 'fairy', 'fighting', 'fire', 'flying', 'ghost', 'grass',
                'ground', 'ice', 'poison', 'psychic', 'rock', 'steel', 'water')]),
        'variants': [
            {'naam': 'Terracotta', 'body': '#c87858'},
            {'naam': 'Hemelsblauw', 'body': '#a8c8f0'},
            {'naam': 'Jade (Chinese hemelgod)', 'body': '#a0d8b0'},
            {'naam': 'Zilvergrijs', 'body': '#9098a8'},
            {'naam': 'Rozenkwarts', 'body': '#f0b8cc'},
            {'naam': 'Kosmos (nachtblauw: de schepper vóór het licht)', 'body': '#303878'},
        ],
    },
}
