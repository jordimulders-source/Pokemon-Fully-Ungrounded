"""Recepten voor de kleurvarianten, per evolutielijn.

'species': per map (onder graphics/pokemon/) welke paletindexen bij welk onderdeel
horen. 'variants': 6 varianten op volgorde van zeldzaamheid (10 / 6 / 4 / 3 / 1,5 /
0,5%); per onderdeel de doelkleur van de meest gebruikte index van die groep, of
(kleur, {'l': lichtheidsschaal, 'c': vaste verzadigingsfactor}). Onderdelen die niet
genoemd worden, blijven zoals ze zijn. Een sleutel 'soort:onderdeel' geldt maar voor
één soort (voor lijnen die bij het evolueren van kleur wisselen).
"""

ALBINO = {'l': 1.0}

LINES = {
    'charmander': {
        'species': {
            'charmander': {'body': [7, 8, 9], 'belly': [4, 5, 6], 'flame': [13, 14, 15], 'eyes': [10, 11, 12]},
            'charmeleon': {'body': [4, 5, 6, 7], 'belly': [8, 9, 12], 'flame': [13, 14, 15], 'eyes': [11]},
            'charizard': {'body': [7, 8, 9], 'belly': [5, 6], 'flame': [13, 14, 15], 'wings': [11, 12],
                          'eyes': [10]},  # ogen: eigen index via sprite_fixes.py
        },
        'variants': [
            {'naam': 'Squirtle-kleuren, witheet vuur', 'body': '#3f7fc0', 'belly': '#e8c888',
             'flame': ('#e8e8f8', {'l': 0.7}), 'wings': '#7a4818'},
            {'naam': 'Bulbasaur-kleuren, violette vlam (kalium)', 'body': '#2f8a80', 'belly': '#98d8b8',
             'flame': '#9038e0', 'wings': '#3c6c20'},
            {'naam': 'Axolotl, groene vlam (koper)', 'body': '#d87898', 'belly': '#f8d0dc', 'flame': '#20b040',
             'wings': '#b84878'},
            {'naam': 'Albino (rode ogen, blauwe gasvlam)', 'body': ('#c4baba', ALBINO), 'belly': ('#f4ecd8', ALBINO),
             'flame': '#3c8cf8', 'eyes': '#d02030', 'wings': ('#bcb0b0', ALBINO)},
            {'naam': 'Mega X (zwart, blauwe vlam)', 'body': ('#343c4c', {'l': 0.8}), 'belly': '#4aa8e0',
             'flame': '#2058ff', 'wings': '#283448', 'eyes': '#e02828'},
            {'naam': 'Synthwave', 'body': '#7038c0', 'belly': '#ff68b8', 'flame': '#18d8f8',
             'wings': '#2c1468'},
        ],
    },
    'bulbasaur': {
        'species': {
            'bulbasaur': {'body': [2, 3, 4, 5], 'spots': [15], 'leaves': [11, 12, 13, 14], 'eyes': [6, 7, 8]},
            'ivysaur': {'body': [5, 6, 7, 8], 'flower': [2, 3, 4, 14], 'leaves': [9, 10, 11, 12]},
            'venusaur': {'body': [1, 2, 3, 4], 'flower': [5, 6, 12], 'trunk': [7, 8], 'center': [9, 10],
                         'leaves': [13, 14]},
        },
        'variants': [
            {'naam': 'Charmander-kleuren', 'body': '#d06030', 'spots': '#902818', 'leaves': '#e8a020',
             'flower': '#f04818'},
            {'naam': 'Squirtle-kleuren', 'body': '#5088b8', 'spots': '#285478', 'leaves': '#98601c',
             'flower': '#e8c070'},
            {'naam': 'Pijlgifkikker', 'body': '#1c4cd0', 'spots': '#101828'},
            {'naam': 'Albino', 'body': ('#c8c8c0', ALBINO), 'spots': ('#b0a4a4', ALBINO),
             'leaves': ('#e8b4c4', ALBINO), 'flower': ('#f0e4ec', ALBINO), 'eyes': '#e83050'},
            {'naam': 'Sakura', 'leaves': '#e088a8', 'flower': '#f0ecff', 'center': '#f8c8e0'},
            {'naam': 'Radioactief', 'body': ('#232a32', {'l': 0.8}), 'spots': '#38f058',
             'leaves': '#38e038', 'flower': '#ff28b8', 'trunk': '#202020'},
        ],
    },
    'squirtle': {
        'species': {
            'squirtle': {'body': [11, 12, 13, 14], 'shell': [3, 4, 5], 'belly': [6, 7, 8, 9],
                         'lines': [10]},  # 10 = kinlijn/buikrand én pupillen
            'wartortle': {'body': [11, 12, 13, 14], 'fur': [2, 3], 'shell': [6, 7], 'belly': [8, 9, 10],
                          'eyes': [4, 5]},
            'blastoise': {'body': [6, 7, 8, 9], 'shell': [13, 14, 15], 'belly': [11], 'cannons': [3, 4, 5],
                          'eyes': [10]},
        },
        'variants': [
            {'naam': 'Charmander-kleuren', 'body': '#d86838', 'shell': '#982818', 'fur': '#f8d048'},
            {'naam': 'Soepschildpad', 'body': '#8a7448', 'shell': '#3c4c1c', 'belly': '#e8d070', 'fur': '#d8e8b0'},
            {'naam': 'Koopa', 'body': '#e0b830', 'shell': '#c82018', 'fur': '#f8f8f0'},
            {'naam': 'Albino', 'body': ('#c4c4d0', ALBINO), 'shell': ('#e4d4a0', ALBINO),
             'belly': '#d8ccb4', 'fur': ('#dcdce8', ALBINO), 'eyes': '#e02030',
             'lines': '#782028'},
            {'naam': 'Ninja Turtle', 'body': '#4e9a2c', 'shell': '#704414', 'belly': '#f0c838'},
            {'naam': 'Vaporwave', 'body': '#f078b8', 'shell': '#28c0e0', 'belly': '#d0b8ec',
             'fur': '#98f0ff', 'cannons': '#8048d8'},
        ],
    },

    # --- Hoenn-dex, groep 1: starters ---
    'treecko': {
        # tail = Treecko's staart, Grovyles hoofdblad + staart, Sceptiles staart (+ stukje tussen de benen);
        # armleaves = Grovyles armbladeren (eigen indices via sprite_fixes.py)
        'species': {
            'treecko': {'body': [1, 3, 4, 5], 'tail': [13, 14, 15], 'belly': [10, 11, 12], 'eyes': [6, 8, 9]},
            'grovyle': {'body': [5, 6, 7, 8], 'tail': [1, 2, 3], 'armleaves': [13, 15], 'belly': [11, 12, 14],
                        'eyes': [9, 10]},
            'sceptile': {'body': [1, 2, 3, 4, 5], 'tail': [12, 13, 14, 15], 'belly': [9, 10], 'seeds': [7, 8, 11]},
        },
        'variants': [
            {'naam': 'Torchic-kleuren', 'body': '#e87828', 'tail': '#c09818', 'armleaves': '#c09818',
             'belly': '#f0d060'},
            {'naam': 'Mudkip-kleuren (vinnen als Swampert, oranje bladeren)', 'body': '#3890d0', 'tail': '#504a58',
             'armleaves': '#e07828', 'belly': '#e07828'},
            {'naam': 'Tokeh', 'body': '#a4b0c4', 'tail': '#e08828', 'armleaves': '#e08828', 'belly': '#dcdce4',
             'seeds': '#e08828'},
            {'naam': 'Albino', 'body': ('#c8c8bc', ALBINO), 'tail': ('#a8aca0', ALBINO),
             'armleaves': ('#a8aca0', ALBINO), 'belly': '#e0a8b0', 'eyes': '#d02030', 'seeds': '#e8d8c8'},
            {'naam': 'Pikachu', 'body': '#f0c828', 'tail': '#986020', 'armleaves': '#986020', 'seeds': '#d83020'},
            {'naam': 'Cyberpunk', 'body': ('#2c2c38', {'l': 0.8}), 'tail': '#28e870', 'armleaves': '#28e870',
             'belly': '#ff3090', 'eyes': '#30e8ff', 'seeds': '#30e8ff'},
        ],
    },
    'torchic': {
        'species': {
            'torchic': {'main': [5, 6, 7, 8, 9], 'second': [1, 2, 3], 'feet': [11, 12, 13, 14]},
            'combusken': {'main': [1, 3, 4, 8], 'second': [5, 6, 7], 'feet': [10, 11, 12, 13, 14]},
            'blaziken': {'main': [1, 5, 6, 9], 'second': [3, 4, 7, 8, 13], 'flame': [10, 12, 15], 'eyes': [11]},
        },
        'variants': [
            {'naam': 'Treecko-kleuren', 'main': '#70a830', 'second': '#386838', 'flame': '#e04868'},
            {'naam': 'Mudkip-kleuren', 'main': '#68b8e0', 'second': '#c8d4ec', 'feet': '#e88830'},
            {'naam': 'Flamingo, cyaan vuur', 'main': '#f07898', 'second': '#f8c8d0', 'feet': '#d86878',
             'flame': '#30c8f0'},
            {'naam': 'Albino', 'main': ('#c8bebe', ALBINO), 'second': ('#d4ccc4', ALBINO), 'feet': '#d8a8a8',
             'flame': '#38a8f8', 'eyes': '#d02030'},
            {'naam': 'Ayam Cemani (zwarte kip)', 'main': ('#3c3844', {'l': 1.3}), 'second': ('#4c4854', {'l': 1.3}),
             'feet': ('#34303c', {'l': 1.3})},
            {'naam': 'Captain Falcon', 'main': '#2c44a8', 'second': '#f0c020', 'feet': '#d83020',
             'flame': '#f04818'},
        ],
    },
    'mudkip': {
        'species': {
            'mudkip': {'body': [1, 2, 3, 4, 9], 'belly': [6, 7, 8], 'cheeks': [10, 11, 12], 'eyes': [14]},
            'marshtomp': {'body': [4, 5, 6, 7, 8], 'crest': [1, 3], 'belly': [10, 13], 'cheeks': [9, 11, 12]},
            'swampert': {'body': [4, 5, 6, 10], 'crest': [2, 3], 'belly': [13, 14, 15], 'cheeks': [7, 8, 9]},
        },
        'variants': [
            {'naam': 'Torchic-kleuren', 'body': '#e88030', 'crest': '#a88010', 'belly': '#f0e0b0', 'cheeks': '#f0d040'},
            {'naam': 'Treecko-kleuren', 'body': '#70a830', 'crest': '#305830', 'belly': '#d8f0a0', 'cheeks': '#e04868'},
            {'naam': 'Slijkspringer', 'body': '#887850', 'crest': '#504030', 'belly': '#d8d0b0', 'cheeks': '#3898e0'},
            {'naam': 'Axolotl (leucistisch)', 'body': '#dcbcc0', 'crest': '#d0a4ac', 'belly': '#ecd8d8',
             'cheeks': '#e83870', 'eyes': '#283048'},
            {'naam': 'Koi (Showa)', 'body': ('#282830', {'l': 0.8}), 'crest': '#d82818', 'belly': '#e8e8e8',
             'cheeks': '#e83018'},
            {'naam': 'Axolotl (GFP, lichtgevend)', 'body': '#d4e4a4', 'crest': '#38e858', 'belly': '#f0f8d8',
             'cheeks': '#20ff50'},
        ],
    },

    # --- Hoenn-dex, groep 2 ---
    'poochyena': {
        'species': {
            'poochyena': {'grey': [3, 4], 'dark': [1, 5, 13], 'eyes': [6, 7], 'mouth': [8, 10]},
            'mightyena': {'grey': [2, 3, 4], 'dark': [5, 6], 'eyes': [8, 9], 'mouth': [7, 10, 11]},
        },
        'variants': [
            {'naam': 'Blauwe merle', 'grey': '#8a9cc0', 'dark': '#202430', 'eyes': '#58b0f0'},
            {'naam': 'Rode wolf', 'grey': '#c87838', 'dark': '#4c2c20'},
            {'naam': 'Poolwolf', 'grey': '#c4c8d0', 'dark': '#7c8490', 'eyes': '#58b8e8'},
            {'naam': 'Albino', 'grey': ('#c4c0c0', ALBINO), 'dark': ('#9c9494', ALBINO), 'eyes': '#d02030',
             'mouth': '#e08898'},
            {'naam': 'Midnight Lycanroc', 'grey': '#b83838', 'dark': '#28242c', 'eyes': '#58e070'},
            {'naam': 'Amaterasu (Okami)', 'grey': '#d8dce6', 'dark': '#c02030', 'eyes': '#e83030', 'mouth': '#c02030'},
        ],
    },
    'zigzagoon': {
        'species': {
            'zigzagoon': {'light': [3, 4, 13], 'brown': [1, 5, 6, 10], 'dark': [7, 8, 12]},
            'linoone': {'light': [4, 5], 'brown': [2, 3, 8, 13], 'eyes': [9, 10]},
        },
        'variants': [
            {'naam': 'Wasbeer', 'light': '#b4b4b4', 'brown': '#5c5c60'},
            {'naam': 'Aardbeienmelk', 'light': '#f6e0e6', 'brown': '#d86890', 'dark': '#682838'},
            {'naam': 'Pikachu-kleuren', 'light': '#f8ecb8', 'brown': '#f0c020', 'dark': '#6a4020', 'eyes': '#e84830'},
            {'naam': 'Albino', 'light': ('#d4cccc', ALBINO), 'brown': ('#bcb0b0', ALBINO), 'dark': '#a08888',
             'eyes': '#d02030'},
            {'naam': 'Sonic', 'light': '#f0c890', 'brown': '#2860d0', 'dark': '#183880', 'eyes': '#38c048'},
            {'naam': 'Vaporwave', 'light': '#78ecf4', 'brown': '#c03898', 'dark': '#581870'},
        ],
    },
    'wurmple': {
        'species': {
            'wurmple': {'body': [1, 2, 3, 4], 'spikes': [6, 7, 8], 'face': [9, 10, 11], 'tail': [12, 13, 14]},
            'silcoon': {'shell': [1, 2, 3, 4, 6], 'eye': [7, 8]},
            'cascoon': {'shell': [1, 3, 4, 5, 6], 'eye': [8, 9, 11, 12]},
            'beautifly': {'body': [1, 3, 5, 6], 'wing': [7, 8, 9], 'spots': [10, 11], 'face': [2, 12],
                          'blue': [13, 14, 15]},
            'dustox': {'wing': [9, 10, 11, 12, 13], 'body': [3, 6, 7, 8], 'yellow': [1, 2, 4], 'spots': [14, 15]},
        },
        'variants': [
            {'naam': 'Monarchvlinder', 'wurmple:body': '#e8c020', 'spikes': '#303030', 'shell': '#58c088',
             'beautifly:wing': '#f07818', 'beautifly:spots': '#f0f0f0', 'dustox:wing': '#e87818',
             'dustox:spots': '#f0f0f0', 'dustox:body': '#383038'},
            {'naam': 'Blauwe morpho', 'wurmple:body': '#2860c8', 'shell': '#a08050', 'beautifly:wing': '#3080f0',
             'beautifly:spots': '#182850', 'dustox:wing': '#2858c0', 'dustox:spots': '#f0d020'},
            {'naam': 'Maanvlinder', 'wurmple:body': '#78c040', 'shell': '#c8e4b0', 'beautifly:wing': '#b8e898',
             'beautifly:spots': '#c060a0', 'dustox:wing': '#bce890', 'dustox:spots': '#c060a0'},
            {'naam': 'Melanisme (zwart)', 'wurmple:body': ('#403840', {'l': 1.3}), 'spikes': '#d83040',
             'shell': ('#44444e', {'l': 1.3}), 'beautifly:wing': '#d0d0d8', 'beautifly:body': '#202024',
             'dustox:wing': ('#343438', {'l': 1.3}), 'dustox:body': '#1c1c20'},
            {'naam': 'Kanto-neven (Caterpie, Metapod, Kakuna, Butterfree, Venomoth)', 'wurmple:body': '#78b838',
             'spikes': '#e88830', 'silcoon:shell': '#58a848', 'cascoon:shell': '#e0c030',
             'beautifly:wing': '#e4e4ec', 'beautifly:body': '#4048a0', 'dustox:wing': '#c8a8e0',
             'dustox:body': '#6040a0', 'dustox:spots': '#7050b0'},
            {'naam': 'Neon', 'wurmple:body': '#f040a0', 'spikes': '#30e8f8', 'shell': '#40e0f0',
             'beautifly:wing': '#30e0f8', 'beautifly:spots': '#ff30b0', 'beautifly:body': '#202028',
             'dustox:wing': '#e030a0', 'dustox:spots': '#30e8f8', 'dustox:body': '#282030'},
        ],
    },
    'lotad': {
        'species': {
            'lotad': {'leaf': [1, 3, 4, 5, 8], 'body': [6, 7, 11, 13], 'beak': [9, 10, 14]},
            'lombre': {'leaf': [1, 3, 4, 5], 'body': [8, 9, 13], 'red': [10, 11, 12]},
            'ludicolo': {'leaf': [6, 7, 9, 10, 11], 'body': [3, 4, 5], 'stripes': [2, 8], 'mouth': [13, 14, 15]},
        },
        'variants': [
            {'naam': 'Lotus (roze)', 'leaf': '#e078a0'},
            {'naam': 'Día de los Muertos', 'leaf': '#f08c10', 'body': '#7034a8', 'ludicolo:body': '#e4dcd0',
             'stripes': '#242024', 'red': '#e02890', 'beak': '#e02890', 'mouth': '#e02890'},
            {'naam': 'Mandarijneend', 'leaf': '#207050', 'body': '#e07830', 'beak': '#d83030', 'red': '#3858c8'},
            {'naam': 'Albino', 'leaf': ('#c4d0bc', ALBINO), 'body': ('#c8c8d4', ALBINO), 'beak': '#e0a8a8',
             'red': '#e0a0b0', 'stripes': ('#b8b0a8', ALBINO), 'ludicolo:body': ('#d8d4c4', ALBINO)},
            {'naam': 'Kappa', 'leaf': '#8c9098', 'body': '#3cb058', 'ludicolo:body': '#3cb058', 'stripes': '#286838'},
            {'naam': 'Gouden idool', 'leaf': '#d8a828', 'body': '#c89028', 'ludicolo:body': '#e0b838',
             'stripes': '#7a4c18', 'red': '#28a8a0', 'beak': '#28a8a0'},
        ],
    },
    'seedot': {
        'species': {
            'seedot': {'hair': [1, 2, 4, 5, 6], 'body': [7, 9, 12], 'face': [8, 10, 11]},
            'nuzleaf': {'leaf': [1, 2, 3, 4], 'body': [7, 8, 11], 'face': [6, 9, 10, 12]},
            'shiftry': {'leaf': [6, 9, 10], 'body': [1, 2, 5, 7], 'hair': [3, 8, 11, 12], 'eyes': [13]},
        },
        'variants': [
            {'naam': 'Onrijpe eikel', 'body': '#80a040', 'hair': '#8a6840', 'leaf': '#c0b040'},
            {'naam': 'Tengu', 'body': '#c83020', 'hair': '#303034', 'face': '#f0d8c0'},
            {'naam': 'Sakura', 'leaf': '#f090b0', 'hair': '#f8e0ec', 'body': '#5c3a2c'},
            {'naam': 'Albino', 'body': ('#c8bcb4', ALBINO), 'face': ('#ddd4cc', ALBINO), 'leaf': ('#c4ccbc', ALBINO),
             'hair': ('#d0d0d8', ALBINO), 'eyes': '#d02030'},
            {'naam': 'Oni', 'body': '#3858c0', 'hair': '#28282c', 'leaf': '#e0b020', 'face': '#c8d0f0', 'eyes': '#f02828'},
            {'naam': 'Winterdemon (Grass/Ice)', 'body': '#5c7cb8', 'hair': '#eef4fc', 'leaf': '#9cdcf0',
             'face': '#d8e8f8', 'eyes': '#f02838'},
        ],
    },

    # --- Hoenn-dex, groep 3 ---
    'taillow': {
        'species': {
            'taillow': {'blue': [1, 2, 5], 'red': [3, 4], 'white': [7, 8], 'beak': [10, 11, 12, 13]},
            'swellow': {'blue': [1, 4, 5], 'red': [2, 3, 6], 'white': [9, 10], 'beak': [8, 11, 12, 13]},
        },
        'variants': [
            {'naam': 'Roodborst', 'blue': '#7a6048', 'red': '#e87030', 'white': '#f0e4d0'},
            {'naam': 'IJsvogel', 'blue': '#1898c0', 'red': '#f07020', 'white': '#f0d8b8'},
            {'naam': 'Kardinaal', 'blue': '#c02028', 'red': '#202024', 'beak': '#e86030'},
            {'naam': 'Albino', 'blue': ('#c4c4cc', ALBINO), 'red': '#e0a8b4', 'beak': '#e8c8b0'},
            {'naam': 'Blauw-gele ara', 'blue': '#2848c0', 'red': '#f0c020', 'white': '#f8f0c8'},
            {'naam': 'Zwaluwstaart (rokkostuum)', 'blue': ('#24242a', {'l': 1.3}), 'red': '#e4e0d8',
             'beak': '#d8b030'},
        ],
    },
    'wingull': {
        'species': {
            'wingull': {'white': [3, 4], 'wings': [5, 6, 7], 'beak': [9, 10, 12]},
            'pelipper': {'white': [6, 7, 8, 15], 'wings': [1, 3, 4, 5], 'beak': [9, 10, 11, 12, 13]},
        },
        'variants': [
            {'naam': 'Bruine pelikaan', 'white': '#c8b8a0', 'wings': '#7a5838'},
            {'naam': 'Papegaaiduiker', 'wings': '#242428', 'beak': '#e85020'},
            {'naam': 'Galah (roze kaketoe)', 'white': '#f0c4d4', 'wings': '#8c94a4', 'beak': '#e8e0d8'},
            {'naam': 'Melanisme', 'white': ('#50505c', {'l': 1.3}), 'wings': '#202024'},
            {'naam': 'Postbode (PostNL)', 'wings': '#f07818', 'beak': '#283c88'},
            {'naam': 'Onweersvogel', 'white': '#6c7484', 'wings': '#f0d020', 'beak': '#283048'},
        ],
    },
    'ralts': {
        'species': {
            'ralts': {'hair': [5, 6, 7, 8], 'horn': [1, 2, 3], 'body': [9, 10, 11, 12]},
            'kirlia': {'hair': [2, 6, 7, 8], 'horn': [1, 3, 4], 'body': [9, 10, 11]},
            'gardevoir': {'hair': [1, 2, 3, 4], 'horn': [8, 11, 13], 'body': [6, 7, 10, 12]},
            'gallade': {'hair': [1, 3, 7], 'horn': [12, 13, 14], 'body': [8, 9, 10, 11], 'legs': [4, 5, 6]},
        },
        'variants': [
            {'naam': 'Lavendel', 'hair': '#9070c8', 'horn': '#28a898'},
            {'naam': 'Roos (rood en groen omgedraaid)', 'hair': '#d84868', 'horn': '#58b858'},
            {'naam': 'Hemelsblauw', 'hair': '#58a8e8', 'horn': '#e8b828', 'legs': '#4870b0'},
            {'naam': 'Albino', 'hair': ('#ccd8c4', ALBINO), 'horn': '#e8a8b8'},
            {'naam': 'Zwarte zwaan (ballet)', 'body': ('#2c2c34', {'l': 1.3}), 'hair': '#4c5058', 'horn': '#d82838',
             'legs': '#202024'},
            {'naam': 'Hyrule-koninklijk (Zelda)', 'hair': '#e8c040', 'body': '#d0b8ec', 'horn': '#3060d0',
             'legs': '#6848a8'},
        ],
    },
    'surskit': {
        'species': {
            'surskit': {'body': [6, 7, 8], 'head': [1, 2, 4, 5], 'cheeks': [11, 12]},
            'masquerain': {'body': [7, 9, 11, 12], 'wingedge': [1, 2, 4], 'wing': [5, 6], 'eyespots': [8, 10]},
        },
        'variants': [
            {'naam': 'Rode waterjuffer', 'body': '#d03838', 'wingedge': '#d03838', 'eyespots': '#3060d0'},
            {'naam': 'Dagpauwoog', 'body': '#8a5838', 'head': '#3868d0', 'wingedge': '#a83020', 'eyespots': '#2858d0'},
            {'naam': 'Groene glazenmaker', 'body': '#30a860', 'head': '#3070e0', 'wingedge': '#20a0a0',
             'eyespots': '#e8c020'},
            {'naam': 'Albino', 'body': ('#c8ccd8', ALBINO), 'head': '#e8e0c0', 'wingedge': '#e8c4b4',
             'eyespots': '#d83040'},
            {'naam': 'Mothra', 'body': '#d8d0c0', 'surskit:body': '#8a6a50', 'head': '#3c78e0',
             'wingedge': '#f0a018', 'eyespots': '#2050d0'},
            {'naam': 'Luxury Ball', 'body': ('#2c2c30', {'l': 1.3}), 'head': '#d82828', 'wingedge': '#e0b030',
             'eyespots': '#d82828', 'cheeks': '#e0b030'},
        ],
    },
    'shroomish': {
        'species': {
            'shroomish': {'cap': [1, 2, 3, 5, 9], 'spots': [6, 7, 8, 10], 'red': [11, 12]},
            'breloom': {'cap': [8, 9, 10, 11], 'spots': [1, 2, 3], 'red': [4, 5, 7]},
        },
        'variants': [
            {'naam': 'Vliegenzwam', 'cap': '#d02820', 'spots': '#ece8dc', 'breloom:cap': '#d02820',
             'breloom:spots': '#e4dccc', 'breloom:red': '#f0f0e8'},
            {'naam': 'Cantharel', 'cap': '#e8a020', 'spots': '#c87818', 'breloom:spots': '#a87830'},
            {'naam': 'Toad', 'cap': '#ece8e0', 'spots': '#d82828', 'breloom:spots': '#3058c0'},
            {'naam': 'Albino', 'cap': ('#d0ccc4', ALBINO), 'spots': ('#c4c4bc', ALBINO), 'red': '#d83040'},
            {'naam': 'Amethistzwam', 'cap': '#8048b0', 'spots': '#c8a8e8', 'breloom:spots': '#6838a0',
             'red': '#e8d040'},
            {'naam': 'Lichtgevende zwam', 'cap': ('#1c4250', {'l': 1.2}), 'spots': '#60f088',
             'breloom:spots': '#2c5868', 'red': '#60f088'},
        ],
    },

    # --- Hoenn-dex, groep 4 ---
    'slakoth': {
        'species': {
            'slakoth': {'fur': [1, 5, 6, 7], 'face': [3, 4], 'nose': [11, 12, 13]},
            'vigoroth': {'fur': [6, 7, 10], 'face': [8, 9, 15], 'mane': [1, 2, 4]},
            'slaking': {'fur': [2, 5, 6], 'face': [8, 9], 'mane': [3, 4, 7], 'nose': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Grijze luiaard', 'fur': '#80848c', 'vigoroth:fur': '#5c5c64', 'mane': '#d8c8b0'},
            {'naam': 'Algenvacht (echte luiaards hebben algen)', 'fur': '#7a9050', 'vigoroth:fur': '#a8c080'},
            {'naam': 'Goudaap', 'fur': '#e0a040', 'face': '#7898c8', 'slaking:face': '#f0e0b8', 'mane': '#f0d088'},
            {'naam': 'Albino', 'fur': ('#cdc4bc', ALBINO), 'face': ('#e0d8d0', ALBINO), 'nose': '#e08898',
             'mane': '#e0b0b8'},
            {'naam': 'Zilverrug', 'fur': ('#2c2c30', {'l': 1.3}), 'vigoroth:fur': '#c4c8d0', 'mane': '#c4c8d0',
             'face': '#58585c'},
            {'naam': 'Garfield', 'fur': '#f08820', 'vigoroth:fur': '#f8b048', 'face': '#f8e0a0', 'mane': '#a85010'},
        ],
    },
    'abra': {
        'species': {
            'abra': {'yellow': [9, 10, 11, 12, 13, 14], 'brown': [4, 5, 6, 7]},
            'kadabra': {'yellow': [10, 11, 12, 13, 14], 'brown': [6, 7, 8, 9], 'spoon': [1, 2, 3, 4], 'star': [5]},
            'alakazam': {'yellow': [11, 12, 13, 14], 'brown': [5, 6, 7, 8], 'spoon': [1, 2, 3, 4]},
        },
        'variants': [
            {'naam': 'Rode vos', 'yellow': '#e07830', 'brown': '#4c3020'},
            {'naam': 'Zilvervos', 'yellow': '#b8bcc8', 'brown': '#2c2c30', 'spoon': '#e0b030'},
            {'naam': 'Tovenaar', 'yellow': '#3050b0', 'brown': '#6838a0', 'spoon': '#e0b030', 'star': '#f0d020'},
            {'naam': 'Albino', 'yellow': ('#d8d0c0', ALBINO), 'brown': ('#bcaca4', ALBINO), 'star': '#d02030'},
            {'naam': 'Mewtwo-kleuren', 'yellow': '#d4c4e4', 'brown': '#8048a0'},
            {'naam': 'Joker', 'yellow': '#7838b0', 'brown': '#38a040', 'star': '#e02020'},
        ],
    },
    'nincada': {
        'species': {
            'nincada': {'shell': [6, 7, 8, 9, 10, 11], 'wings': [1, 3, 5], 'claws': [12, 13, 14, 15]},
            'ninjask': {'wings': [1, 3, 8, 11], 'red': [5, 6, 7, 9], 'body': [14, 15], 'yellow': [10, 12, 13]},
            'shedinja': {'halo': [1, 2, 3, 4], 'shell': [5, 6, 7, 9, 10, 11]},
        },
        'variants': [
            {'naam': 'Groene cicade', 'shell': '#78b858', 'yellow': '#40b878', 'wings': '#d8f0c8'},
            {'naam': 'Barnsteen', 'shell': '#e09018', 'yellow': '#e09018', 'red': '#a84810', 'wings': '#f8e0a8'},
            {'naam': 'Brons', 'shell': '#a8743c', 'yellow': '#a8743c', 'red': '#5c3c20', 'halo': '#c89050'},
            {'naam': 'Albino', 'shell': ('#ccc8c4', ALBINO), 'yellow': ('#e0dcd0', ALBINO), 'red': '#d02838',
             'claws': '#d8b8b8'},
            {'naam': 'Hemels', 'shell': '#e8c860', 'halo': '#f0c830', 'wings': '#f0d860', 'yellow': '#f0ece0',
             'body': '#283058'},
            {'naam': 'Japans lakwerk', 'shell': ('#2c2028', {'l': 1.3}), 'wings': '#e0b030', 'yellow': '#e0b030',
             'red': '#e04020', 'body': '#1c1418', 'halo': '#e04020'},
        ],
    },
    'whismur': {
        'species': {
            'whismur': {'body': [1, 2, 3, 9, 11], 'yellow': [4, 5, 6, 7]},
            'loudred': {'body': [1, 2, 3, 4], 'pink': [6, 7, 8, 14], 'yellow': [11, 12, 13]},
            'exploud': {'body': [5, 6, 7, 8], 'yellow': [1, 2, 4], 'pink': [9, 10, 11, 12]},
        },
        'variants': [
            {'naam': 'Luidspreker', 'body': '#44444c', 'yellow': '#c0c4cc'},
            {'naam': 'Olifant', 'body': '#9898a0', 'yellow': '#e8e0d0'},
            {'naam': 'KISS', 'body': '#e0e0e8', 'yellow': '#202024', 'pink': '#d82838'},
            {'naam': 'Albino', 'body': ('#d0c8cc', ALBINO), 'yellow': ('#e0dcd0', ALBINO), 'pink': '#e090a0'},
            {'naam': 'Gouden plaat', 'body': '#d8a830', 'yellow': '#28282c'},
            {'naam': 'Banshee', 'body': '#a8d8b8', 'yellow': '#3c4048', 'pink': '#283028'},
        ],
    },
    'makuhita': {
        'species': {
            'makuhita': {'skin': [1, 2, 4, 5, 6, 7], 'belt': [11, 12, 13], 'cheeks': [8, 9]},
            'hariyama': {'skin': [6, 7, 8, 11, 13, 14, 15], 'hands': [2, 3, 4, 5], 'belt': [9, 10]},
        },
        'variants': [
            {'naam': 'Kumamon', 'skin': ('#2c2c30', {'l': 1.3}), 'hands': '#3c3c44', 'cheeks': '#e02828',
             'belt': '#d82828'},
            {'naam': 'Kappa-sumo', 'skin': '#60a848', 'hands': '#3c7c38', 'belt': '#2c58a8'},
            {'naam': 'Hokusai (indigo)', 'skin': '#ece4d0', 'hands': '#3c58a0', 'belt': '#283c78'},
            {'naam': 'Albino', 'skin': ('#e0d8cc', ALBINO), 'hands': '#e0b8b0', 'cheeks': '#e88898'},
            {'naam': 'Lucha libre', 'belt': '#e02890', 'hands': '#e0b030', 'cheeks': '#2858d0'},
            {'naam': 'Daruma', 'skin': '#c83028', 'hands': '#a82020', 'belt': '#e0b030', 'cheeks': '#f0e8d8'},
        ],
    },

    # --- Hoenn-dex, groep 5 ---
    'goldeen': {
        'species': {
            'goldeen': {'white': [2, 4, 5], 'orange': [6, 8, 10, 11], 'eyes': [12, 13], 'fins': [1, 3]},
            'seaking': {'white': [2, 3, 11], 'orange': [7, 8, 9, 10], 'fins': [1, 4, 12]},
        },
        'variants': [
            {'naam': 'Goudvis (helemaal oranje)', 'white': '#f09030', 'orange': '#c82818'},
            {'naam': 'Black Moor', 'white': ('#34343c', {'l': 1.3}), 'orange': '#6c5c4c'},
            {'naam': 'Shubunkin (blauw)', 'white': '#a0c4e8', 'orange': '#e86818'},
            {'naam': 'Panda-oranda', 'orange': '#2c2c30'},
            {'naam': 'Kempvis (halfmoon)', 'white': '#2848c0', 'orange': '#c82838', 'eyes': '#e8c020'},
            {'naam': 'Nemo (clownvis)', 'white': '#f07818', 'orange': '#f0eee8', 'fins': '#1c1c20'},
        ],
    },
    'magikarp': {
        'species': {
            'magikarp': {'body': [3, 4, 8, 9, 12, 14], 'gold': [2, 15], 'fins': [7, 11]},  # 5 = oogwit
            'gyarados': {'body': [3, 5, 6, 7, 9], 'gold': [10, 11, 12], 'fins': [4, 8], 'mouth': [13, 14, 15]},
        },
        'variants': [
            {'naam': 'Omgewisseld (Magikarp blauw, Gyarados oranje)', 'magikarp:body': '#2890b8',
             'magikarp:gold': '#d8c088', 'gyarados:body': '#f07020', 'gyarados:gold': '#f8d828'},
            {'naam': 'Kohaku (koi)', 'body': '#e8e4dc', 'magikarp:body': ('#c4c0b8', {'l': 1.2}), 'fins': '#d03020',
             'magikarp:gold': '#d03020', 'gyarados:gold': '#d03020'},
            {'naam': 'Karasu (zwarte koi)', 'body': ('#2c2c34', {'l': 1.3}), 'fins': '#e87020', 'gold': '#e87020'},
            {'naam': 'Drakenpoort (jade)', 'body': '#38a068', 'gold': '#e0b828', 'fins': '#e8f0d0'},
            {'naam': 'Godzilla', 'body': ('#3c4a3c', {'l': 1.2}), 'fins': '#90c8f0', 'gold': '#707870'},
            {'naam': 'Hemelse draak', 'body': '#c4d8f0', 'fins': '#e8c030', 'gold': '#e8c030'},
        ],
    },
    'azurill': {
        'species': {
            'azurill': {'blue': [1, 2, 3, 4, 8, 9], 'red': [6, 7]},
            'marill': {'blue': [1, 2, 3, 4, 5], 'red': [6, 7, 8], 'belly': [10, 11, 13]},
            'azumarill': {'blue': [1, 2, 3, 8, 11, 15], 'red': [5, 6, 7, 10, 12], 'belly': [9, 13, 14]},
        },
        'variants': [
            {'naam': 'Lavendel', 'blue': '#a888d8', 'red': '#f0c030'},
            {'naam': 'Roze', 'blue': '#f088b0', 'red': '#4098d0'},
            {'naam': 'Sinaasappel', 'blue': '#f09038', 'red': '#48a838', 'belly': '#f8e8c0'},
            {'naam': 'Albino', 'blue': ('#d0d0dc', ALBINO), 'red': '#e890a0'},
            {'naam': 'Sterrennacht (Van Gogh)', 'blue': '#203070', 'red': '#f0c020', 'belly': '#f0e8a8'},
            {'naam': 'Kerstbal', 'blue': '#c82028', 'red': '#e0b030', 'belly': '#f0e8d0'},
        ],
    },
    'geodude': {
        'species': {
            'geodude': {'rock': [2, 3, 4, 5, 6]},
            'graveler': {'rock': [2, 3, 4, 5, 6]},
            'golem': {'rock': [6, 7, 8, 9]},
        },
        'variants': [
            {'naam': 'Koper', 'rock': '#b86838'},
            {'naam': 'Zilver', 'rock': ('#7c8490', {'l': 1.2})},
            {'naam': 'Saffier', 'rock': '#2858c0'},
            {'naam': 'Robijn', 'rock': '#c02838'},
            {'naam': 'Amethist', 'rock': '#8848c0'},
            {'naam': 'Diamant', 'rock': ('#6c98c0', {'l': 1.25})},
        ],
    },
    'nosepass': {
        # rituele beelden uit verschillende culturen (Jordi)
        'species': {
            'nosepass': {'body': [1, 2, 3, 4, 5], 'nose': [7, 8, 9, 10, 11]},
            'probopass': {'body': [9, 10, 11, 12, 13], 'nose': [1, 3, 4, 5], 'beard': [6, 14]},  # 6 is ook de omlijning: altijd donker
        },
        'variants': [
            {'naam': 'Moai (tufsteen met rode pukao)', 'body': '#6c6864', 'nose': '#a84830', 'beard': '#3c3834'},
            {'naam': 'Terracottaleger', 'body': '#b86838', 'nose': '#4c5c78', 'beard': '#3c3030'},
            {'naam': 'Olmeekse jade', 'body': '#48a078', 'nose': '#e0b030', 'beard': '#1c4030'},
            {'naam': 'Azteeks turkoois-mozaïek', 'body': '#30b0a8', 'nose': '#e05038', 'beard': '#1c1c24'},
            {'naam': 'Totempaal', 'body': '#b83028', 'nose': '#202024', 'beard': '#203434'},  # beard 6 = ook omlijning
            {'naam': 'Toetanchamon (goud en lapis)', 'body': '#e0b030', 'nose': '#2848a8', 'beard': '#1c2c68'},
        ],
    },
    'skitty': {
        'species': {
            'skitty': {'main': [5, 6, 7, 8, 12], 'cream': [1, 2, 3, 11], 'tip': [9, 10]},
            'delcatty': {'main': [1, 2, 3, 5], 'cream': [6, 7, 10, 13]},
        },
        'variants': [
            {'naam': 'Siamees', 'main': '#5c3c2c', 'tip': '#3c2820'},
            {'naam': 'Doraemon', 'main': '#2898e0', 'cream': '#f0f0f0', 'tip': '#e02020'},
            {'naam': 'Grijze tabby', 'main': '#8a8a8e', 'tip': '#4c4c54'},
            {'naam': 'Albino', 'main': ('#dcd0d4', ALBINO), 'cream': ('#ece4dc', ALBINO), 'tip': '#e090a8'},
            {'naam': 'Cheshire Cat', 'main': '#c040a0', 'cream': '#7838a8', 'tip': '#f0c8e8'},
            {'naam': 'Luna (Sailor Moon)', 'main': ('#2c2834', {'l': 1.3}), 'cream': '#f0c830', 'tip': '#f0c830'},
        ],
    },

    # --- Hoenn-dex, groep 6 ---
    'sableye': {
        # eye2 = rechteroog (eigen indexen via sprite_fixes.py); rim = oogrand (beide ogen)
        'species': {'sableye': {'body': [1, 2, 5], 'eyes': [7, 8], 'rim': [9, 11], 'eye2': [6, 15], 'gem': [12, 13, 14]}},
        'variants': [
            {'naam': 'Gold, Silver en Crystal', 'body': ('#34343c', {'l': 1.3}), 'eyes': '#f0c030', 'eye2': '#d0d4e0',
             'rim': '#202024', 'gem': '#b8f0f8'},
            {'naam': 'Obsidiaan', 'body': ('#2c2830', {'l': 1.3}), 'eyes': '#e02838', 'eye2': '#e02838', 'rim': '#801820',
             'gem': '#30c060'},
            {'naam': 'Diamond, Pearl en Platinum', 'body': ('#2c3448', {'l': 1.3}), 'eyes': '#a8d8f8', 'eye2': '#f4c8d8',
             'rim': '#202430', 'gem': '#c4c8d0'},
            {'naam': 'Albino', 'body': ('#c8c4d4', ALBINO), 'eyes': '#e02838', 'eye2': '#e02838', 'rim': '#901828',
             'gem': '#f0a8b8'},
            {'naam': 'Ruby, Sapphire en Emerald', 'body': ('#3a2a20', {'l': 1.3}), 'eyes': '#e02030', 'eye2': '#2850e0',
             'rim': '#1c1418', 'gem': '#20c058'},
            {'naam': 'Gollum (my precious)', 'body': '#9ca08c', 'eyes': '#a8d0f0', 'eye2': '#a8d0f0', 'rim': '#4888a8',
             'gem': '#e0b030'},
        ],
    },
    'mawile': {
        'species': {'mawile': {'jaw': [2, 3, 4, 5], 'body': [6, 7, 8, 9], 'mouth': [12]}},
        'variants': [
            {'naam': 'Koper', 'jaw': '#a86838'},
            {'naam': 'Blauw staal', 'jaw': '#4870b0'},
            {'naam': 'Venusvliegenval', 'jaw': '#58a040', 'mouth': '#d02838', 'body': '#c8e090'},
            {'naam': 'Albino', 'jaw': ('#c8c4c4', ALBINO), 'body': ('#ece4d8', ALBINO), 'mouth': '#e88898'},
            {'naam': 'Sadako (The Ring)', 'jaw': ('#1c1c20', {'l': 1.3}), 'body': '#d8dce4'},
            {'naam': 'Harley Quinn', 'jaw': '#c02030', 'body': '#2c2c34', 'mouth': '#2858c0'},
        ],
    },
    'aron': {
        'species': {
            'aron': {'armor': [1, 2, 3, 5], 'body': [4, 10, 11], 'eyes': [8, 9]},
            'lairon': {'armor': [1, 2, 3, 4, 7], 'body': [6, 8, 9, 10, 11], 'eyes': [12]},
            'aggron': {'armor': [1, 2, 4, 5, 6], 'body': [7, 9, 10, 11], 'eyes': [8]},
        },
        'variants': [
            {'naam': 'Brons', 'armor': '#c08848', 'aggron:armor': '#a8743c'},
            {'naam': 'Goud', 'armor': '#f0c848', 'aggron:armor': '#d8a828'},
            {'naam': 'Geanodiseerd titanium', 'armor': '#90a8e0', 'aggron:armor': '#5878c8', 'eyes': '#f0c030'},
            {'naam': 'Gunmetal', 'armor': '#787c88', 'aggron:armor': '#4c5058', 'eyes': '#e02838'},
            {'naam': 'Roségoud', 'armor': '#e8b8a8', 'aggron:armor': '#d0988c'},
            {'naam': 'Gundam', 'armor': '#dcdfe8', 'aggron:armor': '#c8ccd8', 'body': '#2850b0', 'eyes': '#f0c030'},
        ],
    },
    'meditite': {
        'species': {
            'meditite': {'skin': [1, 3, 4, 6], 'clothes': [7, 8, 9, 10, 11], 'red': [12, 13, 14]},
            'medicham': {'clothes': [1, 3, 4, 5, 13], 'skin': [6, 7, 8, 9, 10], 'gold': [11, 12, 15]},
        },
        'variants': [
            {'naam': 'Z-fighter (Dragon Ball)', 'clothes': '#f07818', 'gold': '#2850c0', 'red': '#2850c0'},
            {'naam': 'Zen (jadegroen)', 'clothes': '#48a070', 'gold': '#e8e0c8'},
            {'naam': 'Krishna (blauwe huid)', 'skin': '#5878d0', 'clothes': '#f0c030', 'gold': '#e8d8a0'},
            {'naam': 'Albino', 'skin': ('#e0dcdc', ALBINO), 'clothes': ('#e8c8d0', ALBINO), 'red': '#e02838'},
            {'naam': 'Akuma (Street Fighter)', 'clothes': ('#2c2c34', {'l': 1.3}), 'gold': '#c02020', 'red': '#c02020'},
            {'naam': 'Verlicht (goud, monnikspij)', 'skin': '#e0b030', 'clothes': '#a02028', 'gold': '#f0c830'},
        ],
    },
    'electrike': {
        'species': {
            'electrike': {'body': [4, 5, 6, 7, 9], 'yellow': [1, 2, 8]},
            'manectric': {'body': [6, 7, 8, 9, 13], 'yellow': [2, 3, 4, 5]},
        },
        'variants': [
            {'naam': 'Teslaspoel (koper)', 'body': '#b86838', 'yellow': '#40a0f0'},
            {'naam': 'Zekrom-kleuren', 'body': ('#2c2c34', {'l': 1.3}), 'yellow': '#40a8f0'},
            {'naam': 'Plasma', 'body': '#7040c0', 'yellow': '#40d8f0'},
            {'naam': 'Albino', 'body': ('#d0d0c8', ALBINO), 'yellow': ('#ece8d0', ALBINO)},
            {'naam': 'Raikou-kleuren', 'body': '#e8c030', 'yellow': '#6040a0'},
            {'naam': 'Thor', 'body': '#c02830', 'yellow': '#c4c8d4'},
        ],
    },
    'plusle': {
        # Plusle en Minun als één groep: ze ruilen en delen thema's
        'species': {
            'plusle': {'accent': [1, 2, 3], 'cream': [5, 6, 7, 8], 'cheeks': [11, 12]},
            'minun': {'accent': [1, 2, 4], 'cream': [5, 6, 7, 9], 'cheeks': [11, 12]},
        },
        'variants': [
            {'naam': 'Omgewisseld', 'plusle:accent': '#5880e8', 'minun:accent': '#d84840'},
            {'naam': 'Pastel', 'plusle:accent': '#f090b8', 'minun:accent': '#78d4b4'},
            {'naam': 'Batterij (plus koper, min zwart)', 'plusle:accent': '#d08838', 'plusle:cream': ('#34343c', {'l': 1.3}),
             'minun:accent': ('#2c2c30', {'l': 1.3}), 'minun:cream': '#d8a060'},
            {'naam': 'Yin en yang', 'plusle:accent': ('#2c2c30', {'l': 1.3}), 'plusle:cream': '#ece8e0',
             'minun:accent': '#ece8e0', 'minun:cream': ('#34343c', {'l': 1.3})},
            {'naam': 'Halloween', 'plusle:accent': '#f08020', 'minun:accent': '#7838a8'},
            {'naam': 'Ladybug en Cat Noir', 'plusle:cream': ('#2c2c30', {'l': 1.3}), 'minun:accent': ('#2c2c30', {'l': 1.3}),
             'minun:cream': '#f0d060', 'minun:cheeks': '#40c040'},
        ],
    },

    # --- Hoenn-dex, groep 7 ---
    'volbeat': {
        # paar: binnen één variant contrasteren
        'species': {
            'volbeat': {'main': [8, 9, 13, 15], 'yellow': [5, 6, 7], 'face': [10, 11, 12], 'dark': [1, 4]},
            'illumise': {'main': [5, 6, 8], 'yellow': [1, 2, 3], 'face': [9, 10, 11], 'dark': [14, 15]},
        },
        'variants': [
            {'naam': 'Omgewisseld', 'volbeat:main': '#9850b8', 'illumise:main': '#d84050'},
            {'naam': 'Vuur en ijs', 'volbeat:main': '#f06018', 'volbeat:face': '#f0b040', 'volbeat:dark': '#802018',
             'illumise:main': '#58b0e8', 'illumise:face': '#e4f0f8', 'illumise:dark': '#283c70', 'illumise:yellow': '#c8e8f8'},
            {'naam': 'Lieveheersbeestje en goudscarabee', 'volbeat:main': '#e02020', 'volbeat:face': ('#2c2c30', {'l': 1.3}),
             'volbeat:dark': ('#202024', {'l': 1.3}), 'volbeat:yellow': '#f0f0e8', 'illumise:main': '#30a868',
             'illumise:face': '#e0b030', 'illumise:dark': '#6c4c1c'},
            {'naam': 'Albino en melanisme', 'volbeat:main': ('#d8ccd0', ALBINO), 'volbeat:face': '#e8dce0',
             'volbeat:dark': '#a8a0a4', 'illumise:main': ('#2c2c34', {'l': 1.3}), 'illumise:face': '#4c4c58'},
            {'naam': 'Mario en Luigi', 'volbeat:dark': '#2848c0', 'volbeat:face': '#f0d0a8', 'illumise:main': '#30a040',
             'illumise:dark': '#2848c0', 'illumise:face': '#f0d0a8'},
            {'naam': 'Daft Punk', 'volbeat:main': '#e0b030', 'illumise:main': '#c0c4cc', 'dark': '#202024',
             'face': '#303038'},
        ],
    },
    'roselia': {
        'species': {'roselia': {'body': [1, 2, 3, 4, 6, 7], 'rose1': [8, 9, 10], 'rose2': [12, 13, 15],
                                'thorns': [11, 14]}},
        'variants': [
            {'naam': 'Witte en gele roos', 'rose1': '#e4e0e0', 'rose2': '#f0d030'},
            {'naam': 'Hollandse tulpen', 'rose2': '#f08020'},
            {'naam': 'Cactusbloei', 'body': '#6c9a6c', 'rose1': '#e030a0', 'rose2': '#f0d030'},
            {'naam': 'Albino', 'body': ('#ccd4c8', ALBINO), 'rose1': '#f0c0cc', 'rose2': '#c8d4f0'},
            {'naam': 'Betoverde roos', 'body': ('#2c3c34', {'l': 1.3}), 'rose1': '#f03050', 'rose2': '#e0b030'},
            {'naam': 'Gifbloem', 'body': '#7040a0', 'rose1': '#60e040', 'rose2': ('#2c2c30', {'l': 1.3})},
        ],
    },
    'gulpin': {
        'species': {
            'gulpin': {'body': [6, 7, 8, 9, 10], 'yellow': [1, 2, 4, 5]},
            'swalot': {'body': [1, 2, 3, 4, 14], 'yellow': [8, 9, 10], 'red': [7, 15], 'grey': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Omgewisseld', 'gulpin:body': '#a880e8', 'swalot:body': '#a0d890'},
            {'naam': 'Karamelpudding', 'body': '#d89848', 'yellow': '#6c3c1c'},
            {'naam': 'Kirby', 'body': '#f090b8', 'yellow': '#e02838', 'grey': '#e02838'},
            {'naam': 'Albino', 'body': ('#dcd8d0', ALBINO), 'yellow': '#f0e0c0', 'red': '#e02838'},
            {'naam': 'Pac-Man', 'body': '#f0d020', 'yellow': '#e02020', 'grey': '#2848c0'},
            {'naam': 'Biohazard', 'body': ('#2c2c30', {'l': 1.3}), 'yellow': '#60e040', 'grey': '#f0d020',
             'red': '#60e040'},
        ],
    },
    'carvanha': {
        'species': {
            'carvanha': {'blue': [9, 10, 11], 'red': [7, 8, 12, 13, 15], 'yellow': [1, 4, 5, 6]},
            'sharpedo': {'blue': [1, 2, 3, 4], 'yellow': [6, 7], 'belly': [11, 12], 'red': [9, 10, 13]},
        },
        'variants': [
            {'naam': 'Witte haai', 'blue': '#7c8490', 'yellow': '#d8dce0'},
            {'naam': 'Vuurvis', 'blue': '#c02830', 'red': '#f0b020', 'yellow': '#f0b020'},
            {'naam': 'Zwarte piranha', 'blue': ('#2c2c34', {'l': 1.3}), 'yellow': '#c0c4cc'},
            {'naam': 'Albino', 'blue': ('#d8d0d4', ALBINO), 'red': '#f0a0b0', 'yellow': ('#ece4d8', ALBINO)},
            {'naam': 'Megalodon (fossiel)', 'blue': '#c8b898', 'yellow': '#6c5034', 'red': '#8c6c50'},
            {'naam': 'Gulf-racekleuren', 'blue': '#78b8e0', 'yellow': '#f07818', 'red': '#f07818'},
        ],
    },
    'wailmer': {
        'species': {
            'wailmer': {'blue': [1, 2, 3, 4, 5], 'belly': [8, 9, 11, 13, 14]},
            'wailord': {'blue': [1, 2, 4, 7, 9], 'belly': [5, 6, 8, 11]},
        },
        'variants': [
            {'naam': 'Tropisch turkoois', 'blue': '#30a8a0'},
            {'naam': 'Orka', 'blue': ('#202024', {'l': 1.3}), 'belly': '#f0f0f0'},
            {'naam': 'Migaloo (witte bultrug)', 'blue': '#c8ccd8'},
            {'naam': 'Roze rivierdolfijn', 'blue': '#e8a0b0', 'belly': '#f8e0e4'},
            {'naam': 'Zeppelin', 'blue': '#b8bcc4', 'belly': '#c02828'},
            {'naam': 'Tennisbal', 'blue': '#c8e030', 'belly': '#eef2d8'},
        ],
    },
    'numel': {
        'species': {
            'numel': {'body': [2, 3, 4, 5, 9, 10], 'hump': [6, 7, 8, 13]},
            'camerupt': {'body': [6, 7, 8, 11], 'hump': [1, 2, 3], 'rings': [9, 10]},
        },
        'variants': [
            {'naam': 'Dromedaris', 'body': '#a87848', 'hump': '#7c5434', 'rings': '#e8c070'},
            {'naam': 'Basalt en lava', 'body': ('#3c3c44', {'l': 1.3}), 'hump': '#28282c', 'rings': '#f07020',
             'numel:hump': '#f07020'},
            {'naam': 'Kawah Ijen (blauw vuur)', 'body': '#6c7078', 'hump': '#e8d040', 'rings': '#3890f0'},
            {'naam': 'Albino', 'body': ('#e0d8d0', ALBINO), 'hump': '#d8d0c8', 'rings': '#e898a8'},
            {'naam': 'IJsvulkaan', 'body': '#a8c8e0', 'hump': '#eef4fa', 'rings': '#3870c8'},
            {'naam': 'Lavalamp', 'body': '#8040b0', 'hump': '#f08030', 'rings': '#c8f040'},
        ],
    },

    # --- Hoenn-dex, groep 8 ---
    'torkoal': {
        'species': {'torkoal': {'smoke': [1, 2, 3], 'shell': [4, 10, 12], 'body': [5, 6, 7, 8, 9]}},
        'variants': [
            {'naam': 'Steenkool met aswolk', 'shell': ('#2c2c30', {'l': 1.3}), 'smoke': '#6c6c74'},
            {'naam': 'Delfts blauw', 'shell': '#d8e0f0', 'body': '#3858b0'},
            {'naam': 'Gifgas', 'smoke': '#a070d0', 'shell': '#3c5c34', 'body': '#88b048'},
            {'naam': 'Albino', 'shell': '#d8d0d0', 'body': ('#f0d0c8', ALBINO)},
            {'naam': 'Zwavelwolk', 'smoke': '#e8e060', 'shell': '#7c6c30', 'body': '#c8a030'},
            {'naam': 'Lavafontein', 'smoke': '#e85830', 'shell': ('#202024', {'l': 1.3}), 'body': '#f0a020'},
        ],
    },
    'spoink': {
        'species': {
            'spoink': {'dark': [7, 8, 9, 10], 'pearl': [1, 2, 3, 5]},
            'grumpig': {'fur': [6, 8, 9, 10], 'dark': [1, 2, 3, 5], 'pearl': [7, 11, 13, 15]},
        },
        'variants': [
            {'naam': 'Boerderijvarken', 'dark': '#e8a0b0', 'fur': '#f0b8c4'},
            {'naam': 'Wild zwijn', 'dark': '#6c4c34', 'fur': '#9c7458', 'pearl': '#f0e8d8'},
            {'naam': 'Parelmoer', 'pearl': '#b8f0f0', 'fur': '#b8a0e0'},
            {'naam': 'Albino', 'dark': ('#c8c4c8', ALBINO), 'fur': ('#d4c4cc', ALBINO), 'pearl': '#e02838'},
            {'naam': 'Miss Piggy', 'fur': '#f0a0b8', 'dark': '#9070c0', 'pearl': '#f0f0f0'},
            {'naam': 'Ganon (Zelda)', 'dark': '#3c4c88', 'fur': '#4c5c98', 'grumpig:dark': ('#202028', {'l': 1.3}),
             'pearl': '#d02020'},
        ],
    },
    'spinda': {
        # vlekken worden in de game getekend met index 5-7
        'species': {'spinda': {'body': [1, 2, 3], 'spots': [5, 6, 7], 'ears': [4, 13, 14]}},  # ears = ook de spiraalogen: donker houden
        'variants': [
            {'naam': 'Reuzenpanda', 'body': '#dcdce0', 'spots': ('#2c2c30', {'l': 1.3}), 'ears': '#2c2c30'},
            {'naam': 'Rode panda', 'body': '#c06030', 'spots': '#f0e0c8', 'ears': '#4c2818'},
            {'naam': 'Giraf', 'body': '#e8c860', 'spots': '#7c4c20'},
            {'naam': 'Aardbei', 'body': '#f0b0c0', 'spots': '#d02838', 'ears': '#6c1c28'},
            {'naam': 'Psychedelisch', 'body': '#f0e890', 'spots': '#d030a0', 'ears': '#3080d0'},
            {'naam': 'Lavendel met goud', 'body': '#b8a0d8', 'spots': '#e8b828', 'ears': '#3c2850'},
        ],
    },
    'trapinch': {
        # per evolutie een eigen verloop (zoals normaal en shiny); 'red' = Flygons lenzen en vleugelranden
        'species': {
            'trapinch': {'body': [1, 2, 3, 4]},
            'vibrava': {'body': [7, 8, 11, 12], 'wings': [5, 6, 13]},
            'flygon': {'body': [10, 12, 14, 15], 'wings': [1, 2, 3, 5], 'red': [6, 7, 9, 11]},
        },
        'variants': [
            {'naam': 'Woestijn naar oase', 'trapinch:body': '#e0c070', 'vibrava:body': '#e8d090',
             'vibrava:wings': '#30a8a0', 'flygon:body': '#40b0a8', 'flygon:wings': '#e0c070', 'red': '#40d0f0'},
            {'naam': 'Garchomp-kleuren', 'trapinch:body': '#4c5c98', 'vibrava:body': '#4c5c98', 'vibrava:wings': '#c83030',
             'flygon:body': '#4c5c98', 'flygon:wings': '#c83030', 'red': '#f0c030'},
            {'naam': 'Libel (nimf naar glans)', 'trapinch:body': '#7c7448', 'vibrava:body': '#a8a070',
             'vibrava:wings': '#50c8e8', 'flygon:body': '#30a8b0', 'flygon:wings': '#80d8f0', 'red': '#60e060'},
            {'naam': 'Albino', 'body': ('#e0d8d0', ALBINO), 'wings': ('#d4dcd4', ALBINO), 'red': '#e02838'},
            {'naam': 'Vuur (gloed naar vlam)', 'trapinch:body': '#f0c030', 'vibrava:body': '#f0d040',
             'vibrava:wings': '#f08020', 'flygon:body': '#d83820', 'flygon:wings': '#f0a020', 'red': '#f8f0a0'},
            {'naam': 'Ghidorah (brons naar goud)', 'trapinch:body': '#a87038', 'vibrava:body': '#c89040',
             'vibrava:wings': '#e0b030', 'flygon:body': '#e0b030', 'flygon:wings': '#c88820', 'red': '#d02020'},
        ],
    },
    'cacnea': {
        'species': {
            'cacnea': {'body': [5, 6, 7, 8, 9, 10, 11, 12], 'flower': [3, 4]},
            'cacturne': {'body': [3, 4, 5, 6, 8, 9, 13, 14], 'dark': [1, 7], 'eyes': [12]},
        },
        'variants': [
            {'naam': 'Opuntia', 'body': '#5c9c9c', 'flower': '#f070a8', 'eyes': '#f070a8'},
            {'naam': 'Rode maancactus', 'body': '#d03040', 'flower': '#f0e030', 'dark': '#6c1420'},
            {'naam': 'Pompoenvogelverschrikker', 'body': '#e07828', 'dark': '#2c2028', 'flower': '#58a038', 'eyes': '#f0e030'},
            {'naam': 'Albino', 'body': ('#dcdcd0', ALBINO), 'flower': '#f0c0c8', 'eyes': '#e02838'},
            {'naam': 'Woestijnnacht', 'body': '#6848a0', 'dark': '#28203c', 'flower': '#f0f0f8', 'eyes': '#f0f0a0'},
            {'naam': 'Snoepcactus', 'body': '#80e0c0', 'flower': '#f080c0', 'dark': '#3c8c80', 'eyes': '#f080c0'},
        ],
    },
    'swablu': {
        'species': {
            'swablu': {'blue': [1, 2, 3, 4], 'cotton': [6, 7, 8, 9, 10, 11]},
            'altaria': {'blue': [1, 3, 4, 5, 6], 'cotton': [7, 8, 9, 10, 11]},
        },
        'variants': [
            {'naam': 'Suikerspin', 'cotton': '#f0b8d0'},
            {'naam': 'Onweerswolk', 'cotton': '#787c88', 'blue': '#f0d020'},
            {'naam': 'Zonsondergang', 'cotton': '#f8c8a0', 'blue': '#7848b0'},
            {'naam': 'Pauw', 'blue': '#209890', 'cotton': '#c8d878'},
            {'naam': 'Kinto-un (Dragon Ball)', 'cotton': '#f0d040', 'blue': '#e07020'},
            {'naam': 'Poollicht', 'cotton': '#70e0b0', 'blue': '#c030a0'},
        ],
    },
}
