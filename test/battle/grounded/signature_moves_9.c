#include "global.h"
#include "test/battle.h"
#include "text.h"

// Project Grounded: negende ronde moves (920-926) en ability Trade Wind (319).
// Let op: Wobbuffet is in deze rom Psychic/Normal (immuun voor Ghost).

TEST("Project Grounded moves round 9 have the agreed data")
{
    EXPECT_EQ(GetMoveEffect(MOVE_COLD_SHOULDER), EFFECT_COLD_SHOULDER);
    EXPECT_EQ(GetMoveType(MOVE_COLD_SHOULDER), TYPE_ICE);
    EXPECT_EQ(GetMoveCategory(MOVE_COLD_SHOULDER), DAMAGE_CATEGORY_PHYSICAL);
    EXPECT_EQ(GetMovePower(MOVE_COLD_SHOULDER), 75);
    EXPECT_EQ(GetMovePP(MOVE_COLD_SHOULDER), 15);
    EXPECT(MoveMakesContact(MOVE_COLD_SHOULDER));

    EXPECT_EQ(GetMoveEffect(MOVE_JUMP_SCARE), EFFECT_JUMP_SCARE);
    EXPECT_EQ(GetMoveType(MOVE_JUMP_SCARE), TYPE_GHOST);
    EXPECT_EQ(GetMovePower(MOVE_JUMP_SCARE), 80);
    EXPECT(MoveMakesContact(MOVE_JUMP_SCARE));
    EXPECT(MoveHasAdditionalEffectWithChance(MOVE_JUMP_SCARE, MOVE_EFFECT_FLINCH, 30));

    EXPECT_EQ(GetMoveEffect(MOVE_DIM_MAK), EFFECT_DIM_MAK);
    EXPECT_EQ(GetMoveType(MOVE_DIM_MAK), TYPE_PSYCHIC);
    EXPECT_EQ(GetMoveCategory(MOVE_DIM_MAK), DAMAGE_CATEGORY_PHYSICAL);
    EXPECT_EQ(GetMovePower(MOVE_DIM_MAK), 75);
    EXPECT(MoveIgnoresDefenseEvasionStages(MOVE_DIM_MAK));
    EXPECT(MoveHasAdditionalEffectWithChance(MOVE_DIM_MAK, MOVE_EFFECT_PARALYSIS, 30));

    EXPECT_EQ(GetMoveEffect(MOVE_UPDRAFT), EFFECT_UPDRAFT);
    EXPECT_EQ(GetMoveType(MOVE_UPDRAFT), TYPE_FLYING);
    EXPECT_EQ(GetMoveCategory(MOVE_UPDRAFT), DAMAGE_CATEGORY_SPECIAL);
    EXPECT(IsWindMove(MOVE_UPDRAFT));

    EXPECT_EQ(GetMoveEffect(MOVE_COUNTERFEIT_BALL), EFFECT_MULTI_HIT);
    EXPECT_EQ(GetMovePower(MOVE_COUNTERFEIT_BALL), 25);
    EXPECT(IsBallisticMove(MOVE_COUNTERFEIT_BALL));

    EXPECT_EQ(GetMoveType(MOVE_HOT_TAKE), TYPE_FIRE);
    EXPECT_EQ(GetMoveCategory(MOVE_HOT_TAKE), DAMAGE_CATEGORY_SPECIAL);
    EXPECT_EQ(GetMovePower(MOVE_HOT_TAKE), 85);
    EXPECT(MoveHasAdditionalEffectWithChance(MOVE_HOT_TAKE, MOVE_EFFECT_CONFUSION, 20));

    EXPECT_EQ(GetMoveEffect(MOVE_BRAMBLE_LASH), EFFECT_BRAMBLE_LASH);
    EXPECT_EQ(GetMoveType(MOVE_BRAMBLE_LASH), TYPE_GRASS);
    EXPECT(MoveMakesContact(MOVE_BRAMBLE_LASH));
}

// Cold Shoulder: het doelwit kan zijn laatste move de volgende beurt niet gebruiken, daarna weer wel.
SINGLE_BATTLE_TEST("Cold Shoulder stops the target from using its last move next turn only")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); Moves(MOVE_SCRATCH, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SCRATCH); MOVE(player, MOVE_COLD_SHOULDER); }
        TURN { MOVE(opponent, MOVE_SCRATCH, allowed: FALSE); MOVE(opponent, MOVE_CELEBRATE); MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(opponent, MOVE_CELEBRATE); MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(opponent, MOVE_SCRATCH); MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COLD_SHOULDER, player);
        MESSAGE("Wobbuffet gave the opposing Wobbuffet the cold shoulder!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
    }
}

// Cold Shoulder geldt dynamisch voor de move die het doelwit in de beurt van de klap gebruikt (ook als het daarna komt).
SINGLE_BATTLE_TEST("Cold Shoulder also blocks the move a slower target uses after being hit")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); Moves(MOVE_SCRATCH, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_COLD_SHOULDER); MOVE(opponent, MOVE_SCRATCH); }
        TURN { MOVE(opponent, MOVE_SCRATCH, allowed: FALSE); MOVE(opponent, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COLD_SHOULDER, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
    }
}

