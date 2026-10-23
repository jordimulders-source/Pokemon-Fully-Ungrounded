#include "global.h"
#include "test/battle.h"

// Project Grounded: Laser Beam - Psychic, special, 75 BP. Gaat door Protect, breekt Reflect/Light Screen
// en negeert de defense-boosts van het doelwit.
ASSUMPTIONS
{
    ASSUME(GetMoveType(MOVE_LASER_BEAM) == TYPE_PSYCHIC);
    ASSUME(GetMovePower(MOVE_LASER_BEAM) == 75);
}

SINGLE_BATTLE_TEST("Laser Beam goes through Protect")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_LASER_BEAM); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_PROTECT); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_PROTECT); MOVE(player, MOVE_LASER_BEAM); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PROTECT, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_LASER_BEAM, player);
        HP_BAR(opponent);
    }
}

SINGLE_BATTLE_TEST("Laser Beam breaks Light Screen")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_LASER_BEAM); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_LIGHT_SCREEN); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_LIGHT_SCREEN); MOVE(player, MOVE_LASER_BEAM); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_LIGHT_SCREEN, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_LASER_BEAM, player);
        MESSAGE("The opposing side's Light Screen wore off!");
    }
}

SINGLE_BATTLE_TEST("Laser Beam ignores the target's Sp. Def boosts", s16 damage)
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_AMNESIA; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_LASER_BEAM); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_CELEBRATE, MOVE_AMNESIA); }
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_LASER_BEAM); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_EQ(results[0].damage, results[1].damage);
    }
}
