#include "global.h"
#include "test/battle.h"

// Project Grounded: Marionette (930, Banette). Een gok zoals Sucker Punch: het doelwit raakt zichzelf met de
// aanval die het deze beurt koos (eigen actie vervalt), of met zijn laatste move als het al gehandeld heeft.
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

SINGLE_BATTLE_TEST("Marionette makes a target that has not moved yet use its chosen attack on itself")
{
    s16 tackleDmg, selfDmg;
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); Moves(MOVE_TACKLE, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_CELEBRATE); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
        HP_BAR(player, captureDamage: &tackleDmg);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("Wobbuffet pulled the opposing Wobbuffet's strings!");
        MESSAGE("The opposing Wobbuffet hit itself with Tackle!");
        HP_BAR(opponent, captureDamage: &selfDmg);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
    } THEN {
        EXPECT_EQ(selfDmg, tackleDmg);
        EXPECT_EQ(opponent->pp[0], GetMovePP(MOVE_TACKLE) - 2);
    }
}

SINGLE_BATTLE_TEST("Marionette fails if the target chose a status move, which then goes through")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_SWORDS_DANCE); }
    } SCENE {
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("But it failed!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SWORDS_DANCE, opponent);
    }
}

SINGLE_BATTLE_TEST("Marionette fails if the target chose a move without fixed power")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_SEISMIC_TOSS); }
    } SCENE {
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("But it failed!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SEISMIC_TOSS, opponent);
    }
}

SINGLE_BATTLE_TEST("Marionette fails if the target switches out")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
        OPPONENT(SPECIES_WYNAUT) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_CELEBRATE); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(player, MOVE_MARIONETTE); SWITCH(opponent, 1); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("But it failed!");
    }
}

SINGLE_BATTLE_TEST("Marionette uses the last move of a target that already moved this turn")
{
    s16 tackleDmg, selfDmg;
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(50); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
        HP_BAR(player, captureDamage: &tackleDmg);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("The opposing Wobbuffet hit itself with Tackle!");
        HP_BAR(opponent, captureDamage: &selfDmg);
    } THEN {
        EXPECT_EQ(selfDmg, tackleDmg);
    }
}

SINGLE_BATTLE_TEST("Marionette fails if a faster target used a status move this turn")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(50); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("But it failed!");
    }
}

SINGLE_BATTLE_TEST("Marionette works on consecutive turns")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(50); }
    } WHEN {
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_TACKLE); }
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("The opposing Wobbuffet hit itself with Tackle!");
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("The opposing Wobbuffet hit itself with Tackle!");
    } THEN {
        EXPECT_EQ(opponent->pp[0], GetMovePP(MOVE_TACKLE) - 2);
    }
}

SINGLE_BATTLE_TEST("Marionette boosted by Prankster does not affect Dark types")
{
    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_UMBREON, 0) == TYPE_DARK || GetSpeciesType(SPECIES_UMBREON, 1) == TYPE_DARK);
        PLAYER(SPECIES_BANETTE) { Ability(ABILITY_PRANKSTER); Speed(50); }
        OPPONENT(SPECIES_UMBREON) { Speed(100); }
    } WHEN {
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_EMBER); }
    } SCENE {
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("It doesn't affect the opposing Umbreon…");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_EMBER, opponent);
    }
}

SINGLE_BATTLE_TEST("Marionette with Prankster goes first against a faster target")
{
    GIVEN {
        PLAYER(SPECIES_BANETTE) { Ability(ABILITY_PRANKSTER); Speed(50); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(player, MOVE_MARIONETTE); MOVE(opponent, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MARIONETTE, player);
        MESSAGE("The opposing Wobbuffet hit itself with Tackle!");
        HP_BAR(opponent);
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, opponent);
    }
}
