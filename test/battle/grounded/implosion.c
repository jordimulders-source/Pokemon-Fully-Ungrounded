#include "global.h"
#include "test/battle.h"

// Project Grounded: Implosion - Dark, special, 200 BP, self-KO. Daarna een zwart gat (5 beurten): alle hazards weg,
// en elke Pokémon die het veld op komt (beide kanten) krijgt -1 Atk en -1 SpAtk.
ASSUMPTIONS
{
    ASSUME(IsExplosionMove(MOVE_IMPLOSION));
    ASSUME(GetMoveType(MOVE_IMPLOSION) == TYPE_DARK);
    ASSUME(GetMoveCategory(MOVE_IMPLOSION) == DAMAGE_CATEGORY_SPECIAL);
}

SINGLE_BATTLE_TEST("Implosion makes the user faint and forms a black hole that lowers Atk and SpAtk on switch-in")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_IMPLOSION); }
        PLAYER(SPECIES_WYNAUT);
        OPPONENT(SPECIES_WOBBUFFET) { HP(1000); MaxHP(1000); }
    } WHEN {
        TURN { MOVE(player, MOVE_IMPLOSION); SEND_OUT(player, 1); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_IMPLOSION, player);
        MESSAGE("The implosion left a black hole!\pEvery hazard, screen and stat change\non the field was swallowed up!");
        MESSAGE("Wobbuffet fainted!");
        MESSAGE("Wynaut is pulled\ntoward the black hole!");
        MESSAGE("Wynaut's Attack fell!");
        MESSAGE("Wynaut's Sp. Atk fell!");
    } THEN {
        EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE - 1);
        EXPECT_EQ(player->statStages[STAT_SPATK], DEFAULT_STAT_STAGE - 1);
    }
}

SINGLE_BATTLE_TEST("Implosion removes hazards on both sides")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_STEALTH_ROCK) == EFFECT_STEALTH_ROCK);
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_IMPLOSION, MOVE_STEALTH_ROCK); }
        PLAYER(SPECIES_WYNAUT);
        OPPONENT(SPECIES_WOBBUFFET) { HP(1000); MaxHP(1000); Moves(MOVE_STEALTH_ROCK, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_STEALTH_ROCK); MOVE(opponent, MOVE_STEALTH_ROCK); }
        TURN { MOVE(player, MOVE_IMPLOSION); SEND_OUT(player, 1); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_IMPLOSION, player);
        MESSAGE("Wynaut is pulled\ntoward the black hole!");
        NOT HP_BAR(player);
    }
}

SINGLE_BATTLE_TEST("The black hole of Implosion lasts 5 turns")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_IMPLOSION); }
        PLAYER(SPECIES_WYNAUT) { Moves(MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { HP(1000); MaxHP(1000); Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_IMPLOSION); SEND_OUT(player, 1); }
        TURN { }
        TURN { }
        TURN { }
        TURN { }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_IMPLOSION, player);
        MESSAGE("The black hole evaporated.\nThanks, Hawking.");
    }
}
