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
            {'naam': 'Spookwolf', 'grey': '#50d0e8', 'dark': '#3a2a5c', 'eyes': '#ff4898'},
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
            {'naam': 'Neon', 'leaf': '#e040c0', 'body': '#40e0e8', 'ludicolo:body': '#40e0e8', 'stripes': '#6038c0',
             'red': '#f8e030'},
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
}
