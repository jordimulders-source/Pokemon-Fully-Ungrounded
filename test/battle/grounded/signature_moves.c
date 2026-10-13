#include "global.h"
#include "test/battle.h"

// Project Grounded: signature moves van Cofagrigus, Stunfisk, Galar-Stunfisk, Mightyena, Wailord en Luvdisc.

// Mummy's Curse: Ghost 60, bindt het doelwit 4-5 beurten (1/8 per beurt) en zijn ability wordt Mummy.
// Wobbuffet is in deze rom Psychic/Normal (immuun voor Ghost), daarom Abra als doelwit.
SINGLE_BATTLE_TEST("Mummy's Curse binds the target and turns its ability into Mummy")
{
    GIVEN {
        ASSUME(GetMoveType(MOVE_MUMMYS_CURSE) == TYPE_GHOST);
        ASSUME(MoveHasAdditionalEffect(MOVE_MUMMYS_CURSE, MOVE_EFFECT_WRAP));
        ASSUME(MoveHasAdditionalEffect(MOVE_MUMMYS_CURSE, MOVE_EFFECT_MUMMIFY));
        PLAYER(SPECIES_COFAGRIGUS);
        OPPONENT(SPECIES_ABRA) { Ability(ABILITY_INNER_FOCUS); MaxHP(500); HP(500); }
    } WHEN {
        TURN { MOVE(player, MOVE_MUMMYS_CURSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MUMMYS_CURSE, player);
        HP_BAR(opponent);
        MESSAGE("The opposing Abra was wrapped in cursed bandages!");
        ABILITY_POPUP(opponent, ABILITY_INNER_FOCUS);
        MESSAGE("The opposing Abra was mummified! Its ability became Mummy!");
        HP_BAR(opponent); // binding damage at end of turn
    } THEN {
        EXPECT_EQ(opponent->ability, ABILITY_MUMMY);
        EXPECT(opponent->volatiles.wrapped);
    }
}

SINGLE_BATTLE_TEST("Mummy's Curse spreads Mummy to a contact attacker of the mummified target")
{
    GIVEN {
        ASSUME(MoveMakesContact(MOVE_SCRATCH));
        PLAYER(SPECIES_WOBBUFFET) { Ability(ABILITY_SHADOW_TAG); }
        OPPONENT(SPECIES_ABRA) { Ability(ABILITY_INNER_FOCUS); MaxHP(500); HP(500); }
    } WHEN {
        TURN { MOVE(player, MOVE_MUMMYS_CURSE); }
        TURN { MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        ABILITY_POPUP(opponent, ABILITY_MUMMY);
        MESSAGE("Wobbuffet acquired Mummy!");
    } THEN {
        EXPECT_EQ(player->ability, ABILITY_MUMMY);
    }
}

SINGLE_BATTLE_TEST("Mummy's Curse does not overwrite abilities that cannot be overwritten")
{
    GIVEN {
        PLAYER(SPECIES_COFAGRIGUS);
        OPPONENT(SPECIES_MIMIKYU) { Ability(ABILITY_DISGUISE); }
    } WHEN {
        TURN { MOVE(player, MOVE_MUMMYS_CURSE); }
    } SCENE {
        NOT MESSAGE("The opposing Mimikyu was mummified! Its ability became Mummy!");
    } THEN {
        EXPECT_EQ(opponent->ability, ABILITY_DISGUISE);
    }
}

// Zap Trap: Electric 80, contact, het doelwit kan niet meer wisselen, 30% verlamming.
SINGLE_BATTLE_TEST("Zap Trap prevents the target from escaping")
{
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_ZAP_TRAP, MOVE_EFFECT_PREVENT_ESCAPE));
        ASSUME(GetMovePower(MOVE_ZAP_TRAP) == 80);
        PLAYER(SPECIES_STUNFISK);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_ZAP_TRAP); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ZAP_TRAP, player);
        HP_BAR(opponent);
    } THEN {
        EXPECT(opponent->volatiles.escapePrevention);
    }
}

SINGLE_BATTLE_TEST("Zap Trap paralyzes the target 30% of the time")
{
    PASSES_RANDOMLY(30, 100, RNG_SECONDARY_EFFECT_2);
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_ZAP_TRAP, MOVE_EFFECT_PARALYSIS));
        PLAYER(SPECIES_STUNFISK);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_ZAP_TRAP); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ZAP_TRAP, player);
        HP_BAR(opponent);
        STATUS_ICON(opponent, paralysis: TRUE);
    }
}

// Steel Trap: Steel 70, contact, bindt 4-5 beurten en verlaagt Speed met 1.
SINGLE_BATTLE_TEST("Steel Trap binds the target and lowers its Speed")
{
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_STEEL_TRAP, MOVE_EFFECT_WRAP));
        ASSUME(MoveHasAdditionalEffect(MOVE_STEEL_TRAP, MOVE_EFFECT_SPD_MINUS_1));
        PLAYER(SPECIES_STUNFISK_GALAR);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_STEEL_TRAP); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_STEEL_TRAP, player);
        HP_BAR(opponent);
        MESSAGE("The opposing Wobbuffet stepped right into Stunfisk's steel trap!");
        ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_STATS_CHANGE, opponent);
        MESSAGE("The opposing Wobbuffet's Speed fell!");
        HP_BAR(opponent); // binding damage at end of turn
    } THEN {
        EXPECT(opponent->volatiles.wrapped);
        EXPECT_EQ(opponent->statStages[STAT_SPEED], DEFAULT_STAT_STAGE - 1);
    }
}

