"""Project Grounded: items die nergens anders in de game te krijgen zijn (Jordi, 9 okt), verdeeld over de diepzeetrog
onder Route 127 en de Spacetime-gebieden. Eén lijst, zodat geen item dubbel ligt; elke kaartgenerator haalt hier zijn
items op (plek bepaalt de generator) en schrijft het flagblok.

Bepaling 'nergens te krijgen' (9 okt): het item komt in geen kaart (item balls, verborgen items), geen script
(giveitem/finditem/marts) en geen C-bron (Floating Market, Fishing Tournament, Battle Frontier, Spire, ...) voor;
alleen in de itemdefinities/gevechtslogica of als held item van trainers. Geen TM's, geen Mega Stones/Z-kristallen
(geen Mega Ring), geen Ability Patch (verborgen abilities zijn niet verkrijgbaar).
Flags FLAG_GROUNDED 840-879 (blok 'nieuwe_items' in flags.h).
Gebruik: import nieuwe_items as ni; ni.items('ChargestoneCave_1F') -> [(flag, item, aantal, verborgen)]; ni.flags()."""
import os, re

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))

# (n, kaart, item, aantal, verborgen?, omschrijving)
ITEMS = [
    # diepzeetrog onder Route 127 (trog127.py)
    (840, 'Underwater_Route127_Trench', 'ITEM_LURE_BALL', 3, False, 'diepzeetrog: Lure Balls'),
    (841, 'Underwater_Route127_Trench', 'ITEM_HEAVY_BALL', 3, False, 'diepzeetrog: Heavy Balls'),
    (842, 'Underwater_Route127_Trench', 'ITEM_BINDING_BAND', 1, False, 'diepzeetrog: Binding Band'),
    (843, 'Underwater_Route127_Trench', 'ITEM_EJECT_BUTTON', 1, False, 'diepzeetrog: Eject Button'),
    (844, 'Underwater_Route127_Trench', 'ITEM_POWER_ANKLET', 1, False, 'diepzeetrog: Power Anklet'),
    (845, 'Underwater_Route127_Trench', 'ITEM_EXP_CANDY_L', 2, False, 'diepzeetrog: Exp. Candy L'),
    (846, 'Underwater_Route127_Trench', 'ITEM_RELIC_VASE', 1, True, 'diepzeetrog: verborgen Relic Vase'),
    # Chargestone Cave (chargestone.py)
    (850, 'ChargestoneCave_1F', 'ITEM_FAST_BALL', 3, False, 'Chargestone Cave 1F: Fast Balls'),
    (851, 'ChargestoneCave_1F', 'ITEM_POWER_LENS', 1, False, 'Chargestone Cave 1F: Power Lens'),
    (852, 'ChargestoneCave_B1F', 'ITEM_EJECT_PACK', 1, False, 'Chargestone Cave B1F: Eject Pack'),
    (853, 'ChargestoneCave_B1F', 'ITEM_TERRAIN_EXTENDER', 1, False, 'Chargestone Cave B1F: Terrain Extender'),
    (854, 'ChargestoneCave_B2F', 'ITEM_ABILITY_SHIELD', 1, False, 'Chargestone Cave B2F: Ability Shield'),
    (855, 'ChargestoneCave_B2F', 'ITEM_EXP_CANDY_XL', 1, True, 'Chargestone Cave B2F: verborgen Exp. Candy XL'),
    # Lavender Town + Pokemon Tower (spacetime_cave.py)
    (860, 'LavenderTown', 'ITEM_EXP_CANDY_S', 3, True, 'Lavender Town: verborgen Exp. Candy S'),
    (861, 'PokemonTower_3F', 'ITEM_MOON_BALL', 3, False, 'Pokemon Tower 3F: Moon Balls'),
    (862, 'PokemonTower_4F', 'ITEM_RED_CARD', 1, False, 'Pokemon Tower 4F: Red Card'),
    (863, 'PokemonTower_2F', 'ITEM_POWER_BRACER', 1, False, 'Pokemon Tower 2F: Power Bracer'),
    # Cerulean Cave (spacetime_cave.py)
    (864, 'CeruleanCave_1F', 'ITEM_LEVEL_BALL', 3, False, 'Cerulean Cave 1F: Level Balls'),
    (865, 'CeruleanCave_2F', 'ITEM_POWER_WEIGHT', 1, False, 'Cerulean Cave 2F: Power Weight'),
    (866, 'CeruleanCave_2F', 'ITEM_ROOM_SERVICE', 1, False, 'Cerulean Cave 2F: Room Service'),
    (867, 'CeruleanCave_B1F', 'ITEM_MIRROR_HERB', 1, False, 'Cerulean Cave B1F: Mirror Herb'),
    (868, 'CeruleanCave_B1F', 'ITEM_POWER_BAND', 1, True, 'Cerulean Cave B1F: verborgen Power Band'),
    # National Park + Ilex Forest (national_park.py)
    (870, 'NationalPark', 'ITEM_SPORT_BALL', 5, False, 'National Park: Sport Balls'),
    (871, 'NationalPark', 'ITEM_INSECT_PLATE', 1, False, 'National Park: Insect Plate'),
    (872, 'NationalPark', 'ITEM_POWER_BELT', 1, True, 'National Park: verborgen Power Belt'),
    (873, 'IlexForest', 'ITEM_FRIEND_BALL', 3, False, 'Ilex Forest: Friend Balls'),
    (874, 'IlexForest', 'ITEM_LOVE_BALL', 3, False, 'Ilex Forest: Love Balls'),
    (875, 'IlexForest', 'ITEM_DESTINY_KNOT', 1, False, 'Ilex Forest: Destiny Knot'),
    (876, 'IlexForest', 'ITEM_ROSE_INCENSE', 1, True, 'Ilex Forest: verborgen Rose Incense'),
    # Area Zero (area_zero.py; flags uit het eigen blok FLAG_GROUNDED 920-999)
    (950, 'AreaZero_Rim', 'ITEM_QUICK_BALL', 5, False, 'Area Zero, kraterwand: Quick Balls'),
    (951, 'AreaZero_Rim', 'ITEM_MUSCLE_BAND', 1, False, 'Area Zero, kraterwand: Muscle Band'),
    (952, 'AreaZero_Depths', 'ITEM_ADRENALINE_ORB', 1, False, 'Area Zero, diepte: Adrenaline Orb'),
    (953, 'AreaZero_Depths', 'ITEM_SHED_SHELL', 1, True, 'Area Zero, diepte: verborgen Shed Shell'),
    (954, 'AreaZero_Crystal', 'ITEM_BEAST_BALL', 3, False, 'Area Zero, kristalgrot: Beast Balls'),
    (955, 'AreaZero_Crystal', 'ITEM_RING_TARGET', 1, True, 'Area Zero, kristalgrot: verborgen Ring Target'),
    (956, 'AreaZero_Future', 'ITEM_BOOSTER_ENERGY', 2, False, 'Area Zero, toekomst: Booster Energy'),
    (957, 'AreaZero_Future', 'ITEM_METAL_ALLOY', 1, False, 'Area Zero, toekomst: Metal Alloy (Duraludon -> Archaludon)'),
    (958, 'AreaZero_Future', 'ITEM_AIR_BALLOON', 1, True, 'Area Zero, toekomst: verborgen Air Balloon'),
    (959, 'AreaZero_Past', 'ITEM_POWER_HERB', 1, False, 'Area Zero, verleden: Power Herb'),
    (960, 'AreaZero_Past', 'ITEM_GRIP_CLAW', 1, False, 'Area Zero, verleden: Grip Claw'),
    (961, 'AreaZero_Past', 'ITEM_STICKY_BARB', 1, True, 'Area Zero, verleden: verborgen Sticky Barb'),
    # Mt. Coronet + Spear Pillar (coronet.py; flags uit het eigen blok FLAG_GROUNDED 1160-1219)
    (1180, 'MtCoronet_4F_Room2', 'ITEM_LINKING_CORD', 1, False, 'Mt. Coronet 4F kamer 2: Linking Cord'),
    (1181, 'MtCoronet_4F_Room2', 'ITEM_ODD_KEYSTONE', 1, False, 'Mt. Coronet 4F kamer 2: Odd Keystone'),
    (1182, 'MtCoronet_4F_Outside', 'ITEM_PEAT_BLOCK', 1, True, 'Mt. Coronet 4F buiten: verborgen Peat Block'),
    (1183, 'MtCoronet_5F', 'ITEM_IRON_BALL', 1, False, 'Mt. Coronet 5F: Iron Ball'),
    (1184, 'SpearPillar', 'ITEM_ADAMANT_ORB', 1, False, 'Spear Pillar: Adamant Orb (bij het altaar van Dialga)'),
    (1185, 'SpearPillar', 'ITEM_LUSTROUS_ORB', 1, False, 'Spear Pillar: Lustrous Orb (bij het altaar van Palkia)'),
]
FIRST, LAST = 840, 879
EXTRA_RANGES = [(920, 999), (1160, 1219)]          # Area Zero gebruikt flags uit zijn eigen blok


