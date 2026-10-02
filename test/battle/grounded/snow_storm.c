#include "global.h"
#include "test/battle.h"

// Project Grounded: Hail heet Snow Storm: 1/16 schade per beurt voor niet-Ice-types én Ice-types +50% Def (zoals Snowscape).
SINGLE_BATTLE_TEST("Snow Storm deals 1/16 damage per turn to non-Ice types")
{
    s16 damage;

    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_GLALIE, 0) == TYPE_ICE);
        PLAYER(SPECIES_GLALIE);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_HAIL); }
    } SCENE {
        MESSAGE("A snow storm started!");
        MESSAGE("The opposing Wobbuffet is buffeted by the snow storm!");
        HP_BAR(opponent, captureDamage: &damage);
    } THEN { EXPECT_EQ(damage, opponent->maxHP / 16); }
}

SINGLE_BATTLE_TEST("Snow Storm multiplies the defense of Ice-types by 1.5x", s16 damage)
{
    u16 move;
    PARAMETRIZE { move = MOVE_HAIL; }
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_GLALIE);
    } WHEN {
        TURN { MOVE(opponent, move); }
        TURN { MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(1.5), results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Snowscape stays harmless")
{
    GIVEN {
        PLAYER(SPECIES_GLALIE);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_SNOWSCAPE); }
    } SCENE {
        NOT HP_BAR(opponent);
    }
}
