"""Fully Ungrounded: wat er van de oude wereld overblijft (het skelet).

Eén plek voor de bewaarlijst; skelet_maps.py bouwt de kaarten, hoenn_eruit.py haalt al het andere weg.
"""

# Nieuwe kaartgroep (achteraan group_order en als laatste sleutel in map_groups.json).
GROUP = 'gMapGroup_FullyUngrounded'

# Stock-interieurs: kaartnaam -> (layout, beschrijving). Elke bewaarde layout hangt aan precies één kaart,
# zodat hij in de debugwarp zit en getest wordt.
STOCK_HOUSES = {
    'Stock_House1':       ('LAYOUT_HOUSE1', 'gewoon huis 10x9 (deur StartTown, linksboven)'),
    'Stock_House2':       ('LAYOUT_HOUSE2', 'gewoon huis 11x8 (deur StartTown, rechtsonder)'),
    'Stock_HouseWithBed': ('LAYOUT_HOUSE_WITH_BED', 'huis met bed 10x8 (TestMap)'),
    'Stock_SmallHouse':   ('LAYOUT_FORTREE_CITY_HOUSE1', 'klein huis 8x6 (TestMap)'),
    'Stock_TwoStory_1F':  ('LAYOUT_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F', 'huis met trap 11x9, spelershuis (TestMap)'),
    'Stock_TwoStory_2F':  ('LAYOUT_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F', 'bovenverdieping 9x8'),
    'Stock_Lab':          ('LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB', 'groot interieur 13x13, lab (TestMap)'),
}

# Layouts die blijven (alle andere gaan weg in hoenn_eruit.py).
KEEP_LAYOUTS = [
    'LAYOUT_START_TOWN',
    'LAYOUT_TEST_MAP',
    'LAYOUT_POKEMON_CENTER_1F',
    'LAYOUT_POKEMON_CENTER_2F',
    'LAYOUT_MART',
] + [v[0] for v in STOCK_HOUSES.values()]

# Kaarten in de nieuwe groep, in volgorde.
MAPS = [
    'StartTown',
    'StartTown_PokemonCenter_1F',
    'StartTown_PokemonCenter_2F',
    'StartTown_Mart',
] + list(STOCK_HOUSES) + ['TestMap']