// Pack Howl: solo +1 Atk +1 Spe, in een dubbelgevecht +1 Atk voor gebruiker en partner.
SINGLE_BATTLE_TEST("Pack Howl raises the user's Attack and Speed when alone")
{
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_PACK_HOWL) == EFFECT_PACK_HOWL);
        PLAYER(SPECIES_MIGHTYENA);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_PACK_HOWL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PACK_HOWL, player);
    } THEN {
        EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(player->statStages[STAT_SPEED], DEFAULT_STAT_STAGE + 1);
    }
}

DOUBLE_BATTLE_TEST("Pack Howl raises the Attack of the user and its partner in a double battle")
{
    GIVEN {
        PLAYER(SPECIES_MIGHTYENA);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(playerLeft, MOVE_PACK_HOWL); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PACK_HOWL, playerLeft);
        MESSAGE("Mightyena's Attack rose!");
        MESSAGE("Wobbuffet's Attack rose!");
    } THEN {
        EXPECT_EQ(playerLeft->statStages[STAT_ATK], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(playerRight->statStages[STAT_ATK], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(playerLeft->statStages[STAT_SPEED], DEFAULT_STAT_STAGE);
    }
}

// Whale Song: Water 70, raakt alle andere Pokemon (ook de partner), 30% slaap.
DOUBLE_BATTLE_TEST("Whale Song hits both opponents and the user's partner")
{
    GIVEN {
        ASSUME(GetMoveTarget(MOVE_WHALE_SONG) == MOVE_TARGET_FOES_AND_ALLY);
        ASSUME(IsSoundMove(MOVE_WHALE_SONG));
        PLAYER(SPECIES_WAILORD);
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(playerLeft, MOVE_WHALE_SONG); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_WHALE_SONG, playerLeft);
        HP_BAR(opponentLeft);
        HP_BAR(playerRight);
        HP_BAR(opponentRight);
    }
}

SINGLE_BATTLE_TEST("Whale Song puts the target to sleep 30% of the time")
{
    PASSES_RANDOMLY(30, 100, RNG_SECONDARY_EFFECT);
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_WHALE_SONG, MOVE_EFFECT_SLEEP));
        PLAYER(SPECIES_WAILORD);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_WHALE_SONG); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_WHALE_SONG, player);
        HP_BAR(opponent);
        STATUS_ICON(opponent, sleep: TRUE);
    }
}

// Heartbreak: Fairy 60, dubbele kracht tegen het andere geslacht of als een van beiden verliefd is; Sp. Atk -1.
SINGLE_BATTLE_TEST("Heartbreak doubles in power against a target of the opposite gender", s16 damage)
{
    u32 gender;
    PARAMETRIZE { gender = MON_MALE; }
    PARAMETRIZE { gender = MON_FEMALE; }
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_HEARTBREAK) == EFFECT_HEARTBREAK);
        PLAYER(SPECIES_WOBBUFFET) { Gender(MON_MALE); }
        OPPONENT(SPECIES_WOBBUFFET) { Gender(gender); }
    } WHEN {
        TURN { MOVE(player, MOVE_HEARTBREAK); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_HEARTBREAK, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(2.0), results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Heartbreak doubles in power if the target is infatuated", s16 damage)
{
    bool32 attract;
    PARAMETRIZE { attract = FALSE; }
    PARAMETRIZE { attract = TRUE; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Gender(MON_MALE); Speed(10); }
        OPPONENT(SPECIES_WOBBUFFET) { Gender(MON_FEMALE); Speed(5); }
    } WHEN {
        if (attract)
            TURN { MOVE(player, MOVE_ATTRACT); }
        TURN { MOVE(player, MOVE_HEARTBREAK); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_HEARTBREAK, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        // Het andere geslacht verdubbelt al; verliefdheid stapelt niet
        EXPECT_EQ(results[0].damage, results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Heartbreak lowers the target's Sp. Atk")
{
    GIVEN {
        PLAYER(SPECIES_LUVDISC);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_HEARTBREAK); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_HEARTBREAK, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_STATS_CHANGE, opponent);
    } THEN {
        EXPECT_EQ(opponent->statStages[STAT_SPATK], DEFAULT_STAT_STAGE - 1);
    }
}

// Hyphal Snare: Grass 75, contact, bindt 4-5 beurten; sporen, dus geen vat op Grass-types.
SINGLE_BATTLE_TEST("Hyphal Snare binds the target")
{
    GIVEN {
        ASSUME(MoveHasAdditionalEffect(MOVE_HYPHAL_SNARE, MOVE_EFFECT_WRAP));
        PLAYER(SPECIES_PARASECT);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_HYPHAL_SNARE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_HYPHAL_SNARE, player);
        HP_BAR(opponent);
        MESSAGE("The opposing Wobbuffet got tangled in Parasect's hyphae! Gross!");
        HP_BAR(opponent); // binding damage at end of turn
    } THEN {
        EXPECT(opponent->volatiles.wrapped);
    }
}

SINGLE_BATTLE_TEST("Hyphal Snare does not bind Grass types")
{
    GIVEN {
        PLAYER(SPECIES_PARASECT);
        OPPONENT(SPECIES_ODDISH);
    } WHEN {
        TURN { MOVE(player, MOVE_HYPHAL_SNARE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_HYPHAL_SNARE, player);
        HP_BAR(opponent);
        NOT MESSAGE("The opposing Oddish got tangled in Parasect's hyphae! Gross!");
    } THEN {
        EXPECT(!opponent->volatiles.wrapped);
    }
}