// Jump Scare: dubbele kracht in de eerste beurt na het binnenkomen (zoals Fake Out).
SINGLE_BATTLE_TEST("Jump Scare doubles in power on the user's first turn", s16 damage)
{
    bool32 firstTurn;
    PARAMETRIZE { firstTurn = TRUE; }
    PARAMETRIZE { firstTurn = FALSE; }
    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_SQUIRTLE, 0) == TYPE_WATER);
        ASSUME(GetSpeciesType(SPECIES_SQUIRTLE, 1) == TYPE_WATER);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_SQUIRTLE);
    } WHEN {
        if (!firstTurn)
            TURN { MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_JUMP_SCARE, criticalHit: FALSE, WITH_RNG(RNG_SECONDARY_EFFECT, FALSE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_JUMP_SCARE, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[1].damage, Q_4_12(2.0), results[0].damage);
    }
}

// Dim Mak negeert Defense-boosts van het doelwit.
SINGLE_BATTLE_TEST("Dim Mak ignores the target's Defense boosts", s16 damage)
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_IRON_DEFENSE; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_SQUIRTLE) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_DIM_MAK, criticalHit: FALSE, WITH_RNG(RNG_SECONDARY_EFFECT, FALSE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DIM_MAK, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_EQ(results[0].damage, results[1].damage);
    }
}

// Dim Mak werkt niet op een doelwit met Unaware.
SINGLE_BATTLE_TEST("Dim Mak doesn't affect a target with Unaware")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_QUAGSIRE) { Ability(ABILITY_UNAWARE); }
    } WHEN {
        TURN { MOVE(player, MOVE_DIM_MAK); }
    } SCENE {
        NONE_OF { ANIMATION(ANIM_TYPE_MOVE, MOVE_DIM_MAK, player); HP_BAR(opponent); }
        ABILITY_POPUP(opponent, ABILITY_UNAWARE);
        MESSAGE("The opposing Quagsire doesn't know where its pressure points are!");
    }
}

// Updraft: 1,5x met Tailwind aan de eigen kant.
SINGLE_BATTLE_TEST("Updraft is 1.5x stronger with Tailwind on the user's side", s16 damage)
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_TAILWIND; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, move); }
        TURN { MOVE(player, MOVE_UPDRAFT, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_UPDRAFT, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(1.5), results[1].damage);
    }
}

// Counterfeit Ball: met Skill Link 5 ballen; 1 op 10 is de laatste een nep-Master Ball die altijd crit.
SINGLE_BATTLE_TEST("Counterfeit Ball's fake Master Ball always crits on the last hit")
{
    GIVEN {
        PLAYER(SPECIES_CINCCINO) { Ability(ABILITY_SKILL_LINK); }
        OPPONENT(SPECIES_WOBBUFFET) { HP(500); MaxHP(500); }
    } WHEN {
        TURN { MOVE(player, MOVE_COUNTERFEIT_BALL, WITH_RNG(RNG_COUNTERFEIT_BALL, TRUE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COUNTERFEIT_BALL, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COUNTERFEIT_BALL, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COUNTERFEIT_BALL, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COUNTERFEIT_BALL, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COUNTERFEIT_BALL, player);
        MESSAGE("A critical hit!");
        MESSAGE("It was a fake MASTER BALL! It still hurt.");
        MESSAGE("The Pokémon was hit 5 time(s)!");
    }
}

SINGLE_BATTLE_TEST("Counterfeit Ball without the fake Master Ball has no message")
{
    GIVEN {
        PLAYER(SPECIES_CINCCINO) { Ability(ABILITY_SKILL_LINK); }
        OPPONENT(SPECIES_WOBBUFFET) { HP(500); MaxHP(500); }
    } WHEN {
        TURN { MOVE(player, MOVE_COUNTERFEIT_BALL, WITH_RNG(RNG_COUNTERFEIT_BALL, FALSE), criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COUNTERFEIT_BALL, player);
        NONE_OF { MESSAGE("It was a fake MASTER BALL! It still hurt."); }
        MESSAGE("The Pokémon was hit 5 time(s)!");
    }
}

SINGLE_BATTLE_TEST("Counterfeit Ball is blocked by Bulletproof")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_CHESPIN) { Ability(ABILITY_BULLETPROOF); }
    } WHEN {
        TURN { MOVE(player, MOVE_COUNTERFEIT_BALL); }
    } SCENE {
        NONE_OF { ANIMATION(ANIM_TYPE_MOVE, MOVE_COUNTERFEIT_BALL, player); }
        ABILITY_POPUP(opponent, ABILITY_BULLETPROOF);
    }
}

// Hot Take: eigen verwarringsmelding.
SINGLE_BATTLE_TEST("Hot Take can confuse the target with its own message")
{
    GIVEN {
        PLAYER(SPECIES_MAGMAR);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_HOT_TAKE, WITH_RNG(RNG_SECONDARY_EFFECT, TRUE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_HOT_TAKE, player);
        HP_BAR(opponent);
        MESSAGE("The opposing Wobbuffet got ratioed and became confused!");
    }
}

