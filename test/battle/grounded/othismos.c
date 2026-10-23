#include "global.h"
#include "test/battle.h"

// Project Grounded: Othismos (Falinks) - 20 power per treffer, 1 + 4 x HP/maxHP treffers (5 bij volle HP).
SINGLE_BATTLE_TEST("Othismos hits 5 times at full HP")
{
    GIVEN {
        ASSUME(GetMovePower(MOVE_OTHISMOS) == 20);
        PLAYER(SPECIES_FALINKS) { HP(100); MaxHP(100); }
        OPPONENT(SPECIES_WOBBUFFET) { HP(500); MaxHP(500); }
    } WHEN {
        TURN { MOVE(player, MOVE_OTHISMOS); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_OTHISMOS, player);
        MESSAGE("The Pokémon was hit 5 times!");
    }
}

SINGLE_BATTLE_TEST("Othismos hits 3 times at half HP")
{
    GIVEN {
        PLAYER(SPECIES_FALINKS) { HP(50); MaxHP(100); }
        OPPONENT(SPECIES_WOBBUFFET) { HP(500); MaxHP(500); }
    } WHEN {
        TURN { MOVE(player, MOVE_OTHISMOS); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_OTHISMOS, player);
        MESSAGE("The Pokémon was hit 3 times!");
    }
}

SINGLE_BATTLE_TEST("Othismos hits once below a quarter HP")
{
    GIVEN {
        PLAYER(SPECIES_FALINKS) { HP(20); MaxHP(100); }
        OPPONENT(SPECIES_WOBBUFFET) { HP(500); MaxHP(500); }
    } WHEN {
        TURN { MOVE(player, MOVE_OTHISMOS); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_OTHISMOS, player);
        MESSAGE("The Pokémon was hit 1 time!");
    }
}