def flag_name(n, mp, it, hid):
    m = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', mp).upper().replace('_1_F', '_1F').replace('_2_F', '_2F')
    m = re.sub(r'_(B?\d)_F\b', r'_\1F', m)
    return 'FLAG_%sITEM_%s_%s' % ('HIDDEN_' if hid else '', m, it[5:])


def items(mp):
    """[(flag, item, aantal, verborgen)] voor kaart mp."""
    return [(flag_name(n, m, it, h), it, q, h) for n, m, it, q, h, _ in ITEMS if m == mp]


def flags():
    assert len({it for _, _, it, *_ in ITEMS}) == len(ITEMS), 'item dubbel'
    assert len({n for n, *_ in ITEMS}) == len(ITEMS) and all(
        FIRST <= n <= LAST or any(a <= n <= b for a, b in EXTRA_RANGES) for n, *_ in ITEMS)
    assert not any(it.startswith(('ITEM_TM', 'ITEM_HM')) for _, _, it, *_ in ITEMS)
    p = os.path.join(REPO, 'include/constants/flags.h')
    s = open(p).read()
    blk = '// nieuwe_items { (tools/grounded/maptools/nieuwe_items.py; FLAG_GROUNDED 840-879, items die nergens anders liggen)\n'
    for n, mp, it, q, h, why in ITEMS:
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (flag_name(n, mp, it, h), n, why)
    blk += '// }'
    if '// nieuwe_items {' in s:
        i = s.index('// nieuwe_items {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// chargestone {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    s = s.replace('800-839 Swords of Justice/Keldeo/Meltan, 840+ vrij.',
                  '800-839 Swords of Justice/Keldeo/Meltan, 840-879 nieuwe items (nieuwe_items.py), 880+ vrij.')
    for n, *_ in ITEMS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


if __name__ == '__main__':
    flags()
    for row in ITEMS:
        print(flag_name(row[0], row[1], row[2], row[4]), row[3])
