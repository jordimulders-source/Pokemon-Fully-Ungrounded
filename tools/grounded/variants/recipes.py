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
        'species': {
            'treecko': {'body': [1, 3, 4, 5], 'leaves': [13, 14, 15], 'belly': [10, 11, 12], 'eyes': [6, 8, 9]},
            'grovyle': {'body': [5, 6, 7, 8, 13], 'leaves': [1, 2, 3], 'belly': [11, 12, 14], 'eyes': [9, 10]},
            'sceptile': {'body': [1, 2, 3, 4, 5], 'leaves': [12, 13, 14], 'belly': [9, 10], 'seeds': [7, 8, 11]},
        },
        'variants': [
            {'naam': 'Torchic-kleuren', 'body': '#e87828', 'leaves': '#c09818', 'belly': '#f0d060'},
            {'naam': 'Mudkip-kleuren', 'body': '#3890d0', 'leaves': '#d87028', 'belly': '#b8c8e8'},
            {'naam': 'Bladstaartgekko', 'body': '#7c5c3c', 'leaves': '#4c2c1c', 'belly': '#c8a878'},
            {'naam': 'Albino', 'body': ('#c8c8bc', ALBINO), 'leaves': ('#a8aca0', ALBINO),
             'belly': '#e0a8b0', 'eyes': '#d02030', 'seeds': '#e8d8c8'},
            {'naam': 'Pikachu', 'body': '#f0c828', 'leaves': '#986020', 'seeds': '#d83020'},
            {'naam': 'Cyberpunk', 'body': ('#2c2c38', {'l': 0.8}), 'leaves': '#28e870', 'belly': '#ff3090',
             'eyes': '#30e8ff', 'seeds': '#30e8ff'},
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
            {'naam': 'Albino', 'body': ('#c4c4cc', ALBINO), 'crest': ('#a8a8b4', ALBINO), 'belly': ('#dcdce4', ALBINO),
             'cheeks': '#e0a0a0', 'eyes': '#c02030'},
            {'naam': 'Koi (Showa)', 'body': ('#282830', {'l': 0.8}), 'crest': '#d82818', 'belly': '#e8e8e8',
             'cheeks': '#e83018'},
            {'naam': 'Bubblegum', 'body': '#f058a8', 'crest': '#901860', 'belly': '#f8f0c0', 'cheeks': '#30e8f8'},
        ],
    },
}
