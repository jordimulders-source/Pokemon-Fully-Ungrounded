#include "global.h"
#include "test/battle.h"

// Project Grounded: Marionette (930, Banette). Het doelwit raakt zichzelf met zijn laatst gebruikte move.
// Let op: Wobbuffet is in deze rom Psychic/Normal.

TEST("Marionette has the agreed data")
{
    EXPECT_EQ(GetMoveEffect(MOVE_MARIONETTE), EFFECT_MARIONETTE);
    EXPECT_EQ(GetMoveType(MOVE_MARIONETTE), TYPE_GHOST);
    EXPECT_EQ(GetMoveCategory(MOVE_MARIONETTE), DAMAGE_CATEGORY_STATUS);
    EXPECT_EQ(GetMoveAccuracy(MOVE_MARIONETTE), 100);
    EXPECT_EQ(GetMovePP(MOVE_MARIONETTE), 10);
    EXPECT_EQ(GetMovePriority(MOVE_MARIONETTE), 0);
}

SINGLE_BATTLE_TEST("Marionette makes the target hit itself with its last move as if it attacked itself")
{
    s16 tackleDmg, selfDmg;
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_CELEBRATE); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
        HP_BAR(player, captureDamage: &tackleDmg);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("Wobbuffet pulled the opposing Wobbuffet's strings!");
        MESSAGE("The opposing Wobbuffet hit itself with Tackle!");
        HP_BAR(opponent, captureDamage: &selfDmg);
    } THEN {
        EXPECT_EQ(selfDmg, tackleDmg);
    }
}

SINGLE_BATTLE_TEST("Marionette fails if the target has not used a move yet")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("But it failed!");
    }
}

SINGLE_BATTLE_TEST("Marionette fails if the target's last move was a status move or had no fixed power")
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_SEISMIC_TOSS; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_CELEBRATE); MOVE(opponent, move); }
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, move, opponent);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("But it failed!");
    }
}

SINGLE_BATTLE_TEST("Marionette works only once per switch-in")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_CELEBRATE); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("The opposing Wobbuffet hit itself with Tackle!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("But it failed!");
    }
}

SINGLE_BATTLE_TEST("Marionette boosted by Prankster does not affect Dark types")
{
    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_UMBREON, 0) == TYPE_DARK || GetSpeciesType(SPECIES_UMBREON, 1) == TYPE_DARK);
        PLAYER(SPECIES_BANETTE) { Ability(ABILITY_PRANKSTER); Speed(100); }
        OPPONENT(SPECIES_UMBREON) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_CELEBRATE); MOVE(opponent, MOVE_EMBER); }
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_EMBER, opponent);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("It doesn't affect the opposing Umbreon…");
    }
}
