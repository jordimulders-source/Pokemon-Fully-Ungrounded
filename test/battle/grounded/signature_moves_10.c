#include "global.h"
#include "test/battle.h"

// Project Grounded: tiende ronde moves (TM99 Disco Inferno, TM100 Super Splash, Overkill).
// Let op: Wobbuffet is in deze rom Psychic/Normal.

TEST("Project Grounded moves round 10 have the agreed data")
{
    EXPECT_EQ(GetMoveEffect(MOVE_SUPER_SPLASH), EFFECT_FUTURE_SIGHT);
    EXPECT_EQ(GetMoveType(MOVE_SUPER_SPLASH), TYPE_WATER);
    EXPECT_EQ(GetMoveCategory(MOVE_SUPER_SPLASH), DAMAGE_CATEGORY_PHYSICAL);
    EXPECT_EQ(GetMovePower(MOVE_SUPER_SPLASH), 120);
    EXPECT_EQ(GetMoveAccuracy(MOVE_SUPER_SPLASH), 100);
    EXPECT_EQ(GetMovePP(MOVE_SUPER_SPLASH), 5);

    EXPECT_EQ(GetMoveType(MOVE_DISCO_INFERNO), TYPE_FIRE);
    EXPECT_EQ(GetMoveCategory(MOVE_DISCO_INFERNO), DAMAGE_CATEGORY_PHYSICAL);
    EXPECT_EQ(GetMovePower(MOVE_DISCO_INFERNO), 85);
    EXPECT_EQ(GetMovePP(MOVE_DISCO_INFERNO), 10);
    EXPECT(MoveMakesContact(MOVE_DISCO_INFERNO));
    EXPECT(IsDanceMove(MOVE_DISCO_INFERNO));
    EXPECT_EQ(GetMoveAdditionalEffectCount(MOVE_DISCO_INFERNO), 2);
    EXPECT_EQ(GetMoveAdditionalEffectById(MOVE_DISCO_INFERNO, 0)->moveEffect, MOVE_EFFECT_CONFUSION);
    EXPECT_EQ(GetMoveAdditionalEffectById(MOVE_DISCO_INFERNO, 0)->chance, 20);
    EXPECT_EQ(GetMoveAdditionalEffectById(MOVE_DISCO_INFERNO, 1)->moveEffect, MOVE_EFFECT_BURN);
    EXPECT_EQ(GetMoveAdditionalEffectById(MOVE_DISCO_INFERNO, 1)->chance, 10);

    EXPECT_EQ(GetMoveEffect(MOVE_OVERKILL), EFFECT_OVERKILL);
    EXPECT_EQ(GetMoveType(MOVE_OVERKILL), TYPE_DARK);
    EXPECT_EQ(GetMoveCategory(MOVE_OVERKILL), DAMAGE_CATEGORY_PHYSICAL);
    EXPECT_EQ(GetMovePower(MOVE_OVERKILL), 90);
    EXPECT(MoveMakesContact(MOVE_OVERKILL));
}

// Super Splash: beurt 1 niets (behalve de melding), aan het eind van beurt 2 de tsunami.
SINGLE_BATTLE_TEST("Super Splash does nothing on the first turn and hits at the end of the next turn")
{
    GIVEN {
        PLAYER(SPECIES_GYARADOS);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_SUPER_SPLASH); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SUPER_SPLASH, player);
        MESSAGE("But nothing happened… yet!");
        NOT HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, player);
        MESSAGE("A tsunami crashed into the opposing Wobbuffet!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SUPER_SPLASH, player);
        HP_BAR(opponent);
    }
}

// Super Splash is fysiek: hangt af van Attack, niet van Sp. Atk.
SINGLE_BATTLE_TEST("Super Splash uses the user's Attack", s16 damage)
{
    u32 atk = 100, spAtk = 100;
    PARAMETRIZE { atk = 100; spAtk = 100; }
    PARAMETRIZE { atk = 200; spAtk = 100; }
    PARAMETRIZE { atk = 100; spAtk = 200; }
    GIVEN {
        PLAYER(SPECIES_GYARADOS) { Attack(atk); SpAttack(spAtk); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_SUPER_SPLASH); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SUPER_SPLASH, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_GT(results[1].damage, results[0].damage);
        EXPECT_EQ(results[2].damage, results[0].damage);
    }
}

// Super Splash stapelt niet: zolang er een tsunami onderweg is, mislukt een tweede.
SINGLE_BATTLE_TEST("Super Splash fails while a tsunami is already on its way")
{
    GIVEN {
        PLAYER(SPECIES_GYARADOS);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_SUPER_SPLASH); }
        TURN { MOVE(player, MOVE_SUPER_SPLASH); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SUPER_SPLASH, player);
        MESSAGE("But nothing happened… yet!");
        MESSAGE("Gyarados used Super Splash!");
        MESSAGE("But it failed!");
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SUPER_SPLASH, player);
    }
}