// Bramble Lash legt doornen: 1/16 bij binnenkomst, ook voor vliegers; een laag.
SINGLE_BATTLE_TEST("Bramble Lash lays brambles that hurt 1/16 on entry, even Flying types")
{
    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_PIDGEY, 0) == TYPE_FLYING || GetSpeciesType(SPECIES_PIDGEY, 1) == TYPE_FLYING);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_PIDGEY);
    } WHEN {
        TURN { MOVE(player, MOVE_BRAMBLE_LASH); }
        TURN { MOVE(player, MOVE_BRAMBLE_LASH); }
        TURN { SWITCH(opponent, 1); }
    } SCENE {
        s32 maxHP = GetMonData(&OPPONENT_PARTY[1], MON_DATA_MAX_HP);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BRAMBLE_LASH, player);
        HP_BAR(opponent);
        MESSAGE("Thorny brambles sprang up around the opposing team!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BRAMBLE_LASH, player);
        HP_BAR(opponent);
        NOT MESSAGE("Thorny brambles sprang up around the opposing team!");
        MESSAGE("2 sent out Pidgey!");
        HP_BAR(opponent, damage: maxHP / 16);
        MESSAGE("The opposing Pidgey got snagged on the brambles!");
    }
}

SINGLE_BATTLE_TEST("Bramble Lash's brambles don't hurt a holder of Heavy-Duty Boots")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET) { Item(ITEM_HEAVY_DUTY_BOOTS); }
    } WHEN {
        TURN { MOVE(player, MOVE_BRAMBLE_LASH); }
        TURN { SWITCH(opponent, 1); }
    } SCENE {
        MESSAGE("Thorny brambles sprang up around the opposing team!");
        MESSAGE("2 sent out Wobbuffet!");
        NOT MESSAGE("The opposing Wobbuffet got snagged on the brambles!");
    }
}

SINGLE_BATTLE_TEST("Rapid Spin clears Bramble Lash's brambles")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); }
    } WHEN {
        TURN { MOVE(player, MOVE_BRAMBLE_LASH); MOVE(opponent, MOVE_RAPID_SPIN); }
        TURN { SWITCH(opponent, 1); }
    } SCENE {
        MESSAGE("Thorny brambles sprang up around the opposing team!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_RAPID_SPIN, opponent);
        MESSAGE("The opposing Wobbuffet cleared away the brambles!");
        MESSAGE("2 sent out Wobbuffet!");
        NOT MESSAGE("The opposing Wobbuffet got snagged on the brambles!");
    }
}

// Trade Wind: 3 beurten Tailwind bij binnenkomst.
SINGLE_BATTLE_TEST("Trade Wind sets up a 3-turn Tailwind on entry")
{
    GIVEN {
        PLAYER(SPECIES_PIDOVE) { Ability(ABILITY_TRADE_WIND); Speed(10); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(15); }
    } WHEN {
        TURN {}
        TURN {}
        TURN {}
        TURN {}
    } SCENE {
        ABILITY_POPUP(player, ABILITY_TRADE_WIND);
        MESSAGE("The Tailwind blew from behind your team!");
        MESSAGE("Pidove used Celebrate!");
        MESSAGE("The opposing Wobbuffet used Celebrate!");
        MESSAGE("Pidove used Celebrate!");
        MESSAGE("The opposing Wobbuffet used Celebrate!");
        MESSAGE("Pidove used Celebrate!");
        MESSAGE("The opposing Wobbuffet used Celebrate!");
        MESSAGE("Your team's Tailwind petered out!");
        MESSAGE("The opposing Wobbuffet used Celebrate!");
        MESSAGE("Pidove used Celebrate!");
    }
}

SINGLE_BATTLE_TEST("Trade Wind does nothing if Tailwind is already up")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        PLAYER(SPECIES_PIDOVE) { Ability(ABILITY_TRADE_WIND); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_TAILWIND); }
        TURN { SWITCH(player, 1); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TAILWIND, player);
        NONE_OF { ABILITY_POPUP(player, ABILITY_TRADE_WIND); }
    }
}

// Namen en beschrijvingen passen op de schermen.
TEST("Project Grounded moves round 9 names and descriptions fit")
{
    static const u16 moves[] = {MOVE_COLD_SHOULDER, MOVE_JUMP_SCARE, MOVE_DIM_MAK, MOVE_UPDRAFT, MOVE_COUNTERFEIT_BALL, MOVE_HOT_TAKE, MOVE_BRAMBLE_LASH};
    u32 i, move = MOVE_NONE;
    for (i = 0; i < ARRAY_COUNT(moves); i++)
    {
        PARAMETRIZE_LABEL("%S", GetMoveName(moves[i])) { move = moves[i]; }
    }
    EXPECT_LE(GetStringWidth(FONT_NARROWER, GetMoveName(move), 0), 64);
    EXPECT_LE(GetStringWidth(FONT_NORMAL, GetMoveDescription(move), 0), 152);
}
