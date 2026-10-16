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
        'species': {'budew': {'body': [4, 1, 5, 2, 12], 'rose1': [6, 8, 7]},
                    'roselia': {'body': [1, 2, 3, 4, 6, 7], 'rose1': [8, 9, 10], 'rose2': [12, 13, 15],
                                'thorns': [11, 14]},
                    'roserade': {'body': [4, 5, 7, 12], 'rose1': [10, 9, 11], 'rose2': [13, 15, 14]}},
        'variants': [
            {'naam': 'Witte en gele roos', 'rose1': '#e4e0e0', 'rose2': '#f0d030'},
            {'naam': 'Hollandse tulpen', 'rose2': '#f08020', 'budew:rose1': '#f08020'},
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

    # --- Hoenn-dex, groep 9 ---
    'zangoose': {
        # rivalen als contrasterend paar; randtinten (1/8, 4; 7, 15) horen bij hun groep (anders lelijke lijnen)
        'species': {
            'zangoose': {'fur': [1, 3, 5, 8, 11], 'red': [4, 6, 7, 10, 12]},
            'seviper': {'body': [2, 3, 6, 15], 'yellow': [1, 4, 5], 'purple': [7, 9, 12], 'blade': [10, 11, 13]},
        },
        'variants': [
            {'naam': 'Tijger en groene mamba', 'zangoose:fur': '#e88830', 'zangoose:red': ('#2c2420', {'l': 1.3}),
             'seviper:body': '#40a840', 'seviper:yellow': '#c8f060', 'seviper:purple': '#286830', 'seviper:blade': '#e8f080'},
            {'naam': 'Sneeuwluipaard en koraalslang', 'zangoose:fur': '#ccd0d8', 'zangoose:red': '#4c4c58',
             'seviper:body': ('#202024', {'l': 1.3}), 'seviper:yellow': '#f0d020', 'seviper:purple': '#d02828',
             'seviper:blade': '#d02828'},
            {'naam': 'IJs en vuur', 'zangoose:fur': '#b8d8f0', 'zangoose:red': '#30a0d0', 'seviper:body': '#a02818',
             'seviper:yellow': '#f0a020', 'seviper:purple': '#f06020'},
            {'naam': 'Zwarte panter en albinopython', 'zangoose:fur': ('#2c2c34', {'l': 1.3}), 'zangoose:red': '#e0b030',
             'seviper:body': '#ece4d0', 'seviper:yellow': '#f0d040', 'seviper:purple': '#e8d890', 'seviper:blade': '#f0a0b0'},
            {'naam': 'Siamese kat en Quetzalcoatl', 'zangoose:fur': '#e8dcc8', 'zangoose:red': '#4c3828',
             'seviper:body': '#2898b0', 'seviper:yellow': '#e8c030', 'seviper:purple': '#d03030', 'seviper:blade': '#40c860'},
            {'naam': 'Bastet en Apophis', 'zangoose:fur': '#e0b030', 'zangoose:red': '#2848a8',
             'seviper:body': ('#2c2038', {'l': 1.3}), 'seviper:yellow': '#d02828', 'seviper:purple': '#d02828',
             'seviper:blade': '#e0b030'},
        ],
    },
    'lunatone': {
        'species': {
            'lunatone': {'body': [1, 2, 3, 4, 5], 'eye': [8, 9, 10]},
            'solrock': {'rays': [3, 4, 5, 6, 7], 'body': [8, 9, 10, 11, 12]},
        },
        'variants': [
            {'naam': 'Omgewisseld', 'lunatone:body': '#e86020', 'solrock:rays': '#c8b868', 'solrock:body': '#b0a050'},
            {'naam': 'Bloedmaan en zwarte zon', 'lunatone:body': '#b83028', 'eye': '#f0d020',
             'solrock:body': ('#2c2c30', {'l': 1.3}), 'solrock:rays': '#a02018'},
            {'naam': 'Zonsverduistering', 'lunatone:body': ('#34343c', {'l': 1.3}), 'eye': '#e0e4f0',
             'solrock:body': ('#202024', {'l': 1.3}), 'solrock:rays': '#e8eef8'},
            {'naam': 'Maansteen en zonnesteen', 'lunatone:body': '#c8d8f0', 'eye': '#6080d0', 'solrock:body': '#e8a090',
             'solrock:rays': '#f0c8a8'},
            {'naam': 'Majoras maan en Shine Sprite', 'lunatone:body': '#8c7c6c', 'eye': '#f07020',
             'solrock:rays': '#f8e040', 'solrock:body': '#f0c020'},
            {'naam': 'Neptunus en Venus', 'lunatone:body': '#3058c0', 'eye': '#80e0f0', 'solrock:body': '#f0e0a0',
             'solrock:rays': '#e0b030'},
        ],
    },
    'barboach': {
        'species': {
            'barboach': {'blue': [1, 2, 3, 5, 10], 'grey': [7, 8, 9, 11]},
            'whiscash': {'blue': [4, 5, 6, 7, 9, 10, 13], 'gold': [1, 2, 3]},
        },
        'variants': [
            {'naam': 'Europese meerval', 'blue': '#6c7c48', 'grey': '#7c6c50'},
            {'naam': 'Goudmeerval', 'blue': '#e0b040', 'gold': '#f0f0e8', 'grey': '#d8c890'},
            {'naam': 'Panda-corydoras', 'blue': '#d4d4dc', 'grey': ('#2c2c30', {'l': 1.3}), 'gold': '#2c2c30'},
            {'naam': 'Albino', 'blue': ('#e0d0d0', ALBINO), 'grey': ('#ece4e4', ALBINO), 'gold': '#f0c0c8'},
            {'naam': 'Namazu (aardbevingsmythe)', 'blue': '#283870', 'gold': '#c03020', 'grey': '#504838'},
            {'naam': 'Sidderaal', 'blue': '#f0d020', 'gold': '#40d0f0', 'grey': '#3c3c44'},
        ],
    },
    'corphish': {
        'species': {
            'corphish': {'red': [2, 3, 4, 5, 6], 'belly': [7, 8, 9, 11]},
            'crawdaunt': {'red': [6, 7, 8, 9], 'star': [1, 2, 5], 'claws': [10, 11, 14], 'mouth': [12, 13, 15]},
        },
        'variants': [
            {'naam': 'Blauwe kreeft', 'red': '#3060c0', 'star': '#f0f0e8'},
            {'naam': 'Gemarmerde rivierkreeft', 'red': '#7c6c38', 'star': '#c8b878'},
            {'naam': 'Paarse kreeft', 'red': '#7840a8', 'star': '#f0d020'},
            {'naam': 'Albino', 'red': ('#e8d0d0', ALBINO), 'belly': ('#f0ece4', ALBINO), 'star': '#f0d8d8'},
            {'naam': 'Glasgarnaal', 'red': '#a8d8e8', 'belly': '#e8f4f8', 'star': '#f0f0f8'},
            {'naam': 'Gele kreeft (1 op 30 miljoen)', 'red': '#f0c030', 'star': '#c02020'},
        ],
    },
    'baltoy': {
        'species': {
            'baltoy': {'body': [2, 3, 4, 5, 6], 'red': [7, 8, 9]},
            'claydol': {'body': [1, 2, 4, 5], 'white': [6, 7, 8], 'red': [9, 10, 11, 12], 'tan': [13, 14]},
        },
        'variants': [
            {'naam': 'Terracotta', 'body': '#c06838', 'red': '#3c3030'},
            {'naam': 'Jade', 'body': '#48a078', 'red': '#e0b030'},
            {'naam': 'Ming-porselein', 'body': '#d8e0f0', 'claydol:body': '#d0d8ec', 'red': '#2848a8', 'white': '#2848a8'},
            {'naam': 'Albino', 'body': ('#d8d4cc', ALBINO), 'red': '#e02838', 'white': '#ece8e4', 'tan': '#e8d8c8'},
            {'naam': 'Dogu (Jomon)', 'body': '#a04830', 'red': '#f0ece0', 'tan': '#f0ece0'},
            {'naam': 'Ufo', 'body': '#b8c0cc', 'red': '#58e058', 'white': '#3c4450'},
        ],
    },
    'lileep': {
        'species': {
            'lileep': {'tentacles': [1, 2, 3, 4], 'body': [5, 6, 12, 13], 'yellow': [9, 10, 11]},
            'cradily': {'tentacles': [1, 2, 3, 4, 6], 'body': [7, 8, 9, 10], 'yellow': [11, 12, 13, 14]},
        },
        'variants': [
            {'naam': 'Koraalrif', 'tentacles': '#f0c830', 'body': '#d84850', 'yellow': '#f0f0e0'},
            {'naam': 'Witte zeeanemoon', 'tentacles': '#e8e4e0'},
            {'naam': 'Versteend', 'tentacles': '#a8a090', 'body': '#7c6c50', 'yellow': '#d0c0a0'},
            {'naam': 'Albino', 'tentacles': '#f0d8e0', 'body': ('#dcd8d4', ALBINO), 'yellow': '#f0e8c8'},
            {'naam': 'Diepzeegloed', 'tentacles': '#60f0f0', 'body': ('#202850', {'l': 1.2}), 'yellow': '#60f0f0'},
            {'naam': 'Ammoniet (parelmoer)', 'tentacles': '#f0d0e0', 'body': '#a0d8d0', 'yellow': '#e8c050'},
        ],
    },
    'anorith': {
        'species': {
            'anorith': {'shell': [2, 3, 10, 11], 'green': [4, 5, 9, 12], 'red': [6, 7, 8]},
            'armaldo': {'shell': [1, 3, 4, 5, 9], 'red': [11, 12], 'gold': [13, 14]},
        },
        'variants': [
            {'naam': 'Versteend', 'shell': '#b0a080', 'green': '#7c6448', 'red': '#e08038'},
            {'naam': 'Degenkrab (blauw bloed)', 'shell': '#7c5c3c', 'green': '#5c4430', 'red': '#3060c0'},
            {'naam': 'Trilobiet (zwart en goud)', 'shell': ('#2c2c30', {'l': 1.3}), 'red': '#e0b030', 'green': '#4c4c54'},
            {'naam': 'Albino', 'shell': ('#dcd8d8', ALBINO), 'green': '#e0e0d8', 'red': '#e02838'},
            {'naam': 'Anomalocaris', 'shell': '#d06070', 'green': '#f0a0a8', 'red': '#f0d020'},
            {'naam': 'Samoeraiharnas', 'shell': '#b02020', 'green': '#801818', 'red': '#202024', 'gold': '#e8c030'},
        ],
    },

    # --- Hoenn-dex, groep 10 ---
    'feebas': {
        'species': {
            'feebas': {'body': [5, 6, 7, 8, 9, 10, 11], 'tail': [1, 2, 3], 'ribbon': [14, 15]},
            'milotic': {'body': [4, 5, 6, 10], 'ribbon': [1, 3, 9, 11, 13, 14], 'tail': [7, 8]},
        },
        'variants': [
            {'naam': 'Riemvis (zilver en rood)', 'body': '#b8c0cc', 'ribbon': '#e04028', 'tail': '#e04028'},
            {'naam': 'Pastel', 'body': '#c8b8e8', 'ribbon': '#80d8b8', 'tail': '#f090b8'},
            {'naam': 'Koninklijk', 'body': '#e0b030', 'ribbon': '#2848a8', 'tail': '#c02028'},
            {'naam': 'Albino', 'body': ('#e4dcd8', ALBINO), 'ribbon': '#f0b8c8', 'tail': '#d8e0e8'},
            {'naam': 'Nachtzwart', 'body': ('#2c2c34', {'l': 1.3}), 'ribbon': '#e0b030', 'tail': '#8040c0'},
            {'naam': 'Feniks', 'body': '#e04820', 'ribbon': '#f0d040', 'tail': '#f0a020'},
        ],
    },
    'castform': {
        # elke weervorm is een eigen vorm met een eigen shiny: per vorm eigen kleuren, één thema per variant
        'species': {
            'castform': {'body': [12, 2, 3, 4], 'face': [6, 7]},
            'castform/sunny': {'petals': [1, 9, 8], 'core': [10, 2, 3, 4], 'face': [6, 7], 'cloud': [11, 12]},
            'castform/rainy': {'hood': [1, 9, 8], 'body': [10, 2, 3, 4], 'face': [6, 7], 'cloud': [11, 12]},
            'castform/snowy': {'leaves': [1, 12, 9, 8, 11], 'body': [10, 2, 3], 'face': [6, 7]},
        },
        'variants': [
            {'naam': 'Zonsondergang', 'castform:body': '#f0a070',
             'castform/sunny:petals': '#e85880', 'castform/sunny:core': '#f0a030',
             'castform/rainy:hood': '#f09058', 'castform/rainy:body': '#b84870',
             'castform/snowy:leaves': '#f0b0a0', 'castform/snowy:body': '#c04870'},
            {'naam': 'Onweer', 'castform:body': '#606078', 'castform:face': '#f0e050',
             'castform/sunny:petals': '#606088', 'castform/sunny:core': '#f0d030', 'castform/sunny:cloud': '#707080',
             'castform/rainy:hood': '#40405c', 'castform/rainy:body': '#e0c020', 'castform/rainy:face': '#f8f0a0',
             'castform/snowy:leaves': '#686888', 'castform/snowy:body': '#e8c828', 'castform/snowy:face': '#f8f0a0'},
            {'naam': 'Noorderlicht', 'castform:body': '#68d0a8',
             'castform/sunny:petals': '#40c890', 'castform/sunny:core': '#8050c0',
             'castform/rainy:hood': '#50e0b0', 'castform/rainy:body': '#7040b0',
             'castform/snowy:leaves': '#8868e0', 'castform/snowy:body': '#40d8a0'},
            {'naam': 'Zure regen', 'castform:body': '#a8c040',
             'castform/sunny:petals': '#a0d030', 'castform/sunny:core': '#704898',
             'castform/rainy:hood': '#98c838', 'castform/rainy:body': '#6a3c8c',
             'castform/snowy:leaves': '#c0d860', 'castform/snowy:body': '#583878'},
            {'naam': 'Bloedmaan', 'castform:body': '#a02830',
             'castform/sunny:petals': '#a01820', 'castform/sunny:core': '#38141c',
             'castform/rainy:hood': '#a02030', 'castform/rainy:body': '#401420',
             'castform/snowy:leaves': '#c03040', 'castform/snowy:body': '#401420'},
            {'naam': 'Sterrennacht', 'castform:body': '#283878', 'castform:face': '#f0e8a0',
             'castform/sunny:petals': '#283878', 'castform/sunny:core': '#f0d040', 'castform/sunny:cloud': '#8890c0',
             'castform/rainy:hood': '#202850', 'castform/rainy:body': '#8090f0',
             'castform/snowy:leaves': '#384890', 'castform/snowy:body': '#d0d8f8'},
        ],
    },
    'kecleon': {
        # in deze rom Grass; een kameleon: kleur wisselen is zijn ding
        'species': {'kecleon': {'body': [2, 6, 7, 9, 10, 11], 'crest': [1, 4, 5, 8], 'stripe': [13, 14]}},
        'variants': [
            {'naam': 'Panterkameleon', 'body': '#30a8c0', 'crest': '#f08030', 'stripe': '#e02838'},
            {'naam': 'Opgewonden rood', 'body': '#d04030', 'crest': '#f0d030', 'stripe': '#3058c0'},
            {'naam': 'Schorscamouflage', 'body': '#7c5c3c', 'crest': '#c8a870', 'stripe': '#3c5c30'},
            {'naam': 'Albino', 'body': ('#dcd8cc', ALBINO), 'crest': '#f0e8c8', 'stripe': '#f0a0b8'},
            {'naam': 'Lisa Frank', 'body': '#9050c0', 'crest': '#f080c0', 'stripe': '#40e0f0'},
            {'naam': 'Bijna onzichtbaar (glas)', 'body': '#b8dce8', 'crest': '#e0f0f8', 'stripe': '#f0c8d8'},
        ],
    },
    'shuppet': {
        'species': {
            'shuppet': {'body': [1, 3, 4, 5, 6, 7], 'eyes': [8, 9, 10, 11], 'zipper': [12, 13]},
            'banette': {'body': [1, 2, 3, 4, 6], 'zipper': [11, 12, 13, 14, 15], 'eyes': [7, 8, 10]},
        },
        'variants': [
            {'naam': 'Billy (Saw)', 'body': ('#e4dcd0', ALBINO), 'zipper': '#c01818', 'eyes': '#c01818'},
            {'naam': 'Beetlejuice', 'body': '#6c8c48', 'zipper': '#58307a', 'eyes': '#e02020'},
            {'naam': 'Marionette (FNAF)', 'body': ('#28242c', {'l': 1.3}), 'zipper': '#f0f0f0', 'eyes': '#e8e8f0'},
            {'naam': 'Carrie (bloed)', 'body': '#801c24', 'zipper': '#e8e0c8', 'eyes': '#f0e040'},
            {'naam': 'Corpse Bride', 'body': '#b8d0e0', 'zipper': '#5a3a70', 'eyes': '#283048'},
            {'naam': 'Harlekijn', 'body': '#b82890', 'zipper': '#f0c030', 'eyes': '#40e0f0'},
        ],
    },
    'duskull': {
        'species': {
            'duskull': {'robe': [1, 2, 3, 4], 'skull': [6, 7, 8, 9, 10], 'eye': [11, 12, 13]},
            'dusclops': {'robe': [7, 8, 9, 10], 'skull': [1, 2, 3, 4, 5], 'eye': [13, 14]},
            'dusknoir': {'robe': [4, 6], 'skull': [8, 7], 'eye': [13]},
        },
        'variants': [
            {'naam': 'Dwaallicht (groen vuur)', 'robe': '#2c8a50', 'skull': '#d8f0c0', 'eye': '#c0f040',
             'dusknoir:robe': '#206840', 'dusknoir:skull': '#a8c890'},
            {'naam': 'Calavera (Día de Muertos)', 'robe': '#e05898', 'skull': '#f0e8d0', 'eye': '#f0a020',
             'dusknoir:robe': '#b83c78', 'dusknoir:skull': '#d8c8b0'},
            {'naam': 'Pompoenlantaarn', 'robe': '#e07020', 'skull': '#f0e0a0', 'eye': '#40d040',
             'dusknoir:robe': '#b85418', 'dusknoir:skull': '#d8c088'},
            {'naam': 'Farao (goud en lapis)', 'robe': '#d8a020', 'skull': '#4870d0', 'eye': '#e02020',
             'dusknoir:robe': '#2c3c88', 'dusknoir:skull': '#d8a838'},
            {'naam': 'Azteekse turkoois', 'robe': '#30b0a0', 'skull': '#e8d8b0', 'eye': '#e03020'},
            {'naam': 'Kristallen schedel', 'robe': '#9070d8', 'skull': '#b0e8f0', 'eye': '#f040b0'},
        ],
    },
    'tropius': {
        'species': {'tropius': {'leaves': [1, 3, 5], 'leafline': [2], 'body': [8, 9, 10], 'bodyline': [6], 'fruit': [11, 12]}},
        'variants': [
            {'naam': 'Herfst', 'leaves': '#d86020', 'leafline': '#782c10'},
            {'naam': 'Kersenboom', 'leaves': '#f0a0c0', 'leafline': '#a84870', 'fruit': '#d02028'},
            {'naam': 'Drakenvrucht', 'body': '#e05088', 'bodyline': '#782040', 'fruit': '#f0f0f0'},
            {'naam': 'Albino', 'leaves': ('#d4dccc', ALBINO), 'leafline': '#788470', 'body': ('#e0d8d0', ALBINO), 'bodyline': '#887870', 'fruit': '#f0e8c0'},
            {'naam': 'Ginkgo (goud)', 'leaves': '#e8c030', 'leafline': '#806010', 'fruit': '#f08030'},
            {'naam': 'Winter', 'leaves': '#dce4ec', 'leafline': '#68788c', 'body': '#4c3424', 'bodyline': '#281810', 'fruit': '#d02028'},
        ],
    },
    'chimecho': {
        # in deze rom Psychic/Steel
        'species': {'chingling': {'body': [11, 9, 8, 10], 'red': [1, 2, 3]},
                    'chimecho': {'body': [7, 8, 9, 11], 'red': [10, 12, 13], 'top': [1, 3, 5, 6, 14]}},
        'variants': [
            {'naam': 'Koperen windgong', 'body': '#c87838', 'red': '#30a0a0'},
            {'naam': 'Zilver', 'body': '#b8bcc8', 'red': '#3058c0'},
            {'naam': 'Amethist', 'body': '#9068c8', 'red': '#f0c040'},
            {'naam': 'Albino', 'body': ('#e0dcdc', ALBINO), 'red': '#f0a8b8'},
            {'naam': 'Kerstklok', 'body': '#e0b030', 'red': '#38a040', 'top': '#c02028'},
            {'naam': 'Fuurin (Japans glas)', 'body': '#283878', 'red': '#f05030', 'top': '#f0f0f8'},
        ],
    },
    'absol': {
        # in deze rom Dark/Fairy
        'species': {'absol': {'fur': [6, 7, 8, 9, 10], 'dark': [1, 2, 3, 4], 'eyes': [11, 12, 13]}},
        'variants': [
            {'naam': 'Bloedmaanwolf', 'fur': '#7a2030', 'dark': '#28242c', 'eyes': '#f0d040'},
            {'naam': 'Lucario', 'fur': '#4a7cc8', 'dark': '#28283a', 'eyes': '#e02828'},
            {'naam': 'Pest (apocalyptische ruiter)', 'fur': '#9cac70', 'dark': '#4a3858', 'eyes': '#e0e040'},
            {'naam': 'Sylveon', 'fur': '#f0b0d0', 'dark': '#4890d0', 'eyes': '#4890d0'},
            {'naam': 'Anubis', 'fur': ('#262230', {'l': 1.3}), 'dark': '#e0b030', 'eyes': '#30c0b0'},
            {'naam': 'Raikou', 'fur': '#f0c830', 'dark': '#4a3070', 'eyes': '#e02828'},
        ],
    },
    'wynaut': {
        'species': {
            'wynaut': {'body': [1, 2, 3, 4, 6], 'mouth': [7, 8, 9]},
            'wobbuffet': {'body': [1, 2, 3, 4, 5], 'mouth': [7, 8, 9], 'tail': [10, 11, 12, 13]},
        },
        'variants': [
            {'naam': 'Oranje', 'body': '#f09038', 'mouth': '#a03828'},
            {'naam': 'Groen', 'body': '#58b048'},
            {'naam': 'Paars', 'body': '#8058c0', 'mouth': '#f0c030'},
            {'naam': 'Albino', 'body': ('#dcd8dc', ALBINO), 'mouth': '#e88898'},
            {'naam': 'SpongeBob', 'body': '#f0d830', 'mouth': '#c03838', 'tail': '#a06830'},
            {'naam': 'Bokszak', 'body': '#c02028', 'mouth': '#f0e8d8', 'tail': '#2c2c30'},
        ],
    },
    # --- Hoenn-dex, groep 11 ---
    'snorunt': {
        'species': {
            'snorunt': {'hood': [2, 1, 4, 3], 'stripe': [9, 6], 'eyes': [11, 12]},
            'glalie': {'shell': [9, 5, 8, 7, 6], 'eyes': [10, 11, 12]},
            'froslass': {'robe': [4, 7, 6], 'blue': [5, 1, 2], 'purple': [9, 8], 'eyes': [11, 12], 'obi': [13, 14, 15]},
        },
        'variants': [
            {'naam': 'Rode oni (Hannya)', 'hood': '#c02828', 'stripe': '#f0e0c0', 'shell': '#c83838', 'glalie:eyes': '#f0c020',
             'blue': '#c02838', 'purple': '#2c2830', 'obi': '#e0b030'},
            {'naam': 'Noorderlicht', 'hood': '#40c890', 'stripe': '#a060e0', 'shell': '#80e0c0', 'glalie:eyes': '#f040b0',
             'blue': '#40c890', 'purple': '#8048c0', 'obi': '#f070c0'},
            {'naam': 'Matcha', 'hood': '#68a040', 'stripe': '#f0f0d8', 'shell': '#b8d898',
             'blue': '#68a040', 'purple': '#3c5028', 'obi': '#c03838'},
            {'naam': 'Albino', 'hood': ('#e8e0dc', ALBINO), 'stripe': '#f0c8c8', 'eyes': '#e02838',
             'shell': ('#ece8e8', ALBINO),
             'blue': ('#e4dcdc', ALBINO), 'purple': '#d8b8c8', 'obi': '#e88898'},
            {'naam': 'Yuki-onna (sakura)', 'hood': '#f0a0c0', 'stripe': '#e04878', 'shell': '#f4c8d8', 'glalie:eyes': '#e04878',
             'blue': '#f0a0c0', 'purple': '#a03058', 'obi': '#f8f0f8'},
            {'naam': 'Lich King', 'hood': '#2c3a60', 'stripe': '#7ae0f8', 'snorunt:eyes': '#60f0ff', 'shell': '#506088', 'glalie:eyes': '#60f0ff',
             'robe': '#8898b8', 'blue': '#20283c', 'purple': '#40d0f0', 'obi': '#a0b0c8'},
        ],
    },
    'spheal': {
        'species': {
            'spheal': {'body': [1, 4, 2, 3, 5], 'belly': [8, 11, 10, 9]},
            'sealeo': {'body': [3, 2, 1, 4, 5], 'belly': [8, 13, 12, 14]},
            'walrein': {'body': [1, 4, 10, 7], 'mane': [3, 6], 'tusks': [8, 11, 12]},
        },
        'variants': [
            {'naam': 'Grijze zeehond', 'body': '#8a8c94', 'belly': '#d8d0c0', 'mane': '#d8d8dc'},
            {'naam': 'Zeeleeuw', 'body': '#6a4a30', 'belly': '#c8a070', 'mane': '#a07848'},
            {'naam': 'Zeehondenpup', 'body': ('#e4e8ec', ALBINO), 'belly': '#f4f0ec', 'mane': '#f4f4f4'},
            {'naam': 'Pokéball', 'body': '#d83030', 'belly': '#f4f4f4', 'mane': '#f4f4f4'},
            {'naam': 'Gouden medaille', 'body': '#e0b030', 'belly': '#f4e8c0', 'mane': '#f4e8c0'},
            {'naam': 'Orka', 'body': ('#24242c', {'l': 1.3}), 'belly': '#f4f4f4', 'mane': '#f4f4f4'},
        ],
    },
    'clamperl': {
        'species': {
            'clamperl': {'shell': [2, 1, 3], 'inner': [8, 10, 14, 13], 'pearl': [9, 11, 12]},
            'huntail': {'body': [1, 4, 2, 10], 'fins': [5, 6, 7], 'mouth': [12, 13, 14]},
            'gorebyss': {'body': [1, 7, 5, 4, 12], 'purple': [8, 11, 10, 9]},
        },
        'variants': [
            {'naam': 'Parelmoer', 'shell': '#c8c0e0', 'pearl': '#f4f0f8', 'huntail:body': '#b8b0d0', 'fins': '#80a0d0',
             'gorebyss:body': '#e8e0f0', 'purple': '#a090c8'},
            {'naam': 'Mandarijnvis', 'shell': '#f08020', 'pearl': '#2858c8', 'huntail:body': '#f08020', 'fins': '#2858c8',
             'gorebyss:body': '#2858c8', 'purple': '#f08020'},
            {'naam': 'Diepzeegloed', 'shell': '#1c2440', 'pearl': '#40e8d8', 'inner': '#304878', 'huntail:body': '#1c2440', 'fins': '#40e8d8',
             'gorebyss:body': '#30285a', 'purple': '#40e8d8'},
            {'naam': 'Albino', 'shell': ('#e4dcdc', ALBINO), 'pearl': '#f8e0e8', 'huntail:body': ('#e8e0e0', ALBINO), 'fins': '#f0c8c0',
             'gorebyss:body': ('#f0e8e8', ALBINO), 'purple': '#e8c0c8'},
            {'naam': 'Zwarte parel (Tahiti)', 'shell': ('#303038', {'l': 1.3}), 'pearl': '#405860', 'huntail:body': '#2c3038', 'fins': '#60a088',
             'gorebyss:body': '#383040', 'purple': '#60a088'},
            {'naam': 'Ariel', 'shell': '#38a888', 'pearl': '#8048b0', 'huntail:body': '#8048b0', 'fins': '#38a888',
             'gorebyss:body': '#38a888', 'purple': '#8048b0'},
        ],
    },
    'relicanth': {
        'species': {'relicanth': {'light': [1, 11, 3, 2, 12], 'dark': [10, 6, 13, 9, 7]}},
        'variants': [
            {'naam': 'Echte coelacant (blauw met witte vlekken)', 'light': '#3c5c98', 'dark': '#d8e0e8'},
            {'naam': 'Lavasteen', 'light': '#5a5a60', 'dark': '#e06020'},
            {'naam': 'Nautilus (Jules Verne, messing en klinknagels)', 'light': '#b87838', 'dark': '#3c4448'},
            {'naam': 'Albino', 'light': ('#ece4dc', ALBINO), 'dark': ('#d0c8c4', ALBINO)},
            {'naam': 'Jade met goud', 'light': '#4a9a70', 'dark': '#e0c060'},
            {'naam': 'Azteeks relikwie', 'light': '#e8c040', 'dark': '#2c7c90'},
        ],
    },
    'luvdisc': {
        'species': {'luvdisc': {'body': [2, 1, 7, 6, 5, 3], 'blush': [11, 12], 'eyes': [8, 10]}},
        'variants': [
            {'naam': 'Rood hart', 'body': '#e03040'},
            {'naam': 'Chocoladehart', 'body': '#7a4a30', 'blush': '#f0a0b0'},
            {'naam': 'Lavendel', 'body': '#b090e0'},
            {'naam': 'Albino', 'body': ('#f0e8e8', ALBINO), 'eyes': '#e02838'},
            {'naam': 'Gebroken hart', 'body': '#4a4a58', 'blush': '#8080a0'},
            {'naam': 'Tiffany (turkoois)', 'body': '#40c0b0', 'blush': '#f0f0f0'},
        ],
    },
    'bagon': {
        'species': {
            'bagon': {'shell': [2, 1, 6, 4, 3], 'body': [7, 10, 11], 'belly': [12, 9, 8]},
            'shelgon': {'shell': [1, 5, 4, 3, 14], 'body': [7, 6, 10]},
            'salamence': {'wings': [1, 4, 3, 2], 'body': [6, 7, 9, 8], 'belly': [14, 10, 15]},
        },
        'variants': [
            {'naam': 'Alduin (Skyrim)', 'shell': ('#2c2828', {'l': 1.3}), 'body': ('#2c2828', {'l': 1.3}), 'wings': '#3a3030', 'belly': '#8a3020'},
            {'naam': 'Bahamut (platina en goud)', 'shell': '#a8b0c0', 'body': '#a8b0c0', 'wings': '#e0b030', 'belly': '#f4f0e0'},
            {'naam': 'Y Ddraig Goch (Welsh)', 'shell': '#30a040', 'body': '#c02028', 'wings': '#30a040', 'belly': '#f4f4f4'},
            {'naam': 'Albino', 'shell': ('#d8d0d0', {'l': 1.3}), 'body': ('#e0d4d4', {'l': 1.3}), 'shelgon:body': '#a08888', 'wings': ('#e4c8c8', {'l': 1.3}), 'belly': '#f0b0a8'},
            {'naam': 'Tiamat (chromatisch)', 'shell': '#6038a0', 'body': '#6038a0', 'wings': '#30a0d0', 'belly': '#e0b030'},
            {'naam': 'Smaug (rood en goud)', 'shell': '#a02828', 'body': '#a02828', 'wings': '#702020', 'belly': '#e0b030'},
        ],
    },
    'beldum': {
        # metalen (Steel/Psychic)
        'species': {
            'beldum': {'body': [2, 4, 6, 1, 3], 'grey': [13, 12, 11], 'eye': [8, 10, 7]},
            'metang': {'body': [5, 10, 7, 9, 8], 'grey': [1, 6, 14, 2], 'eye': [12, 11, 13]},
            'metagross': {'body': [1, 6, 5, 4, 3], 'grey': [9, 8, 7, 10], 'eye': [13, 12]},
        },
        'variants': [
            {'naam': 'Koper', 'body': '#c07038', 'metang:body': '#a05020', 'grey': '#d8c0a0'},
            {'naam': 'Goud', 'body': '#d8a828', 'metang:body': '#b88818', 'grey': '#e0d8c0'},
            {'naam': 'Patina (verdigris)', 'body': '#4a9a80', 'grey': '#a87848'},
            {'naam': 'Gunmetal', 'body': ('#3a3c48', {'l': 1.3}), 'grey': '#909098', 'eye': '#40d0f0'},
            {'naam': 'Roségoud', 'body': '#e0a090', 'metang:body': '#c07868', 'grey': '#f4e0d8'},
            {'naam': 'Iron Man', 'body': '#b82828', 'grey': '#e0b030', 'eye': '#80e0f8'},
        ],
    },
    # --- Hoenn-dex, groep 12: legendaries ---
    'regirock': {
        'species': {'regirock': {'rock': [8, 10, 9, 12, 7], 'orange': [2, 5, 3, 4, 11]}},
        'variants': [
            {'naam': 'Basalt met lava', 'rock': '#4a4a50', 'orange': '#e06020'},
            {'naam': 'Regice-kleuren', 'rock': '#5890b8', 'orange': '#f0d020'},
            {'naam': 'Malachiet', 'rock': '#2c8a60', 'orange': '#e8e4d0'},
            {'naam': 'Petra (roze zandsteen)', 'rock': '#d89878', 'orange': '#8a3020'},
            {'naam': 'Amethistgeode', 'rock': '#6a5a7a', 'orange': '#c060f0'},
            {'naam': 'Regigigas', 'rock': '#b8b4ac', 'orange': '#3c9a50'},
        ],
    },
    'regice': {
        'species': {'regice': {'ice': [6, 2, 3, 1, 7, 5], 'dots': [11, 10, 9]}},
        'variants': [
            {'naam': 'Regirock-kleuren', 'ice': '#c87048', 'dots': '#f0d0b8'},
            {'naam': 'Rozenkwarts', 'ice': '#f0a8c0', 'dots': '#e04878'},
            {'naam': 'Citrien', 'ice': '#e0a830', 'dots': '#f8f0c0'},
            {'naam': 'Zwart ijs', 'ice': ('#303848', {'l': 1.3}), 'dots': '#40e0f0'},
            {'naam': 'Smaragd', 'ice': '#40b080', 'dots': '#f0f0e0'},
            {'naam': 'Regigigas', 'ice': '#e8e4dc', 'dots': '#3c9a50'},
        ],
    },
    'registeel': {
        'species': {'registeel': {'steel': [2, 1, 4, 9, 5], 'dark': [13, 12, 6], 'dots': [11, 10]}},
        'variants': [
            {'naam': 'Roest', 'steel': '#a85830', 'dark': '#5a3020'},
            {'naam': 'Brons', 'steel': '#c09048', 'dark': '#5a4028'},
            {'naam': 'Gegloeid blauw staal', 'steel': '#5870b0', 'dark': '#283050', 'dots': '#f0c040'},
            {'naam': 'Goud', 'steel': '#e0b030', 'dark': '#6a5018'},
            {'naam': 'Geanodiseerd titanium', 'steel': '#9068c8', 'dark': '#30a0a0', 'dots': '#f0e040'},
            {'naam': 'Regigigas', 'steel': '#e8e4dc', 'dark': '#3c9a50', 'dots': '#f0c040'},
        ],
    },
    'latias': {
        # tweeling met Latios: per variant contrasterend
        'species': {
            'latias': {'white': [1, 4, 2], 'red': [6, 8, 7, 10], 'triangle': [15, 14], 'eyes': [11, 13]},
            'latios': {'white': [2, 1, 4, 3, 5], 'blue': [8, 6, 11, 9, 10], 'triangle': [12, 14]},
        },
        'variants': [
            {'naam': 'Mew en Mewtwo', 'red': '#f090c0', 'blue': '#8050b0'},
            {'naam': 'Stealth', 'latias:white': '#38384a', 'red': '#c02838', 'latios:white': '#5c6070', 'blue': '#202838'},
            {'naam': 'Lente en nacht', 'red': '#70b838', 'latios:white': '#9890b8', 'blue': '#3a2858', 'triangle': '#f0e060'},
            {'naam': 'Albino', 'white': ('#ece8e8', ALBINO), 'red': '#f0b8c0', 'blue': '#e0c8d0', 'eyes': '#e02838', 'triangle': '#e02838'},
            {'naam': 'Aurora en amber', 'red': '#30c0a0', 'blue': '#e8a020', 'triangle': '#f0e060'},
            {'naam': 'Sterrenstelsel', 'white': '#283060', 'red': '#e070d0', 'blue': '#40e0f0', 'triangle': '#f0f0a0'},
        ],
    },
    'kyogre': {
        'species': {'kyogre': {'body': [5, 9, 6, 7, 12, 13], 'lines': [11, 10, 8], 'belly': [4, 14, 3]}},
        'variants': [
            {'naam': 'Abyssaal violet', 'body': '#302060', 'lines': '#40e0f0'},
            {'naam': 'Orka', 'body': ('#28282c', {'l': 1.3}), 'belly': '#f4f4f4'},
            {'naam': 'Tsunami (turkoois)', 'body': '#30a8a0', 'lines': '#f0d040'},
            {'naam': 'IJstijd', 'body': '#c0d8ec', 'lines': '#4080e0', 'belly': '#f4f8fc'},
            {'naam': 'Groudon-ruil', 'body': '#a82828', 'lines': '#2050c0', 'belly': '#8c8088'},
            {'naam': 'Leviathan (goud)', 'body': '#d8a828', 'lines': '#2050c0', 'belly': '#f4ecd0'},
        ],
    },
    'groudon': {
        'species': {'groudon': {'red': [2, 6, 7, 4, 5, 3], 'grey': [13, 9, 14, 15], 'claws': [12, 10]}},
        'variants': [
            {'naam': 'Woestijn', 'red': '#d8a860', 'grey': '#806040'},
            {'naam': 'Obsidiaan met lava', 'red': ('#2c2830', {'l': 1.3}), 'grey': '#e06020'},
            {'naam': 'Godzilla', 'red': '#4c6050', 'grey': '#2c3430', 'claws': '#a0e0f0'},
            {'naam': 'Maya-jade', 'red': '#3a9068', 'grey': '#c8b890'},
            {'naam': 'Kyogre-ruil', 'red': '#3060b0', 'grey': '#c8d0d8'},
            {'naam': 'Zonnegod (Inti)', 'red': '#e09820', 'grey': '#e8e0d0'},
        ],
    },
    'rayquaza': {
        'species': {'rayquaza': {'body': [2, 1, 5, 3], 'lines': [9, 8], 'red': [6, 7]}},
        'variants': [
            {'naam': 'Hemelsblauw', 'body': '#4890d0', 'lines': '#f0d040'},
            {'naam': 'Groudon-rood', 'body': '#b83030', 'lines': '#2c2c30', 'red': '#f0d040'},
            {'naam': 'Gouden drakenkoning', 'body': '#d8a828', 'lines': '#c02828'},
            {'naam': 'Wolkendraak (wit)', 'body': '#e0e4ec', 'lines': '#4080e0'},
            {'naam': 'Kosmisch (Deoxys)', 'body': '#5030a0', 'lines': '#40e0f0', 'red': '#f070c0'},
            {'naam': 'Bloedmaandraak', 'body': '#601828', 'lines': '#f0d040', 'red': '#e8e8e8'},
        ],
    },
    'jirachi': {
        'species': {'jirachi': {'gold': [1, 5, 4, 3], 'tags': [7, 6, 8], 'body': [12, 13, 9, 10]}},
        'variants': [
            {'naam': 'Zilveren ster', 'gold': '#c0c4d0', 'tags': '#e070a0'},
            {'naam': 'Robijnen ster', 'gold': '#d03048', 'tags': '#f0d040'},
            {'naam': 'Blauwe wensster', 'gold': '#5070d0', 'tags': '#f0d040'},
            {'naam': '1-up (groen)', 'gold': '#50c050', 'tags': '#f0f0f0'},
            {'naam': 'Zwarte ster', 'gold': ('#383848', {'l': 1.3}), 'tags': '#e04040'},
            {'naam': 'Sterrenstelsel', 'gold': '#382c70', 'tags': '#f0e060', 'body': '#e8e0f8'},
        ],
    },
    'deoxys': {
        # vier vormen met elk een eigen paletvolgorde
        'species': {
            'deoxys': {'red': [4, 1, 3], 'blue': [7, 8, 5], 'gem': [13, 9, 6]},
            'deoxys/attack': {'red': [1, 3, 2], 'blue': [8, 6, 5], 'gem': [9, 7]},
            'deoxys/defense': {'red': [1, 2, 3], 'blue': [8, 7, 6], 'gem': [4, 13, 9]},
            'deoxys/speed': {'red': [4, 7, 5], 'blue': [1, 2, 3], 'gem': [11, 9]},
        },
        'variants': [
            {'naam': 'Virus (zwart en paars)', 'red': ('#3a3048', {'l': 1.3}), 'blue': '#a050e0', 'gem': '#40f0a0'},
            {'naam': 'Mutant (groen)', 'red': '#40a060', 'blue': '#f0d040'},
            {'naam': 'Omgekeerd (blauw en rood)', 'red': '#3060c0', 'blue': '#e04040'},
            {'naam': 'DNA (wit)', 'red': '#e4e4ec', 'blue': '#4080e0', 'gem': '#e04040'},
            {'naam': 'Meteoriet (gloeiend ijzer)', 'red': '#6a6460', 'blue': '#e06020'},
            {'naam': 'Kosmisch roze', 'red': '#f070c0', 'blue': '#40e0f0', 'gem': '#f0e060'},
        ],
    },
    'zigzagoon_galar': {
        # Galar-vormen + Obstagoon: punk. Moderne sprites (alleen front.png) hebben ruizige schaduw:
        # donkere groepen donker houden, vooral de lichte strepen kleuren; geen albino.
        'species': {
            'zigzagoon/galar': {'dark': [1, 3, 4], 'light': [6, 7], 'tongue': [8, 10, 13, 12, 11]},
            'linoone/galar': {'dark': [3, 4, 2], 'light': [5, 6], 'tongue': [8, 9, 10]},
            'obstagoon': {'dark': [2, 4], 'grey': [8, 7], 'light': [5, 6]},
        },
        'variants': [
            {'naam': 'Tijgerpunk', 'light': '#f08020'},
            {'naam': 'Rasta-punk', 'dark': ('#1c4a24', {'l': 0.8}), 'light': '#f0d030', 'grey': '#c03028'},
            {'naam': 'Ziggy Stardust', 'dark': ('#5a1810', {'l': 0.8}), 'light': '#40a0e0', 'grey': '#d8d0c8'},
            {'naam': 'Cyberpunk', 'light': '#40d8f0', 'grey': '#58606c'},
            {'naam': 'Joker', 'dark': ('#2c1848', {'l': 0.8}), 'light': '#80e040', 'grey': '#b8a8c8'},
            {'naam': 'Daft Punk (goud en chroom)', 'light': '#e0b030', 'grey': '#c0c8d0'},
        ],
    },
    # --- groep 14 (Hoenn-dex-aanvulling, revisiesoorten eerst) ---
    'zubat': {
        'species': {
            'zubat': {'body': [9, 8, 7, 6], 'wing': [13, 12, 11]},
            'golbat': {'body': [8, 7, 6, 5], 'wing': [12, 11, 10, 9]},
            'crobat': {'body': [1, 2, 7, 3], 'wing': [5, 6, 8]},
        },
        'variants': [
            {'naam': 'Vampiervleermuis', 'body': '#6a4a38', 'wing': '#d89090'},
            {'naam': 'Vosvleerhond', 'body': '#c87830', 'wing': '#3c2c28'},
            {'naam': 'Batman', 'body': ('#34343c', {'l': 1.3}), 'wing': '#e0c030'},
            {'naam': 'Albino', 'body': ('#e4dcdc', ALBINO), 'wing': '#f0b8c0'},
            {'naam': 'Dracula', 'body': ('#24242c', {'l': 1.3}), 'wing': '#a01828'},
            {'naam': 'Sterrennacht (Van Gogh)', 'body': '#2c4890', 'wing': '#f0d040'},
        ],
    },
    'tentacool': {
        'species': {
            'tentacool': {'body': [4, 5, 6, 7], 'gems': [8, 9, 10, 11], 'tentacles': [12, 13, 14, 15]},
            'tentacruel': {'body': [14, 13, 12, 11], 'gems': [5, 4, 3, 2], 'tentacles': [9, 8, 7, 6]},
        },
        'variants': [
            {'naam': 'Kompaskwal', 'body': '#e8c070', 'gems': '#a03018', 'tentacles': '#a05030'},
            {'naam': 'Bloedkwal', 'body': ('#c83838', {'l': 1.35}), 'gems': '#f4f0f0', 'tentacles': '#f0a0a0'},
            {'naam': 'Oorkwal (doorzichtig)', 'body': ('#b8c8e0', {'l': 1.4}), 'gems': '#e080c0', 'tentacles': '#e8e0f0'},
            {'naam': 'Spiegeleikwal', 'body': ('#e8dcb0', {'l': 1.35}), 'gems': '#f0a020', 'tentacles': '#c8b060'},
            {'naam': 'Gifgroen', 'body': ('#50a038', {'l': 1.35}), 'gems': '#8030a0'},
            {'naam': 'Sterrenstelselkwal', 'body': '#382c70', 'gems': '#f070d0', 'tentacles': '#70e0f0'},
        ],
    },
    'machop': {
        'species': {
            'machop': {'body': [2, 3, 4, 5, 6], 'crest': [8, 9, 10, 11], 'eyes': [13, 14]},
            'machoke': {'body': [3, 4, 5, 6, 7], 'crest': [8, 9, 10, 11], 'briefs': [2]},
            'machamp': {'body': [3, 4, 5, 6], 'crest': [7, 8, 9, 10, 11], 'briefs': [2]},
        },
        'variants': [
            {'naam': 'Bronzen beeld', 'body': '#b07838', 'crest': '#e0c890'},
            {'naam': 'Hulk', 'body': '#5aa040', 'briefs': '#6a3c90', 'crest': '#2c2830'},
            {'naam': 'Hellboy', 'body': '#c03028', 'crest': '#2c2c30', 'briefs': '#2c2c30'},
            {'naam': 'Albino', 'body': ('#d8d0d0', {'l': 1.45}), 'crest': ('#d8c8a8', {'l': 1.3}), 'eyes': '#e02838'},
            {'naam': "Na'vi (Avatar)", 'body': '#3c78c8', 'crest': '#2c2830'},
            {'naam': 'Super Saiyan God', 'body': '#e0b030', 'crest': '#c02828', 'briefs': '#3050b0'},
        ],
    },
    'magnemite': {
        'species': {
            'magnemite': {'body': [14, 13, 12, 11], 'steel': [6, 5, 4, 3, 2], 'red': [8, 7], 'blue': [10, 9]},
            'magneton': {'body': [14, 13, 12, 11], 'steel': [6, 5, 4, 3, 2], 'red': [8, 7], 'blue': [10, 9]},
            'magnezone': {'body': [12, 10, 9, 11], 'steel': [7, 6], 'red': [14, 13], 'blue': [15], 'antenna': [1, 4]},
        },
        'variants': [
            {'naam': 'Koper', 'body': '#c07838', 'magnezone:body': '#7a3c18', 'magnezone:steel': '#606870'},
            {'naam': 'R2-D2 (wit met blauw)', 'body': '#e4e4ec', 'magnezone:body': '#c8ccd8', 'steel': '#3050b0'},
            {'naam': 'WALL-E (geel en roest)', 'body': '#d8a030', 'magnezone:body': '#806010', 'steel': '#8a5a38', 'magnezone:steel': '#6a4a30'},
            {'naam': 'Gunmetal', 'body': ('#3a3c48', {'l': 1.3}), 'red': '#40d0f0', 'blue': '#f0e040'},
            {'naam': 'Hoefijzermagneet', 'body': '#c83030', 'magnezone:body': '#781818', 'steel': '#d0d4dc', 'magnezone:steel': '#9098a8'},
            {'naam': 'Gouden Snaai (Harry Potter)', 'body': '#e0b030', 'magnezone:body': '#7a5810', 'steel': '#f0e8c8', 'magnezone:steel': '#a09060', 'antenna': '#f0f0f0'},
        ],
    },
    'voltorb': {
        # Poké Ball-kleuren als paletwissel (Jordi: patronen werden niets; geen Great Ball, dat is de shiny).
        # Hisui-vormen als Legends: Arceus-ballen (hball/hwood).
        # De Electrode-shiny is weer het origineel; zijn Master Ball-palet is nu de 0,5%.
        'species': {
            'voltorb': {'red': [14, 13, 12, 11, 10, 9], 'white': [4, 3, 2, 1]},
            'electrode': {'red': [14, 13, 12, 11, 10], 'white': [4, 3, 2, 1], 'lines': [5]},
            'voltorb/hisui': {'hball': [2, 3, 4, 5, 6, 7], 'hwood': [12, 9, 13]},
            'electrode/hisui': {'hball': [10, 14, 8, 9], 'hwood': [1, 2, 4, 5, 3, 6]},
        },
        'variants': [
            {'naam': 'Love Ball / Great Ball (Hisui)', 'red': '#f088b8', 'hball': '#2850b0'},
            {'naam': 'Friend Ball / Feather Ball (Hisui)', 'red': '#50b048', 'hball': '#70b0e8'},
            {'naam': 'Premier Ball / Wing Ball (Hisui)', 'red': '#e8e8ec', 'hball': '#3a9a50'},
            {'naam': 'Fast Ball / Ultra Ball (Hisui)', 'red': '#f0c030', 'hball': '#d8c020', 'hwood': '#8a8a90'},
            {'naam': 'Cherish Ball (twee kanten rood) / Strange Ball (Hisui)', 'red': ('#b01828', {'h': 0}), 'white': '#b01828', 'lines': '#3a1010', 'hball': '#c870c0'},
            {'naam': 'Master Ball / Origin Ball (Hisui, paars)', 'red': '#7838b0', 'electrode:palfile': 'master_ball.pal', 'hball': '#8848c0'},
        ],
    },
    'oddish': {
        # bloemkleuren; Oddish' bladeren dragen de kleur van de latere bloem
        'species': {
            'oddish': {'petals': [7, 6, 5, 4], 'body': [14, 13, 12]},
            'gloom': {'petals': [5, 4, 3, 2], 'center': [9, 8, 7], 'body': [14, 13, 12, 11]},
            'vileplume': {'petals': [8, 6, 7, 10, 9, 1], 'center': [4, 3, 2], 'body': [14, 13, 12]},
            'bellossom': {'petals': [1, 7, 2], 'center': [6, 5, 4], 'bbody': [8, 12, 10, 9], 'bleaves': [13, 14, 15]},
        },
        'variants': [
            {'naam': 'Witte rafflesia', 'petals': '#e8e4dc', 'center': '#a08070', 'bbody': '#88b8a0', 'bleaves': '#3a8a70'},
            {'naam': 'Blauwe lotus', 'petals': '#4878d0', 'center': '#f0d040', 'bbody': '#58b0a8', 'bleaves': '#286a88'},
            {'naam': 'Lijkbloem', 'petals': '#5a2858', 'center': '#e8d8a0', 'body': '#3c4a30', 'bbody': '#6a7a40', 'bleaves': '#4a2848'},
            {'naam': 'Zonnebloem', 'petals': '#f0c020', 'center': '#5a3018', 'bbody': '#b0a838', 'bleaves': '#6a8a18'},
            {'naam': 'Sakura', 'petals': '#f4b0c8', 'center': '#a04868', 'body': '#706078', 'bbody': '#b89098', 'bleaves': '#7a5040'},
            {'naam': 'Alruin (Harry Potter)', 'body': '#a07850', 'petals': '#c06080', 'center': '#3a6a30', 'bbody': '#b08860', 'bleaves': '#3a6a30'},
        ],
    },
    # --- groep 15 ---
    'doduo': {
        # in deze rom Ground/Flying; loopvogels
        'species': {
            'doduo': {'body': [8, 7, 6, 5], 'neck': [12, 11, 9, 10]},
            'dodrio': {'body': [4, 3, 2, 1], 'neck': [7, 6, 5], 'tail': [10, 9, 8], 'crest': [13, 12]},
        },
        'variants': [
            {'naam': 'Struisvogel', 'body': ('#34343c', {'l': 1.3}), 'neck': '#e8d0c0', 'tail': '#f0f0f0'},
            {'naam': 'Emoe', 'body': '#7a8090', 'neck': '#5a6070', 'tail': '#a0a8b8'},
            {'naam': 'Flamingo', 'body': '#f090a0', 'neck': '#f0b8c0', 'tail': '#d04060'},
            {'naam': 'Albino', 'body': ('#e4dcd8', ALBINO), 'neck': '#f0e8e0', 'tail': '#f0c8c8', 'crest': '#c8c0c0'},
            {'naam': 'Kasuaris', 'body': ('#24242c', {'l': 1.3}), 'neck': '#3070d0', 'tail': '#d03030', 'crest': '#c03030'},
            {'naam': 'Goudfazant', 'body': '#e0a020', 'neck': '#c02828', 'tail': '#2c6a40', 'crest': '#f0d040'},
        ],
    },
    'slugma': {
        # lavaslak (Fire/Rock)
        'species': {
            'slugma': {'lava': [2, 1, 5, 3, 6]},
            'magcargo': {'lava': [5, 1, 2, 13], 'shell': [7, 6, 9, 11], 'spots': [12, 14, 15]},
        },
        'variants': [
            {'naam': 'Blauw vuur (Kawah Ijen)', 'lava': '#3870e0', 'spots': '#80c0f8'},
            {'naam': 'Koperen vlam (groen)', 'lava': '#40b058', 'spots': '#a0e080'},
            {'naam': 'Paarse lava', 'lava': '#9040c0', 'spots': '#e070d0'},
            {'naam': 'Afgekoeld (obsidiaan)', 'lava': ('#3a3038', {'l': 1.3}), 'shell': ('#202028', {'l': 1.3}), 'spots': '#f08020'},
            {'naam': 'Witheet', 'lava': '#f0d870', 'shell': '#c03020', 'spots': '#f8f0c0'},
            {'naam': 'Sterrennevel', 'lava': '#e050c0', 'shell': '#28205a', 'spots': '#70e0f0'},
        ],
    },
    'grimer': {
        # ook de eigen Hoenn-vorm (bruin)
        'species': {
            'grimer': {'body': [11, 10, 9, 8, 7, 6]},
            'muk': {'body': [11, 10, 9, 8, 7, 6]},
            'grimer/hoenn': {'body': [11, 10, 9, 8, 7, 6]},
            'muk/hoenn': {'body': [11, 10, 9, 8, 7, 6]},
        },
        'variants': [
            {'naam': 'Bloedrood slijm', 'body': '#b02838'},
            {'naam': 'Olie', 'body': ('#30303a', {'l': 1.3})},
            {'naam': 'Kauwgom', 'body': '#f080b0'},
            {'naam': 'Lavaslijm', 'body': '#e07020'},
            {'naam': 'Ectoplasma', 'body': '#40a0e0'},
            {'naam': 'Midas (goud)', 'body': '#d8a828'},
        ],
    },
    'grimer_alola': {
        'species': {
            'grimer/alola': {'body': [3, 6, 8, 1, 2, 5], 'yellow': [11, 10, 9]},
            'muk/alola': {'body': [1, 8, 10], 'pink': [2, 5, 7], 'blue': [9, 11], 'yellow': [13, 12]},
        },
        'variants': [
            {'naam': 'Olie met regenboog', 'body': ('#2c2c34', {'l': 1.3}), 'pink': '#e050a0', 'blue': '#40c0e0', 'yellow': '#f0e040'},
            {'naam': 'Zuurstok', 'body': '#d83040', 'pink': '#f4f0f0', 'blue': '#30a050', 'yellow': '#f4f0f0'},
            {'naam': 'Teal', 'body': '#30a0a0', 'pink': '#f0d040', 'blue': '#e05060'},
            {'naam': 'Kauwgom', 'body': '#f080b0', 'pink': '#80d0f0', 'blue': '#b070e0'},
            {'naam': 'Lavendel en mint', 'body': '#a890d8', 'pink': '#80e0b0', 'blue': '#f0a0c0'},
            {'naam': 'Gouden slijm', 'body': '#d8a828', 'pink': '#c02828', 'blue': '#2c2c34', 'yellow': '#f4f0f0'},
        ],
    },
    'koffing': {
        'species': {
            'koffing': {'body': [14, 13, 12, 11], 'gas': [10, 9, 8]},
            'weezing': {'body': [14, 13, 12, 11, 10], 'gas': [9, 8, 7]},
        },
        'variants': [
            {'naam': 'Smog (LA, grijs met bruinoranje smog)', 'body': '#707078', 'gas': '#c88038'},
            {'naam': 'Tsjernobyl (olijf met radioactief groen)', 'body': '#4a5040', 'gas': '#80f040'},
            {'naam': 'Holi (oranje met roze poederwolken)', 'body': '#e07020', 'gas': '#e858b8'},
            {'naam': 'Droogijs (diepblauw met witte damp)', 'body': '#2c5aa8', 'gas': '#e8f4f8'},
            {'naam': 'Kosmische nevel', 'body': '#282060', 'gas': '#e070d0'},
            {'naam': 'Koninklijk (goud met paarse rook)', 'body': '#c89020', 'gas': '#9058d0'},
        ],
    },
    'weezing_galar': {
        # moderne sprite: grijs lijf + schoorstenen, witte rookhoed, groene gaswolken
        'species': {'weezing/galar': {'body': [7, 9, 8, 11], 'hat': [4, 5], 'gas': [1, 2, 3]}},
        'variants': [
            {'naam': 'Koperen pijpen', 'body': '#b06838', 'gas': '#60c0a0', 'hat': '#d0f0e4'},
            {'naam': 'Victoriaans Londen (erwtensoepmist)', 'body': '#5a6a80', 'gas': '#d8d090', 'hat': '#f4f0d8'},
            {'naam': 'Gietijzer (zwart met zwavelgeel)', 'body': ('#383840', {'l': 1.3}), 'gas': '#d8c040', 'hat': '#f4ecc0'},
            {'naam': 'Steampunk messing', 'body': '#c09040', 'gas': '#e4e4e0', 'hat': '#c0d8e8'},
            {'naam': 'Spookfabriek (paars met roze damp)', 'body': '#6a4a90', 'gas': '#e070c0', 'hat': '#f8d8f0'},
            {'naam': 'Gouden schoorstenen', 'body': '#d8a828', 'gas': '#70c8f0', 'hat': '#d8f0fc'},
        ],
    },
    'sandshrew': {
        'species': {
            'sandshrew': {'body': [7, 6, 5, 4, 3], 'belly': [10, 11, 12]},
            'sandslash': {'body': [5, 4, 3, 2, 1], 'belly': [7], 'spines': [14, 13, 12]},
        },
        'variants': [
            {'naam': 'Schubdier', 'body': '#8a6040', 'spines': '#5a3a20'},
            {'naam': 'Petra-rood', 'body': '#c86040', 'spines': '#7a2818'},
            {'naam': 'Egel', 'body': '#9a9088', 'spines': '#404048', 'belly': '#e8dcc8'},
            {'naam': 'Albino', 'body': ('#e8e0d8', ALBINO), 'spines': '#d8ccc0', 'belly': '#f4ece4'},
            {'naam': 'Roze gordeldier', 'body': '#e8a0b0', 'spines': '#c06080'},
            {'naam': 'Shadow the Hedgehog', 'body': ('#303038', {'l': 1.3}), 'spines': '#c02828', 'belly': '#e8dcc8'},
        ],
    },
    'sandshrew_alola': {
        # Ice/Steel
        'species': {
            'sandshrew/alola': {'body': [2, 1, 5, 4], 'belly': [10, 12, 11]},
            'sandslash/alola': {'body': [1, 8, 7, 5, 3, 6, 9, 12], 'belly': [10, 11]},
        },
        'variants': [
            {'naam': 'Smaragdijs', 'body': '#40b088'},
            {'naam': 'Rozenkwarts', 'body': '#f0a0c0'},
            {'naam': 'Koperijs', 'body': '#c07840'},
            {'naam': 'Amethist', 'body': '#9070d0'},
            {'naam': 'Goudijs', 'body': '#e0b030', 'belly': '#f4ecd8'},
            {'naam': 'Poolnacht', 'body': '#3a3070', 'belly': '#70e0d0'},
        ],
    },
    'skarmory': {
        # Steel/Flying; metalen
        'species': {'skarmory': {'steel': [3, 1, 10, 5, 4, 2], 'red': [7, 8, 11, 9]}},
        'variants': [
            {'naam': 'Koper', 'steel': '#b06838', 'red': '#40a0a0'},
            {'naam': 'Brons met patina', 'steel': '#507860', 'red': '#c08040'},
            {'naam': 'Gunmetal', 'steel': ('#3a3c48', {'l': 1.3}), 'red': '#40d0f0'},
            {'naam': 'Geanodiseerd titanium', 'steel': '#7050a8', 'red': '#f0d040'},
            {'naam': 'Goud (Mega Skarmory)', 'steel': '#d8a828', 'red': '#c02828'},
            {'naam': 'Excalibur (zilver en goud)', 'steel': '#c8ccd8', 'red': '#e0b030'},
        ],
    },
    # --- groep 16 (Hoenn-dex-rest, deel 1) ---
    'igglybuff': {
        'species': {
            'igglybuff': {'body': [1, 4, 6, 3, 2]},
            'jigglypuff': {'body': [15, 14, 13], 'eyes': [5, 4, 3]},
            'wigglytuff': {'body': [14, 13, 12, 11, 10], 'eyes': [6, 5, 4]},
        },
        'variants': [
            {'naam': 'Marshmallow', 'body': '#ece4e8'},
            {'naam': 'Keeby-geel (Kirby)', 'body': '#f0d050'},
            {'naam': 'Lavendel', 'body': '#c0a8e8', 'eyes': '#40a060'},
            {'naam': 'Mint', 'body': '#a8e0c0', 'eyes': '#c04880'},
            {'naam': 'Perzik', 'body': '#f8b890'},
            {'naam': 'Slaapliedje (nachthemel)', 'body': '#3a4078', 'eyes': '#f0d040'},
        ],
    },
    'staryu': {
        # in deze rom is Starmie Water/Electric
        'species': {
            'staryu': {'body': [2, 5, 1, 6, 3], 'core': [9, 7, 11, 10, 8], 'gem': [14, 12, 13]},
            'starmie': {'body': [2, 1, 4, 5, 3], 'core': [7, 11, 10, 8, 9], 'gem': [15, 13, 14, 12]},
        },
        'variants': [
            {'naam': 'Rode zeester (obsidiaan kern, gouden juweel)', 'body': '#c84030', 'core': ('#3a3848', {'l': 1.3}), 'gem': '#f0c830'},
            {'naam': 'Blauwe zeester (Linckia, koraal kern)', 'body': '#3060c0', 'core': '#f08048', 'gem': '#f0e060'},
            {'naam': 'Kussenster (turkoois kern)', 'body': '#e08030', 'core': '#30a0b0', 'gem': '#e04060'},
            {'naam': 'Doornenkroon (rode kern)', 'body': '#706080', 'core': '#c83838', 'gem': '#40d0a0'},
            {'naam': 'Smaragd met robijn', 'body': '#2c8a60', 'core': '#e0e0e8'},
            {'naam': 'Patrick Star', 'body': '#f090a0', 'core': '#80c040'},
        ],
    },
    'vulpix': {
        'species': {
            'vulpix': {'body': [11, 10, 9, 8], 'tail': [15, 14, 13, 12], 'hair': [7, 6]},
            'ninetales': {'fur': [14, 13, 12, 11], 'tips': [7, 6]},
        },
        'variants': [
            {'naam': 'Grijze vos (Urocyon)', 'body': '#5a5a68', 'tail': '#c8c8d0', 'hair': '#e08040', 'fur': '#7a7a84', 'tips': '#e08040'},
            {'naam': 'Fennek', 'body': '#e8c890', 'tail': '#f4e8d0', 'hair': '#c89058', 'fur': '#e0b078', 'tips': '#f4e8d0'},
            {'naam': 'Melanistische vos', 'body': ('#2c2c34', {'l': 1.3}), 'tail': '#5a3060', 'hair': '#a050c0', 'fur': '#484050', 'tips': '#a050c0'},
            {'naam': 'Albino', 'body': ('#ece4e0', ALBINO), 'tail': ('#e4dcd8', ALBINO), 'hair': '#f0d8d0', 'fur': ('#f0ece8', ALBINO), 'tips': '#f0c8c8'},
            {'naam': 'Spookvuur (blauw)', 'body': '#3060c0', 'tail': '#80c0f0', 'hair': '#a0e0f8', 'fur': '#a8c8f0', 'tips': '#3060c0'},
            {'naam': 'Amaterasu (Okami)', 'body': '#f0ece4', 'tail': '#d03030', 'hair': '#d03030', 'fur': '#f4f0ec', 'tips': '#d03030'},
        ],
    },
    'vulpix_alola': {
        # Ice/Fairy
        'species': {
            'vulpix/alola': {'fur': [1, 2, 3], 'curls': [4, 7, 5]},
            'ninetales/alola': {'fur': [1, 3, 2], 'blue': [9, 4, 5]},
        },
        'variants': [
            {'naam': 'Perzik', 'fur': '#f8c8a0', 'curls': '#fce8d8', 'blue': '#e07040'},
            {'naam': 'Kanto-ruil (goud en vuur)', 'fur': '#f0e080', 'curls': '#f8f0c8', 'blue': '#e08030'},
            {'naam': 'Mint', 'fur': '#b0e8d0', 'curls': '#e8f8f0', 'blue': '#30a080'},
            {'naam': 'Gletsjer', 'fur': '#90c8f0', 'curls': '#e0f0f8', 'blue': '#2050a0'},
            {'naam': 'Nachtblauw', 'fur': '#384890', 'curls': '#a0b0e0', 'blue': '#f0e080'},
            {'naam': 'Aurora', 'fur': '#7060c0', 'curls': '#a0f0d0', 'blue': '#40e0a0'},
        ],
    },
    'pichu': {
        # elektrische knaagdieren (Pikachu-kloons)
        'species': {
            'pichu': {'body': [4, 5, 7, 3, 6, 8]},
            'pikachu': {'body': [4, 3, 2, 5, 6, 7], 'tips': [14, 13]},
            'raichu': {'body': [5, 4, 6, 7], 'belly': [2, 3], 'ears': [12, 11], 'tail': [10, 9]},
            'raichu/alola': {'body': [9, 8, 5, 7, 6], 'tail': [2, 4, 1], 'belly': [14, 13]},
        },
        'variants': [
            {'naam': 'Bulbasaur', 'body': '#78c8a8', 'tips': '#2c6a40', 'ears': '#3a8a50', 'tail': '#3a9a50',
             'raichu/alola:body': '#5aa890', 'raichu/alola:tail': '#4a9a48', 'belly': '#e8f0d8'},
            {'naam': 'Squirtle', 'body': '#7ac0e8', 'tips': '#8a5a30', 'ears': '#9a6838', 'tail': '#9a6838', 'belly': '#f0e0a8',
             'raichu/alola:body': '#5aa0d8', 'raichu/alola:tail': '#c08850'},
            {'naam': 'Charmander', 'body': '#e85a30', 'ears': '#d03020', 'tail': '#f0c020', 'belly': '#f8e0a0',
             'raichu/alola:body': '#f09040', 'raichu/alola:tail': '#e03020'},
            {'naam': 'Jigglypuff-roze', 'body': '#f8a8c8', 'tips': '#3a3a48', 'ears': '#c06080', 'tail': '#f8d8e8', 'belly': '#fce8f0',
             'raichu/alola:body': '#e888b0', 'raichu/alola:tail': '#fcd8e8'},
            {'naam': 'Marill', 'body': '#5890e0', 'tips': '#3050a0', 'ears': '#3050a0', 'tail': '#3070d0', 'belly': '#f0f4f8',
             'raichu/alola:body': '#5890e0', 'raichu/alola:tail': '#f0f4f8'},
            {'naam': 'Sterrennacht (Van Gogh)', 'body': ('#2c4090', {'l': 1.3}), 'ears': '#f0d040',
             'tail': '#f0d040', 'belly': '#a8c0f0', 'raichu/alola:tail': '#f0d040', 'tips': ('#202030', {'l': 1.3})},
        ],
    },
    'psyduck': {
        'species': {
            'psyduck': {'body': [14, 13, 12, 11], 'beak': [4, 3, 2, 1]},
            'golduck': {'body': [14, 13, 12, 11], 'beak': [9, 8, 7, 6], 'gem': [5, 4, 3]},
        },
        'variants': [
            {'naam': 'Wilde eend (groen)', 'body': '#3a8050', 'beak': '#e8d060'},
            {'naam': 'Bruine eend', 'body': '#8a6038', 'beak': '#e8a058'},
            {'naam': 'Roze eend', 'body': '#f0a0c0', 'beak': '#f8d0a8'},
            {'naam': 'Albino', 'body': ('#ece8e4', ALBINO), 'beak': '#f0c8a8', 'gem': '#e02838'},
            {'naam': 'Zwarte zwaan', 'body': ('#2c2c34', {'l': 1.3}), 'beak': '#d02830'},
            {'naam': 'Robijneend', 'body': '#c02848', 'gem': '#f0d040', 'beak': '#f0e0b8'},
        ],
    },
    'natu': {
        'species': {
            'natu': {'green': [5, 4, 6, 7], 'red': [1, 3, 2], 'yellow': [11, 10, 9]},
            'xatu': {'green': [3, 1, 5, 2], 'red': [12, 13, 15], 'robe': [10, 11, 14, 9], 'yellow': [7, 4, 6]},
        },
        'variants': [
            {'naam': 'Rode ara', 'green': '#d83020', 'robe': '#2c70c8', 'red': '#f0d040', 'yellow': '#f0c820'},
            {'naam': 'Toekan', 'green': ('#2c2c34', {'l': 1.3}), 'robe': '#f0b020', 'red': '#d02020', 'yellow': '#f08020'},
            {'naam': 'Hyacintara', 'green': '#2c50c0', 'robe': '#f0c820', 'red': '#40c0e0', 'yellow': '#e8c030'},
            {'naam': 'Albino', 'green': ('#e8e4e0', ALBINO), 'red': '#f0b8b8', 'yellow': '#f0e8d0', 'robe': ('#f4f0ec', ALBINO)},
            {'naam': 'Quetzal', 'green': '#20a070', 'robe': '#c02030', 'red': '#f0d040', 'yellow': '#f0d040'},
            {'naam': 'Azteeks goud', 'green': '#d8a828', 'robe': '#2c6a8a', 'red': '#2c9a80'},
        ],
    },
    'girafarig': {
        # Farigiraf is een moderne sprite: alleen de lichte vacht
        'species': {
            'girafarig': {'body': [6, 7, 8], 'rear': [11, 13, 14, 15]},
            'farigiraf': {'body': [15, 14], 'rear': [2, 1]},
        },
        'variants': [
            {'naam': 'Okapi', 'body': '#6a3c28', 'rear': '#d8d0c0'},
            {'naam': 'Witte giraf (leucistisch)', 'body': '#ece8e0', 'rear': '#8a6040'},
            {'naam': 'Lisa Frank-roze', 'body': '#f0a0c0', 'rear': '#6040a0'},
            {'naam': 'Psychic-blauw', 'body': '#6080d0', 'rear': '#d8a030'},
            {'naam': 'Zwart en goud', 'body': ('#383040', {'l': 1.3}), 'rear': '#d8a828'},
            {'naam': 'Kosmisch', 'body': '#2c2060', 'rear': '#e070d0'},
        ],
    },
    'phanpy': {
        'species': {
            'phanpy': {'body': [2, 1, 10, 4, 3], 'ears': [6, 7, 8]},
            'donphan': {'body': [2, 1, 4, 3], 'armor': [9, 6, 11, 7], 'red': [8, 10], 'tusks': [13, 14, 12]},
        },
        'variants': [
            {'naam': 'Mammoet', 'body': '#8a5a38', 'armor': '#a07858', 'tusks': '#f0e8d0'},
            {'naam': 'Witte olifant', 'body': '#e8e4dc', 'armor': '#f4f0ec'},
            {'naam': 'Roze olifant', 'body': '#f0a0c0', 'armor': '#f8c8d8'},
            {'naam': 'Lava-olifant', 'body': ('#3a3038', {'l': 1.3}), 'armor': '#e06020', 'ears': '#f0a020'},
            {'naam': 'Ganesha (blauw en goud)', 'body': '#3870c8', 'armor': '#3870c8', 'tusks': '#e0b030', 'ears': '#e0b030'},
            {'naam': 'Thaise tempelolifant (goud)', 'body': '#d8a828', 'armor': '#f0d060', 'ears': '#c02828'},
        ],
    },
    # --- groep 17 (Hoenn-dex-rest, deel 2) ---
    'pinsir': {
        # Bug/Ground; kevers
        'species': {'pinsir': {'body': [11, 8, 12, 9, 10], 'horns': [2, 1, 5, 3, 4]}},
        'variants': [
            {'naam': 'Zwarte neushoornkever', 'body': ('#3a3038', {'l': 1.3})},
            {'naam': 'Vliegend hert (roodbruin)', 'body': '#8a3020'},
            {'naam': 'Goudkever (Chrysina)', 'body': '#c8a030'},
            {'naam': 'Groene juweelkever', 'body': '#2c8a50'},
            {'naam': 'Paarlemoerkever (zwarte hoorns)', 'body': '#e0dcd8', 'horns': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Scarabee (turkoois en goud)', 'body': '#1c6a78', 'horns': '#e0b030'},
        ],
    },
    'heracross': {
        'species': {'heracross': {'body': [3, 5, 4, 2], 'tip': [6, 8, 7]}},
        'variants': [
            {'naam': 'Herculeskever (olijf)', 'body': '#5a5a30'},
            {'naam': 'Japanse neushoornkever', 'body': '#6a2c20'},
            {'naam': 'Goliathkever (wit)', 'body': ('#aeaaa2', {'l': 1.2}), 'tip': '#2c2c34'},
            {'naam': 'Goudtor', 'body': '#c8a030', 'tip': '#c02828'},
            {'naam': 'Smaragdkever', 'body': '#2c9a60'},
            {'naam': 'Kabuto (samoerai)', 'body': ('#2c2c34', {'l': 1.3}), 'tip': '#c02828'},
        ],
    },
    'rhyhorn': {
        'species': {
            'rhyhorn': {'body': [5, 4, 3, 2, 1]},
            'rhydon': {'body': [14, 13, 12, 11]},
            'rhyperior': {'body': [3, 6, 1, 2, 5], 'armor': [8, 12, 9, 10], '_base': {'body': 1}},
        },
        'variants': [
            {'naam': 'Bemost', 'body': '#6a8a50', 'rhyperior:body': '#5a7a48'},
            {'naam': 'Witte neushoorn', 'body': '#d8d4cc', 'rhyperior:body': ('#c8c4bc', {'l': 1.2})},
            {'naam': 'Basalt met lava', 'body': ('#3a3038', {'l': 1.3}), 'rhyperior:body': ('#3a3440', {'l': 1.3}), 'armor': '#f0e040'},
            {'naam': 'Amethist', 'body': '#8a70b0', 'rhyperior:body': '#6a5a98', 'armor': '#e0c060'},
            {'naam': 'Diamant', 'body': '#c8e0f0', 'rhyperior:body': ('#b0d0ec', {'l': 1.2}), 'armor': '#58b8e8'},
            {'naam': 'Goud', 'body': '#c89828', 'rhyperior:body': ('#c89828', {'h': 0}), 'armor': '#3060b0'},
        ],
    },
    'corsola': {
        # Galar-Corsola/Cursola (moderne, bijna witte sprites) nog niet
        'species': {'corsola': {'body': [7, 1, 5, 4, 6, 2]}},
        'variants': [
            {'naam': 'Hersenkoraal', 'body': '#e0c050'},
            {'naam': 'Groen koraal', 'body': '#60b060'},
            {'naam': 'Edelkoraal (rood)', 'body': '#c02030'},
            {'naam': 'Gebleekt koraal', 'body': '#ece8e4'},
            {'naam': 'Zwart koraal', 'body': ('#3a3038', {'l': 1.3})},
            {'naam': 'Oranje zeewaaier', 'body': '#f08030'},
        ],
    },
    'chinchou': {
        'species': {
            'chinchou': {'body': [7, 2, 1, 3, 6, 13], 'light': [4, 12, 5, 11, 9, 10]},
            'lanturn': {'body': [7, 4, 8, 5, 12], 'light': [11, 1, 6, 3, 2]},
        },
        'variants': [
            {'naam': 'Bloedrode diepzeevis', 'body': '#a02830'},
            {'naam': 'Zilveren lantaarnvis', 'body': '#a8b0c0', 'light': '#40c0f0'},
            {'naam': 'Zwart met cyaan licht', 'body': ('#2c2c38', {'l': 1.3}), 'light': '#40e0f0'},
            {'naam': 'Albino (grottenvis)', 'body': ('#ecdcdc', ALBINO), 'light': '#f8f0c0'},
            {'naam': 'Bioluminescent groen', 'body': '#1c5a50', 'light': '#80f060'},
            {'naam': 'Goudvislantaarn', 'body': '#e08030', 'light': '#f4f4f4'},
        ],
    },
    'horsea': {
        'species': {
            'horsea': {'body': [1, 2, 3, 4], 'fins': [9, 11, 10]},
            'seadra': {'body': [10, 2, 1, 5, 3], 'fins': [6, 9, 7]},
            'kingdra': {'body': [4, 1, 5, 3, 6], 'fins': [13, 12, 11]},
        },
        'variants': [
            {'naam': 'Oranje zeepaardje', 'body': '#e08030', 'fins': '#f8e0a0'},
            {'naam': 'Pygmeezeepaardje', 'body': '#f0a0b0', 'fins': '#e05070'},
            {'naam': 'Blad-zeedraak', 'body': '#8aa040', 'fins': '#e0c060'},
            {'naam': 'Zwart zeepaardje', 'body': ('#2c2c34', {'l': 1.3}), 'fins': '#f0d040'},
            {'naam': 'Spookzeepaardje', 'body': ('#c8d0dc', {'l': 1.5}), 'fins': '#90c8e0'},
            {'naam': 'Robijn en goud', 'body': '#a01830', 'fins': '#e0b030'},
        ],
    },
    'celebi': {
        # in deze rom Fairy/Grass
        'species': {'celebi': {'green': [7, 1, 2], 'light': [10, 12, 9], 'eyes': [6, 4, 5]}},
        'variants': [
            {'naam': 'Herfstblad', 'green': '#d07028', 'light': '#f0d0a0'},
            {'naam': 'Winter', 'green': '#a8b8c8', 'light': '#e8f0f8', 'eyes': '#3060c0'},
            {'naam': 'Lavendelfee', 'green': '#9070c8', 'light': '#e0d0f0'},
            {'naam': 'Bloemgeel', 'green': '#e0c030', 'light': '#f8f0b0', 'eyes': '#40a040'},
            {'naam': 'Tijdreiziger (blauw)', 'green': '#3a70c0', 'light': '#c8e0f8', 'eyes': '#f0d040'},
            {'naam': 'GS Ball (goud en zilver)', 'green': '#c8a030', 'light': '#e0e4ec'},
        ],
    },
    # --- groep 18 (Kanto/Johto, revisiesoorten eerst) ---
    'ekans': {
        # Arbok in deze rom Poison/Dark
        'species': {
            'ekans': {'body': [15, 14, 13, 12, 11], 'belly': [9, 8, 7, 6, 5]},
            'arbok': {'body': [12, 11, 10, 9], 'hood': [7, 4, 13, 6, 3], 'hoodyellow': [2]},
        },
        'variants': [
            {'naam': 'Koraalslang', 'body': '#c02828', 'hood': '#f0d040', 'hoodyellow': '#2c2c34'},
            {'naam': 'Koperkop', 'body': '#c07040', 'hood': '#5a3020'},
            {'naam': 'Zwarte mamba', 'body': ('#3a3a40', {'l': 1.3}), 'hood': '#c8c8d0'},
            {'naam': 'Albino python', 'body': ('#ece8dc', ALBINO), 'belly': '#f0d060', 'hood': '#f0c040'},
            {'naam': 'Blauwe adder', 'body': '#3a70c0', 'hood': '#e0e8f0'},
            {'naam': 'Egyptische cobra (turkoois en goud)', 'body': '#30a8a0', 'hood': '#e0b030', 'hoodyellow': '#c02828'},
        ],
    },
    'venonat': {
        # Venomoth in deze rom Psychic/Poison; nachtvlinders
        'species': {
            'venonat': {'body': [14, 13, 12, 11], 'eyes': [7, 6, 5, 4]},
            'venomoth': {'body': [15, 14, 13, 12, 11]},
        },
        'variants': [
            {'naam': 'Rozenmot (rosy maple moth)', 'body': '#f0a0c0', 'eyes': '#f0d040'},
            {'naam': 'Lunamot', 'body': '#a0d890', 'eyes': '#c06090'},
            {'naam': 'Atlasvlinder', 'body': '#a04828', 'eyes': '#f0d040'},
            {'naam': 'Doodshoofdvlinder', 'body': ('#3a3038', {'l': 1.3}), 'eyes': '#f0c020'},
            {'naam': 'Witte mot', 'body': '#e8e4dc'},
            {'naam': 'Mothra', 'body': '#e0a030', 'eyes': '#3060c0'},
        ],
    },
    'seel': {
        # Dewgong in deze rom Ice/Fairy
        'species': {
            'seel': {'body': [4, 3, 2, 1]},
            'dewgong': {'body': [5, 4, 3, 2, 1]},
        },
        'variants': [
            {'naam': 'Doejong (grijs)', 'body': '#8a9098'},
            {'naam': 'Zeeolifant', 'body': '#a07858'},
            {'naam': 'Roze rivierdolfijn', 'body': '#f0b0c0'},
            {'naam': 'IJsblauw', 'body': '#90c0e0'},
            {'naam': 'Zwarte zeeleeuw', 'body': ('#3a3a44', {'l': 1.3})},
            {'naam': 'Amber', 'body': '#e0a040'},
        ],
    },
    'gastly': {
        'species': {
            'gastly': {'gas': [10, 11, 12], 'orb': [9, 8, 7, 6], 'eyes': [4, 3]},
            'haunter': {'gas': [4, 3, 2, 5], 'mouth': [10, 9]},
            'gengar': {'gas': [13, 12, 11, 10, 14], 'eyes': [6, 5, 4]},
        },
        'variants': [
            {'naam': 'Slimer-groen', 'gas': '#50a040', 'orb': ('#3a2050', {'l': 1.3}), 'eyes': '#f0e040', 'mouth': '#f0e040'},
            {'naam': 'Bloedrood / grijsblauwe geest', 'gas': '#b03040', 'orb': ('#202838', {'l': 1.3}), 'eyes': '#3080e0',
             'haunter:gas': '#6a7a90', 'gengar:gas': '#6a7a90', 'mouth': '#3080e0'},
            {'naam': 'Boo-blauw', 'gas': '#4a70c0', 'orb': ('#3a1830', {'l': 1.3}), 'eyes': '#f0a020', 'mouth': '#f0a020'},
            {'naam': 'Witte Boo (Mario)', 'gas': '#e8e4ec', 'orb': ('#283048', {'l': 1.3}), 'eyes': '#f04060', 'mouth': '#f04060'},
            {'naam': 'Halloween-oranje', 'gas': '#e07020', 'orb': ('#1c3a1c', {'l': 1.3}), 'eyes': '#80e040', 'mouth': '#80e040'},
            {'naam': 'Gouden spook', 'gas': '#d8a828', 'orb': ('#401838', {'l': 1.3}), 'eyes': '#e03030', 'mouth': '#7040c0'},
        ],
    },
    'drowzee': {
        # Hypno in deze rom Psychic/Dark; tapir en hypnotiseur
        'species': {
            'drowzee': {'yellow': [7, 6, 10, 9, 11], 'brown': [2, 3, 4, 5]},
            'hypno': {'yellow': [3, 5, 4, 6, 2, 8, 7]},
        },
        'variants': [
            {'naam': 'Maleise tapir', 'yellow': ('#3a3a42', {'l': 1.3}), 'brown': '#e8e4dc'},
            {'naam': 'Baku (Japanse droomvreter)', 'yellow': '#5070c0'},
            {'naam': 'Freddy Krueger', 'yellow': '#a02828', 'brown': '#3a6a30'},
            {'naam': 'Albino', 'yellow': ('#e0d8d0', ALBINO), 'hypno:yellow': ('#c8c0b8', ALBINO), 'brown': '#e0c8c0'},
            {'naam': 'Hypnosespiraal (groen)', 'yellow': '#60b060'},
            {'naam': 'Paars en goud', 'yellow': '#5a3a8a', 'brown': '#e0b030'},
        ],
    },
    'farfetchd': {
        # Fighting/Flying; Galar-vormen (moderne sprites) nog niet
        'species': {'farfetchd': {'body': [14, 13, 12], 'leek': [10, 9, 8]}},
        'variants': [
            {'naam': 'Grijze gans (rode ui)', 'body': '#8a8a90', 'leek': '#a04880'},
            {'naam': 'Wilde eend (knoflook)', 'body': '#3a7050', 'leek': '#e0dcb8'},
            {'naam': 'Zwarte eend (bieslookbloem)', 'body': ('#2c2c34', {'l': 1.3}), 'leek': '#c8a0e0'},
            {'naam': 'Albino (gele ui)', 'body': ('#ece8e0', ALBINO), 'leek': '#e8c040'},
            {'naam': 'Zuurstok', 'body': '#a02828', 'leek': '#f0f0f0'},
            {'naam': 'Koningsblauw met gouden zwaard', 'body': '#2c4890', 'leek': '#e0b030'},
        ],
    },
    'dunsparce': {
        # Normal/Ground
        'species': {'dunsparce': {'yellow': [1, 4, 3, 2], 'blue': [13, 12, 10]},
                    'dudunsparce': {'yellow': [12, 6, 4, 7], 'blue': [11, 8, 5]}},
        'variants': [
            {'naam': 'Groene drakenslang', 'yellow': '#80b040'},
            {'naam': 'Lavendel', 'yellow': '#b098d8', 'blue': '#e0b030'},
            {'naam': 'Roodbruin', 'yellow': '#a85030'},
            {'naam': 'Albino', 'yellow': ('#ece8e0', ALBINO), 'blue': '#e0b0c0'},
            {'naam': 'Koi', 'yellow': '#e07030', 'blue': '#f4f4f4'},
            {'naam': 'Chinese draak', 'yellow': '#c02828', 'blue': '#e0b030'},
        ],
    },
    # --- groep 19 (Kanto/Johto) ---
    'ledyba': {
        # Ledian in deze rom Bug/Normal; lieveheersbeestjes
        'species': {
            # tokusatsu-helden (Jordi): schild, buik, ledematen en ogen
            'ledyba': {'shell': [4, 5, 3, 6], 'belly': [10, 11, 12, 13], 'limbs': [7, 9], 'accent': [15, 14]},
            'ledian': {'shell': [3, 6, 5, 4], 'belly': [12, 13, 11], 'limbs': [10, 14, 15], 'eyes': [9, 7]},
        },
        'variants': [
            {'naam': 'Kamen Rider 1 (groen, zilver, rode ogen)', 'shell': '#3a8a50', 'belly': '#c8ccd8', 'limbs': ('#3a3a44', {'l': 1.3}),
             'eyes': '#e03030', 'accent': '#e03030'},
            {'naam': 'Ultraman (rood en zilver, gloeiende ogen)', 'shell': '#d02828', 'belly': '#c8ccd8', 'limbs': '#d8dce4',
             'eyes': '#f8f0a0', 'accent': '#f8f0a0'},
            {'naam': 'Super Sentai (Blue Ranger)', 'shell': '#2860c8', 'belly': '#f0f0f0', 'limbs': '#f0f0f0',
             'eyes': ('#2c2c34', {'l': 1.3}), 'accent': '#2c2c34'},
            {'naam': 'Kamen Rider Black (zwart en groen)', 'shell': ('#2c2c34', {'l': 1.3}), 'belly': '#3a9a50', 'limbs': ('#3a3a44', {'l': 1.3}),
             'eyes': '#e03030', 'accent': '#e03030'},
            {'naam': 'Space Sheriff Gavan (chroom met blauw)', 'shell': '#d8dce8', 'belly': ('#2c2c34', {'l': 1.3}), 'limbs': '#3060c0',
             'eyes': '#40c0f0', 'accent': '#40c0f0'},
            {'naam': 'Kamen Rider Kuuga Rising (goud en zwart)', 'shell': ('#d8a828', {'h': 0}), 'belly': ('#2c2c34', {'l': 1.3}),
             'limbs': ('#2c2c34', {'l': 1.3}), 'eyes': '#e03030', 'accent': '#e03030'},
        ],
    },
    'remoraid': {
        'species': {
            'remoraid': {'body': [2, 1, 10, 7, 3, 4]},
            'octillery': {'body': [2, 5, 6, 8], 'pot': [3, 4, 11]},
        },
        'variants': [
            {'naam': 'Groene octopus', 'body': '#50a050'},
            {'naam': 'Blauwringoctopus', 'body': '#d8b840', 'pot': '#3060d0'},
            {'naam': 'Mimic-octopus', 'body': '#8a5a38', 'pot': '#f0ece4'},
            {'naam': 'Albino (glasoctopus)', 'body': ('#ece4e0', ALBINO), 'pot': '#f0c8c8'},
            {'naam': 'Dumbo-octopus', 'body': '#f0a0b0'},
            {'naam': 'Kraken', 'body': ('#2c2830', {'l': 1.3}), 'pot': '#c02828'},
        ],
    },
    'poliwag': {
        # kikkers; de spiraal blijft
        'species': {
            'poliwag': {'body': [14, 13, 12, 11, 7], 'spiral': [4]},
            'poliwhirl': {'body': [14, 13, 12, 11], 'spiral': [9]},
            'poliwrath': {'body': [14, 13, 12, 11], 'spiral': [9]},
            'politoed': {'body': [5, 4, 7, 6], 'spiral': [2, 1], 'belly': [12, 14]},
        },
        'variants': [
            {'naam': 'Oranje pijlgifkikker', 'body': '#e07020', 'spiral': '#284898', 'belly': '#4a4a58'},
            {'naam': 'Pad (bruin)', 'body': '#8a6a40', 'spiral': '#d89838', 'belly': '#e8dcb8'},
            {'naam': 'Paarse kikker', 'body': '#7048a8', 'spiral': '#e0b020', 'belly': '#f0d040'},
            {'naam': 'Albino', 'body': ('#ece0e0', ALBINO), 'spiral': '#e07090', 'belly': '#d03838'},
            {'naam': 'Gouden gifkikker (zwarte buik)', 'body': '#e8c030', 'spiral': '#a02818', 'belly': '#3a3a48'},
            {'naam': 'Aardbeigifkikker (blauwe jeans)', 'body': '#c82828', 'spiral': '#3050c0', 'belly': '#4068d0'},
        ],
    },
    'porygon': {
        # Porygon-Z in deze rom Electric/Ghost; digitaal
        'species': {
            'porygon': {'red': [12, 1, 3, 5, 4], 'blue': [8, 9, 11, 10, 14]},
            'porygon2': {'red': [3, 1, 2, 5], 'blue': [9, 4, 8, 7]},
            'porygon_z': {'red': [1, 2, 5, 3, 6], 'blue': [8, 9, 12, 11]},
        },
        'variants': [
            {'naam': 'Wireframe (groen op zwart)', 'red': ('#2c2c34', {'l': 1.3}), 'blue': '#40e060'},
            {'naam': 'Windows 95', 'red': '#a8a8b0', 'blue': '#3050b0'},
            {'naam': 'Super Famicom (grijs, per evolutie een knopkleur: groen Y, geel B, rood A)', 'red': '#d0d0d8', 'blue': '#3aa048',
             'porygon2:blue': '#e0c030', 'porygon_z:blue': '#c83838'},
            {'naam': 'Virtual Boy', 'red': '#c02020', 'blue': ('#2c2c30', {'l': 1.3})},
            {'naam': 'Glitch (MissingNo.)', 'red': '#a040c0', 'blue': '#40e0e0'},
            {'naam': 'Game Boy Color Pikachu-editie', 'red': '#f0c030', 'blue': '#3060c0'},
        ],
    },
    'caterpie': {
        # rupsen en vlinders: de rups draagt de kleur van de vlinder
        'species': {
            'caterpie': {'body': [1, 2, 3, 4, 5, 6], 'antenna': [12, 13, 14, 11]},
            'metapod': {'body': [1, 2, 4, 3, 5, 6]},
            'butterfree': {'wings': [13, 14], 'body': [1, 2, 3, 4, 11], 'eyes': [8, 9, 10, 7], 'feet': [5, 6]},
        },
        'variants': [
            {'naam': 'Blauwe morpho', 'body': '#3060c0', 'antenna': '#f0d040', 'butterfree:body': ('#2c2c34', {'l': 1.3}),
             'wings': '#4890e8', 'eyes': '#f0d040', 'feet': '#f0d040'},
            {'naam': 'Rode admiraal', 'body': '#c83030', 'antenna': '#40c0e0', 'butterfree:body': ('#2c2c34', {'l': 1.3}),
             'wings': '#d04030', 'eyes': '#40c0e0', 'feet': '#f0f0f0'},
            {'naam': 'Koninginnenpage (zwarte rups, oranje nekvork)', 'body': ('#34343c', {'l': 1.3}), 'antenna': '#f08020',
             'butterfree:body': ('#2c2c34', {'l': 1.3}), 'wings': '#f0c840', 'eyes': '#4080f0', 'feet': '#4080f0'},
            {'naam': 'Venomoth-knipoog', 'body': '#8a6ab0', 'antenna': '#e04040', 'butterfree:body': '#6a4a78',
             'wings': '#e8c8f0', 'eyes': '#88c8c0', 'feet': '#a08070'},
            {'naam': 'Grote weerschijnvlinder (paars)', 'body': '#6040a0', 'antenna': '#f0a020', 'butterfree:body': ('#2c2c34', {'l': 1.3}),
             'wings': '#7050c0', 'eyes': '#f0a020', 'feet': '#f0a020'},
            {'naam': 'Smaragdpijlstaart', 'body': '#20a0a0', 'antenna': '#f04080', 'butterfree:body': ('#1c3040', {'l': 1.3}),
             'wings': '#50c080', 'eyes': '#f04080', 'feet': '#f04080'},
        ],
    },
    'weedle': {
        # Bug/Poison; wespen en bijen
        'species': {
            'weedle': {'body': [10, 9, 8, 7, 6], 'red': [13, 14, 12, 11], 'stinger': [3, 4, 2]},
            'kakuna': {'body': [7, 6, 5, 4, 3, 2]},
            'beedrill': {'body': [6, 5, 4, 3, 2], 'red': [12, 13, 11]},
        },
        'variants': [
            {'naam': 'Hoornaar', 'body': '#a05020', 'red': ('#2c2c34', {'l': 1.3}), 'stinger': '#f0c030'},
            {'naam': 'Blauwe houtbij', 'body': '#3050b0', 'red': '#f0d040', 'stinger': '#3a3a44'},
            {'naam': 'Rode wesp', 'body': '#c02828', 'red': '#40c0e0', 'stinger': '#3a3a44'},
            {'naam': 'Paarse houtbij', 'body': '#7040a0', 'red': '#80e040', 'stinger': '#e0b030'},
            {'naam': 'Albino', 'body': ('#ece8dc', ALBINO), 'red': '#e04060', 'stinger': '#e8b0b0'},
            {'naam': 'Zwarte hoornaar', 'body': ('#2c2c34', {'l': 1.3}), 'red': '#f0a020', 'stinger': '#c02828'},
        ],
    },
    'pidgey': {
        'species': {
            'pidgey': {'body': [14, 13, 12, 11], 'cream': [10, 9, 8]},
            'pidgeotto': {'body': [11, 10, 9], 'cream': [7, 6], 'crest': [15, 14, 13, 12]},
            'pidgeot': {'body': [14, 13, 12], 'cream': [5, 4, 3], 'crest': [9, 8, 7, 6]},
        },
        'variants': [
            {'naam': 'Stadsduif', 'body': '#8a8a98', 'cream': '#d8d8e0'},
            {'naam': 'Roodborst', 'body': '#7a5a40', 'cream': '#e06030'},
            {'naam': 'Pimpelmees', 'body': '#3a70c0', 'cream': '#f0d040'},
            {'naam': 'Albino', 'body': ('#ece4e0', ALBINO), 'pidgeot:body': ('#a8a0a0', ALBINO), 'cream': '#f4f0ec'},
            {'naam': 'Kardinaal', 'body': ('#b01818', {'h': 0}), 'crest': '#2c2c34'},
            {'naam': 'Paradijsvogel', 'body': '#5a3a90', 'crest': '#30c0c0', 'cream': '#f0d040'},
        ],
    },
    'rattata': {
        'species': {
            'rattata': {'body': [7, 6, 5, 4]},
            'raticate': {'body': [12, 11, 10, 9]},
        },
        'variants': [
            {'naam': 'Witte labrat', 'body': '#ece8e4'},
            {'naam': 'Chinchilla', 'body': '#7a8498'},
            {'naam': 'Agouti', 'body': '#b06030'},
            {'naam': 'Naakte molrat', 'body': '#f0b0b0'},
            {'naam': 'Fancy rat (oranje)', 'body': '#e09040'},
            {'naam': 'Gouden rat (dierenriem)', 'body': '#d8a828'},
        ],
    },
    'rattata_alola': {
        # Alola-Rattata/Raticate: stadsratten van de maffia
        'species': {
            'rattata/alola': {'body': [1, 2, 4]},
            'raticate/alola': {'body': [1, 3, 6]},
        },
        'variants': [
            {'naam': 'Rioolgrijs', 'body': '#7a7a84'},
            {'naam': 'Krijtstreep (maffiapaars)', 'body': '#5a3a78'},
            {'naam': 'Kastanje', 'body': '#7a3028'},
            {'naam': 'Nachtblauw', 'body': '#2c3a68'},
            {'naam': 'Riool-mutant (TMNT-groen)', 'body': '#4a8030'},
            {'naam': 'Wit-goud (de Peetvader)', 'body': '#e4e0d8', 'raticate/alola:body': '#d8a828'},
        ],
    },
    # --- groep 20 (Kanto) ---
    'spearow': {
        'species': {
            'spearow': {'body': [9, 8, 7, 6], 'red': [14, 13, 12, 11, 10]},
            'fearow': {'body': [6, 5, 4, 3], 'red': [11, 10, 9, 8, 7]},
        },
        'variants': [
            {'naam': 'Torenvalk', 'body': '#a05828', 'red': '#7088a8'},
            {'naam': 'Bonte specht', 'body': ('#2c2c34', {'l': 1.3}), 'red': '#c02828'},
            {'naam': 'Vlaamse gaai', 'body': '#c0a090', 'red': '#3a70c0'},
            {'naam': 'Albino', 'body': ('#d8d0cc', {'l': 1.3}), 'red': '#f0c8c8'},
            {'naam': 'Groene specht', 'body': '#4a8a40', 'red': '#c02828'},
            {'naam': 'Kroonkraanvogel', 'body': '#3a3a48', 'red': '#e0b030'},
        ],
    },
    'nidoran_f': {
        'species': {
            'nidoran_f': {'body': [5, 4, 3, 2], 'spots': [8, 10]},
            'nidorina': {'body': [14, 13, 12, 11], 'spots': [6, 5, 4]},
            'nidoqueen': {'body': [14, 13, 12, 11]},
        },
        'variants': [
            {'naam': 'Mint', 'body': '#80d0b0', 'spots': '#3060a0'},
            {'naam': 'Zand (woestijnkonijn)', 'body': '#d0b080', 'spots': '#7a5030'},
            {'naam': 'Koraal', 'body': '#e06050', 'spots': '#f0d040'},
            {'naam': 'Albino', 'body': ('#ece4e8', ALBINO), 'spots': '#e0b0c0'},
            {'naam': 'Zwart', 'body': ('#34343c', {'l': 1.3}), 'spots': '#e04080'},
            {'naam': 'Koningin (goud)', 'body': '#d8a828', 'spots': '#7040a0'},
        ],
    },
    'nidoran_m': {
        'species': {
            'nidoran_m': {'body': [13, 12, 11, 10], 'spots': [8, 7]},
            'nidorino': {'body': [13, 12, 11, 10], 'spots': [7, 6]},
            'nidoking': {'body': [14, 13, 12, 11], 'spots': [10, 9, 8]},
        },
        'variants': [
            {'naam': 'Oranje gif', 'body': '#e08030', 'spots': '#3a3a48'},
            {'naam': 'Groen', 'body': '#50a050', 'spots': '#f0d040'},
            {'naam': 'Grijze haas', 'body': '#8a8a90', 'spots': '#c02828'},
            {'naam': 'Albino', 'body': ('#ece4e8', ALBINO), 'spots': '#e0b0c0'},
            {'naam': 'Zwart', 'body': ('#34343c', {'l': 1.3}), 'spots': '#40c0e0'},
            {'naam': 'Koning (goud)', 'body': '#d8a828', 'spots': '#c02828'},
        ],
    },
    'clefairy': {
        'species': {
            'cleffa': {'body': [5, 1, 4, 3, 2]},
            'clefairy': {'body': [14, 13, 12, 11]},
            'clefable': {'body': [8, 7, 6, 4]},
        },
        'variants': [
            {'naam': 'Maanwit', 'body': '#ece8f0'},
            {'naam': 'Maansteen (lila)', 'body': '#c0a8e8'},
            {'naam': 'Mint', 'body': '#b0e8c8'},
            {'naam': 'Bloedmaan', 'body': '#b83828'},
            {'naam': 'Ruimte (nachtblauw)', 'body': '#384890'},
            {'naam': 'Volle maan (goud)', 'body': '#f0d060'},
        ],
    },
    'paras': {
        # Bug/Grass; paddenstoelen
        'species': {
            'paras': {'mushroom': [8, 7, 6], 'spots': [4, 5]},
            'parasect': {'mushroom': [9, 8, 7, 6, 11], 'spots': [5, 4]},
        },
        'variants': [
            {'naam': 'Eekhoorntjesbrood', 'mushroom': '#8a5a30', 'spots': '#e0d0a0'},
            {'naam': 'Amethistzwam', 'mushroom': '#8050b0', 'spots': '#e0d0f0'},
            {'naam': 'Cordyceps', 'mushroom': '#e09020', 'spots': '#f8f0c0'},
            {'naam': 'Groenplaatzwam', 'mushroom': '#60a040', 'spots': '#f0f0d0'},
            {'naam': 'Indigo-melkzwam', 'mushroom': '#3060b0', 'spots': '#a0c8f0'},
            {'naam': 'Toad (Mario)', 'mushroom': '#f0f0f0', 'spots': '#d02828'},
        ],
    },
    'diglett': {
        # mollen; Alola-haar blijft blond
        'species': {
            'diglett': {'body': [15, 14, 13, 12], 'nose': [4, 3, 2, 5]},
            'dugtrio': {'body': [15, 14, 13, 12], 'nose': [4, 3, 2, 5]},
            'diglett/alola': {'body': [3, 1, 6, 5]},
            'dugtrio/alola': {'body': [4, 1, 5, 3, 15], 'hair': [2, 11], 'nose': [10, 9, 8], '_base': {'body': 4}},
        },
        'variants': [
            {'naam': 'Sterneusmol / Ziggy Stardust', 'body': ('#34343c', {'l': 1.3}), 'nose': '#f090b0', 'hair': '#e04820'},
            {'naam': 'Gouden mol / Gorillaz', 'body': ('#c89030', {'h': 0}), 'nose': '#4a3a48', 'hair': '#3050c0'},
            {'naam': 'Mol (grijs) / Billie Eilish', 'body': '#7a7a80', 'nose': '#f0a0c0', 'hair': '#80e040'},
            {'naam': 'Albino / emo', 'body': ('#ece4e0', ALBINO), 'nose': '#f08090', 'hair': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Naakte molrat / Nicki Minaj', 'body': '#f0b0a8', 'nose': '#c03040', 'hair': '#f060b0'},
            {'naam': 'Amethistgrond / Billy Idol', 'body': '#9070c8', 'nose': '#f0d040', 'hair': '#f0f0f8'},
        ],
    },
    'meowth': {
        # katten (Galar-Meowth/Perrserker: moderne sprites, nog niet)
        'species': {
            'meowth': {'body': [15, 14, 13, 12], 'ears': [11, 10, 9]},
            'persian': {'body': [15, 14, 13, 12, 11], 'gem': [6, 5, 4]},
        },
        'variants': [
            {'naam': 'Blauwe Rus', 'body': '#7a8498', 'ears': '#4a5060', 'gem': '#e0b030'},
            {'naam': 'Zwarte kat', 'body': ('#34343c', {'l': 1.3}), 'gem': '#40c060'},
            {'naam': 'Lilac (lila kat)', 'body': '#b0a0c0', 'ears': '#6a5080', 'gem': '#40b0c0'},
            {'naam': 'Havana Brown (chocolade)', 'body': '#6a4030', 'ears': '#3a2018', 'gem': '#40b0c0'},
            {'naam': 'Sphynx', 'body': '#e8b0a8'},
            {'naam': 'Maneki-neko (wit, rode oren, gouden munt)', 'body': '#f4f0ec', 'ears': '#c02828', 'gem': '#e0b030'},
        ],
    },
    'meowth_alola': {
        # Alola-Meowth/Persian: eigen kattenreeks, los van Kanto
        'species': {
            'meowth/alola': {'body': [6, 3, 1]},
            'persian/alola': {'body': [6, 7, 2, 13, 14], 'eyes': [8, 10, 11]},
        },
        'variants': [
            {'naam': 'Rode Abessijn', 'body': '#b06838', 'eyes': '#40b060'},
            {'naam': 'Lila Burmees', 'body': '#a890b0', 'eyes': '#f0c030'},
            {'naam': 'Witte Turkse Angora', 'body': ('#c8c4c0', {'l': 1.2}), 'eyes': '#3080e0'},
            {'naam': 'Bombay (zwart, gouden ogen)', 'body': ('#2c2c34', {'l': 1.3}), 'eyes': '#f0c030'},
            {'naam': 'Bengaal (goud)', 'body': '#c89040', 'eyes': '#40c080'},
            {'naam': 'Cheshire Cat', 'body': '#b050a8', 'eyes': '#f0e040'},
        ],
    },
    'mankey': {
        # apen (Annihilape: moderne sprite, nog niet)
        'species': {
            'mankey': {'body': [15, 14, 13, 12], 'brown': [11, 10, 9, 8], 'nose': [5, 6, 4]},
            'primeape': {'body': [15, 14, 13, 12], 'brown': [10, 9, 8, 7], 'nose': [5, 6]},
        },
        'variants': [
            {'naam': 'Japanse makaak', 'body': ('#a8a098', {'h': 0}), 'brown': '#c04848', 'nose': '#e07070'},
            {'naam': 'Gouden stompneusaap', 'body': ('#e0b040', {'h': 0}), 'brown': '#5a7090', 'nose': '#8098b8'},
            {'naam': 'Gorilla', 'body': ('#3a3a40', {'l': 1.3, 'h': 0}), 'brown': '#5a5a60', 'nose': '#8a8a94'},
            {'naam': 'Albino', 'body': ('#ece8e0', {'l': 1.0, 'h': 0}), 'brown': '#f0c8c0', 'nose': '#f0a0a8'},
            {'naam': 'Mandril', 'body': ('#6a7080', {'h': 0}), 'brown': '#c03030', 'nose': '#3060c0'},
            {'naam': 'Sun Wukong (Apenkoning)', 'body': ('#e8c050', {'h': 0}), 'brown': '#c02828', 'nose': '#e05030'},
        ],
    },
    'growlithe': {
        # honden (Hisui-vormen: moderne sprites, nog niet)
        'species': {
            'growlithe': {'body': [14, 13, 12, 11], 'mane': [10, 9, 8, 7]},
            'arcanine': {'body': [14, 13, 12, 11], 'mane': [10, 9, 8, 7, 6]},
        },
        'variants': [
            {'naam': 'Dobermann', 'body': ('#34343c', {'l': 1.3}), 'mane': '#c06020'},
            {'naam': 'Husky', 'body': '#7a8090', 'mane': '#f0f0f0'},
            {'naam': 'Blauwe chow chow', 'body': '#3a4870', 'mane': '#a0b0d0'},
            {'naam': 'Albino', 'body': ('#ece4e0', ALBINO), 'mane': '#f8f4f0'},
            {'naam': 'Foo-hond (groen en goud)', 'body': '#3a8a60', 'mane': '#e0b030'},
            {'naam': 'Blauw vuur', 'body': '#3070d0', 'mane': '#e8f0f8'},
        ],
    },
    # --- groep 21 (Kanto) ---
    'bellsprout': {
        # bekerplanten
        'species': {
            'bellsprout': {'body': [13, 14], 'leaves': [9, 10, 11, 12], 'lips': [5, 6, 7, 8]},
            'weepinbell': {'body': [5, 6, 7, 4, 3], 'leaves': [12, 13, 14, 15], 'lips': [8, 9, 10, 11]},
            'victreebel': {'body': [6, 7, 8, 5, 4], 'leaves': [12, 13, 14, 15], 'lips': [9, 10, 11]},
        },
        'variants': [
            {'naam': 'Rode Nepenthes (gele bladeren)', 'body': '#c04030', 'leaves': '#c8c040'},
            {'naam': 'Venusvliegenval', 'body': '#80b040', 'leaves': '#40802a', 'lips': '#e02020'},
            {'naam': 'Paarse bekerplant (herfstblad)', 'body': '#8050a0', 'leaves': '#d08030'},
            {'naam': 'Sakura (wit met roze bloesem)', 'body': '#f0ece8', 'leaves': '#f0a0c0', 'lips': '#c03040'},
            {'naam': 'Zwarte bekerplant (bloedrood blad)', 'body': ('#3a3038', {'l': 1.3}), 'leaves': '#8a1830'},
            {'naam': 'Glasplant (bladgoud)', 'body': '#80c0e0', 'lips': '#3060c0', 'leaves': '#e0b030'},
        ],
    },
    'ponyta': {
        # Galar-vormen (moderne sprites) nog niet
        'species': {
            'ponyta': {'body': [7, 6, 5, 4, 3], 'flames': [9, 10, 11], 'edge': [8]},
            'rapidash': {'body': [7, 6, 5, 4, 3], 'flames': [9, 10, 11], 'edge': [8]},
        },
        'variants': [
            {'naam': 'Vos (bruin paard, groen vuur)', 'body': '#9a6040', 'flames': '#40c060', 'edge': '#208038'},
            {'naam': 'Schimmel (grijs paard, paars vuur)', 'body': '#a0a0b0', 'flames': '#a050e0', 'edge': '#6020a0'},
            {'naam': 'Zwart paard met wit vuur', 'body': ('#3a3038', {'l': 1.3}), 'flames': '#f0f0f8', 'edge': '#8890b8'},
            {'naam': 'Wit paard met bloedrood vuur', 'body': ('#c8c4c0', {'l': 1.2}), 'flames': ('#c01818', {'h': 0}), 'edge': '#700810'},
            {'naam': 'Spookpaard (blauwschimmel, spookvuur)', 'body': '#6a7898', 'flames': '#a0f0f0', 'edge': '#3090b0'},
            {'naam': 'Gouden paard (Sleipnir)', 'body': '#d8a828', 'flames': '#f0f0f8', 'edge': '#8890b8'},
        ],
    },
    'slowpoke': {
        # Galar-vormen (moderne sprites) nog niet
        'species': {
            'slowpoke': {'body': [13, 12, 11, 10, 9]},
            'slowbro': {'body': [14, 13, 12, 11]},
            'slowking': {'body': [5, 8, 7, 9]},
        },
        'variants': [
            {'naam': 'Blauw', 'body': '#6090d0'},
            {'naam': 'Mint', 'body': '#80d0b0'},
            {'naam': 'Luiaard-bruin', 'body': '#8a6a48'},
            {'naam': 'Albino', 'body': ('#ece4e4', ALBINO)},
            {'naam': 'Oranje', 'body': '#e08040'},
            {'naam': 'Hipster (zwart)', 'body': ('#3a3a42', {'l': 1.3})},
        ],
    },
    'shellder': {
        'species': {
            'shellder': {'shell': [5, 4, 3, 2, 1], 'tongue': [6, 7, 8]},
            'cloyster': {'shell': [5, 4, 2, 1, 3], 'head': [12, 11, 10, 13]},
        },
        'variants': [
            {'naam': 'Abalone', 'shell': '#3a8a90', 'tongue': '#f0a060', 'head': '#d8c0a0'},
            {'naam': 'Mossel (oranje vlees)', 'shell': '#2c3a58', 'tongue': '#f0a040', 'head': '#e8a850'},
            {'naam': 'Kokkel', 'shell': '#d8c098', 'tongue': '#c05030', 'head': '#7a6a5a'},
            {'naam': 'Parelmoer', 'shell': '#ecdce8', 'tongue': '#c080d0', 'head': '#a0a8c8'},
            {'naam': 'Groenlipmossel', 'shell': '#40a070', 'tongue': '#f0d060', 'head': '#3a7058'},
            {'naam': 'Gouden parel', 'shell': '#d8a828', 'tongue': '#c02848', 'head': '#f0ece0'},
        ],
    },
    'onix': {
        'species': {
            'onix': {'body': [15, 14, 13, 12, 11, 10]},
            'steelix': {'body': [6, 2, 1, 5, 4]},
        },
        'variants': [
            {'naam': 'Zandsteen / brons', 'body': '#c8a068', 'steelix:body': '#8a5030'},
            {'naam': 'Basalt / gunmetal', 'body': ('#3a3a44', {'l': 1.3})},
            {'naam': 'Kristallen Onix/Steelix (anime)', 'body': '#a0e0f0', 'steelix:body': '#90c8e8'},
            {'naam': 'Kwarts / chroom', 'body': '#d8e0f0', 'steelix:body': '#c8ccd8'},
            {'naam': 'Lava / roest', 'body': '#a03020', 'steelix:body': '#904020'},
            {'naam': 'Goud / roségoud', 'body': '#d8a828', 'steelix:body': '#d89890'},
        ],
    },
    'krabby': {
        'species': {
            'krabby': {'shell': [14, 13, 12, 11], 'cream': [8, 7, 6, 5, 4]},
            'kingler': {'shell': [4, 3, 2, 1], 'cream': [8, 7, 6, 5]},
        },
        'variants': [
            {'naam': 'Blauwe zwemkrab', 'shell': '#3070c0'},
            {'naam': 'Turkoois', 'shell': '#30a0a0'},
            {'naam': 'Kokoskrab', 'shell': '#7040a0'},
            {'naam': 'Albino', 'shell': ('#c8c0bc', {'l': 1.4})},
            {'naam': 'Zwarte krab', 'shell': ('#34343c', {'l': 1.3})},
            {'naam': 'Gouden krab', 'shell': '#d8a828'},
        ],
    },
    'exeggcute': {
        'species': {
            'exeggcute': {'eggs': [15, 14, 13, 12, 11]},
            'exeggutor': {'leaves': [12, 11, 10, 9], 'eggs': [5, 4, 3, 2, 1], 'trunk': [7, 6, 8]},
            'exeggutor/alola': {'leaves': [13, 11, 14, 15], 'trunk': [4, 3, 1]},
        },
        'variants': [
            {'naam': 'Kersenbloesem (kersenbast)', 'eggs': '#f0c080', 'leaves': '#f0a0c0', 'trunk': '#5a3a40'},
            {'naam': 'Paaseieren (rieten mand)', 'eggs': '#90c8f0', 'leaves': '#80d0a0', 'trunk': '#c09060'},
            {'naam': 'Dinosaurusei (cycas)', 'eggs': '#a0c890', 'leaves': '#3a7040', 'trunk': '#6a6a50'},
            {'naam': 'Albino (berkenstam)', 'eggs': ('#ece8e4', ALBINO), 'leaves': '#c8d8c0', 'trunk': ('#d0c8c0', ALBINO)},
            {'naam': 'Sneeuwpalm (berijpt)', 'eggs': '#e8f0f8', 'leaves': '#a0c8e0', 'trunk': '#8a98a8'},
            {'naam': 'Fabergé (blauw email)', 'eggs': '#c02848', 'leaves': '#e0b030', 'trunk': '#3050a0'},
        ],
    },
    'cubone': {
        # Alola-Marowak (moderne sprite) nog niet
        'species': {
            'cubone': {'body': [4, 3, 2], 'bones': [7, 5, 6, 8]},
            'marowak': {'body': [15, 14, 13], 'bones': [3, 1, 2, 4]},
        },
        'variants': [
            {'naam': 'Blauw met suikerschedel (roze)', 'body': '#4870c0', 'bones': '#f0b8d0'},
            {'naam': 'Rouwgrijs met zwarte schedel', 'body': '#7a7a80', 'bones': ('#3a3a42', {'l': 1.3})},
            {'naam': 'Paars met turkoois calavera', 'body': '#7050a0', 'bones': '#90d8e8'},
            {'naam': 'Roze met mint calavera', 'body': '#e090a0', 'bones': '#90e0b0'},
            {'naam': 'Spook (zwart, lichtgevend skelet)', 'body': ('#34343c', {'l': 1.3}), 'bones': '#a8f070'},
            {'naam': 'Farao (goud met gouden masker)', 'body': ('#c89820', {'h': 0}), 'bones': '#f0d060'},
        ],
    },
    # --- groep 22 (Kanto/Johto) ---
    'tyrogue': {
        # vechtsporters
        'species': {
            'tyrogue': {'body': [2, 1, 3, 4]},
            'hitmonlee': {'body': [5, 4, 3, 2, 1]},
            'hitmonchan': {'body': [5, 4, 3], 'gear': [10, 9, 8, 7]},
            'hitmontop': {'body': [5, 4, 3, 2], 'gear': [9, 8, 7, 6]},
        },
        'variants': [
            {'naam': 'Bruce Lee', 'body': ('#e8c020', {'h': 0}), 'gear': '#2c2c34'},
            {'naam': 'Karate-gi', 'body': '#ece8e0', 'gear': '#c02828'},
            {'naam': 'Luchador', 'body': '#4070c0', 'gear': '#e050a0'},
            {'naam': 'Shaolin', 'body': '#e08030', 'gear': '#c8a030'},
            {'naam': 'Ninja', 'body': ('#34343c', {'l': 1.3}), 'gear': '#5070c0'},
            {'naam': 'Kampioensgordel (rood met goud)', 'body': ('#b02020', {'h': 0}), 'gear': '#e0b030'},
        ],
    },
    'lickitung': {
        'species': {
            'lickitung': {'body': [14, 13, 12, 11, 10], 'belly': [5, 4, 3], 'tongue': [7, 8, 6, 9]},
            'lickilicky': {'body': [6, 1, 2, 4, 3], 'tongue': [9, 10, 11]},
        },
        'variants': [
            {'naam': 'Kauwgomblauw (roze kauwgomtong)', 'body': '#70a0e0', 'tongue': '#f0a0d0'},
            {'naam': 'Pad (groen, blauwe snoeptong)', 'body': '#60a050', 'tongue': '#4090f0'},
            {'naam': 'Druif (zure-appeltong)', 'body': '#8060b0', 'tongue': '#90e060'},
            {'naam': 'Perzik (druivensnoeptong)', 'body': '#f0a070', 'tongue': '#a050d0'},
            {'naam': 'Venom (zwart)', 'body': ('#34343c', {'l': 1.3}), 'tongue': '#f04060'},
            {'naam': 'Mint-chocolade (citroentong)', 'body': '#80d0b0', 'belly': '#6a4030', 'tongue': '#f0d040'},
        ],
    },
    'happiny': {
        'species': {
            'happiny': {'body': [1, 2, 3]},
            'chansey': {'body': [15, 14, 13, 12, 11], 'egg': [2, 1, 3, 4]},
            'blissey': {'body': [1, 2, 6, 5, 3]},
        },
        'variants': [
            {'naam': 'Lavendel (eendenei)', 'body': '#c0a8e0', 'egg': '#a8d8f0'},
            {'naam': 'Citroen (century egg)', 'body': '#f0e890', 'egg': '#5a4028'},
            {'naam': 'Perzik (groen paasei)', 'body': '#f8c8a0', 'egg': '#90d080'},
            {'naam': 'Hemelsblauw (kwartelei)', 'body': '#90c0f0', 'egg': '#c8b090'},
            {'naam': 'Kers (Fabergé-ei)', 'body': '#d04050', 'egg': '#e0b030'},
            {'naam': 'Pruim (drakenei)', 'body': '#5a3a6a', 'egg': '#d04040'},
        ],
    },
    'tangela': {
        'species': {
            'tangela': {'vines': [4, 3, 2, 1]},
            'tangrowth': {'vines': [4, 5, 7, 6]},
        },
        'variants': [
            {'naam': 'Herfstranken', 'vines': '#c05828'},
            {'naam': 'Blauweregen', 'vines': '#8060c0'},
            {'naam': 'Zwarte ranken', 'vines': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Spaghetti', 'vines': '#e8d8a8'},
            {'naam': 'Bougainville', 'vines': '#e060a0'},
            {'naam': 'Gouden ranken', 'vines': '#d8a828'},
        ],
    },
    'kangaskhan': {
        'species': {'kangaskhan': {'body': [10, 1, 9, 12], 'belly': [5, 4], 'plates': [3, 2]}},
        'variants': [
            {'naam': 'Rode reuzenkangoeroe', 'body': '#b84830', 'belly': '#f0d8b0', 'plates': '#5a3a30'},
            {'naam': 'Panda-kangoeroe', 'body': ('#3a3a40', {'l': 1.3}), 'belly': '#f0f0f0', 'plates': '#e8e8ec'},
            {'naam': 'Boomkangoeroe (rood met goud)', 'body': '#8a3a20', 'belly': '#f0c040', 'plates': '#e0a030'},
            {'naam': 'Albino', 'body': ('#ece4e0', ALBINO), 'belly': '#f8f0e8', 'plates': '#e0d0d0'},
            {'naam': 'Boxing kangaroo (groen en goud)', 'body': ('#d8a828', {'h': 0}), 'belly': '#f0e0a0', 'plates': '#2c8a40'},
            {'naam': 'Kosmisch', 'body': '#4a3a80', 'belly': '#f0c0f0', 'plates': '#f0d040'},
        ],
    },
    'mr_mime': {
        # Galar-Mr. Mime/Mr. Rime (moderne sprites) nog niet
        'species': {
            'mime_jr': {'blue': [6, 7, 8], 'pink': [9, 12, 11, 10]},
            'mr_mime': {'blue': [1, 2, 3], 'pink': [12, 13, 11, 14]},
        },
        'variants': [
            {'naam': 'Pierrot', 'blue': ('#2c2c34', {'l': 1.3}), 'pink': '#ece8e8'},
            {'naam': 'Harlekijn', 'blue': '#c02828', 'pink': '#40a050'},
            {'naam': 'Paarse mime', 'blue': '#7040a0', 'pink': '#f0d040'},
            {'naam': 'Circusclown', 'blue': '#e08030', 'pink': '#f0e040'},
            {'naam': 'Barbie', 'blue': '#f080b0', 'pink': '#80c0f0'},
            {'naam': 'Pennywise (oranje haar, rood)', 'blue': '#e06020', 'pink': '#d02838'},
        ],
    },
    'scyther': {
        # bidsprinkhanen; Kleavor (moderne sprite) nog niet
        'species': {
            'scyther': {'body': [1, 8, 6, 2]},
            'scizor': {'body': [1, 4, 5, 2]},
        },
        'variants': [
            {'naam': 'Orchideebidsprinkhaan / Scizor paars', 'body': '#f0a0c0', 'scizor:body': '#7040a0'},
            {'naam': 'Bruine bidsprinkhaan / Scizor brons', 'body': '#8a6a40', 'scizor:body': '#c08040'},
            {'naam': 'Blauwe bidsprinkhaan / Scizor patina', 'body': '#3a70c0', 'scizor:body': '#30a0a0'},
            {'naam': 'Albino', 'body': ('#ece8e0', ALBINO)},
            {'naam': 'Ninja (zwart) / Scizor indigo', 'body': ('#34343c', {'l': 1.3}), 'scizor:body': ('#2c3a60', {'l': 1.3})},
            {'naam': 'Samoerai (goud) / Scizor zilver', 'body': '#d8a828', 'scizor:body': '#c8ccd8'},
        ],
    },
    'smoochum': {
        'species': {
            'smoochum': {'hair': [1, 3, 2, 15], 'dress': [5, 6, 8]},
            'jynx': {'hair': [1, 3, 2, 4], 'dress': [14, 13, 10, 11]},
        },
        'variants': [
            {'naam': 'Zomer (bruin haar, oranje jurk)', 'hair': '#7a5030', 'dress': '#e08030'},
            {'naam': 'Gothic', 'hair': ('#2c2c34', {'l': 1.3}), 'dress': '#5a2a70'},
            {'naam': 'Zeemeermin (rood haar, groene jurk)', 'hair': '#c03030', 'dress': '#30a070'},
            {'naam': 'Suikerspin (roze haar, wit)', 'hair': '#f0a0c0', 'dress': '#f0f0f0'},
            {'naam': 'IJskoningin (Elsa)', 'hair': '#e8f0f8', 'dress': '#80b8e8'},
            {'naam': 'Zilver en goud', 'hair': '#c8ccd8', 'dress': '#d8a828'},
        ],
    },
    'elekid': {
        'species': {
            'elekid': {'body': [4, 1, 3, 10]},
            'electabuzz': {'body': [5, 1, 4, 3]},
            'electivire': {'body': [7, 10, 6, 9]},
        },
        'variants': [
            {'naam': 'Blauwe bliksem', 'body': '#4080e0'},
            {'naam': 'Paarse tijger', 'body': '#9060c0'},
            {'naam': 'Radioactief groen', 'body': '#70c040'},
            {'naam': 'Witte tijger', 'body': '#ece8e0'},
            {'naam': 'Roze bliksem', 'body': '#e070b0'},
            {'naam': 'Zilver', 'body': '#c0c4d0'},
        ],
    },
    'magby': {
        'species': {
            'magby': {'red': [2, 1, 3], 'yellow': [11, 9, 10, 8]},
            'magmar': {'red': [8, 9, 6, 10], 'yellow': [1, 4, 3, 5]},
            'magmortar': {'red': [7, 5, 8, 6, 4], 'yellow': [1, 3, 2]},
        },
        'variants': [
            {'naam': 'Blauw vuur', 'red': '#3060d0', 'yellow': '#a0e0f8'},
            {'naam': 'Groen vuur', 'red': '#40a050', 'yellow': '#d0f080'},
            {'naam': 'Paars vuur', 'red': '#8040c0', 'yellow': '#f0a0f0'},
            {'naam': 'Witheet', 'red': '#f0e0c8', 'yellow': '#f8f8f0'},
            {'naam': 'Electabuzz-ruil', 'red': '#e0c030', 'yellow': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Obsidiaan met lava', 'red': ('#2c2830', {'l': 1.3}), 'yellow': '#f06020'},
        ],
    },
    # --- groep 23 (Kanto) ---
    'tauros': {
        # runderen (Paldea-vormen: eigen reeks)
        'species': {'tauros': {'body': [12, 14, 8, 13, 7], 'mane': [4, 6, 5, 9]}},
        'variants': [
            {'naam': 'Spaanse stier (zwart)', 'body': ('#3a3a40', {'l': 1.3})},
            {'naam': 'Brahmaan (wit)', 'body': '#e8e4dc'},
            {'naam': 'Schotse hooglander', 'body': '#b05028', 'mane': '#d89050'},
            {'naam': 'Bizon', 'body': '#5a3a28', 'mane': '#3a2818'},
            {'naam': 'Babe de blauwe os', 'body': '#4a70b0'},
            {'naam': 'Minotaurus', 'body': '#901818', 'mane': '#2c2c30'},
        ],
    },
    'lapras': {
        'species': {'lapras': {'body': [1, 4, 3, 5], 'shell': [11, 8, 12]}},
        'variants': [
            {'naam': 'Nessie (groen)', 'body': '#4a8a50'},
            {'naam': 'Walvisgrijs', 'body': '#7a8090'},
            {'naam': 'Roze', 'body': '#e8a0b0'},
            {'naam': 'Albino', 'body': ('#ece4e4', ALBINO), 'shell': '#e0d8d8'},
            {'naam': 'Orka', 'body': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Galjoen (goud)', 'body': '#d8a828', 'shell': '#8a5030'},
        ],
    },
    'ditto': {
        'species': {'ditto': {'body': [2, 1, 7, 4, 3, 5]}},
        'variants': [
            {'naam': 'Rode gelei', 'body': '#d03040'},
            {'naam': 'Groen slijm', 'body': '#60c050'},
            {'naam': 'Oranje', 'body': '#e08030'},
            {'naam': 'Wit', 'body': '#ece8f0'},
            {'naam': 'Venom (zwart)', 'body': ('#34343c', {'l': 1.3})},
            {'naam': 'Goud', 'body': ('#c89820', {'h': 0})},
        ],
    },
    'eevee': {
        # de Eeveelutions wisselen van kleur met elkaar (per soort een eigen ruil)
        'species': {
            'eevee': {'fur': [5, 2, 1, 3]},
            'vaporeon': {'body': [1, 2, 12, 10, 11]},
            'jolteon': {'fur': [2, 5, 4, 3, 7, 6]},
            'flareon': {'body': [4, 8, 7, 9]},
            'espeon': {'fur': [1, 4, 5, 2]},
            'umbreon': {'fur': [11, 1, 7, 2], 'rings': [4, 6, 5]},
            'leafeon': {'leaves': [1, 3, 2, 9]},
            'glaceon': {'body': [5, 8, 2, 3, 6, 7]},
            'sylveon': {'pink': [1, 10, 4, 7], 'blue': [2, 6, 5]},
        },
        'variants': [
            {'naam': 'Broerruil A', 'eevee:fur': '#4a70b0', 'vaporeon:body': '#e0c030', 'jolteon:fur': '#d84838',
             'flareon:body': '#3a80c0', 'espeon:fur': ('#34343c', {'l': 1.3}), 'umbreon:fur': '#b080b0', 'rings': '#e05090',
             'leaves': '#60a0d0', 'glaceon:body': '#70b060', 'pink': '#70c890', 'blue': '#f080a0'},
            {'naam': 'Broerruil B', 'eevee:fur': '#c8a0e0', 'vaporeon:body': '#d84838', 'jolteon:fur': '#3a80c0',
             'flareon:body': '#3a9a60', 'espeon:fur': '#d84838', 'umbreon:fur': '#3a4880', 'rings': '#70e0f0',
             'leaves': '#b080b0', 'glaceon:body': '#f090b0', 'pink': ('#34343c', {'l': 1.3}), 'blue': '#f0d040'},
            {'naam': 'Schaduw', 'eevee:fur': ('#34343c', {'l': 1.3}), 'vaporeon:body': ('#34343c', {'l': 1.3}), 'jolteon:fur': ('#34343c', {'l': 1.3}),
             'flareon:body': ('#34343c', {'l': 1.3}), 'espeon:fur': ('#34343c', {'l': 1.3}), 'rings': '#d03030',
             'leaves': ('#34343c', {'l': 1.3}), 'glaceon:body': ('#34343c', {'l': 1.3}), 'pink': ('#34343c', {'l': 1.3})},
            {'naam': 'Albino', 'eevee:fur': ('#ece4e0', ALBINO), 'vaporeon:body': ('#ece8ec', ALBINO), 'jolteon:fur': ('#c4bcb4', ALBINO),
             'flareon:body': ('#f0e8e4', ALBINO), 'espeon:fur': ('#f0e8f0', ALBINO), 'umbreon:fur': ('#b4b0b8', {'l': 1.5}), 'rings': '#f0c0c8',
             'leaves': ('#ece8e0', ALBINO), 'glaceon:body': ('#ecf0f4', ALBINO), 'pink': ('#f4ecf0', ALBINO), 'blue': '#f0c8d8'},
            {'naam': 'Sterrennacht', 'eevee:fur': '#283078', 'vaporeon:body': '#283078', 'jolteon:fur': '#283078', 'flareon:body': '#283078',
             'espeon:fur': '#283078', 'umbreon:fur': '#283078', 'rings': '#f0e070', 'leaves': '#283078', 'glaceon:body': '#283078',
             'pink': '#283078', 'blue': '#f0e070'},
            {'naam': 'Zilveren beeld (Eevee: goud)', 'eevee:fur': ('#c89820', {'h': 0}), 'vaporeon:body': '#b8bcc8', 'jolteon:fur': '#b8bcc8',
             'flareon:body': '#b8bcc8', 'espeon:fur': '#b8bcc8', 'umbreon:fur': '#8a8e98', 'rings': '#e8ecf4', 'leaves': '#b8bcc8',
             'glaceon:body': '#b8bcc8', 'pink': '#b8bcc8', 'blue': '#e0b030'},
        ],
    },
    'omanyte': {
        'species': {
            'omanyte': {'shell': [1, 2, 4, 3, 5], 'body': [8, 7, 10, 9]},
            'omastar': {'shell': [1, 5, 4, 2, 6], 'body': [8, 7, 10, 9]},
        },
        'variants': [
            {'naam': 'Nautilus', 'shell': '#e8e0d0', 'body': '#d08060'},
            {'naam': 'Opaalammoniet', 'shell': '#a0e0d0', 'body': '#e070b0'},
            {'naam': 'Twitch Plays (Game Boy-grijs, Lord Helix)', 'omanyte:palfile': 'gameboy.pal', 'omastar:palfile': 'gameboy.pal'},
            {'naam': 'Barnsteen', 'shell': '#d08020'},
            {'naam': 'Zwarte ammoniet', 'shell': ('#3a3038', {'l': 1.3}), 'body': '#c03040'},
            {'naam': 'Roze opaal', 'shell': '#e090c0', 'body': '#40d0e0'},
        ],
    },
    'kabuto': {
        'species': {
            'kabuto': {'shell': [5, 1, 6, 3, 2]},
            'kabutops': {'shell': [7, 9, 10, 8, 6], 'blades': [3, 12, 5, 1, 2]},
        },
        'variants': [
            {'naam': 'Keizerkrab (paars, jade zwaarden)', 'shell': '#7050a0', 'blades': '#a0e0d0'},
            {'naam': 'Trilobiet (grijs, roestrode zwaarden)', 'shell': '#7a7a80', 'blades': '#e07050'},
            {'naam': 'Blauw bloed (gouden zwaarden)', 'shell': '#3060a0', 'blades': '#f0d050'},
            {'naam': 'Zwart (rode zwaarden)', 'shell': ('#2c2c34', {'l': 1.3}), 'blades': '#d03030'},
            {'naam': 'Kabuto-helm (rood, zwarte zwaarden)', 'shell': '#a02020', 'blades': ('#3a3a44', {'l': 1.3})},
            {'naam': 'Gouden fossiel (zilveren zwaarden)', 'shell': ('#c89820', {'h': 0}), 'blades': '#d8e0e8'},
        ],
    },
    'aerodactyl': {
        'species': {'aerodactyl': {'body': [2, 1, 4, 3], 'wings': [5, 6, 7]}},
        'variants': [
            {'naam': 'Zandsteenfossiel', 'body': '#a08060', 'wings': '#d0a070'},
            {'naam': 'Jurassic-groen', 'body': '#5a8a50', 'wings': '#c05030'},
            {'naam': 'Quetzalcoatlus (rood)', 'body': '#a83830', 'wings': '#f0c040'},
            {'naam': 'Albino', 'body': ('#ece4e4', ALBINO), 'wings': '#f0c0c8'},
            {'naam': 'Zwarte draak', 'body': ('#34343c', {'l': 1.3}), 'wings': '#c02828'},
            {'naam': 'Barnsteen', 'body': '#d89020', 'wings': '#f0d070'},
        ],
    },
    'snorlax': {
        # de buik blijft
        'species': {
            'munchlax': {'body': [2, 1, 3, 5]},
            'snorlax': {'body': [15, 2, 4, 3, 6]},
        },
        'variants': [
            {'naam': 'Grizzly', 'body': '#7a5038'},
            {'naam': 'Panda', 'body': ('#34343c', {'l': 1.3}), 'mud': '#e8e8ec'},
            {'naam': 'IJsbeer', 'body': '#d8e4f0', 'mud': '#d8dce8'},
            {'naam': 'Totoro (grijs)', 'body': '#8a8a90'},
            {'naam': 'Kirby-honger (roze)', 'body': '#f090b0'},
            {'naam': 'Gouden beeld', 'body': ('#c89820', {'h': 0})},
        ],
    },
    # --- groep 24 (Kanto-legendaries, Dratini, Johto-starters) ---
    'articuno': {
        # de drie vogels dragen elkaars kleuren (Galar-vormen: moderne sprites, nog niet)
        'species': {'articuno': {'body': [6, 1, 3, 7, 4, 2]}},
        'variants': [
            {'naam': 'Zapdos-geel', 'body': '#f0c830'},
            {'naam': 'Moltres-rood', 'body': '#e05030'},
            {'naam': 'Smaragd', 'body': '#40b080'},
            {'naam': 'Sneeuwuil (wit)', 'body': ('#ecf0f4', ALBINO)},
            {'naam': 'Poolnacht', 'body': '#283078'},
            {'naam': 'Psychic-paars', 'body': '#8050c0'},
        ],
    },
    'zapdos': {
        'species': {'zapdos': {'body': [3, 1, 5, 7, 2], 'orange': [11, 10, 9]}},
        'variants': [
            {'naam': 'Articuno-blauw', 'body': '#4a90e0'},
            {'naam': 'Moltres-rood', 'body': '#e05030', 'orange': '#f0d040'},
            {'naam': 'Paarse bliksem', 'body': '#9060d0'},
            {'naam': 'Witte bliksem', 'body': '#ece8e0', 'orange': '#40a0f0'},
            {'naam': 'Stormvogel (zwart)', 'body': ('#34343c', {'l': 1.3}), 'orange': '#40e0f0'},
            {'naam': 'Thunderbird (totemrood met turkoois)', 'body': '#a04a30', 'orange': '#30a0c0'},
        ],
    },
    'moltres': {
        'species': {'moltres': {'body': [1, 2, 7, 8], 'yellow': [4, 6, 9]}},
        'variants': [
            {'naam': 'Articuno-blauw vuur', 'body': '#3070e0', 'yellow': '#a0e0f8'},
            {'naam': 'Zapdos-geel', 'body': '#f0c830', 'yellow': '#f8f0c0'},
            {'naam': 'Paars vuur', 'body': '#9040c0', 'yellow': '#f0a0f0'},
            {'naam': 'Zilvervuur', 'body': '#b8bcc8', 'yellow': '#f0f0f8'},
            {'naam': 'Zwarte feniks', 'body': ('#34343c', {'l': 1.3}), 'yellow': '#e02020'},
            {'naam': 'Groen vuur', 'body': '#40b050', 'yellow': '#d0f080'},
        ],
    },
    'dratini': {
        'species': {
            'dratini': {'body': [6, 5, 8, 7]},
            'dragonair': {'body': [5, 13, 6, 10, 7, 14, 9]},
            'dragonite': {'body': [7, 1, 3, 6, 5], 'wings': [12, 13, 14]},
        },
        'variants': [
            {'naam': 'Zeedraak (groen)', 'body': '#40a070', 'dragonite:body': '#40a0a0'},
            {'naam': 'Chinese draak (rood)', 'body': '#c03030', 'wings': '#e0b030'},
            {'naam': 'Paars', 'body': '#8050c0'},
            {'naam': 'Albino', 'body': ('#ece8e8', ALBINO), 'wings': '#f0c8c8'},
            {'naam': 'Zwart', 'body': ('#34343c', {'l': 1.3}), 'wings': '#c02828'},
            {'naam': 'Sterrenstelsel', 'body': '#283078', 'wings': '#f0e070'},
        ],
    },
    'mewtwo': {
        'species': {'mewtwo': {'body': [3, 1, 4, 2, 6], 'tail': [11, 7, 8, 10]}},
        'variants': [
            {'naam': 'Shadow Mewtwo', 'body': ('#3a3a44', {'l': 1.3}), 'tail': '#c02040'},
            {'naam': 'Smash Bros. blauw', 'body': '#c8d0f0', 'tail': '#3060d0'},
            {'naam': 'Smash Bros. rood', 'body': '#f0c8c8', 'tail': '#c03030'},
            {'naam': 'Smash Bros. groen', 'body': '#d0e8c8', 'tail': '#40a040'},
            {'naam': 'Mew-ruil (roze)', 'body': '#f8c8e0', 'tail': '#e070b0'},
            {'naam': 'Kristal', 'body': '#c0e0f0', 'tail': '#40b0d0'},
        ],
    },
    'mew': {
        'species': {'mew': {'body': [4, 1, 3, 5, 2]}},
        'variants': [
            {'naam': 'Mewtwo-paars', 'body': '#b0a0c8'},
            {'naam': 'Mint', 'body': '#a0e0c0'},
            {'naam': 'Citroen', 'body': '#f0e080'},
            {'naam': 'Wit', 'body': '#f0f0f4'},
            {'naam': 'Sterrennacht', 'body': '#283078'},
            {'naam': 'Ancient Mew (goud)', 'body': ('#c89820', {'h': 0})},
        ],
    },
    'chikorita': {
        # de Johto-starters dragen elkaars kleuren
        'species': {
            'chikorita': {'body': [10, 8, 9, 7], 'leaf': [2, 1, 4, 3]},
            'bayleef': {'body': [9, 8, 6, 7], 'leaf': [1, 2, 4, 3]},
            'meganium': {'body': [5, 4, 7, 6], 'petals': [11, 10, 13, 12]},
        },
        'variants': [
            {'naam': 'Cyndaquil-kleuren', 'body': '#3a5a7a', 'leaf': '#e04020', 'petals': '#f0c020'},
            {'naam': 'Totodile-kleuren', 'body': '#60a8e0', 'leaf': '#d04030', 'petals': '#f0d050'},
            {'naam': 'Torchic-kleuren', 'body': '#f0a050', 'leaf': '#f0d040', 'petals': '#f06030'},
            {'naam': 'Albino', 'body': ('#ece8e0', ALBINO), 'leaf': '#e0e8d8', 'petals': '#f0c8d0'},
            {'naam': 'Schaduw', 'body': ('#34343c', {'l': 1.3}), 'leaf': '#c02040', 'petals': '#c02040'},
            {'naam': 'Pokémon Crystal', 'body': '#a8d8f0', 'leaf': '#4080d0', 'petals': '#80e0f0'},
        ],
    },
    'cyndaquil': {
        'species': {
            'cyndaquil': {'back': [9, 4, 5, 3], 'flames': [1, 2, 6, 8]},
            'quilava': {'back': [15, 6, 5, 7], 'flames': [9, 1, 2, 4, 3]},
            'typhlosion': {'back': [6, 15, 5, 7], 'flames': [1, 2, 4, 3]},
        },
        'variants': [
            {'naam': 'Totodile-kleuren', 'back': '#3080c8', 'flames': ('#d03020', {'h': 0})},
            {'naam': 'Chikorita-kleuren', 'back': '#70a840', 'flames': '#80d040'},
            {'naam': 'Mudkip-kleuren', 'back': '#80c8f0', 'flames': '#f08030'},
            {'naam': 'Albino', 'back': ('#ece4e0', ALBINO), 'flames': '#f0c0a0'},
            {'naam': 'Schaduw', 'back': ('#34343c', {'l': 1.3}), 'flames': '#a050e0'},
            {'naam': 'Pokémon Crystal', 'back': '#a8d8f0', 'flames': '#4080f0'},
        ],
    },
    'totodile': {
        'species': {
            'totodile': {'blue': [2, 1, 3, 4], 'red': [9, 11, 10, 12]},
            'croconaw': {'blue': [6, 7, 8, 9], 'red': [1, 5, 4, 2, 11, 12]},
            'feraligatr': {'blue': [5, 7, 6, 8], 'red': [1, 4, 2]},
        },
        'variants': [
            {'naam': 'Chikorita-kleuren', 'blue': '#a0d070', 'red': '#408030'},
            {'naam': 'Cyndaquil-kleuren', 'blue': '#2c4870', 'red': '#f06020'},
            {'naam': 'Treecko-kleuren', 'blue': '#3a8a40', 'red': '#c02828'},
            {'naam': 'Albino', 'blue': ('#ece8e8', ALBINO), 'red': '#f0b0b0'},
            {'naam': 'Schaduw', 'blue': ('#34343c', {'l': 1.3}), 'red': '#40e0f0'},
            {'naam': 'Pokémon Crystal', 'blue': '#a8d8f0', 'red': '#4080d0'},
        ],
    },
    # --- groep 25 (Johto) ---
    'sentret': {
        'species': {
            'sentret': {'body': [12, 1, 3, 7, 11, 9, 8]},
            'furret': {'body': [1, 3, 6, 8, 7, 2, 5, 9]},
        },
        'variants': [
            {'naam': 'Zilverfret', 'body': '#6a6a74'},
            {'naam': 'Mangoest', 'body': '#b05828'},
            {'naam': 'Bunzing', 'body': ('#2c2c34', {'l': 1.3}), 'cream': '#f0ece4'},
            {'naam': 'Albino fret', 'body': ('#ece4e0', ALBINO), 'furret:body': ('#c8c0bc', ALBINO), 'cream': '#f4f0ec'},
            {'naam': 'Stokstaartje', 'body': '#c8a070'},
            {'naam': 'Gouden fret', 'body': ('#c89020', {'h': 0})},
        ],
    },
    'hoothoot': {
        'species': {
            'hoothoot': {'body': [5, 4, 6, 3], 'cream': [12, 13], 'eyes': [10, 9, 11, 8]},
            'noctowl': {'body': [6, 4, 1, 7], 'cream': [5, 3], 'eyes': [11]},
        },
        'variants': [
            {'naam': 'Kerkuil (zwarte ogen)', 'body': '#d8a060', 'cream': '#f8f0e8', 'eyes': ('#3a3038', {'l': 1.3})},
            {'naam': 'Kakapo (groen)', 'body': '#60a050', 'cream': '#e0d890', 'eyes': '#f0a020'},
            {'naam': 'Bosuil (rood, gele ogen)', 'body': '#a04830', 'eyes': '#f0d040'},
            {'naam': 'Sneeuwuil (gele ogen)', 'body': ('#c4c0bc', {'l': 1.3}), 'cream': '#f8f8f8', 'eyes': '#f0c820'},
            {'naam': 'Zwarte uil (blauwe ogen)', 'body': ('#34343c', {'l': 1.3}), 'eyes': '#40a0f0'},
            {'naam': 'Uil van Minerva (goud, groene ogen)', 'body': ('#c89020', {'h': 0}), 'eyes': '#40c070'},
        ],
    },
    'spinarak': {
        'species': {
            'spinarak': {'body': [2, 6, 4, 5], 'bands': [12, 9, 8]},
            'ariados': {'body': [8, 9, 10, 11], 'legs': [7, 5, 6], 'bands': [2, 4, 1]},
        },
        'variants': [
            {'naam': 'Zwarte weduwe', 'body': ('#2c2c34', {'l': 1.3}), 'legs': '#c02828', 'bands': '#e03030'},
            {'naam': 'Vogelspin', 'body': '#a06030', 'legs': '#e0a060', 'bands': '#f0e0c0'},
            {'naam': 'Pauwspin', 'body': '#3070d0', 'legs': '#f08030', 'bands': '#40d0f0'},
            {'naam': 'Albino grotspin', 'body': ('#ece4e0', ALBINO), 'legs': '#e0c8d0', 'bands': '#f0a0b0'},
            {'naam': 'Kruisspin', 'body': '#e0a030', 'legs': '#7a5030', 'bands': '#f0f0e0'},
            {'naam': 'Venom / Carnage', 'body': ('#2c2c34', {'l': 1.3}), 'legs': '#f0f0f0', 'bands': '#c02828'},
        ],
    },
    'mareep': {
        'species': {
            'mareep': {'wool': [5, 2, 8, 7], 'skin': [13, 12, 15, 14], 'orb': [4, 1, 11]},
            'flaaffy': {'body': [11, 7, 9, 8, 10], 'wool': [1, 4, 2, 3], 'orb': [14, 13, 12, 15]},
            'ampharos': {'body': [5, 4, 3, 7], 'orb': [8, 6, 13, 10, 14]},
        },
        'variants': [
            {'naam': 'Zwart schaap (rode bol)', 'wool': ('#3a3a42', {'l': 1.3}), 'body': ('#3a3a42', {'l': 1.3}), 'flaaffy:wool': '#9898a8',
             'skin': '#d8c8b8', 'orb': '#f04040'},
            {'naam': 'Vosschaap (oranje, blauwe bol)', 'wool': '#e8a060', 'body': '#e08040', 'flaaffy:wool': '#fff0e0', 'skin': '#5a3a20', 'orb': '#40c0f0'},
            {'naam': 'Elektrisch blauw (gele bol)', 'wool': '#a0c8f0', 'body': '#4080e0', 'skin': '#2c3a80', 'orb': '#f0e040'},
            {'naam': 'Groen (roze bol)', 'wool': '#b0e0a0', 'body': '#70c060', 'skin': '#2c6a40', 'orb': '#f060c0'},
            {'naam': 'Paars (mint bol)', 'wool': '#c0a8e8', 'body': '#a080d0', 'skin': '#4a2c80', 'orb': '#60f0a0'},
            {'naam': 'Gulden vlies (robijnen bol)', 'wool': ('#e0b030', {'h': 0}), 'body': ('#e0b030', {'h': 0}), 'ampharos:body': '#c07020',
             'flaaffy:wool': '#f8ecc0', 'skin': '#a06020', 'orb': '#e03030'},
        ],
    },
    'togepi': {
        'species': {
            'togepi': {'shell': [14, 10, 8], 'head': [6, 4, 3, 1, 5], 'red': [13, 12, 7], 'blue': [15, 11, 9]},
            'togetic': {'body': [4, 5, 2, 1], 'red': [6, 7], 'blue': [8, 9]},
            'togekiss': {'body': [1, 4, 2, 3], 'red': [8, 7, 11], 'blue': [6, 9, 12]},
        },
        'variants': [
            {'naam': 'Kinder Surprise (chocolade-ei)', 'shell': '#8a5a38', 'body': '#8a5a38', 'head': '#f8e8c0', 'red': '#e06020', 'blue': '#f0f0f0'},
            {'naam': 'Roze paasei (gele kop)', 'shell': '#f8b8d0', 'body': '#f8b8d0', 'head': '#f8f0a0', 'red': '#40b0e0', 'blue': '#80d060'},
            {'naam': 'Mint-chocolade-ijsje', 'shell': '#a8e8c8', 'body': '#a8e8c8', 'head': '#7a4a30', 'red': '#f06080', 'blue': ('#3a3048', {'l': 1.3})},
            {'naam': 'Nachtei (zwart met goud)', 'shell': ('#3a3a48', {'l': 1.3}), 'body': ('#3a3a48', {'l': 1.3}), 'head': '#d8c8f0', 'red': '#f0d040', 'blue': '#c040c0'},
            {'naam': 'Fabergé blauw', 'shell': '#80b0f0', 'body': '#80b0f0', 'head': '#f8f0e0', 'red': '#f0c040', 'blue': '#f0f0f0'},
            {'naam': 'Gouden zegen-ei', 'shell': '#e8c050', 'body': '#e8c050', 'head': '#f8f0d8', 'red': '#d02828', 'blue': '#2c70d0'},
        ],
    },
    'bonsly': {
        'species': {
            'bonsly': {'body': [7, 6, 8, 9], 'leaves': [1, 2, 4, 3]},
            'sudowoodo': {'body': [1, 5, 4, 10, 3], 'leaves': [6, 9, 8, 7]},
        },
        'variants': [
            {'naam': 'Kersenbloesem (kersenhout)', 'leaves': '#f0a0c0', 'body': '#5a3a40'},
            {'naam': 'Herfst (sequoia)', 'leaves': '#d07028', 'body': '#a05030'},
            {'naam': 'Berk (wit hout)', 'body': '#e8e4dc'},
            {'naam': 'Jeneverbesbonsai (zilverhout)', 'body': '#a8a8b0', 'leaves': '#2c8a70'},
            {'naam': 'Nachtsakura (zwart hout, paars blad)', 'leaves': '#8050c0', 'body': ('#2c2c3c', {'l': 1.3})},
            {'naam': 'Laurelin (gouden blad, zilveren stam)', 'leaves': ('#e0b030', {'h': 0}), 'body': '#c8c8d4'},
        ],
    },
    'hoppip': {
        'species': {
            'hoppip': {'body': [9, 6, 8, 7], 'leaves': [1, 3, 2, 4]},
            'skiploom': {'body': [11, 9, 8, 10], 'flower': [4, 3, 5, 13, 1, 14]},
            'jumpluff': {'body': [9, 10, 11, 12], 'cotton': [2, 4, 3, 5, 1], 'leaves': [8, 6]},
        },
        'variants': [
            {'naam': 'Lente (kersenbloesem)', 'body': '#98d070', 'leaves': '#f0a0c0', 'flower': '#f8c0d8', 'cotton': '#f0b8d0'},
            {'naam': 'Zomer (oranje met rode bloem)', 'body': '#f0a030', 'leaves': '#3a9a40', 'flower': '#f04030', 'cotton': '#e8d870'},
            {'naam': 'Herfst (roest met oranje blad)', 'body': '#a05030', 'leaves': '#e08020', 'flower': '#c03828', 'cotton': '#c8a060'},
            {'naam': 'Winter (sneeuw met ijsblauw)', 'body': ('#c8ccd8', {'l': 1.3}), 'leaves': '#80b8d8', 'flower': '#a8d8f0', 'cotton': '#c8d8f0'},
            {'naam': 'Lavendelveld', 'body': '#8a70c8', 'leaves': '#6a9a50', 'flower': '#c090e0', 'cotton': '#c8a8e8'},
            {'naam': 'Sterrennacht', 'body': '#283078', 'leaves': '#f0d040', 'flower': '#f0d040', 'cotton': '#8090d0'},
        ],
    },
    'aipom': {
        'species': {
            'aipom': {'body': [2, 1, 4, 3], 'face': [7, 8, 6, 12]},
            'ambipom': {'body': [8, 9, 11, 10], 'face': [5, 6, 7, 12], 'tips': [3, 2, 1]},
        },
        'variants': [
            {'naam': 'Kapucijnaap (wit gezicht)', 'body': '#7a5038', 'face': '#f0e4d8', 'tips': '#3a2a20'},
            {'naam': 'Goudleeuwaapje (donker gezicht)', 'body': '#e09030', 'face': '#6a4430', 'tips': '#f0c040'},
            {'naam': 'Langoer (grijs, zwart gezicht)', 'body': '#9a9aa0', 'face': ('#34343c', {'l': 1.3}), 'tips': '#f0f0f0'},
            {'naam': 'Albino', 'body': ('#ece4e0', ALBINO), 'face': '#f8d0c8', 'tips': '#f0a0a0'},
            {'naam': 'Groen (roze handen)', 'body': '#50a050', 'face': '#f0e8a0', 'tips': '#e05080'},
            {'naam': 'Abu (Aladdin, blauw vest, rode fez)', 'body': '#3a60c0', 'face': '#d8a070', 'tips': '#e03030'},
        ],
    },
    # --- groep 26 (Johto) ---
    'sunkern': {
        'species': {
            'sunkern': {'petals': [8, 7, 9], 'leaves': [3, 1, 4, 2]},
            'sunflora': {'petals': [4, 1, 5, 3, 6, 7], 'leaves': [12, 11, 13, 14]},
        },
        'variants': [
            {'naam': 'Velvet Queen (rode zonnebloem, aubergine blad)', 'petals': '#b03028', 'leaves': '#5a3048'},
            {'naam': 'Italiaanse witte (blauwgrijs blad)', 'petals': '#f0ece0', 'leaves': '#708898'},
            {'naam': 'Roze (herfstbruin blad)', 'petals': '#f080b0', 'leaves': '#a07040'},
            {'naam': 'Paars (goudgeel blad)', 'petals': '#8060c0', 'leaves': '#d0b030'},
            {'naam': 'Blauw (berijpt zilverblad)', 'petals': '#4a80d0', 'leaves': '#d0d4e0'},
            {'naam': 'Van Gogh (goud op blauw)', 'petals': '#e0a020', 'leaves': '#2848a0'},
        ],
    },
    'yanma': {
        'species': {
            'yanma': {'body': [5, 8, 6, 9, 4], 'green': [10, 12, 11, 13], 'tail': [14, 15]},
            'yanmega': {'body': [3, 1, 2], 'green': [10, 13, 12, 11]},
        },
        'variants': [
            {'naam': 'Blauwe glazenmaker', 'body': '#3070d0', 'green': '#203050', 'tail': '#5080d0'},
            {'naam': 'Keizerlibel (groen borststuk, blauw achterlijf)', 'body': '#40a050', 'green': '#2c5a90', 'tail': '#3a70b0'},
            {'naam': 'Paarse libel', 'body': '#8040b0', 'green': '#3a2850', 'tail': '#7040a0'},
            {'naam': 'Goudlibel', 'body': '#e0b030', 'green': '#5a4010', 'tail': '#c08020'},
            {'naam': 'Vuurjuffer (rood met zwart)', 'body': '#c02828', 'green': ('#2c2c34', {'l': 1.3}), 'tail': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Juffer (cyaan)', 'body': '#30c0c0', 'green': '#2c3a70', 'tail': '#30c0c0'},
        ],
    },
    'wooper': {
        # axolotls (Paldea-Wooper/Clodsire: moderne sprites, nog niet)
        'species': {
            'wooper': {'body': [12, 11, 4, 5, 7, 6], 'gills': [3, 1, 8, 2]},
            'quagsire': {'body': [1, 2, 3, 4]},
        },
        'variants': [
            {'naam': 'Wildtype (olijf)', 'body': '#6a7040', 'gills': '#a04060'},
            {'naam': 'Goudaxolotl', 'body': '#e8c060', 'gills': '#e06040'},
            {'naam': 'Melanistisch (zwart)', 'body': ('#3a3a44', {'l': 1.3}), 'gills': '#7a3a60'},
            {'naam': 'Albino', 'body': ('#f4ece8', ALBINO), 'gills': '#f08090'},
            {'naam': 'Koper', 'body': '#c07040', 'gills': '#f0a060'},
            {'naam': 'Lavendel', 'body': '#a090d8', 'quagsire:body': '#40b0a0', 'gills': '#f0a0e0'},
        ],
    },
    'murkrow': {
        # raven en kraaien; de snavel blijft
        'species': {
            'murkrow': {'body': [1, 4, 2, 8]},
            'honchkrow': {'body': [3, 2, 1]},
        },
        'variants': [
            {'naam': 'Witte raaf', 'body': '#e8e4e0', 'murkrow:body': ('#c8c4c8', {'l': 1.3})},
            {'naam': 'Turkoois', 'body': '#2c7a8a'},
            {'naam': 'Iriserend groen', 'body': '#2a5a40'},
            {'naam': 'Bonte kraai', 'body': '#7a7a84'},
            {'naam': 'Maffiabaas (wijnrood)', 'body': '#5a2030'},
            {'naam': 'Hugin (goud)', 'body': ('#c89020', {'h': 0})},
        ],
    },
    'misdreavus': {
        'species': {
            'misdreavus': {'body': [6, 7, 5, 8], 'hat': [4, 1, 3]},
            'mismagius': {'body': [7, 4, 6], 'hat': [2, 3, 1]},
        },
        'variants': [
            {'naam': 'Boo-blauw', 'body': '#4a70c0'},
            {'naam': 'Bloedrood', 'body': '#901828'},
            {'naam': 'Bleke geest', 'body': '#d8d8e8'},
            {'naam': 'Halloween', 'body': '#e07020', 'hat': '#3a2850'},
            {'naam': 'Zwart', 'body': ('#2c2c34', {'l': 1.3}), 'hat': '#c02848'},
            {'naam': 'Goud', 'body': ('#c89020', {'h': 0})},
        ],
    },
    'pineco': {
        'species': {
            'pineco': {'shell': [1, 2, 4, 3, 9]},
            'forretress': {'shell': [3, 1, 5, 2, 12], 'inner': [7, 6, 8, 10]},
        },
        'variants': [
            {'naam': 'Blauwspar (oranje binnenkant)', 'shell': '#6a88a8', 'inner': '#f08030'},
            {'naam': 'Verse kegel (groen, gele binnenkant)', 'shell': '#4a8a40', 'inner': '#e8c030'},
            {'naam': 'Roestijzer (turkoois binnenkant)', 'shell': '#904020', 'inner': '#30a0a0'},
            {'naam': 'Berijpt (blauwe binnenkant)', 'shell': ('#c8d0dc', {'l': 1.3}), 'inner': '#3070d0'},
            {'naam': 'Zwart staal (gloeiend groen)', 'shell': ('#3a3a44', {'l': 1.3}), 'inner': '#60e040'},
            {'naam': 'Goud (paarse binnenkant)', 'shell': ('#c89020', {'h': 0}), 'inner': '#8040c0'},
        ],
    },
    'gligar': {
        'species': {
            'gligar': {'body': [1, 5, 4, 2], 'wings': [9, 11, 10]},
            'gliscor': {'body': [3, 1, 5, 2, 4], 'wings': [13]},
        },
        'variants': [
            {'naam': 'Woestijnschorpioen (oranje vlies)', 'body': '#c8a060', 'wings': '#d06020'},
            {'naam': 'Groen (geel vlies)', 'body': '#50a050', 'wings': '#d0b020'},
            {'naam': 'Rood (zwart vlies)', 'body': '#b03030', 'wings': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Albino (roze vlies)', 'body': ('#ece4e8', ALBINO), 'wings': '#e0a0b0'},
            {'naam': 'Zwarte schorpioen (rood vlies)', 'body': ('#34343c', {'l': 1.3}), 'wings': '#a02020'},
            {'naam': 'Serket (turkoois, gouden vlies)', 'body': '#30a0a0', 'wings': '#d8a828'},
        ],
    },
    'snubbull': {
        'species': {
            'snubbull': {'body': [4, 3, 6, 7], 'dark': [2, 5], 'collar': [10, 11]},
            'granbull': {'body': [1, 3, 4, 2], 'dark': [9, 8]},
        },
        'variants': [
            {'naam': 'Engelse bulldog (wit, bruine vlekken)', 'body': '#ece8e4', 'dark': '#8a5a38', 'collar': '#c02828'},
            {'naam': 'Brindle (zwart, roze halsband)', 'body': '#8a6040', 'dark': ('#2c2c34', {'l': 1.3}), 'collar': '#f070b0'},
            {'naam': 'Zwart (wit, rode halsband)', 'body': ('#3a3a42', {'l': 1.3}), 'dark': '#e8e8ec', 'collar': '#e03030'},
            {'naam': 'Fawn (zwart masker)', 'body': '#d8b080', 'dark': ('#2c2c34', {'l': 1.3}), 'collar': '#3070d0'},
            {'naam': 'Blauwe Franse bulldog (wit, gele halsband)', 'body': '#7a8aa8', 'dark': '#f0f0f0', 'collar': '#f0c030'},
            {'naam': 'Goud (zwart, diamanten halsband)', 'body': ('#c89020', {'h': 0}), 'dark': ('#2c2c34', {'l': 1.3}), 'collar': '#d8f0f8'},
        ],
    },
    # --- groep 27 (Johto) ---
    'qwilfish': {
        # kogelvissen (Hisui-vorm/Overqwil nog niet)
        'species': {'qwilfish': {'body': [1, 5, 4, 2], 'spikes': [14, 13, 12, 11]}},
        'variants': [
            {'naam': 'Fugu', 'body': '#c8a050', 'spikes': '#7a5030'},
            {'naam': 'Koraalvis (rood)', 'body': '#c04040'},
            {'naam': 'Zee-egel (paars)', 'body': '#6a3a90', 'spikes': '#2c2c34'},
            {'naam': 'Albino', 'body': ('#ece4e4', ALBINO)},
            {'naam': 'Zwart', 'body': ('#2c2c34', {'l': 1.3}), 'spikes': '#f0d040'},
            {'naam': 'Mandarijnvis', 'body': '#e07030', 'spikes': '#3060c0'},
        ],
    },
    'sneasel': {
        # marters (Hisui-Sneasel/Sneasler nog niet)
        'species': {
            'sneasel': {'body': [3, 5, 6, 8], 'feather': [1, 2, 4, 14]},
            'weavile': {'body': [12, 10, 9, 11], 'feather': [2, 1, 3, 4]},
        },
        'variants': [
            {'naam': 'Hermelijn (winterwit)', 'body': '#e8ecf0'},
            {'naam': 'Marter (gele veer)', 'body': '#7a5038', 'feather': '#f0c030'},
            {'naam': 'Groen (oranje veer)', 'body': '#3a7a50', 'feather': '#f08030'},
            {'naam': 'Paars (turkooizen veer)', 'body': '#5a3a80', 'feather': '#30c0b0'},
            {'naam': 'Rood met zwarte veer', 'body': '#901828', 'feather': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Goud met blauwe veer', 'body': ('#c89020', {'h': 0}), 'feather': '#3060d0'},
        ],
    },
    'teddiursa': {
        # beren (Ursaluna: moderne sprite, nog niet)
        'species': {
            'teddiursa': {'body': [1, 2, 4, 3]},
            'ursaring': {'body': [3, 1, 2, 6]},
            'ursaluna': {'body': [4, 3, 1, 5], 'mud': [6, 10, 2]},
            'ursaluna/bloodmoon': {'body': [4, 1, 8], 'mud': [6, 12, 3]},
        },
        'variants': [
            {'naam': 'IJsbeer', 'body': '#ece8e4', 'ursaring:body': ('#c4c0b8', {'l': 1.3})},
            {'naam': 'Panda', 'body': ('#3a3a42', {'l': 1.3})},
            {'naam': 'Blauwe beer', 'body': '#5070b0', 'mud': '#40507a'},
            {'naam': 'Grizzly (grijs)', 'body': '#8a8070', 'mud': '#8a7a60'},
            {'naam': 'Troetelbeer (roze)', 'body': '#f0a0c0', 'mud': '#f8d0e0'},
            {'naam': 'Winnie de Poeh', 'body': ('#e0b030', {'h': 0}), 'mud': '#c02828'},
        ],
    },
    'swinub': {
        'species': {
            'swinub': {'body': [6, 1, 3, 2, 5]},
            'piloswine': {'body': [2, 14, 1, 5, 4, 3], '_base': {'body': 4}},
            'mamoswine': {'body': [3, 1, 2]},
        },
        'variants': [
            {'naam': 'Sneeuwzwijn', 'body': '#e0dcd4', 'mamoswine:body': ('#bcb8b0', {'l': 1.4})},
            {'naam': 'Duroc (rood)', 'body': '#a05030'},
            {'naam': 'Wild zwijn (zwart)', 'body': ('#3a3a40', {'l': 1.3})},
            {'naam': 'Wolharige neushoorn (grijs)', 'body': '#8a8a90'},
            {'naam': 'Hangbuikzwijn (roze)', 'body': '#e0a0a0'},
            {'naam': 'Goud', 'body': ('#c89020', {'h': 0})},
        ],
    },
    'delibird': {
        'species': {'delibird': {'red': [12, 7, 6, 13], 'white': [11, 3, 5]}},
        'variants': [
            {'naam': 'IJsblauw (lichtblauw pak)', 'red': '#3060c0', 'white': '#c8e4f8'},
            {'naam': 'Kerstelf (groen met goud)', 'red': '#30a050', 'white': '#f0dc90'},
            {'naam': 'Paars (lila)', 'red': '#7040a0', 'white': '#f0d8f4'},
            {'naam': 'Pinguïn (zwart-wit)', 'red': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Roze (vanille)', 'red': '#e070a0', 'white': '#f8f0c0'},
            {'naam': 'Goud (zwart pak)', 'red': ('#c89020', {'h': 0}), 'white': ('#4a4a58', {'l': 1.3})},
        ],
    },
    'mantyke': {
        # roggen
        'species': {
            'mantyke': {'body': [14, 1, 5, 3, 2], 'belly': [10, 7, 11, 15]},
            'mantine': {'body': [2, 4, 3, 7], 'belly': [6, 5, 9]},
        },
        'variants': [
            {'naam': 'Gevlekte adelaarsrog (zwart, witte buik)', 'body': ('#2c2c34', {'l': 1.3}), 'belly': '#e8ecf0'},
            {'naam': 'Pijlstaartrog (zand, roze buik)', 'body': '#c8a878', 'belly': '#f0c8c8'},
            {'naam': 'Groen (gele buik)', 'body': '#3a7a60', 'belly': '#e8e0a0'},
            {'naam': 'Roze (lila buik)', 'body': '#d080a0', 'belly': '#d0c0f0'},
            {'naam': 'Rood (oranje buik)', 'body': '#a02830', 'belly': '#f0b070'},
            {'naam': 'Goud (blauwe buik)', 'body': ('#c89020', {'h': 0}), 'belly': '#90c0f0'},
        ],
    },
    'houndour': {
        # hellehonden: de zwarte vacht krijgt een kleur
        'species': {
            'houndour': {'body': [1, 2, 3], 'bone': [4, 8]},
            'houndoom': {'body': [6, 7, 8], 'bone': [3, 2, 1]},
        },
        'variants': [
            {'naam': 'Witte hellehond (zwarte hoorns)', 'body': '#a8a8b8', 'bone': ('#3a3a44', {'l': 1.3})},
            {'naam': 'Bloedrood (zwarte hoorns)', 'body': '#6a1818', 'bone': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Dobermann (bruin, roestrode hoorns)', 'body': '#5a3820', 'bone': '#c06838'},
            {'naam': 'Paars (lila hoorns)', 'body': '#3a2850', 'bone': '#c0a0e8'},
            {'naam': 'Groen (gifgroene hoorns)', 'body': '#2c4a30', 'bone': '#90e060'},
            {'naam': 'Goud (rode hoorns)', 'body': ('#a87818', {'h': 0}), 'bone': '#d03030'},
        ],
    },
    'stantler': {
        # herten (Wyrdeer: moderne sprite, nog niet)
        'species': {'stantler': {'body': [3, 1, 9, 10]}, 'wyrdeer': {'body': [9, 8, 7], 'beard': [11, 12]}},
        'variants': [
            {'naam': 'Bosgeest (mosgroen, Mononoke)', 'body': '#5a8a50', 'beard': '#c0e0a0'},
            {'naam': 'Rendier', 'body': '#8a7a68', 'beard': '#e8dcc8'},
            {'naam': 'Edelhert (rood)', 'body': '#a04828', 'beard': '#d8b090'},
            {'naam': 'Melanistisch (zwart)', 'body': ('#3a3a40', {'l': 1.3}), 'beard': '#8a8a94'},
            {'naam': 'Mythisch blauw hert', 'body': '#4060b0', 'beard': '#c0d8f8'},
            {'naam': 'Zilveren hinde (Artemis; Wyrdeer goud)', 'body': '#b8bcc8', 'wyrdeer:body': ('#d8a828', {'h': 0}), 'beard': '#f8f0d0'},
        ],
    },
    'smeargle': {
        # de verfkleur van de staart
        # schilders: vacht, baret/oren en verf
        'species': {'smeargle': {'body': [5, 2, 12], 'hat': [4, 1], 'paint': [13, 8, 9, 11]}},
        'variants': [
            {'naam': 'Picasso, blauwe periode', 'body': '#98a8d0', 'hat': '#2c3a70', 'paint': '#f0d040'},
            {'naam': 'Picasso, roze periode', 'body': '#f0c0c8', 'hat': '#a04060', 'paint': '#40a0c0'},
            {'naam': 'Van Gogh (zonnebloemgeel, blauwe verf)', 'body': '#e8c860', 'hat': '#2848a0', 'paint': '#2860d0'},
            {'naam': 'Frida Kahlo (zwarte vlechten, rode bloem)', 'body': '#c89070', 'hat': ('#2c2c34', {'l': 1.3}), 'paint': '#d02838'},
            {'naam': 'Andy Warhol (popart)', 'body': '#f090c8', 'hat': '#3050c0', 'paint': '#f0e040'},
            {'naam': 'Klimt (bladgoud)', 'body': '#d8b048', 'hat': '#3a2a20', 'paint': ('#c89020', {'h': 0})},
        ],
    },
    'miltank': {
        'species': {'miltank': {'body': [10, 9, 7, 13], 'spots': [5, 1], 'belly': [13, 15, 12, 8]}},
        'variants': [
            {'naam': 'Holstein (wit)', 'body': '#ece8e4'},
            {'naam': 'Jersey (bruin)', 'body': '#b07848'},
            {'naam': 'Milka (paars)', 'body': '#a080d0'},
            {'naam': 'Hooglander (rood)', 'body': '#b05028'},
            {'naam': 'Belted Galloway (witte band om de buik)', 'body': ('#6a6a74', {'l': 1.2}), 'belly': '#f4f4f0',
             'miltank:parts': {'body': [10, 9, 7, 6], 'belly': [13, 15, 12, 8]}},
            {'naam': 'Gouden kalf', 'body': ('#c89020', {'h': 0})},
        ],
    },
    # --- groep 28 (Johto-rest en legendaries) ---
    'unown': {
        # alle letters delen één palet
        'species': {'unown': {'body': [9, 8, 7, 4]}},
        'variants': [
            {'naam': 'Zandsteen (Ruins of Alph)', 'body': '#a08860'},
            {'naam': 'Hiëroglief-goud', 'body': ('#c89020', {'h': 0})},
            {'naam': 'Jade', 'body': '#3a8a60'},
            {'naam': 'Amethist', 'body': '#7a50b0'},
            {'naam': 'Obsidiaanrood', 'body': '#902020'},
            {'naam': 'Unown-dimensie (cyaan)', 'body': '#30c0d0'},
        ],
    },
    'shuckle': {
        'species': {'shuckle': {'body': [4, 1, 3, 2], 'shell': [6, 10, 11]}},
        'variants': [
            {'naam': 'Groene schelp (paars lijf)', 'shell': '#40a050', 'body': '#b080d0'},
            {'naam': 'Paarse schelp (mint lijf)', 'shell': '#8040b0', 'body': '#90e0b0'},
            {'naam': 'Zwarte schelp', 'shell': ('#2c2c34', {'l': 1.3}), 'body': '#e8e4dc'},
            {'naam': 'Porselein', 'shell': '#ece8e0', 'body': '#f0c060'},
            {'naam': 'Bessensap', 'shell': '#f08030', 'body': '#f0a0b0'},
            {'naam': 'Gouden schelp', 'shell': ('#c89020', {'h': 0}), 'body': '#c02828'},
        ],
    },
    'raikou': {
        # de drie honden dragen elkaars kleuren
        'species': {'raikou': {'body': [13, 12, 11, 14], 'cloud': [4, 1, 3]}},
        'variants': [
            {'naam': 'Entei-bruin', 'body': '#a07050', 'cloud': '#d0d0d0'},
            {'naam': 'Suicune-blauw', 'body': '#58b8d0', 'cloud': '#a868d0'},
            {'naam': 'Witte tijger (stormgrijze wolk)', 'body': '#ece8e0', 'cloud': '#5a6070'},
            {'naam': 'Zwarte tijger (gouden wolk)', 'body': ('#34343c', {'l': 1.3}), 'cloud': '#e0b030'},
            {'naam': 'Groen (onweer-indigo)', 'body': '#60b050', 'cloud': '#3a3a90'},
            {'naam': 'Rood (zwarte wolk)', 'body': '#c03030', 'cloud': ('#34343c', {'l': 1.3})},
        ],
    },
    'entei': {
        'species': {'entei': {'body': [1, 15, 3, 4], 'mane': [9, 13, 14]}},
        'variants': [
            {'naam': 'Raikou-geel (paarse stekels)', 'body': '#e0b030', 'mane': '#8060b0'},
            {'naam': 'Suicune-blauw (witte stekels)', 'body': '#4880b0', 'mane': '#e8eef8'},
            {'naam': 'Witte leeuw (rode stekels)', 'body': '#e8e4dc', 'mane': '#c03030'},
            {'naam': 'Zwarte leeuw (vuurrode stekels)', 'body': ('#34343c', {'l': 1.3}), 'mane': '#e04020'},
            {'naam': 'Rood vuur (zwarte stekels)', 'body': '#a02020', 'mane': ('#3a3a44', {'l': 1.3})},
            {'naam': 'Groen (gouden stekels)', 'body': '#3a8a50', 'mane': '#d8a828'},
        ],
    },
    'suicune': {
        'species': {'suicune': {'body': [1, 4, 3, 13], 'mane': [6, 5, 7, 8], 'spots': [11, 15, 14]}},
        'variants': [
            {'naam': 'Raikou-geel (lichtblauwe ruiten)', 'body': '#e0b030', 'mane': '#7040a0', 'spots': '#a8d0f8'},
            {'naam': 'Entei-bruin (gele ruiten)', 'body': '#805028', 'mane': '#d0d0d0', 'spots': '#f0d040'},
            {'naam': 'Roze (lila ruiten)', 'body': '#f0a0c0', 'spots': '#d0c0f8'},
            {'naam': 'Zwart (cyaan ruiten)', 'body': ('#34343c', {'l': 1.3}), 'spots': '#70e0f0'},
            {'naam': 'Groen (gele ruiten)', 'body': '#40b080', 'spots': '#f0f0a0'},
            {'naam': 'Wit (Lugia-achtig, blauwe ruiten)', 'body': '#e8ecf4', 'spots': '#4870c0'},
        ],
    },
    'larvitar': {
        'species': {
            'larvitar': {'body': [1, 3, 2]},
            'pupitar': {'body': [1, 5, 3, 4]},
            'tyranitar': {'body': [1, 5, 2, 4], 'belly': [11, 12, 13]},
        },
        'variants': [
            {'naam': 'Turkoois (koraal buik)', 'body': '#30a0a0', 'belly': '#f08070'},
            {'naam': 'Lava (rood, gloeiende buik)', 'body': '#a03828', 'belly': '#f0b030'},
            {'naam': 'Godzilla (zwart, atoomblauwe buik)', 'body': ('#3a3a44', {'l': 1.3}), 'belly': '#40c8f0'},
            {'naam': 'IJs (wit, ijsblauwe buik)', 'body': '#d8e0e8', 'belly': '#70a8e0'},
            {'naam': 'Blauw (gouden buik)', 'body': '#4870c0', 'belly': '#e0b030'},
            {'naam': 'Kaiju-koning (goud, rode buik)', 'body': ('#c89020', {'h': 0}), 'belly': '#c02828'},
        ],
    },
    'lugia': {
        'species': {'lugia': {'body': [5, 3, 1, 8], 'blue': [6, 7, 11, 14], 'lines': [2]}},
        'variants': [
            {'naam': 'Shadow Lugia', 'body': ('#70708c', {'l': 0.7}), 'blue': '#c02848', 'lines': '#2c2c40'},
            {'naam': 'Ho-Oh-ruil', 'body': '#f0c040', 'blue': '#c02828', 'lines': '#8a5a20'},
            {'naam': 'Zeegroen', 'body': '#c8f0e0', 'blue': '#30a080', 'lines': '#4a7a70'},
            {'naam': 'Roze', 'body': '#f8d8e8', 'blue': '#e05090', 'lines': '#8a6078'},
            {'naam': 'Nachtzee (Shadow Lugia uit XD)', 'body': ('#5060a0', {'l': 0.7}), 'blue': '#e0e8f8', 'lines': '#141828'},
            {'naam': 'Pokémon Silver', 'body': '#c8ccd8', 'blue': '#606878'},
        ],
    },
    'ho_oh': {
        'species': {'ho_oh': {'red': [4, 3, 8, 6], 'green': [1, 2, 5]}},
        'variants': [
            {'naam': 'Lugia-ruil', 'red': '#e8ecf4', 'green': '#5070b0'},
            {'naam': 'Blauw vuur', 'red': '#3070d0'},
            {'naam': 'Paars', 'red': '#8040c0'},
            {'naam': 'Shadow Ho-Oh', 'red': ('#34343c', {'l': 1.3})},
            {'naam': 'Groene feniks', 'red': '#40a050', 'green': '#c02828'},
            {'naam': 'Zilverfeniks', 'red': '#c8ccd8'},
        ],
    },
    # --- moderne regionale vormen (Gen 8+ sprites, alleen front.png) ---
    'corsola_galar': {
        # spookkoraal: takken, lijf, gloed (Cursola: tentakels + schelpvoet)
        'species': {
            'corsola/galar': {'coral': [4, 2, 1, 3, 14], 'body': [13, 7, 5], 'glow': [6], 'rock': [9, 12]},
            'cursola': {'coral': [5, 2, 1, 3, 4, 7, 6, 12], 'body': [15, 14]},
        },
        'variants': [
            {'naam': 'Verdronken (blauwgrijs, cyaan spookgloed)', 'coral': '#7088a0', 'body': '#d8e0e8', 'glow': '#60e0f0', 'rock': '#384858'},
            {'naam': 'Schimmel (grauwgroen, groene gloed)', 'coral': '#98ac98', 'body': '#e4ece0', 'glow': '#80f080', 'rock': '#4a5a48'},
            {'naam': 'Vergeeld bot (oranje gloed)', 'coral': '#c0b090', 'body': '#f0e8d8', 'glow': '#f0a050', 'rock': '#6a5a48'},
            {'naam': 'Verdroogd bloedkoraal (roestrood)', 'coral': '#9a5c5c', 'body': '#ecdcdc', 'glow': '#f05050', 'rock': '#5a3838'},
            {'naam': 'Verkoold (zwart, sintels)', 'coral': ('#4a4452', {'l': 1.2}), 'body': '#d0c8d0', 'glow': '#f08030', 'rock': '#2c2830'},
            {'naam': 'Spookviolet (roze gloed)', 'coral': '#a088b8', 'body': '#ece4f4', 'glow': '#f070c0', 'rock': '#4a3a58'},
        ],
    },
    'farfetchd_galar': {
        # ridders: veren, prei-lans/-schild, snavel blijft
        'species': {
            'farfetchd/galar': {'body': [1, 2, 5], 'leek': [14, 15, 4]},
            'sirfetchd': {'body': [7, 12, 5, 8], 'leek': [2, 3, 1, 10, 9]},
        },
        'variants': [
            {'naam': 'Tempelier (wit met rode lans)', 'body': '#b8b0a8', 'sirfetchd:body': '#f0ece8', 'leek': '#c03030'},
            {'naam': 'Zwarte ridder (paarse ui)', 'body': ('#34343c', {'l': 1.3}), 'sirfetchd:body': ('#4a4a58', {'l': 1.3}), 'leek': '#a040c0'},
            {'naam': 'Koning Arthur (blauw, gouden Excalibur)', 'body': '#3a58a0', 'leek': '#e0b030'},
            {'naam': 'Groene ridder (Sir Gawain, knoflook)', 'body': '#3a6a40', 'leek': '#e8dcb0'},
            {'naam': 'Rode ridder (gele prei)', 'body': '#a03028', 'leek': '#f0d040'},
            {'naam': 'Gouden ridder (zilveren zwaard)', 'body': ('#d8a828', {'h': 0}), 'leek': '#d8dce8'},
        ],
    },
    'meowth_galar': {
        # Viking-katten van metaal: vacht/metaal, ogen
        'species': {
            'meowth/galar': {'body': [3, 5, 4], 'eyes': [10]},
            'perrserker': {'body': [13, 14, 12], 'metal': [5, 2, 1, 11], 'eyes': [8, 9]},
        },
        'variants': [
            {'naam': 'Kobalt (oranje ogen)', 'body': '#3a60b0', 'metal': '#4a70c0', 'eyes': '#f0a040'},
            {'naam': 'Bronspatina (roze ogen)', 'body': '#4a9a80', 'metal': '#5aa890', 'eyes': '#f04080'},
            {'naam': 'Roestijzer (gele ogen)', 'body': '#a04020', 'metal': '#a85030', 'eyes': '#f0e040'},
            {'naam': 'Chroom (rode ogen)', 'body': '#c8ccd8', 'metal': '#d0d4e0', 'eyes': '#e03030'},
            {'naam': 'Zwart staal (ijsblauwe ogen)', 'body': ('#3a3a44', {'l': 1.3}), 'metal': ('#4a4a58', {'l': 1.3}), 'eyes': '#40e0f0'},
            {'naam': 'Roségoud (groene ogen)', 'body': '#e0a090', 'metal': '#e8b0a0', 'eyes': '#40c060'},
        ],
    },
    'growlithe_hisui': {
        # vulkaanhonden: steen (helm/vacht) en vuurvacht
        'species': {
            'growlithe/hisui': {'stone': [4, 3, 6, 2], 'fur': [7, 9, 8]},
            'arcanine/hisui': {'stone': [4, 2, 1], 'fur': [8, 7, 6, 5]},
        },
        'variants': [
            {'naam': 'Obsidiaan met lava', 'stone': ('#3a3440', {'l': 1.2}), 'fur': '#f08020'},
            {'naam': 'Basalt met blauw vuur', 'stone': '#5a6070', 'fur': '#3070e0'},
            {'naam': 'Zandsteen met paars vuur', 'stone': '#c8a878', 'fur': '#8040b0'},
            {'naam': 'Marmer met goud', 'stone': ('#d8d4d0', {'l': 1.2}), 'fur': '#e0b030'},
            {'naam': 'Lapis lazuli met goud', 'stone': '#2c4a98', 'fur': '#f0c030'},
            {'naam': 'Robijn met zwart vuur', 'stone': '#8a2028', 'fur': ('#3a3440', {'l': 1.3})},
        ],
    },
    'ponyta_galar': {
        # eenhoorns: lijf, manen, cyaan lokken
        'species': {
            'ponyta/galar': {'body': [10, 11, 12, 13], 'mane': [6, 5, 4, 9], 'cyan': [1, 2, 3]},
            'rapidash/galar': {'body': [6, 11, 12, 10], 'mane': [7, 5, 9, 8], 'cyan': [3, 2, 1]},
        },
        'variants': [
            {'naam': 'Nachtmerrie (zwart, rode manen)', 'body': ('#3a3440', {'l': 1.3}), 'mane': '#c02838', 'cyan': '#f08030'},
            {'naam': 'Zonne-eenhoorn (crème, oranje manen)', 'body': '#f8e8c0', 'mane': '#f0a030', 'cyan': '#f05050'},
            {'naam': 'Kristal (ijsblauw)', 'body': '#e0f0f8', 'mane': '#80b0f0', 'cyan': '#f4f4ff'},
            {'naam': 'Feeënroze met mint', 'body': '#f8e0ec', 'mane': '#f080b0', 'cyan': '#80e0b0'},
            {'naam': 'Sterrennacht', 'body': ('#2c3878', {'l': 1.3}), 'mane': '#f0d040', 'cyan': '#a0c0f0'},
            {'naam': 'Twilight Sparkle (lila, paars, roze)', 'body': '#c8b0e8', 'mane': '#4a2a80', 'cyan': '#f070c0'},
        ],
    },
    'slowpoke_galar': {
        # Galar-luiaards: lijf, kroon/kop, Shellder
        'species': {
            'slowpoke/galar': {'body': [10, 5, 4, 6], 'crown': [3, 2, 1]},
            'slowbro/galar': {'body': [4, 8, 7], 'arm': [5, 13, 12], 'crown': [2, 1]},
            'slowking/galar': {'body': [3, 1, 2, 15, 5], 'arm': [12, 11, 10]},
        },
        'variants': [
            {'naam': 'Gifkruid (mint, magenta)', 'body': '#80c8a0', 'crown': '#c040a0', 'arm': '#7060a0'},
            {'naam': 'Hemelsblauw (oranje kroon)', 'body': '#80b0e8', 'crown': '#f0a030', 'arm': '#e0e0ec'},
            {'naam': 'Galar-gif (paars, geel)', 'body': '#9060c0', 'crown': '#e0e040', 'arm': '#40a080'},
            {'naam': 'Perzik (lichtblauw)', 'body': '#f8b890', 'crown': '#80d0f0', 'arm': '#806090'},
            {'naam': 'Toxapex (zwart, roze)', 'body': ('#3a3440', {'l': 1.3}), 'crown': '#f070c0', 'arm': '#40c0a0'},
            {'naam': 'Galarica-goud (blauwe kroon)', 'body': '#e8c050', 'crown': '#40c0f0', 'arm': '#c03050'},
        ],
    },
    'marowak_alola': {
        # vuurdansers: vlammen, lijf, botten
        'species': {'marowak/alola': {'flames': [1, 2, 3, 4], 'body': [12, 14, 11, 10], 'bones': [8, 7, 9, 5]}},
        'variants': [
            {'naam': 'Halloween (oranje vuur, zwart lijf)', 'flames': '#f08020', 'body': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Paars spookvuur', 'flames': '#b060f0', 'body': '#2c3a50', 'bones': '#e0d8f0'},
            {'naam': 'Blauw vuur (vergeeld bot)', 'flames': '#40a0f0', 'body': '#5a2c40', 'bones': '#f0e0c0'},
            {'naam': 'Suikerschedel (roze vuur en botten)', 'flames': '#f070c0', 'body': '#2c2848', 'bones': '#f0c0d8'},
            {'naam': 'Rood vuur met gouden botten', 'flames': '#e03030', 'body': '#3a2050', 'bones': '#f0d060'},
            {'naam': 'Zonnedans (goud vuur)', 'flames': '#f0d040', 'body': '#2c4a3a', 'bones': '#f8f8f8'},
        ],
    },
    'mr_mime_galar': {
        # tapdansers: haar/jas, blauwe delen (schmink kleurt mee)
        'species': {
            'mr_mime/galar': {'blue': [12, 13, 3, 2, 1], 'skin': [8, 7, 6]},
            'mr_rime': {'coat': [4, 2, 1], 'blue': [14, 13, 15, 6], 'skin': [9, 5]},
        },
        'variants': [
            {'naam': 'Carnaval (oranje met turkoois)', 'blue': '#e07020', 'coat': '#9a4010', 'skin': '#80d0e0'},
            {'naam': 'Rode tapdanser', 'blue': '#c03030', 'coat': '#7a1828', 'pink': '#f0d040', 'skin': '#f0e0a0'},
            {'naam': 'The Riddler (groen met paars)', 'blue': '#3a9a50', 'coat': '#2c5a38', 'pink': '#a060d0', 'skin': '#a0d890'},
            {'naam': 'Joker (paars met groen)', 'blue': '#7040a0', 'coat': '#4a2870', 'pink': '#60c040', 'skin': '#f4f4ec'},
            {'naam': 'Fred Astaire (goud)', 'blue': ('#d8a828', {'h': 0}), 'coat': '#8a6018', 'pink': '#f080a0', 'skin': '#e0c8f0'},
            {'naam': 'IJskoningin (lichtblauw, lila)', 'blue': '#a0d8f0', 'coat': '#5080c0', 'pink': '#c0a0f0', 'skin': '#d0e8f8'},
        ],
    },
    'kleavor': {
        # Hisui-bijlen: stenen armen en lijf (eigen kleuren, los van Scyther/Scizor)
        'species': {'kleavor': {'stone': [2, 4, 1], 'body': [9, 6, 5, 12, 11, 10]}},
        'variants': [
            {'naam': 'Obsidiaan (oranje lijf)', 'stone': ('#3a3440', {'l': 1.3}), 'body': '#d08040'},
            {'naam': 'Jade', 'stone': '#4a8a68', 'body': '#e0d0a0'},
            {'naam': 'Lapis lazuli', 'stone': '#2c4a98', 'body': '#e8c070'},
            {'naam': 'Marmer (roze lijf)', 'stone': ('#c8c4c0', {'l': 1.2}), 'body': '#e0a0a0'},
            {'naam': 'Rode jaspis', 'stone': '#a03028', 'body': '#c8b090'},
            {'naam': 'Gouden bijlen', 'stone': ('#d8a828', {'h': 0}), 'body': '#806040'},
        ],
    },
    'annihilape': {
        # spookaap: vacht, armen/benen, ogen
        'species': {'annihilape': {'fur': [1, 6, 5], 'limbs': [12, 13, 10, 14], 'eyes': [7]}},
        'variants': [
            {'naam': 'Woede (rood, gele ogen)', 'fur': '#a04040', 'limbs': '#3a2028', 'eyes': '#f0e040'},
            {'naam': 'Spookpaars (groene ogen)', 'fur': '#8a70b0', 'limbs': '#3a2c50', 'eyes': '#40f0a0'},
            {'naam': 'Zwart met witte ogen', 'fur': ('#3a3a44', {'l': 1.3}), 'limbs': ('#202028', {'l': 1.3}), 'eyes': '#f0f0f0'},
            {'naam': 'Yeti (wit, blauwe ogen)', 'fur': ('#d0d0d8', {'l': 1.2}), 'limbs': '#7080a0', 'eyes': '#3080e0'},
            {'naam': 'Apenkoning (goud)', 'fur': ('#d8a838', {'h': 0}), 'limbs': '#8a3020', 'eyes': '#e03030'},
            {'naam': 'Blauw vuur (oranje ogen)', 'fur': '#5a80c0', 'limbs': '#202c50', 'eyes': '#f08030'},
        ],
    },
    'tauros_paldea': {
        # vechtstieren: lijf (1/5), manen voorop (2/6), hoorns; Blaze = Team Magma, Aqua = Team Aqua
        'species': {
            'tauros/paldea_combat': {'body': [5, 1], 'mane': [2, 6], 'horns': [8, 9, 7, 10]},
            'tauros/paldea_blaze': {'body': [7, 1], 'mane': [2], 'horns': [11, 10, 9, 8], 'accent': [6, 5]},
            'tauros/paldea_aqua': {'body': [5, 1], 'mane': [3], 'horns': [11, 9, 7, 6], 'accent': [14, 13]},
        },
        'variants': [
            {'naam': 'Bizon (bruin, crème hoorns)', 'body': '#7a5434', 'mane': '#4a3020', 'horns': '#e8dcc0', 'accent': '#f0d040'},
            {'naam': 'Team Magma (Blaze) / Team Aqua (Aqua) / Team Galactic (Combat)',
             'tauros/paldea_combat:body': '#5a7090', 'tauros/paldea_combat:mane': '#2c3a58', 'tauros/paldea_combat:horns': '#40e0f0',
             'tauros/paldea_blaze:body': '#b82828', 'tauros/paldea_blaze:mane': ('#2c2c34', {'l': 1.3}), 'tauros/paldea_blaze:horns': '#a0a0a8',
             'tauros/paldea_blaze:accent': '#f08020',
             'tauros/paldea_aqua:body': '#2c4aa8', 'tauros/paldea_aqua:mane': ('#1c2440', {'l': 1.3}), 'tauros/paldea_aqua:horns': '#f0f0f8',
             'tauros/paldea_aqua:accent': '#f0f0f8'},
            {'naam': 'Colorado (roodbruin, crème hoorns)', 'body': '#8a3a20', 'mane': '#5a2410', 'horns': '#e8d8b0', 'accent': '#40c0f0'},
            {'naam': 'Ensabanado (wit, donkere hoorns)', 'body': ('#c8c4bc', {'l': 1.3}), 'mane': ('#a8a49c', {'l': 1.3}), 'horns': '#5a4a40', 'accent': '#e03030'},
            {'naam': 'Indigo met gouden hoorns', 'body': '#3a3a80', 'mane': '#2a2a60', 'horns': '#f0d040', 'accent': '#f0d040'},
            {'naam': 'Gouden stier', 'body': ('#c89828', {'h': 0}), 'mane': '#a07818', 'horns': '#f0f0f0', 'accent': '#e03030'},
        ],
    },
    'birds_galar': {
        # de Galar-vogels dragen elkaars kleuren; 'main' = kenmerkende kleur, 'dark' = tweede kleur
        'species': {
            'articuno/galar': {'main': [8, 10, 11], 'dark': [5, 9, 1, 3]},
            'zapdos/galar': {'main': [3, 5, 1, 2], 'dark': [6, 9]},
            'moltres/galar': {'main': [1, 3, 9, 12, 10, 6, 8], 'dark': [4, 5, 2]},
        },
        'variants': [
            {'naam': 'Ruil A (Articuno oranje, Zapdos karmozijn, Moltres paars)',
             'articuno/galar:main': '#f07828', 'articuno/galar:dark': '#8a3018', 'zapdos/galar:main': '#e03050', 'zapdos/galar:dark': '#3a4450', 'moltres/galar:main': '#b080e0', 'moltres/galar:dark': '#3a3060'},
            {'naam': 'Ruil B (Articuno karmozijn, Zapdos paars, Moltres ijsblauw)',
             'articuno/galar:main': '#e03050', 'articuno/galar:dark': '#3a4450', 'zapdos/galar:main': '#a070d0', 'zapdos/galar:dark': '#3a2c60', 'moltres/galar:main': '#60b0f0', 'moltres/galar:dark': '#2c3a60'},
            {'naam': 'IJs, bliksem en wit vuur',
             'articuno/galar:main': ('#d8e4f0', {'l': 1.2}), 'articuno/galar:dark': '#3070c0', 'zapdos/galar:main': '#4870d0', 'zapdos/galar:dark': '#3a3020', 'moltres/galar:main': ('#e8e8f4', {'l': 1.2}), 'moltres/galar:dark': '#3a3048'},
            {'naam': 'Ravenzwart (rood; Moltres zwart vuur op een zilveren lijf)', 'main': ('#3a3a48', {'l': 1.3}), 'dark': '#a03040', 'moltres/galar:dark': ('#b8bcc8', {'l': 1.2})},
            {'naam': 'Smaragd', 'main': '#40b080', 'dark': '#1c3a30'},
            {'naam': 'Goud (Zapdos zilver)', 'main': ('#e0b030', {'h': 0}), 'dark': '#4a3010', 'zapdos/galar:main': ('#c8ccd8', {'l': 1.2})},
        ],
    },
    'typhlosion_hisui': {
        # spookvuur: vlammen, kern, lijf
        'species': {'typhlosion/hisui': {'flames': [2, 1, 3], 'core': [4], 'body': [8, 5, 7, 6]}},
        'variants': [
            {'naam': 'Blauw spookvuur', 'flames': '#3070f0', 'core': '#80e0f0', 'body': '#2c3048'},
            {'naam': 'Groen dwaallicht', 'flames': '#40d060', 'core': '#e0f060', 'body': '#203828'},
            {'naam': 'Johto-vuur (oranje)', 'flames': '#f08020', 'core': '#f0d040', 'body': '#2c3a58'},
            {'naam': 'Wit vuur', 'flames': ('#d8d8f0', {'l': 1.2}), 'core': '#a0b0f0', 'body': ('#3a3448', {'l': 1.3})},
            {'naam': 'Rood vuur op zwart', 'flames': '#d02828', 'core': '#f0a040', 'body': ('#2c2c34', {'l': 1.3})},
            {'naam': 'Gouden vuur', 'flames': '#f0c030', 'core': '#f06020', 'body': '#4a2c60'},
        ],
    },
    'wooper_paldea': {
        # gifsalamanders: lijf, kieuwen/vinnen, buik (Clodsire)
        'species': {
            'wooper/paldea': {'body': [7, 3, 4, 6, 10], 'gills': [8, 1, 2]},
            'clodsire': {'body': [8, 9, 7, 10, 11], 'belly': [4, 5, 6], 'gills': [14, 15, 13]},
        },
        'variants': [
            {'naam': 'Blauwe pijlgifkikker (gele kieuwen)', 'body': '#3060b0', 'gills': '#f0d040', 'belly': '#a8c0e8'},
            {'naam': 'Moerasgroen (oranje kieuwen)', 'body': '#4a7040', 'gills': '#f08030', 'belly': '#a8c090'},
            {'naam': 'Zwart met rood', 'body': ('#34343c', {'l': 1.3}), 'gills': '#d03030', 'belly': '#7a7a84'},
            {'naam': 'Roze axolotl', 'body': '#e8a0b0', 'gills': '#d04070', 'belly': '#f8d8e0'},
            {'naam': 'Lava (cyaan kieuwen)', 'body': '#a03020', 'gills': '#60e0f0', 'belly': '#e09060'},
            {'naam': 'Goud (paarse kieuwen)', 'body': ('#c89828', {'h': 0}), 'gills': '#7040b0', 'belly': '#f0e0a0'},
        ],
    },
    'qwilfish_hisui': {
        # Hisui-kogelvissen: lijf, stekels, roze/paarse accenten
        'species': {
            'qwilfish/hisui': {'body': [4, 6, 5, 10], 'spikes': [8, 9, 13], 'pink': [2, 7, 1]},
            'overqwil': {'body': [2, 4, 1], 'spikes': [12, 14, 6, 3], 'pink': [8, 9, 5], 'purple': [7, 10, 11]},
        },
        'variants': [
            {'naam': 'Zee-egel (paars, witte stekels)', 'body': '#4a3a68', 'spikes': '#e0e0f0', 'pink': '#f0d040', 'purple': '#f0a020'},
            {'naam': 'Koraal (oranje)', 'body': '#c06030', 'spikes': '#f0e0b0', 'pink': '#30a0c0', 'purple': '#2c6090'},
            {'naam': 'Gifkogel (groen)', 'body': '#3a6a40', 'spikes': '#e0c060', 'pink': '#f04080', 'purple': '#a040c0'},
            {'naam': 'IJsvis', 'body': '#8098c0', 'spikes': '#f0f4f8', 'pink': '#40c0f0', 'purple': '#3060c0'},
            {'naam': 'Wit met rode stekels', 'body': ('#c0c0cc', {'l': 1.3}), 'spikes': '#c02828', 'pink': '#3a3a48', 'purple': '#808090'},
            {'naam': 'Goud met zwarte stekels', 'body': ('#c89020', {'h': 0}), 'spikes': ('#3a3a44', {'l': 1.3}), 'pink': '#c02848', 'purple': '#7040a0'},
        ],
    },
    'sneasel_hisui': {
        # gifklimmers: vacht (Sneasler: blauw lijf + paarse kap)
        'species': {
            'sneasel/hisui': {'body': [7, 12, 14, 15, 11], 'pale': [2, 9, 13]},
            'sneasler': {'body': [11, 14, 9], 'top': [10, 3, 1], 'accent': [7, 5]},
        },
        'variants': [
            {'naam': 'Bergmarter (bruin)', 'body': '#7a5038', 'top': '#4a2c20', 'accent': '#f0c030', 'pale': '#e0c8a8'},
            {'naam': 'Gifgroen', 'body': '#3a7a50', 'top': '#203a28', 'accent': '#d040c0', 'pale': '#c0e0b0'},
            {'naam': 'Bloedrood', 'body': '#8a2030', 'top': '#3a1018', 'accent': '#f0e040', 'pale': '#e8c0c0'},
            {'naam': 'Sneeuwvos (wit)', 'body': ('#c0c0d0', {'l': 1.3}), 'top': '#5a6a90', 'accent': '#40a0f0', 'pale': '#c8d8f0'},
            {'naam': 'Ninja (zwart)', 'body': ('#34343e', {'l': 1.3}), 'top': ('#202028', {'l': 1.3}), 'accent': '#e03030', 'pale': '#8a8aa0'},
            {'naam': 'Goud', 'body': ('#c89020', {'h': 0}), 'top': '#6a4010', 'accent': '#3060d0', 'pale': '#f0e0b0'},
        ],
    },
}


# Extra recepten per generatie staan in losse bestanden (recipes_gen4.py e.d.), zodat
# parallel werken niet botst. Elk bestand definieert een eigen LINES-dict.
def _load_extra():
    import glob
    import importlib
    import os
    for path in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipes_*.py'))):
        mod = importlib.import_module(os.path.basename(path)[:-3])
        for key, line in mod.LINES.items():
            assert key not in LINES, 'dubbele lijn: %s' % key
            LINES[key] = line


_load_extra()