// Disco Inferno: kan verwarren (discokoorts) en verbranden.
SINGLE_BATTLE_TEST("Disco Inferno can confuse the target")
{
    GIVEN {
        PLAYER(SPECIES_MAGMAR);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_DISCO_INFERNO, WITH_RNG(RNG_SECONDARY_EFFECT, TRUE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DISCO_INFERNO, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_CONFUSION, opponent);
        MESSAGE("The opposing Wobbuffet became confused!");
    }
}

// Disco Inferno is een dansmove: Dancer kopieert hem.
SINGLE_BATTLE_TEST("Disco Inferno is copied by Dancer")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_ORICORIO) { Ability(ABILITY_DANCER); }
    } WHEN {
        TURN { MOVE(player, MOVE_DISCO_INFERNO, WITH_RNG(RNG_SECONDARY_EFFECT, FALSE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DISCO_INFERNO, player);
        ABILITY_POPUP(opponent, ABILITY_DANCER);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_DISCO_INFERNO, opponent);
    }
}

// Overkill: de overtollige schade (berekend min resterende HP) raakt de volgende die binnenkomt.
SINGLE_BATTLE_TEST("Overkill stores the overflow damage and hits the next switch-in with it", s16 damage)
{
    u32 hp = 1;
    PARAMETRIZE { hp = 1; }
    PARAMETRIZE { hp = 11; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET) { HP(hp); }
        OPPONENT(SPECIES_BLISSEY);
    } WHEN {
        TURN { MOVE(player, MOVE_OVERKILL); SEND_OUT(opponent, 1); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_OVERKILL, player);
        MESSAGE("The opposing Wobbuffet fainted!");
        MESSAGE("The leftover beating is waiting for the next one in line…");
        HP_BAR(opponent, captureDamage: &results[i].damage);
        MESSAGE("The leftover beating hit the opposing Blissey!");
    } FINALLY {
        EXPECT_GT(results[0].damage, 0);
        EXPECT_EQ(results[0].damage - results[1].damage, 10);
    }
}

// Overkill: hoogstens de helft van de max-HP van wie binnenkomt, en daarna is hij weg.
SINGLE_BATTLE_TEST("Overkill's leftover beating is capped at half of the switch-in's max HP and is used up")
{
    s16 damage;
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET) { HP(1); }
        OPPONENT(SPECIES_WYNAUT) { MaxHP(40); HP(40); }
        OPPONENT(SPECIES_WYNAUT);
    } WHEN {
        TURN { MOVE(player, MOVE_OVERKILL); SEND_OUT(opponent, 1); }
        TURN { SWITCH(opponent, 2); }
    } SCENE {
        MESSAGE("The opposing Wobbuffet fainted!");
        HP_BAR(opponent, captureDamage: &damage);
        MESSAGE("The leftover beating hit the opposing Wynaut!");
        NOT MESSAGE("The leftover beating hit the opposing Wynaut!");
    } THEN {
        EXPECT_EQ(damage, 20);
        EXPECT(!IsHazardOnSide(B_SIDE_OPPONENT, HAZARDS_OVERKILL));
    }
}

// Overkill: Heavy-Duty Boots beschermen; de schade blijft dan liggen.
SINGLE_BATTLE_TEST("Overkill's leftover beating does not hit a switch-in with Heavy-Duty Boots")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET) { HP(1); }
        OPPONENT(SPECIES_WYNAUT) { Item(ITEM_HEAVY_DUTY_BOOTS); }
    } WHEN {
        TURN { MOVE(player, MOVE_OVERKILL); SEND_OUT(opponent, 1); }
    } SCENE {
        MESSAGE("The opposing Wobbuffet fainted!");
        NONE_OF {
            MESSAGE("The leftover beating hit the opposing Wynaut!");
            HP_BAR(opponent);
        }
    } THEN {
        EXPECT(IsHazardOnSide(B_SIDE_OPPONENT, HAZARDS_OVERKILL));
    }
}

// Overkill zonder KO laat niets liggen.
SINGLE_BATTLE_TEST("Overkill stores nothing if the target survives")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_BLISSEY);
    } WHEN {
        TURN { MOVE(player, MOVE_OVERKILL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_OVERKILL, player);
        NOT MESSAGE("The leftover beating is waiting for the next one in line…");
    } THEN {
        EXPECT(!IsHazardOnSide(B_SIDE_OPPONENT, HAZARDS_OVERKILL));
    }
}
