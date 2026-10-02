#include "global.h"
#include "test/battle.h"

// Project Grounded: Transmutation - omgekeerde Transform: het doelwit wordt een kopie van de gebruiker (moves met 5 PP).
ASSUMPTIONS
{
    ASSUME(GetMoveEffect(MOVE_TRANSMUTATION) == EFFECT_TRANSMUTATION);
}

SINGLE_BATTLE_TEST("Transmutation turns the target into a copy of the user")
{
    GIVEN {
        PLAYER(SPECIES_ALAKAZAM) { Speed(20); Moves(MOVE_TRANSMUTATION, MOVE_PSYCHIC); }
        OPPONENT(SPECIES_MACHAMP) { Speed(10); Moves(MOVE_CROSS_CHOP); }
    } WHEN {
        TURN { MOVE(player, MOVE_TRANSMUTATION); MOVE(opponent, MOVE_CROSS_CHOP); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TRANSMUTATION, opponent); // de animatie speelt op het doelwit
        MESSAGE("The opposing Machamp was transmuted\ninto Alakazam!");
    } THEN {
        EXPECT_EQ(opponent->species, SPECIES_ALAKAZAM);
        EXPECT_EQ(opponent->moves[0], MOVE_TRANSMUTATION);
        EXPECT_EQ(opponent->moves[1], MOVE_PSYCHIC);
        EXPECT_EQ(opponent->pp[1], 5);
        EXPECT_EQ(opponent->spAttack, player->spAttack);
        EXPECT_EQ(opponent->types[0], player->types[0]);
    }
}

SINGLE_BATTLE_TEST("Transmutation fails on a target that is already transformed")
{
    GIVEN {
        PLAYER(SPECIES_ALAKAZAM) { Speed(20); Moves(MOVE_TRANSMUTATION, MOVE_PSYCHIC); }
        OPPONENT(SPECIES_MACHAMP) { Speed(10); Moves(MOVE_CROSS_CHOP, MOVE_PSYCHIC); }
    } WHEN {
        TURN { MOVE(player, MOVE_TRANSMUTATION); MOVE(opponent, MOVE_CROSS_CHOP); }
        TURN { MOVE(player, MOVE_TRANSMUTATION); MOVE(opponent, MOVE_PSYCHIC); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TRANSMUTATION, opponent); // de animatie speelt op het doelwit
        MESSAGE("Alakazam used Transmutation!");
        MESSAGE("But it failed!");
    }
}
