"""Kleurvarianten Gen 6 (Kalos). Formaat: zie recipes.py."""

ALBINO = {'l': 1.0}
DARK = {'l': 1.3}

LINES = {
    'chespin': {
        # kastanjeridders: kap/schild (groen), lijf/gezicht, bruine vacht, rode punten (neus, staart,
        # stekels), pantser (Chesnaught), klauwen
        'species': {
            'chespin': {'hood': [4, 3, 1, 5], 'body': [7, 9, 8, 6], 'tips': [13, 12], 'claws': [14, 10]},
            'quilladin': {'hood': [8, 7, 6], 'fur': [9, 5, 4], 'face': [10, 11, 13], 'tips': [2, 1],
                          'claws': [12, 14]},
            'chesnaught': {'armor': [3, 4, 1], 'tips': [5, 6], 'hood': [7, 14, 15], 'fur': [8, 13],
                           'face': [10, 9, 12]},
        },
        'variants': [
            {'naam': 'Zee-egel (paarse stekels, zandkleurig lijf)', 'hood': '#6a4a9a', 'body': '#d8b888',
             'face': '#e8d0a8', 'fur': '#5a4038', 'tips': '#f0d040', 'armor': '#c8b8e0', 'claws': '#f0e8d8'},
            {'naam': 'Sonic (blauw, perzik, rode schoenen, witte handschoenen)', 'hood': '#2a58c8', 'body': '#f0c090',
             'face': '#f0c090', 'fur': '#2a3a80', 'tips': '#e02828', 'armor': '#f0c090', 'claws': '#f8f8f8',
             'chesnaught:armor': '#2a58c8', 'chesnaught:hood': '#f0c090'},
            {'naam': 'Herfstblad en eikel (oranje kap, roodbruin)', 'hood': '#e08a28', 'body': '#a86038',
             'face': '#e8c090', 'fur': '#6a3a20', 'tips': '#a03020', 'armor': '#9a6034', 'claws': '#3a2818'},
            {'naam': 'Ridderharnas (staal met heraldisch rood)', 'hood': '#9aa4b8', 'body': '#e0c8a8',
             'face': '#e8d8c0', 'fur': ('#4a4a58', DARK), 'tips': '#c02828', 'armor': ('#c8ccd8', {'l': 1.2}),
             'claws': '#5a5a68'},
            {'naam': 'Zwarte Ridder (obsidiaan, gloeiend rood)', 'hood': ('#3a3a48', DARK), 'body': '#8a7a80',
             'face': '#a8a0a8', 'fur': ('#2c2c34', DARK), 'tips': '#ff3030', 'armor': ('#4a4a58', DARK),
             'claws': '#d02828'},
            {'naam': 'Paladijn (goud en ivoor, blauwe punten)', 'hood': ('#d8b040', {'h': 0}), 'body': '#f0e0c0',
             'face': '#f8ecd8', 'fur': '#8a5a30', 'tips': '#3060d0', 'armor': '#f0ecdc', 'claws': '#3060d0',
             'chesnaught:armor': ('#d8b040', {'h': 0}), 'chesnaught:hood': '#3060d0', 'chesnaught:tips': '#f0ecdc'},
        ],
    },
    'fennekin': {
        # vossen en heksen: vacht (geel), oorpluimen/vuur (ook de vlam van de staf), witte borst/snuit,
        # benen/gewaad, staf, ogen
        'species': {
            'fennekin': {'fur': [3, 4, 1], 'ears': [6, 7, 5], 'chest': [10, 11], 'eyes': [12],
                         '_base': {'ears': 6}},
            'braixen': {'fur': [2, 4, 1], 'ears': [6, 7, 5, 15], 'chest': [8, 10, 9], 'robe': [14, 13],
                        'stick': [12, 11], '_base': {'ears': 6}},
            'delphox': {'robe': [14, 15, 9], 'ears': [3, 5, 1], 'fur': [6, 7, 4], 'chest': [8, 10, 13],
                        'stick': [12], '_base': {'fur': 6, 'ears': 3}},
        },
        'variants': [
            {'naam': 'Zilvervos (zwart en zilver)', 'fur': '#a8a8b8', 'ears': ('#3a3a46', DARK), 'chest': '#f4f4f8',
             'robe': ('#34343e', DARK), 'eyes': '#f0c030', 'stick': '#6a5a50'},
            {'naam': 'Blauw vuur van de Ijen-vulkaan', 'fur': '#f0e8c8', 'ears': '#3878e0', 'chest': '#ffffff',
             'robe': '#283a88', 'eyes': '#3878e0', 'stick': '#5a4a3a'},
            {'naam': 'Halloween-heks (pompoen en paars vuur)', 'fur': '#f08828', 'ears': '#8040c0', 'chest': '#f8e8c8',
             'robe': ('#3a2458', DARK), 'eyes': '#a050e0', 'stick': '#3a2a20'},
            {'naam': 'Miko (sakura-roze, rood gewaad)', 'fur': '#f8c0d4', 'ears': '#d02848', 'chest': '#ffffff',
             'robe': '#c82030', 'eyes': '#d02848', 'stick': '#c09040'},
            {'naam': 'Sterrennacht (nachtblauw met gouden vuur)', 'fur': ('#3a4078', DARK), 'ears': '#f0c838',
             'chest': '#c8c8f0', 'robe': ('#20244a', DARK), 'eyes': '#f0c838', 'stick': '#a0a0c0'},
            {'naam': 'Smaragdtovenaar van Oz (groen met goud)', 'fur': '#40a870', 'ears': '#f0d040', 'chest': '#e0f4e0',
             'robe': '#18603a', 'eyes': '#f0d040', 'stick': '#d8b040'},
        ],
    },
    'froakie': {
        # ninjakikkers: lijf, schuim (Froakie/Frogadier, Greninja's witte vlekken), ogen, tong (sjaal),
        # crèmekleurige kop/kling (Greninja). Ash-Greninja overgeslagen (Ash' kleuren).
        'species': {
            'froakie': {'body': [4, 2, 1, 3, 9], 'froth': [8, 10, 7, 11], 'eyes': [5]},
            'frogadier': {'body': [3, 4, 1, 5, 7, 9], 'froth': [8, 11, 12, 6], 'eyes': [10], '_base': {'body': 4}},
            'greninja': {'body': [2, 1, 6, 7], 'tongue': [14, 11, 12], 'face': [5, 4, 13], 'froth': [10, 9, 8],
                         '_base': {'body': 6}},
        },
        'variants': [
            {'naam': 'Roodoogboomkikker (groen, rode ogen, oranje tong)', 'body': '#3cb048', 'froth': '#f4f4e8',
             'eyes': '#e03020', 'tongue': '#f08020', 'face': '#f0f0c0'},
            {'naam': 'Naruto (oranje, blauwe hoofdband, blond)', 'body': '#f08020', 'froth': '#f8f0e0',
             'eyes': '#3070e0', 'tongue': '#3060c0', 'face': '#f8d860'},
            {'naam': 'Tomaatkikker (rood, gele tong)', 'body': '#d03828', 'froth': '#f8e8d0', 'eyes': '#f0d040',
             'tongue': '#f0d040', 'face': '#f8e0c0'},
            {'naam': 'Glaskikker (bleek lime, doorschijnend)', 'body': '#b0dc98', 'froth': '#ffffff', 'eyes': '#f0b030',
             'tongue': '#f0a0b0', 'face': '#f0f8e8'},
            {'naam': 'Paarse varkenskikker (cyaan ogen)', 'body': '#7a4a9a', 'froth': '#e8d8f0', 'eyes': '#40d0f0',
             'tongue': '#f0d040', 'face': '#d8c8f0'},
            {'naam': 'Panamese gouden kikker (smaragd tong)', 'body': ('#e0b028', {'h': 0}), 'froth': '#f8f0d0',
             'eyes': ('#2c2c34', DARK), 'tongue': '#30a050', 'face': '#3a3020'},
        ],
    },
    'bunnelby': {
        # konijnen: vacht (grijs), oren/broek (bruin), binnenoor/neus (roze), buik (Diggersby, geel)
        'species': {
            'bunnelby': {'fur': [9, 6, 5], 'ears': [3, 2, 1], 'pink': [8, 7]},
            'diggersby': {'fur': [2, 3, 1], 'ears': [7, 14, 6, 5], 'belly': [11, 12, 13], 'pink': [8]},
        },
        'variants': [
            {'naam': 'Lila konijn (lila-grijs met pruimkleurige oren)', 'fur': '#b8a0c0', 'ears': '#7a4a80', 'belly': '#f0e0f0',
             'pink': '#f0a0a0'},
            {'naam': 'Tan-konijn (zwart met roestbruine oren)', 'fur': ('#3a3a44', DARK), 'ears': '#c86030', 'belly': '#e09050',
             'pink': '#f08098'},
            {'naam': 'Chocolade paashaas (goudfolie)', 'fur': '#6a4028', 'ears': '#3a2014', 'belly': ('#e0b030', {'h': 0}),
             'pink': '#e04050'},
            {'naam': 'Weens blauw konijn', 'fur': '#7088b0', 'ears': '#3a4a78', 'belly': '#c8d8f0', 'pink': '#f0a0c0'},
            {'naam': 'Graafmachine (Caterpillar-geel met zwart)', 'fur': '#e8b820', 'ears': ('#34343c', DARK),
             'belly': '#7a7a84', 'pink': '#f08020'},
            {'naam': "Maanhaas van Chang'e (nachtblauw met goud)", 'fur': ('#3a4078', DARK), 'ears': '#d8b040',
             'belly': '#f0e080', 'pink': '#f0a0c0'},
        ],
    },
    'fletchling': {
        # vuurvogels: kop/borst (rood), rug/vleugels (grijs), buik, vlammen/poten/snavel (goud)
        'species': {
            'fletchling': {'red': [7, 5, 4], 'grey': [3, 2], 'belly': [10, 8, 6], 'gold': [11]},
            'fletchinder': {'red': [2, 4, 1], 'grey': [7, 6, 8], 'belly': [12, 11, 15], 'gold': [5, 13, 14]},
            'talonflame': {'red': [6, 7, 5, 8], 'grey': [3, 2, 1, 12], 'gold': [10, 9, 13]},
        },
        'variants': [
            {'naam': 'Blauwe gaai (blauw, wit, cyaan vlammen)', 'red': '#3070d0', 'grey': '#4a5068', 'belly': '#e8eef8',
             'gold': '#40c0f0'},
            {'naam': 'Kolibrie (smaragd met roze keel)', 'red': '#30a868', 'grey': '#3a5040', 'belly': '#c0e0c0',
             'gold': '#e04080'},
            {'naam': 'Kraai met spookvuur (paars)', 'red': ('#3a3a48', DARK), 'grey': '#7a7a88', 'belly': '#a0a0b0',
             'gold': '#a050f0'},
            {'naam': 'Sneeuwuil (wit, gele klauwen)', 'red': ('#e8e8ee', ALBINO), 'grey': '#a8a8b8', 'belly': '#f0f0f8',
             'gold': '#f0d040'},
            {'naam': 'Gouldamadine (paars, groen en geel)', 'red': '#9040b0', 'grey': '#40a050', 'belly': '#f0d040',
             'gold': '#40c0f0'},
            {'naam': 'Garuda (goud met rood)', 'red': ('#e0b030', {'h': 0}), 'grey': '#c03020', 'belly': '#f8e8b0',
             'gold': '#f0f0f0'},
        ],
    },
    'litleo': {
        # leeuwen: manen/vuur (rood), goud (Pyroar), lichte vacht, donker lijf, ogen
        'species': {
            'litleo': {'tan': [4, 5, 2], 'body': [7, 8, 10], 'mane': [3, 1, 6]},
            'pyroar': {'mane': [5, 4, 2], 'gold': [3, 1], 'tan': [12, 10, 15], 'body': [8, 9, 6], 'eyes': [14]},
        },
        'variants': [
            {'naam': 'Witte leeuw van Timbavati', 'tan': '#f0e8d8', 'body': '#b8b0a4', 'mane': '#e8c890', 'gold': '#f8f0d0',
             'eyes': '#40a0e0'},
            {'naam': 'Scar (zwarte manen, groene ogen)', 'tan': '#a07048', 'body': ('#4a3a36', DARK), 'mane': ('#2c2428', DARK),
             'gold': '#7a3020', 'eyes': '#a0e040'},
            {'naam': 'Blauw vuur', 'tan': '#e8d8b8', 'body': '#3a4058', 'mane': '#3070e0', 'gold': '#60d0f0', 'eyes': '#f0d040'},
            {'naam': 'Aslan (gouden manen)', 'tan': '#d8a868', 'body': '#8a6038', 'mane': ('#e0a028', {'h': 0}),
             'gold': '#f8e8a0', 'eyes': '#f0c030'},
            {'naam': 'Sterrenbeeld Leo (nachtblauw, zilveren manen)', 'tan': '#5a6898', 'body': '#283460', 'mane': '#c8d0e8',
             'gold': '#f0f0f8', 'eyes': '#f0d040'},
            {'naam': 'De Groene Leeuw (alchemie: de leeuw die de zon verslindt)', 'tan': '#d8c8a0', 'body': '#2c3a30',
             'mane': '#20b050', 'gold': '#f0d040', 'eyes': '#f04040'},
        ],
    },
    'skiddo': {
        # rijgeiten: bladeren, lijf (bruin), lichte vacht (Gogoat), gezicht, hoorns, hoeven
        'species': {
            'skiddo': {'leaves': [9, 10, 8], 'body': [6, 5, 4], 'face': [12, 11, 13], 'horns': [2], 'hooves': [14, 7]},
            'gogoat': {'leaves': [6, 8, 4], 'body': [7, 5], 'tan': [9, 13], 'face': [10, 11], 'horns': [3],
                       'hooves': [15, 12, 14]},
        },
        'variants': [
            {'naam': 'Herfst (oranje bladeren)', 'leaves': '#d87028', 'body': '#6a4028', 'tan': '#c8a070', 'face': '#f0f0e8',
             'horns': '#5a4a3a', 'hooves': '#3a3a44'},
            {'naam': 'Kersenbloesem', 'leaves': '#f0a0c0', 'body': '#5a3a40', 'tan': '#e8d0c8', 'face': '#f8f0f0',
             'horns': '#3a2830', 'hooves': '#a03050'},
            {'naam': 'Sneeuwgeit (wit, zwarte hoorns, dennengroen)', 'leaves': '#2c6a58', 'body': ('#e0e0e4', ALBINO),
             'tan': ('#ececf0', ALBINO), 'face': '#f8f8f8', 'horns': ('#2c2c34', DARK), 'hooves': '#3a3a44'},
            {'naam': 'Lavendelvelden van de Provence', 'leaves': '#9070c8', 'body': '#7a6a50', 'tan': '#d8c8a8',
             'face': '#f0ecf8', 'horns': '#4a3a60', 'hooves': '#5a3a80'},
            {'naam': 'Black Phillip (The Witch: zwart met bloedrood)', 'leaves': '#8a2020', 'body': ('#3a3a44', DARK),
             'tan': ('#4a4a54', DARK), 'face': '#b0b0b8', 'horns': '#a08060', 'hooves': '#d03030'},
            {'naam': 'Ginkgo (goudgele bladeren)', 'leaves': ('#f0c030', {'h': 0}), 'body': '#8a5a30', 'tan': '#f0e0b0',
             'face': '#f8f4e8', 'horns': '#5a3a20', 'hooves': '#c02828'},
        ],
    },
    'pancham': {
        # panda's: witte vacht, zwarte vlekken, blad
        'species': {
            'pancham': {'white': [2, 3, 13, 1], 'black': [5, 6, 11, 4], 'leaf': [10, 9]},
            'pangoro': {'white': [3, 4, 1], 'black': [6, 7, 10, 5, 11, 12], 'leaf': [9, 8], '_base': {'black': 6}},
        },
        'variants': [
            {'naam': 'Rode panda (roest met crème)', 'white': '#f0e0c8', 'black': '#a84a20', 'leaf': '#30a050'},
            {'naam': 'Fotonegatief (zwart met witte vlekken, roze blad)', 'white': ('#3a3a44', DARK), 'black': '#d8d8e0',
             'leaf': '#e04080'},
            {'naam': 'Jadekrijger (jadegroen, gouden blad)', 'white': '#f0f0e0', 'black': '#2a6a50', 'leaf': '#f0d040'},
            {'naam': 'IJsbeer (wit en ijsgrijs, blauw blad)', 'white': ('#f4f4f8', ALBINO), 'black': '#98a4b8',
             'leaf': '#40a0f0'},
            {'naam': 'Yakuza (paars pak, gouden blad)', 'white': '#f0e8f0', 'black': '#4a2c68', 'leaf': '#f0c030'},
            {'naam': 'Gouden panda (diplomatiek geschenk)', 'white': ('#e8c048', {'h': 0}), 'black': '#5a3a10',
             'leaf': '#e02828'},
        ],
    },
    'espurr': {
        # psychokatten: vacht (Espurr), blauw/wit (Meowstic), binnenoor, ogen
        'species': {
            'espurr': {'fur': [2, 4, 1, 5], 'accent': [10, 12], 'eyes': [11]},
            'meowstic': {'blue': [5, 8, 6, 9], 'white': [2, 4, 3, 1], 'eyes': [10]},
            'meowstic/f': {'white': [3, 4, 1], 'blue': [7, 6, 5], 'eyes': [8], 'accent': [9]},
        },
        'variants': [
            {'naam': 'Siamees (crème, chocoladepunten, blauwe ogen)', 'blue': '#5a3a28', 'white': '#f0e4d0', 'fur': '#e0d0b8',
             'accent': '#5a3a28', 'eyes': '#3080e0'},
            {'naam': 'Rode kater', 'blue': '#e07828', 'white': '#f8f0e8', 'fur': '#f0b070', 'accent': '#f08080', 'eyes': '#40c040'},
            {'naam': 'Heksenkat (zwart, groene ogen)', 'blue': ('#2c2c38', DARK), 'white': '#6a6a78', 'fur': ('#4a4a58', DARK),
             'accent': '#80e040', 'eyes': '#80e040'},
            {'naam': 'Mint', 'blue': '#30a088', 'white': '#e8f8f0', 'fur': '#a8dcc8', 'accent': '#f08098', 'eyes': '#f08098'},
            {'naam': 'Cheshire Cat (magenta en roze)', 'blue': '#a040a0', 'white': '#f0a0d0', 'fur': '#9050b0',
             'accent': '#f0a0d0', 'eyes': '#f0e040'},
            {'naam': 'Bastet (zwart en goud, lapis-ogen)', 'blue': ('#d8a830', {'h': 0}), 'white': ('#2c2c38', DARK),
             'fur': ('#d8b040', {'h': 0}), 'accent': '#2050c0', 'eyes': '#2050c0'},
        ],
    },
    'honedge': {
        # vervloekte zwaarden: kling, gevest/schild (goud), lint/arm (cloth), greepomwikkeling, oog,
        # donkere schildrand (Aegislash)
        'species': {
            'honedge': {'blade': [11, 12, 10], 'hilt': [5, 4, 6, 7], 'cloth': [2, 1], 'wrap': [14, 13, 15],
                        'eye': [8, 9], '_base': {'hilt': 6}},
            'doublade': {'blade': [3, 4, 1], 'hilt': [6, 5], 'cloth': [12, 13, 14, 15], 'wrap': [8, 9, 10, 11]},
            'aegislash': {'hilt': [6, 2, 5, 12, 13], 'cloth': [8, 9], 'dark': [7]},
            'aegislash/blade': {'hilt': [6, 2, 5, 12, 13], 'cloth': [8, 9], 'dark': [7], 'blade': [10, 14]},
        },
        'variants': [
            {'naam': 'Katana (bronzen tsuba, indigo-geverfd lint)', 'blade': '#c8d0e0', 'hilt': '#7a6a48', 'cloth': '#283a6a',
             'wrap': ('#2c2c34', DARK), 'eye': '#e03030', 'dark': '#5a1818'},
            {'naam': 'Keyblade (Kingdom Hearts: goud, wit lint, blauwe greep)', 'blade': '#c8ccd8',
             'hilt': ('#e0c030', {'h': 0}), 'cloth': '#e8e8f0', 'wrap': '#3060c0', 'eye': '#40c0f0', 'dark': '#2a3a80'},
            {'naam': 'Master Sword (Zelda: paars gevest, Triforce-goud)', 'blade': '#d0e0f0', 'hilt': '#6040a0',
             'cloth': '#f0d040', 'wrap': '#40a0e0', 'eye': '#40d070', 'dark': '#3a2a60'},
            {'naam': 'Azteekse obsidiaan (turkoois, rood en goud)', 'blade': ('#3a3a48', DARK), 'hilt': '#30a0a0',
             'cloth': '#e04030', 'wrap': '#f0d040', 'eye': '#f0d040', 'dark': '#4a1810'},
            {'naam': 'Lichtzwaard (gloeiend cyaan, metalen gevest)', 'blade': '#60d0f0', 'hilt': '#a0a0a8',
             'cloth': ('#2c2c34', DARK), 'wrap': '#606068', 'eye': '#60d0f0', 'dark': '#202028'},
            {'naam': 'Kusanagi (jade en goud)', 'blade': '#60c090', 'hilt': ('#e0b030', {'h': 0}), 'cloth': '#c02838',
             'wrap': '#f0e0b0', 'eye': '#e03030', 'dark': '#1a4030'},
        ],
    },
    'spritzee': {
        # parfums: lijf, jurk/kuif (Aromatisse), witte kap/kraag, snavel/lippen, goud (Aromatisse)
        'species': {
            'spritzee': {'body': [4, 2, 1], 'white': [5, 6], 'beak': [8], 'purple': [10]},
            'aromatisse': {'body': [13, 14, 15], 'purple': [1, 2, 3], 'white': [7, 8], 'beak': [11, 10], 'gold': [4, 6]},
        },
        'variants': [
            {'naam': 'Perzik (eau de toilette)', 'body': '#f8b890', 'purple': '#d06040', 'white': '#fff8f0', 'beak': '#40a050',
             'gold': '#f0f0f0'},
            {'naam': 'Eau de Cologne (citroen en sinaasappel)', 'body': '#f0d860', 'purple': '#e07828', 'white': '#fff8e0',
             'beak': '#40a040', 'gold': '#f8f8f8'},
            {'naam': 'Pepermunt', 'body': '#90d8c0', 'purple': '#2a8a70', 'white': '#f8f8f8', 'beak': '#e03050', 'gold': '#f0f0f0'},
            {'naam': 'Chanel No. 5 (zwart, wit en goud)', 'body': ('#3a3a44', DARK), 'purple': '#e8e8ec', 'white': '#f4f4f4',
             'beak': '#d02030', 'gold': ('#e0c040', {'h': 0})},
            {'naam': 'Marie Antoinette (poederblauw met roze)', 'body': '#a8c8f0', 'purple': '#f0a0c0', 'white': '#ffffff',
             'beak': '#e04070', 'gold': '#f0d040'},
            {'naam': 'Oud (agarhout: amber met donker hout)', 'body': '#d89040', 'purple': '#5a2c18', 'white': '#f8e8c0',
             'beak': '#3a2010', 'gold': '#f0d040'},
        ],
    },
    'swirlix': {
        # desserts: slagroom, roze suiker, accenten (neus, kers, slierten)
        'species': {
            'swirlix': {'cream': [2, 8, 1, 5], 'pink': [4, 6, 3], 'accent': [10, 11, 12], '_base': {'cream': 8}},
            'slurpuff': {'pink': [7, 6, 5], 'cream': [8, 10, 9, 13], 'accent': [3, 1, 2, 12]},
        },
        'variants': [
            {'naam': 'Chocolademousse', 'cream': '#9a6a48', 'pink': '#5a3020', 'accent': '#f0e0c0'},
            {'naam': 'Matcha', 'cream': '#c8e0a0', 'pink': '#6a9a40', 'accent': '#f0a0b8'},
            {'naam': 'Kauwgom (babyblauw)', 'cream': '#d8e8f8', 'pink': '#60a8f0', 'accent': '#3050c0'},
            {'naam': 'Ube (paarse yam)', 'cream': '#c8a8e0', 'pink': '#7a4aa0', 'accent': '#f0d060'},
            {'naam': 'Engelse drop (zwart met roze en blauw)', 'cream': ('#3a3a44', DARK), 'pink': '#f080c0',
             'accent': '#40c0f0'},
            {'naam': 'Bladgoud-dessert (goud met rood fruit)', 'cream': ('#e8c050', {'h': 0}), 'pink': '#8a3020',
             'accent': '#f8f0d8'},
        ],
    },
    'inkay': {
        # inktvissen: kop/onderlijf (blauw), roze vinnen/kap, witte rand/tentakels, gele vlekken,
        # paars lijf (Malamar)
        'species': {
            'inkay': {'white': [4, 2, 1, 5], 'pink': [6, 7, 9, 12], 'spots': [8], 'blue': [13, 10, 11, 14]},
            'malamar': {'blue': [4, 3, 1, 5, 6, 7], 'pink': [9, 8], 'spots': [11], 'body': [13],
                        'white': [10, 14, 12, 15]},
        },
        'variants': [
            {'naam': 'Vampierinktvis (bloedrood en zwart, blauwe lichtjes)', 'blue': '#7a1828', 'white': '#c8a0a0',
             'pink': ('#3a2c34', DARK), 'spots': '#40c0f0', 'body': '#3a1020'},
            {'naam': 'Bioluminescente pijlinktvis', 'blue': '#20a0b0', 'white': '#e8f8f8', 'pink': '#40f0e0',
             'spots': '#f0f0a0', 'body': '#2a5060'},
            {'naam': 'Sepia (zandkleur)', 'blue': '#8a6a48', 'white': '#e8d8c0', 'pink': '#c08048', 'spots': '#f0f0f0',
             'body': '#5a4434'},
            {'naam': 'Glazen inktvis (doorschijnend)', 'blue': '#b8c4e0', 'white': '#f4f4f8', 'pink': '#f0a0c0',
             'spots': '#f0c040', 'body': '#a8a0c0'},
            {'naam': 'Splatoon (oranje en blauwe inkt)', 'blue': '#f07020', 'white': '#f8f0e0', 'pink': '#3050f0',
             'spots': '#40f040', 'body': ('#2c2c38', DARK)},
            {'naam': 'Pink Floyd-prisma (zwart met cyaan en rood)', 'blue': ('#2c2c38', DARK), 'white': '#f0f0f8',
             'pink': '#40e0f0', 'spots': '#f04040', 'body': '#3a2a5a'},
        ],
    },
    'binacle': {
        # zeepokken: rots (blauw), vingers (groen), lijf (bruin), oranje accenten
        'species': {
            'binacle': {'claws': [2, 1, 4], 'body': [9, 8, 5], 'orange': [6, 7], 'rock': [12, 13, 14, 15]},
            'barbaracle': {'claws': [1, 2, 4], 'body': [7, 6, 5], 'orange': [9, 8], 'rock': [15, 13, 14, 10]},
        },
        'variants': [
            {'naam': 'Koraalrif (koraalrode rots, turquoise vingers)', 'rock': '#d86048', 'claws': '#40c0b0',
             'body': '#5a4038', 'orange': '#f0e080'},
            {'naam': 'Basalt (zwart, rode vingers)', 'rock': ('#3a3a44', DARK), 'claws': '#c03028', 'body': '#8a7a6a',
             'orange': '#f08020'},
            {'naam': 'Mosselbank (blauwzwart met geel)', 'rock': '#2a3a5a', 'claws': '#e0c860', 'body': '#c8a878',
             'orange': '#f0f0f0'},
            {'naam': 'Pareloester (parelmoer)', 'rock': ('#e8e0f0', ALBINO), 'claws': '#b0a0c8', 'body': '#7a6a80',
             'orange': '#f0a0b0'},
            {'naam': 'Lava (gloeiende vingers)', 'rock': '#4a2020', 'claws': '#f08020', 'body': '#3a2a28', 'orange': '#f0e040'},
            {'naam': 'Malachiet en goud', 'rock': '#30a088', 'claws': ('#e0b030', {'h': 0}), 'body': '#5a3a20',
             'orange': '#e03030'},
        ],
    },
    'skrelp': {
        # zeedraken/kelp: lijf (bruin), vinnen (Skrelp blauw, Dragalge rode kop), paarse delen, stengels, oog
        'species': {
            'skrelp': {'body': [3, 6, 1], 'fins': [4, 7, 2], 'purple': [8, 10, 11], 'eye': [9]},
            'dragalge': {'body': [8, 7, 9], 'fins': [5, 6, 4], 'stem': [3, 1], 'purple': [10, 12, 13], 'eye': [11]},
        },
        'variants': [
            {'naam': 'Algenbloei (roestoranje met geel)', 'body': '#b05a28', 'fins': '#f0d040', 'purple': '#f0c8a0',
             'stem': '#5a3018', 'eye': '#40c0e0'},
            {'naam': 'Kelpwoud (olijf en mosgroen)', 'body': '#5a6a30', 'fins': '#a0b040', 'purple': '#d0b080',
             'stem': '#3a4020', 'eye': '#e03030'},
            {'naam': 'Blauwe draak (Glaucus atlanticus)', 'body': '#3060c0', 'fins': '#a0d0f0', 'purple': '#e8f0f8',
             'stem': '#283a70', 'eye': '#f0d040'},
            {'naam': 'Giftig afval (zwart met neongroen)', 'body': '#304030', 'fins': '#60f040', 'purple': '#a0f080',
             'stem': '#203020', 'eye': '#f040c0'},
            {'naam': 'Inktzwart rif (roze vinnen)', 'body': ('#34303c', DARK), 'fins': '#f080b0', 'purple': '#c0a0d0',
             'stem': '#5a4a60', 'eye': '#40e0f0'},
            {'naam': 'Jadedraak (jade en goud)', 'body': '#40a080', 'fins': ('#e0b030', {'h': 0}), 'purple': '#f0e0b0',
             'stem': '#2a5a40', 'eye': '#e03030'},
        ],
    },
    'clauncher': {
        # kreeften: schild/lijf (blauw), grote schaar (Clawitzer, donker), grijze delen, gouden voelsprieten
        'species': {
            'clauncher': {'blue': [5, 6, 4], 'grey': [8, 9, 10, 12], 'gold': [2, 1]},
            'clawitzer': {'shell': [6, 8, 4], 'blue': [11, 13, 12], 'grey': [7, 9, 5], 'gold': [3, 10, 1]},
        },
        'variants': [
            {'naam': 'Bidsprinkhaankreeft (groen met oranje poten)', 'blue': '#40b060', 'shell': '#2a7a40', 'grey': '#e08030',
             'gold': '#e03080'},
            {'naam': 'Cocktailgarnaal (roze met wit)', 'blue': '#f0a0b8', 'shell': '#c05a80', 'grey': '#f0f0f0',
             'gold': '#40c0a0'},
            {'naam': 'Albino kreeft', 'blue': ('#e8e8f0', ALBINO), 'shell': ('#c8ccd8', ALBINO), 'grey': '#a09098',
             'gold': '#f0a0a0'},
            {'naam': 'Paarse rifkreeft', 'blue': '#9060c0', 'shell': '#5a3090', 'grey': '#3a3a48', 'gold': '#f0e040'},
            {'naam': 'Zwart kanon (gunmetal met cyaan)', 'blue': ('#4a5058', DARK), 'shell': ('#2a3038', DARK),
             'grey': '#7a8088', 'gold': '#40e0f0'},
            {'naam': 'Gouden kreeft (Fabergé)', 'blue': ('#e0b030', {'h': 0}), 'shell': ('#b08018', {'h': 0}),
             'grey': '#5a3a20', 'gold': '#e03030'},
        ],
    },
    'helioptile': {
        # zonnehagedissen: lijf (geel), kraag/kop (zwart), oranje (Heliolisk), ogen
        'species': {
            'helioptile': {'yellow': [10, 9, 11, 13, 6], 'frill': [4, 2], 'eyes': [7]},
            'heliolisk': {'yellow': [1, 2, 3, 14, 15], 'frill': [4, 5], 'orange': [6, 7], 'eyes': [13]},
        },
        'variants': [
            {'naam': 'Groene anolis (roze keelzak)', 'yellow': '#60b840', 'frill': '#3a5030', 'orange': '#f06090',
             'eyes': '#f0d040'},
            {'naam': 'Blauwe leguaan (Grand Cayman)', 'yellow': '#4890d0', 'frill': '#2a3a58', 'orange': '#a0d0f0',
             'eyes': '#f0e040'},
            {'naam': 'Zonnepaneel (wit frame, blauwe cellen)', 'yellow': ('#e4e4ec', ALBINO), 'frill': '#2a50a0',
             'orange': '#a0a0b0', 'eyes': '#3080e0'},
            {'naam': 'Paarse bliksem', 'yellow': '#9070d0', 'frill': '#2c2448', 'orange': '#f0e060', 'eyes': '#60f0f0'},
            {'naam': 'Zonsverduistering (zwart met gouden corona)', 'yellow': ('#3a3a46', DARK), 'frill': '#f0c040',
             'orange': '#f08030', 'eyes': '#e04020'},
            {'naam': 'Synthwave (roze met cyaan)', 'yellow': '#f060c0', 'frill': '#2a1a50', 'orange': '#40f0f0',
             'eyes': '#f0f040'},
        ],
    },
    'tyrunt': {
        # tyrannosaurussen: lijf, rugstekels (oranje), witte baard/kraag
        'species': {
            'tyrunt': {'body': [5, 7, 4], 'spikes': [3, 1], 'beard': [9, 11, 12, 8]},
            'tyrantrum': {'body': [8, 10, 9, 12], 'spikes': [2, 1], 'beard': [13, 7, 6, 4]},
        },
        'variants': [
            {'naam': 'Speelgoed-T. rex (groen, gele stekels)', 'body': '#4a7a38', 'spikes': '#f0d040', 'beard': '#e8e0c8'},
            {'naam': 'Godzilla (zwart, witte rugplaten)', 'body': ('#3a3a42', DARK), 'spikes': '#e8e8f0', 'beard': '#8a8a94'},
            {'naam': 'Fossiel (zandsteen en bot)', 'body': '#c8a878', 'spikes': '#7a4a28', 'beard': '#f0e8d8'},
            {'naam': 'Barney (paars met groen)', 'body': '#8050b0', 'spikes': '#80c040', 'beard': '#c0e080'},
            {'naam': 'Albino', 'body': ('#e0dcd4', ALBINO), 'spikes': '#f0a0a0', 'beard': '#f8f8f8'},
            {'naam': 'Barnsteen (Jurassic Park: de mug in amber)', 'body': '#d89030', 'spikes': '#5a3010', 'beard': '#f8e0a0'},
        ],
    },
    'amaura': {
        # poollicht: lijf (blauw), zeil/kraag (geel/crème), tweede kraagkleur (roze/lila), edelstenen, buik
        'species': {
            'amaura': {'body': [1, 2, 6], 'frill': [3, 8], 'frill2': [5, 7], 'gems': [10, 11, 13]},
            'aurorus': {'body': [7, 9, 5], 'belly': [15, 1], 'frill': [4, 2], 'frill2': [3], 'gems': [12, 13]},
        },
        'variants': [
            {'naam': 'Groen noorderlicht', 'body': '#40a888', 'frill': '#a0f0c0', 'frill2': '#c080f0', 'gems': '#7030c0',
             'belly': '#c0f0e0'},
            {'naam': 'Roze ochtendgloren', 'body': '#e890b0', 'frill': '#f8e0a0', 'frill2': '#a0c8f0', 'gems': '#3058d0',
             'belly': '#f8d0e0'},
            {'naam': 'Poolnacht (diepblauw met cyaan zeil)', 'body': '#283a80', 'frill': '#60e0f0', 'frill2': '#f0f0f8',
             'gems': '#f0f060', 'belly': '#5a70b0'},
            {'naam': 'Elsa (Frozen: lavendel-ijs)', 'body': '#a090d8', 'frill': '#c8e8f8', 'frill2': '#f0f0f8',
             'gems': '#2878d0', 'belly': '#d8d0f0'},
            {'naam': 'IJsland (zwart lavagesteente met vuurzeil)', 'body': ('#3a3a46', DARK), 'frill': '#f08030',
             'frill2': '#f0d040', 'gems': '#20b0d0', 'belly': '#6a6a78'},
            {'naam': 'Zuiderlicht (karmozijn en violet)', 'body': '#a02848', 'frill': '#c060f0', 'frill2': '#f080a0',
             'gems': '#4020a0', 'belly': '#e080a0'},
        ],
    },
    'hawlucha': {
        # luchadores: vleugels (groen), pak (rood), wit, kuif (oranje), geel
        'species': {'hawlucha': {'green': [6, 5, 7], 'red': [12, 10, 11], 'white': [14, 13, 15], 'crest': [2, 4, 1],
                                 'yellow': [9, 8]}},
        'variants': [
            {'naam': 'El Santo (zilveren masker, zwart pak)', 'green': '#b0b4c0', 'red': ('#3a3a48', DARK), 'white': '#f4f4f8',
             'crest': '#c8ccd8', 'yellow': '#f0d040'},
            {'naam': 'Rey Mysterio (blauw, wit en goud)', 'green': '#3060d0', 'red': '#2a3a80', 'white': '#f0f0f8',
             'crest': '#f0c030', 'yellow': '#40c0f0'},
            {'naam': 'Toekan (zwart en wit, oranje kuif)', 'green': ('#34343e', DARK), 'red': ('#d8d0c0', {'l': 1.6}), 'white': '#f8f8f8',
             'crest': '#f08020', 'yellow': '#f0c020'},
            {'naam': 'Flamingo-luchador (roze)', 'green': '#f080b0', 'red': '#a02860', 'white': '#ffffff', 'crest': '#f0d040',
             'yellow': '#f0f0f0'},
            {'naam': 'Hulk Hogan (geel en rood, blonde snor)', 'green': '#f0d030', 'red': '#d02020', 'white': '#f8f8f8',
             'crest': '#f8f0d8', 'yellow': '#f0f0f0'},
            {'naam': 'Mil Máscaras (goud met blauw)', 'green': ('#e0b030', {'h': 0}), 'red': '#2a3a80', 'white': '#f8f0e0',
             'crest': '#f0e0a0', 'yellow': '#40c0f0'},
        ],
    },
    'dedenne': {
        # antennemuis: vacht (oranje), oren/staart (donker), binnenoor (crème), wangen
        'species': {'dedenne': {'fur': [8, 9, 7, 6, 10], 'dark': [1, 2], 'ears': [5, 4], 'cheek': [12]}},
        'variants': [
            {'naam': 'Huismuis (grijs)', 'fur': '#a0a0a8', 'dark': '#3a3a44', 'ears': '#e8d8d0', 'cheek': '#f0a0b0'},
            {'naam': 'Chocolademuis', 'fur': '#7a4a30', 'dark': '#2c2024', 'ears': '#f0c0b0', 'cheek': '#f0a0c0'},
            {'naam': 'Witte labmuis', 'fur': ('#ececf0', ALBINO), 'dark': '#9a9aa8', 'ears': '#f8c8d0', 'cheek': '#f06080'},
            {'naam': 'Elektrisch blauw', 'fur': '#5080d0', 'dark': '#2a3060', 'ears': '#c0e0f8', 'cheek': '#40e0f0'},
            {'naam': 'Mint-chocolade', 'fur': '#90d8b0', 'dark': '#4a3020', 'ears': '#f0f8f0', 'cheek': '#f0d040'},
            {'naam': 'Plasmabol (paars met neongele wangen)', 'fur': '#8040c0', 'dark': '#20183a', 'ears': '#e0c0f8',
             'cheek': '#f0f040'},
        ],
    },
    'carbink': {
        # juwelen: steen (grijspaars), witte kristallen, blauwe kristallen, ogen
        'species': {'carbink': {'body': [3, 6, 9, 2], 'crystals': [13, 5, 14], 'gems': [7, 4, 11, 15], 'eyes': [8, 10, 12]}},
        'variants': [
            {'naam': 'Rozenkwarts', 'body': '#a08088', 'crystals': '#fff0f4', 'gems': '#f0a0c0', 'eyes': '#d04070'},
            {'naam': 'Smaragd in leisteen', 'body': '#5a6a60', 'crystals': '#f0fff4', 'gems': '#40c070', 'eyes': '#20a050'},
            {'naam': 'Robijn in graniet', 'body': '#7a6a6a', 'crystals': '#fff4f0', 'gems': '#e03040', 'eyes': '#e03040'},
            {'naam': 'Amethistgeode', 'body': '#5a4a50', 'crystals': '#f4f0ff', 'gems': '#a060e0', 'eyes': '#a060e0'},
            {'naam': 'Obsidiaan met diamant', 'body': ('#3a3a46', DARK), 'crystals': '#ffffff', 'gems': '#e8f0f8',
             'eyes': '#60e0f0'},
            {'naam': 'Opaal (wit met cyaan en roze vuur)', 'body': '#c8c0d8', 'crystals': '#fff8ff', 'gems': '#60e0d0',
             'eyes': '#f080c0'},
        ],
    },
    'goomy': {
        # slijmdraken: lijf (lila), onderkant/staart, groene stippen/buik, slakkenhuis (Hisui)
        'species': {
            'goomy': {'body': [2, 3, 1, 4], 'bottom': [8, 9, 10], 'green': [7, 6]},
            'sliggoo': {'body': [2, 5, 4, 1], 'bottom': [10, 12, 11], 'green': [7, 6, 8, 9]},
            'goodra': {'body': [3, 4, 5, 2], 'bottom': [11, 9, 10], 'green': [12, 13, 14, 6]},
            'sliggoo/hisui': {'body': [2, 4, 1, 5], 'shell': [10, 8, 9, 11], 'green': [6, 7], 'bottom': [13, 12, 14]},
            'goodra/hisui': {'shell': [1, 2, 3, 4, 10], 'body': [7, 8, 6, 9], 'bottom': [15, 14, 13]},
        },
        'variants': [
            {'naam': 'Kauwgomslak (roze, blauwe stippen)', 'body': '#f0a8c8', 'bottom': '#c05090', 'green': '#40a0f0',
             'shell': '#a8a8b8'},
            {'naam': 'Slime (Dragon Quest: blauw, witte glans, messing huis)', 'body': '#3898e8', 'bottom': '#2058b8',
             'green': '#f8f8f8', 'shell': '#c8a040'},
            {'naam': 'Honing (bruine stippen, houten huis)', 'body': '#f0c860', 'bottom': '#c07820', 'green': '#a04020',
             'shell': '#8a6040'},
            {'naam': 'Lavalamp (rood en oranje)', 'body': '#e05848', 'bottom': '#902030', 'green': '#f0d040',
             'shell': ('#3a3a44', DARK)},
            {'naam': 'Petroleum (zwart met groenblauwe glans)', 'body': ('#3a3a48', DARK), 'bottom': ('#241e38', DARK),
             'green': '#40e0c0', 'shell': '#806040'},
            {'naam': 'Metal Slime (Dragon Quest: zilver, gouden huis)', 'body': ('#c8ccd8', {'l': 1.2}), 'bottom': '#7a8090',
             'green': '#3a3a44', 'shell': ('#e0b030', {'h': 0})},
        ],
    },
    'klefki': {
        # sleutelbossen: ring/lijf (metaal), sleutels (goud), tong/binnenkant (roze)
        'species': {'klefki': {'grey': [3, 2, 1, 6, 15], 'gold': [12, 11, 13, 14], 'pink': [8, 7]}},
        'variants': [
            {'naam': 'Roodkoper (zilveren sleutels)', 'grey': '#c07850', 'gold': '#d0d0d8', 'pink': '#40c0a0'},
            {'naam': 'Patina (Vrijheidsbeeld-groen, bronzen sleutels)', 'grey': '#60b0a0', 'gold': '#c08848', 'pink': '#f08060'},
            {'naam': 'Gotisch smeedijzer (zwart, rode tong)', 'grey': ('#4a4a58', DARK), 'gold': '#a0a0a8', 'pink': '#e03030'},
            {'naam': 'Roségoud', 'grey': '#e8b0a8', 'gold': '#f0e0c0', 'pink': '#d04060'},
            {'naam': 'Geanodiseerd titanium (paarsblauw met cyaan)', 'grey': '#7060c0', 'gold': '#40c0e0', 'pink': '#f0d040'},
            {'naam': 'Sleutels van Sint-Petrus (goud en zilver)', 'grey': ('#e0b030', {'h': 0}), 'gold': '#e0e0e8',
             'pink': '#c02030'},
        ],
    },
    'phantump': {
        # spookbomen: hout, bladeren, spooklijf (donker), ogen
        'species': {
            'phantump': {'wood': [6, 10, 5, 4, 13], 'ghost': [2, 3, 1], 'leaves': [8, 9, 7], 'eye': [11, 12]},
            'trevenant': {'wood': [5, 6, 3, 9], 'leaves': [2, 1, 12], 'ghost': [8, 13, 14], 'eye': [10, 11]},
        },
        'variants': [
            {'naam': 'Kersenbloesem (kersenhout)', 'wood': '#9a5048', 'leaves': '#f0a0c0', 'ghost': '#3a2838', 'eye': '#f0f0a0'},
            {'naam': 'Esdoorn (rode bladeren)', 'wood': '#b08060', 'leaves': '#c02828', 'ghost': '#2c2430', 'eye': '#f0d040'},
            {'naam': 'Spookbos (zwart hout, paarse bladeren)', 'wood': ('#3a3440', DARK), 'leaves': '#7040a0',
             'ghost': '#1a1830', 'eye': '#60f0a0'},
            {'naam': 'Pandora (Avatar: lichtgevende blauwe bladeren)', 'wood': '#4a4060', 'leaves': '#3080e0',
             'ghost': '#101830', 'eye': '#60e0f0'},
            {'naam': 'Berijpte boom (witblauw blad)', 'wood': '#a8b8d0', 'leaves': '#e8f4fc', 'ghost': '#202838',
             'eye': '#40a0f0'},
            {'naam': 'Yggdrasil (gouden bladeren)', 'wood': '#c08848', 'leaves': ('#f0c030', {'h': 0}), 'ghost': '#2a1c30',
             'eye': '#40e0f0'},
        ],
    },
    'pumpkaboo': {
        # pompoenen: pompoen (Pumpkaboo) / haar (Gourgeist), bruine kap/lijf, gloed in het gezicht
        'species': {
            'pumpkaboo': {'pumpkin': [11, 12, 9, 13, 10], 'brown': [3, 4, 5], 'glow': [6, 14, 7]},
            'gourgeist': {'pumpkin': [8, 2, 7, 6, 5], 'brown': [3, 13, 4], 'glow': [11, 14, 12, 10]},
        },
        'variants': [
            {'naam': 'Butternut (zandbeige)', 'pumpkin': '#e8c890', 'brown': '#6a5030', 'glow': '#f05020'},
            {'naam': 'Kabocha (groene pompoen)', 'pumpkin': '#3a7040', 'brown': '#5a4028', 'glow': '#f0d040'},
            {'naam': 'Jarrahdale (blauwgrijze pompoen)', 'pumpkin': '#8aa0b0', 'brown': '#4a4038', 'glow': '#f0a040'},
            {'naam': "Assepoesters koets (Rouge vif d'Étampes)", 'pumpkin': '#d03828', 'brown': '#4a3a28', 'glow': '#f0f060'},
            {'naam': "Stingy Jack's knolraap (wit-paars, groen spookvuur)", 'pumpkin': '#e8e0f0', 'brown': '#7a4a90',
             'glow': '#40f060'},
            {'naam': 'Gouden pompoen', 'pumpkin': ('#e8b830', {'h': 0}), 'brown': '#3a2a18', 'glow': '#e02020'},
        ],
    },
    'bergmite': {
        # ijsbergen: ijs, paarse strepen, ogen; Hisui-Avalugg: rotslijf
        'species': {
            'bergmite': {'ice': [2, 3, 4, 1], 'purple': [10, 9], 'eyes': [11, 12]},
            'avalugg': {'ice': [3, 2, 4, 1], 'purple': [7, 6], 'eyes': [8, 9]},
            'avalugg/hisui': {'ice': [2, 3, 6, 1], 'rock': [5, 7, 8, 9], 'eyes': [13, 14]},
        },
        'variants': [
            {'naam': 'Baikalijs (turkoois)', 'ice': '#60d0c8', 'purple': '#2a6a90', 'eyes': '#f0e040', 'rock': '#5a5048'},
            {'naam': 'Watermeloensneeuw (roze ijs)', 'ice': '#f0b0c0', 'purple': '#c04060', 'eyes': '#40c0f0', 'rock': '#6a3a3a'},
            {'naam': 'Amethistijs', 'ice': '#b8a0e8', 'purple': '#5a2a90', 'eyes': '#f0f040', 'rock': '#3a3048'},
            {'naam': 'Zwart ijs (cyaan strepen)', 'ice': ('#3a4050', DARK), 'purple': '#60e0f0', 'eyes': '#f04040',
             'rock': '#7a7a84'},
            {'naam': 'Smaragdijs', 'ice': '#70d090', 'purple': '#2a7040', 'eyes': '#f080c0', 'rock': '#3a4a30'},
            {'naam': 'Citrien (gouden ijs)', 'ice': ('#f0d070', {'h': 0}), 'purple': '#c06020', 'eyes': '#3060d0',
             'rock': '#5a3a20'},
        ],
    },
    'noibat': {
        # geluidsvleermuizen: vlieghuid (paars), lijf (donker), oren (Noivern), vacht (wit), rood, geel
        'species': {
            'noibat': {'purple': [4, 2, 1, 5, 7, 8], 'body': [12, 6, 13], 'yellow': [11, 9]},
            'noivern': {'body': [4, 3, 1], 'purple': [8, 10, 7], 'ears': [5, 6], 'white': [12, 14, 9], 'red': [13, 11],
                        'yellow': [15]},
        },
        'variants': [
            {'naam': 'Vampier (bloedrode vleugels, zwart lijf)', 'purple': '#8a1828', 'body': ('#2c2c34', DARK),
             'ears': '#c02838', 'white': '#e8e0e0', 'red': '#f0d040', 'yellow': '#f0d040'},
            {'naam': 'Vliegende hond (roodbruin)', 'purple': '#a05a30', 'body': '#4a3020', 'ears': '#d08848',
             'white': '#f0d8a0', 'red': '#3a2010', 'yellow': '#f0d040'},
            {'naam': 'Hondurese witte vleermuis (wit met gele oren)', 'purple': ('#e8e8ec', ALBINO), 'body': '#a8a8b0',
             'ears': '#f0d040', 'white': '#ffffff', 'red': '#f08030', 'yellow': '#f0c030'},
            {'naam': 'Batman (zwart en grijs, geel embleem)', 'purple': ('#3a3a48', DARK), 'body': '#6a6a78',
             'ears': '#f0d040', 'white': '#b0b0b8', 'red': '#f0d040', 'yellow': '#f0d040'},
            {'naam': 'Basbox (neonblauwe equalizer)', 'purple': '#2050c0', 'body': '#202838', 'ears': '#40e0f0',
             'white': '#c0c8d8', 'red': '#f040c0', 'yellow': '#40f0f0'},
            {'naam': 'King Ghidorah (gouden draak)', 'purple': ('#e0b030', {'h': 0}), 'body': '#8a6018', 'ears': '#f0e080',
             'white': '#f8f0d0', 'red': '#e03030', 'yellow': '#e03030'},
        ],
    },
    'scatterbug': {
        # rupsen die de kleur van hun Vivillon-variant voorspellen: lijf, vacht (Spewpa), crème, stippen
        'species': {
            'scatterbug': {'body': [6, 7, 1, 5], 'cream': [9, 8]},
            'spewpa': {'fur': [9, 7, 14, 6], 'body': [3, 5], 'cream': [4, 13, 1, 15], 'spots': [11, 10, 12]},
        },
        'variants': [
            {'naam': 'Hoogvlakte (roestoranje)', 'body': '#8a4a28', 'fur': '#e0a070', 'cream': '#f0d8a0', 'spots': '#f0e040'},
            {'naam': 'Tuin (groen)', 'body': '#3a6a38', 'fur': '#a0d090', 'cream': '#e8e0a0', 'spots': '#f05050'},
            {'naam': 'Marine (blauw)', 'body': '#2a4a88', 'fur': '#90b8f0', 'cream': '#f0f0d0', 'spots': '#f0d040'},
            {'naam': 'Weide (magenta)', 'body': '#8a2a68', 'fur': '#f0a0d0', 'cream': '#f8e0a0', 'spots': '#40c0a0'},
            {'naam': 'Savanne (teal)', 'body': '#1a6a70', 'fur': '#60c8c0', 'cream': '#f0e070', 'spots': '#f08030'},
            {'naam': 'Zon (rood met geel)', 'body': '#a02828', 'fur': '#f08070', 'cream': '#f8e060', 'spots': '#3060d0'},
        ],
    },
    'vivillon': {
        # Jordi: de patronen zijn de varianten. Let op: de patroonvormen hebben eigen sprites; met het
        # palet op de basissprite (Ijssneeuw) blijft het basispatroon staan, in de kleuren van dat patroon.
        'species': {'vivillon': {}},
        'variants': [
            {'naam': 'Hoogvlakte-patroon (kleuren)', 'vivillon:palfile': 'high_plains/normal.pal'},
            {'naam': 'Tuin-patroon (kleuren)', 'vivillon:palfile': 'garden/normal.pal'},
            {'naam': 'Marine-patroon (kleuren)', 'vivillon:palfile': 'marine/normal.pal'},
            {'naam': 'Weide-patroon (kleuren)', 'vivillon:palfile': 'meadow/normal.pal'},
            {'naam': 'Savanne-patroon (kleuren)', 'vivillon:palfile': 'savanna/normal.pal'},
            {'naam': 'Zon-patroon (kleuren, donkere omlijning)', 'vivillon:palfile': 'variant_sun.pal'},
        ],
    },
    'flabebe': {
        # bloemenfeeën (alleen de rode vorm): bloem, lijf (wit), haar/stuifmeel (geel), stengel/bladeren,
        # teal accenten (Floette, Florges' bladeren), roze bloemen (Florges)
        'species': {
            'flabebe': {'flower': [11, 12, 10, 8], 'body': [5, 6, 4], 'yellow': [2, 7, 1], 'stem': [13, 14, 15, 9]},
            'floette': {'flower': [4, 2, 1, 15], 'body': [13, 12, 11], 'yellow': [6, 14, 5], 'stem': [8, 7],
                        'teal': [10, 9]},
            'florges': {'flower': [1, 3, 10], 'pink': [4, 2, 5], 'teal': [7, 6, 14], 'body': [12, 13, 11], 'yellow': [9]},
        },
        'variants': [
            {'naam': 'Lavendel (paarse bloem)', 'flower': '#9060c8', 'pink': '#c8a0e8', 'yellow': '#f0e0f8',
             'stem': '#5a8a50', 'teal': '#4a7a70'},
            {'naam': 'Groene roos (Rosa chinensis viridiflora)', 'flower': '#70b048', 'pink': '#c0e090', 'yellow': '#f0f0a0',
             'stem': '#3a5a30', 'teal': '#2a6a50'},
            {'naam': 'La Tulipe Noire (Dumas: de zwarte tulp)', 'flower': ('#3a2c3c', DARK), 'pink': '#7a4a6a',
             'yellow': '#e0c0d0', 'stem': '#3a4a38', 'teal': '#2a3a40'},
            {'naam': 'Fuchsia (magenta met paars)', 'flower': '#d03890', 'pink': '#8a40c0', 'yellow': '#f8c0e0',
             'stem': '#40804a', 'teal': '#6a3080'},
            {'naam': 'Chocoladekosmos (Cosmos atrosanguineus)', 'flower': '#6a2820', 'pink': '#a05a40', 'yellow': '#f0d0a0',
             'stem': '#4a5a30', 'teal': '#5a4030'},
            {'naam': 'De zilveren roos (Der Rosenkavalier)', 'flower': ('#c8ccd8', {'l': 1.2}), 'pink': '#e8e8f0',
             'yellow': '#d0d8f0', 'stem': '#5a6a70', 'teal': '#7a8a98'},
        ],
    },
    'floette_eternal': {
        # AZ' eeuwige bloem: donkere bloembladen, rode bloem/stengel, blauwe benen, lijf
        'species': {'floette/eternal': {'dark': [3, 2], 'red': [5, 4, 6, 13], 'blue': [9, 7, 8], 'body': [11, 10, 12]}},
        'variants': [
            {'naam': 'Nachtviool (paars met zwart)', 'dark': ('#2c2438', DARK), 'red': '#9050c0', 'blue': '#3a5aa0'},
            {'naam': 'Witte rouwlelie (wit met zwart)', 'dark': '#e8e8f0', 'red': '#3a3a44', 'blue': '#606878'},
            {'naam': 'Onmogelijke blauwe roos', 'dark': '#283868', 'red': '#3878e0', 'blue': '#c0c8e0'},
            {'naam': 'Kerstroos (groene kelk, witte bloem)', 'dark': '#3a7a40', 'red': '#f0f0e8', 'blue': '#2a5a30'},
            {'naam': 'Bloedmaan (karmozijn met goud)', 'dark': '#6a1020', 'red': '#f0c030', 'blue': '#8a2030'},
            {'naam': 'Het ultieme wapen (AZ: zilver met jade)', 'dark': ('#a8acb8', {'l': 1.2}), 'red': '#40c090',
             'blue': '#e0b030'},
        ],
    },
    'xerneas': {
        # levenshert: lijf (blauw), gewei, benen (zwart), geweilichtjes (actieve vorm, regenboog draait mee)
        'species': {
            'xerneas': {'antlers': [2, 1, 3], 'body': [5, 6, 7], 'legs': [10, 9, 11]},
            'xerneas/active': {'antlers': [6, 4, 7], 'body': [9, 5, 8], 'legs': [2, 3], 'bulbs': [11, 12, 13, 14, 15, 10]},
        },
        'variants': [
            {'naam': 'Sikahert (roodbruin, crème gewei)', 'body': '#a05a30', 'antlers': '#e8d8b0', 'legs': '#3a2a20',
             'bulbs': '#f04040'},
            {'naam': 'Cernunnos (woudgroen)', 'body': '#3a8a50', 'antlers': '#a0e080', 'legs': '#2a3020', 'bulbs': '#f0a0c0'},
            {'naam': 'Sakura-hert van Nara (roze)', 'body': '#e090b0', 'antlers': '#f8e0e8', 'legs': '#5a3048', 'bulbs': '#80d0f0'},
            {'naam': 'Shishigami als Nachtloper (Mononoke: nachtblauw)', 'body': '#283068', 'antlers': '#80b0f0',
             'legs': '#101830', 'bulbs': '#f0f0a0'},
            {'naam': 'Herfsthert (oranje, gouden gewei)', 'body': '#d07030', 'antlers': '#f0c040', 'legs': '#4a2a18',
             'bulbs': '#e03030'},
            {'naam': 'Hinde van Keryneia (wit, gouden gewei, bronzen hoeven)', 'body': '#e8e0cc', 'antlers': ('#e0b030', {'h': 0}),
             'legs': '#a06830', 'bulbs': '#e0b030'},
        ],
    },
    'yveltal': {
        # vernietigingsvogel: lijf (zwart), grijze veren, rood, ogen
        'species': {'yveltal': {'body': [3, 1, 13, 14], 'grey': [2, 5, 6], 'red': [8, 7, 9, 10], 'eyes': [11]}},
        'variants': [
            {'naam': 'Gier (bruin, beige kraag, rode kop)', 'body': '#4a3828', 'grey': '#a08868', 'red': '#d07060', 'eyes': '#f0d040'},
            {'naam': 'Blauw doodsvuur', 'body': '#202838', 'grey': '#7080a0', 'red': '#3070f0', 'eyes': '#f04040'},
            {'naam': 'Necrose (gifgroen)', 'body': '#1c2a20', 'grey': '#708070', 'red': '#40d040', 'eyes': '#f040f0'},
            {'naam': 'Engel des doods (wit met goud)', 'body': ('#b8b8c4', {'l': 1.2}), 'grey': '#f0f0f4', 'red': '#e0b030',
             'eyes': '#3060d0'},
            {'naam': 'Nidhöggr (paars, de wortelknager)', 'body': '#20182c', 'grey': '#6a5a80', 'red': '#a040e0', 'eyes': '#40f0a0'},
            {'naam': 'Kronos (zwart met goud)', 'body': '#1a1820', 'grey': '#6a6050', 'red': ('#e0b030', {'h': 0}), 'eyes': '#e02020'},
        ],
    },
    'zygarde': {
        # ordehond/-slang: lijf (donker), cellen/aders (groen), kern (rood), blauw (Complete)
        'species': {
            'zygarde': {'body': [2, 3, 1], 'green': [5, 6, 4, 8]},
            'zygarde/10_percent': {'body': [4, 2, 1], 'green': [9, 10, 7, 6, 5], 'red': [11, 12]},
            'zygarde/complete': {'body': [3, 2, 1], 'green': [5, 8, 9, 6, 15], 'red': [10, 11, 12], 'blue': [13, 14]},
        },
        'variants': [
            {'naam': 'Rode cellen', 'green': '#e03030', 'body': '#2c2028', 'red': '#f0d040', 'blue': '#f0d040'},
            {'naam': 'Tron (cyaan op zwart)', 'green': '#40e0f0', 'body': '#1a2030', 'red': '#f040c0', 'blue': '#f0f040'},
            {'naam': 'Lava (oranje aders)', 'green': '#f08020', 'body': '#2a2020', 'red': '#40c0f0', 'blue': '#40c0f0'},
            {'naam': 'Ultra-ruimte (paars)', 'green': '#a050f0', 'body': '#20182c', 'red': '#f0e040', 'blue': '#40f0a0'},
            {'naam': 'Woestijn (zandkleur met turkoois)', 'green': '#30c0b0', 'body': '#8a7050', 'red': '#e05030',
             'blue': '#f0d040'},
            {'naam': 'Quetzalcoatl (goud en jade)', 'green': ('#e0b030', {'h': 0}), 'body': '#3a2a18', 'red': '#30a070',
             'blue': '#30a070'},
        ],
    },
    'diancie': {
        # juwelenprinses: roze edelsteen, rotslijf, goud, witte kristallen
        'species': {'diancie': {'pink': [2, 3, 4, 5], 'rock': [7, 6, 8], 'gold': [10, 11], 'white': [14, 15], 'gem': [12]}},
        'variants': [
            {'naam': 'Aquamarijn (zilver)', 'pink': '#90d0e8', 'rock': '#6a7080', 'gold': '#e0e0e8', 'gem': '#3080e0'},
            {'naam': 'Smaragd', 'pink': '#60d090', 'rock': '#5a6a60', 'gold': '#f0d040', 'gem': '#208050'},
            {'naam': 'Topaas (zilver)', 'pink': '#f0c060', 'rock': '#7a6a58', 'gold': '#e0e0e8', 'gem': '#c06020'},
            {'naam': 'Amethist', 'pink': '#b090e0', 'rock': '#5a5070', 'gold': '#f0d040', 'gem': '#7030c0'},
            {'naam': 'Zwarte diamant (onyx)', 'pink': '#6a6a7a', 'rock': ('#2a2a34', DARK), 'gold': '#e0e0e8', 'gem': '#e0e0f0'},
            {'naam': 'De Hope-diamant (vervloekt diepblauw)', 'pink': '#3a58c8', 'rock': '#3a3a50', 'gold': '#f0f0f8',
             'gem': '#f0f0f8', 'white': '#c0d0f0'},
        ],
    },
    'hoopa': {
        # djinn: roze (kop/armen), lijf (lavendel), gouden ringen, edelsteen
        'species': {
            'hoopa': {'pink': [3, 2, 1], 'lavender': [7, 10], 'gold': [12, 13, 9, 11], 'gem': [14]},
            'hoopa/unbound': {'pink': [11, 6, 5], 'lavender': [4, 7], 'gold': [10, 8, 13, 9]},
        },
        'variants': [
            {'naam': 'De Geest van Aladdin (blauw)', 'pink': '#4080e0', 'lavender': '#c8d8f0', 'gold': '#f0c030', 'gem': '#e03030'},
            {'naam': 'Paarse djinn', 'pink': '#8040c0', 'lavender': '#e0d0f0', 'gold': '#f0c030', 'gem': '#40e080'},
            {'naam': 'Jafar als djinn (rood en zwart)', 'pink': '#a01828', 'lavender': ('#3a3a44', DARK), 'gold': '#f0c030',
             'gem': '#40c0f0'},
            {'naam': 'Perzische tegels (turkoois)', 'pink': '#30b0b0', 'lavender': '#f0e8d8', 'gold': '#d0a040', 'gem': '#d03050'},
            {'naam': 'Ifrit (rook en vuur)', 'pink': ('#2c2c38', DARK), 'lavender': '#6a6a78', 'gold': '#f08020', 'gem': '#f04040'},
            {'naam': 'Zilveren wonderlamp (saffier)', 'pink': ('#c0c4d0', {'l': 1.2}), 'lavender': '#f0f0f8', 'gold': '#d0d0d8',
             'gem': '#3060e0'},
        ],
    },
    'volcanion': {
        # stoommachine: lijf (rood), stoomring/armen (cyaan), goud
        'species': {'volcanion': {'body': [4, 5, 2], 'cyan': [9, 7, 10, 11], 'gold': [3, 12, 13, 14, 1, 6]}},
        'variants': [
            {'naam': 'Omgekeerd (blauw met rode stoom)', 'body': '#3060b0', 'cyan': '#f04030', 'gold': '#f0e0a0'},
            {'naam': 'Basalt (zwart met gloeiende oranje stoom)', 'body': ('#3a3a44', DARK), 'cyan': '#f08020', 'gold': '#c0c0c8'},
            {'naam': 'Steampunk (messing, witte stoom)', 'body': '#b08040', 'cyan': '#f0f0f0', 'gold': '#6a4020'},
            {'naam': 'Paars magma', 'body': '#7a3a90', 'cyan': '#f0d040', 'gold': '#f0a0f0'},
            {'naam': 'Grand Prismatic Spring (turkoois met oranje)', 'body': '#30a0a0', 'cyan': '#f08030', 'gold': '#f0e060'},
            {'naam': 'Gouden stoommachine', 'body': ('#d8a830', {'h': 0}), 'cyan': '#f0f0f8', 'gold': '#7a3a18'},
        ],
    },
}
