#include "global.h"
#include "test/battle.h"

// Project Grounded: derde ronde signature moves (Beedrill, Nidoking, Nidoqueen, Fearow, Kabutops, Sawk,
// Throh, Carnivine, Kingler) en de herziene Bonemerang/Bone Club/Pay Day.
// Let op: Wobbuffet is in deze rom Psychic/Normal.

TEST("Project Grounded signature moves round 3 have the agreed data")
{
    EXPECT_EQ(GetMovePower(MOVE_TWIN_LANCE), 60);
    EXPECT_EQ(GetMoveStrikeCount(MOVE_TWIN_LANCE), 2);
    EXPECT_EQ(GetMoveType(MOVE_TWIN_LANCE), TYPE_BUG);
    EXPECT_EQ(GetMovePower(MOVE_TYRANT_HORN), 85);
    EXPECT_EQ(GetMoveEffect(MOVE_TYRANT_HORN), EFFECT_TWO_TYPED_MOVE);
    EXPECT_EQ(GetMoveType(MOVE_TYRANT_HORN), TYPE_POISON);
    EXPECT_EQ(GetMoveArgType(MOVE_TYRANT_HORN), TYPE_GROUND);
    EXPECT_EQ(GetMoveEffect(MOVE_QUEENS_WEIGHT), EFFECT_BODY_PRESS);
    EXPECT_EQ(GetMoveType(MOVE_QUEENS_WEIGHT), TYPE_GROUND);
    EXPECT_EQ(GetMoveCriticalHitStage(MOVE_SKY_SPEAR), 1);
    EXPECT_EQ(GetMoveAccuracy(MOVE_SKY_SPEAR), 95);
    EXPECT_EQ(GetMoveCriticalHitStage(MOVE_ANCIENT_SCYTHE), 1);
    EXPECT(IsSlicingMove(MOVE_ANCIENT_SCYTHE));
    EXPECT_EQ(GetMoveCriticalHitStage(MOVE_MAWASHI_GERI), 1);
    EXPECT(MoveIgnoresProtect(MOVE_MAWASHI_GERI));
    EXPECT(MoveIgnoresSubstitute(MOVE_MAWASHI_GERI));
    EXPECT_EQ(GetMovePriority(MOVE_IPPON), -6);
    EXPECT(MoveAlwaysCrits(MOVE_IPPON));
    EXPECT(IsBitingMove(MOVE_FLYTRAP));
    EXPECT(MoveHasAdditionalEffect(MOVE_FLYTRAP, MOVE_EFFECT_ABSORB));
    for (u32 i = 0; i < GetMoveAdditionalEffectCount(MOVE_FLYTRAP); i++)
    {
        if (GetMoveAdditionalEffectById(MOVE_FLYTRAP, i)->moveEffect == MOVE_EFFECT_ABSORB)
            EXPECT_EQ(GetMoveAdditionalEffectById(MOVE_FLYTRAP, i)->argument.absorbPercentage, 50);
    }
    EXPECT_EQ(GetMovePower(MOVE_COLOSSAL_CLAW), 150);
    EXPECT_EQ(GetMoveAccuracy(MOVE_COLOSSAL_CLAW), 85);
    EXPECT(!MoveIsAffectedBySheerForce(MOVE_COLOSSAL_CLAW));
    EXPECT_EQ(GetMovePower(MOVE_BONEMERANG), 60);
    EXPECT_EQ(GetMoveAccuracy(MOVE_BONEMERANG), 95);
    EXPECT_EQ(GetMovePower(MOVE_BONE_CLUB), 85);
    EXPECT_EQ(GetMoveAccuracy(MOVE_BONE_CLUB), 100);
    EXPECT_EQ(GetMoveAdditionalEffectById(MOVE_BONE_CLUB, 0)->chance, 20);
    EXPECT_EQ(GetMovePower(MOVE_PAY_DAY), 60);
}

// Twin Lance: twee klappen, per klap 25% vergif; een al vergiftigd doelwit wordt badly poisoned.
SINGLE_BATTLE_TEST("Twin Lance strikes twice")
{
    GIVEN {
        PLAYER(SPECIES_BEEDRILL);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_TWIN_LANCE, WITH_RNG(RNG_SECONDARY_EFFECT, FALSE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TWIN_LANCE, player);
        HP_BAR(opponent);
        HP_BAR(opponent);
        MESSAGE("The Pokémon was hit 2 times!");
    }
}

SINGLE_BATTLE_TEST("Twin Lance turns regular poison into bad poison")
{
    bool32 effect;
    PARAMETRIZE { effect = FALSE; }
    PARAMETRIZE { effect = TRUE; }
    GIVEN {
        PLAYER(SPECIES_BEEDRILL);
        // Veel HP: twee super-effectieve klappen + gifschade waren een KO (en flauwvallen wist de status)
        OPPONENT(SPECIES_WOBBUFFET) { Status1(STATUS1_POISON); MaxHP(999); HP(999); }
    } WHEN {
        TURN { MOVE(player, MOVE_TWIN_LANCE, WITH_RNG(RNG_SECONDARY_EFFECT, effect)); }
    } THEN {
        if (effect)
        {
            EXPECT(opponent->status1 & STATUS1_TOXIC_POISON);
            EXPECT(!(opponent->status1 & STATUS1_POISON));
        }
        else
        {
            EXPECT(opponent->status1 & STATUS1_POISON);
        }
    }
}

// Tyrant Horn: Poison + Ground voor type-effectiviteit, STAB voor Poison- én Ground-gebruikers.
SINGLE_BATTLE_TEST("Tyrant Horn is super effective on Electric types through its Ground typing")
{
    GIVEN {
        PLAYER(SPECIES_NIDOKING);
        OPPONENT(SPECIES_PIKACHU);
    } WHEN {
        TURN { MOVE(player, MOVE_TYRANT_HORN, WITH_RNG(RNG_SECONDARY_EFFECT, FALSE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TYRANT_HORN, player);
        HP_BAR(opponent);
        MESSAGE("It's super effective!");
    }
}

SINGLE_BATTLE_TEST("Tyrant Horn gets STAB from either Poison or Ground", s16 damage)
{
    u32 species, move;
    PARAMETRIZE { species = SPECIES_KOFFING; move = MOVE_CELEBRATE; }
    PARAMETRIZE { species = SPECIES_KOFFING; move = MOVE_SOAK; }
    PARAMETRIZE { species = SPECIES_CUBONE; move = MOVE_CELEBRATE; }
    PARAMETRIZE { species = SPECIES_CUBONE; move = MOVE_SOAK; }
    GIVEN {
        ASSUME(GetMoveEffect(MOVE_SOAK) == EFFECT_SOAK);
        PLAYER(species) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_TYRANT_HORN, WITH_RNG(RNG_SECONDARY_EFFECT, FALSE)); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TYRANT_HORN, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[1].damage, Q_4_12(1.5), results[0].damage);
        EXPECT_MUL_EQ(results[3].damage, Q_4_12(1.5), results[2].damage);
    }
}

// Queen's Weight: Body Press als Ground-move.
SINGLE_BATTLE_TEST("Queen's Weight uses the user's Defense instead of its Attack", s16 damage)
{
    u32 def, atk;
    PARAMETRIZE { def = 150; atk = 179; }
    PARAMETRIZE { atk = 150; def = 179; }
    GIVEN {
        PLAYER(SPECIES_NIDOQUEEN) { Attack(atk); Defense(def); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_QUEENS_WEIGHT); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_QUEENS_WEIGHT, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_GT(results[1].damage, results[0].damage);
    }
}

// Mawashi Geri: door Protect en door Substitute heen.
SINGLE_BATTLE_TEST("Mawashi Geri hits through Protect")
{
    GIVEN {
        PLAYER(SPECIES_SAWK) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_PROTECT); MOVE(player, MOVE_MAWASHI_GERI); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PROTECT, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MAWASHI_GERI, player);
        HP_BAR(opponent);
    }
}

SINGLE_BATTLE_TEST("Mawashi Geri hits through Substitute")
{
    GIVEN {
        PLAYER(SPECIES_SAWK) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SUBSTITUTE); }
        TURN { MOVE(player, MOVE_MAWASHI_GERI); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SUBSTITUTE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_MAWASHI_GERI, player);
        NOT MESSAGE("The substitute took damage for the opposing Wobbuffet!");
        HP_BAR(opponent);
    }
}

// Ippon: altijd een crit en het doelwit wordt eruit gegooid.
SINGLE_BATTLE_TEST("Ippon always crits and drags out a replacement")
{
    GIVEN {
        PLAYER(SPECIES_THROH);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_BULBASAUR);
    } WHEN {
        TURN { MOVE(player, MOVE_IPPON); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_IPPON, player);
        HP_BAR(opponent);
        MESSAGE("A critical hit!");
        MESSAGE("The opposing Bulbasaur was dragged out!");
    }
}

// Flytrap: drain 50% en dubbele kracht tegen Bug en Flying.
SINGLE_BATTLE_TEST("Flytrap recovers 50% of the damage dealt")
{
    s16 damage;
    s16 healed;
    GIVEN {
        PLAYER(SPECIES_CARNIVINE) { HP(1); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_FLYTRAP); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_FLYTRAP, player);
        HP_BAR(opponent, captureDamage: &damage);
        HP_BAR(player, captureDamage: &healed);
    } THEN {
        EXPECT_MUL_EQ(damage, Q_4_12(-0.5), healed);
    }
}

SINGLE_BATTLE_TEST("Flytrap doubles in power against Bug and Flying types", s16 damage)
{
    u32 move, species;
    PARAMETRIZE { species = SPECIES_CATERPIE; move = MOVE_SEED_BOMB; }
    PARAMETRIZE { species = SPECIES_CATERPIE; move = MOVE_FLYTRAP; }
    PARAMETRIZE { species = SPECIES_PIDGEY; move = MOVE_SEED_BOMB; }
    PARAMETRIZE { species = SPECIES_PIDGEY; move = MOVE_FLYTRAP; }
    PARAMETRIZE { species = SPECIES_WOBBUFFET; move = MOVE_SEED_BOMB; }
    PARAMETRIZE { species = SPECIES_WOBBUFFET; move = MOVE_FLYTRAP; }
    GIVEN {
        ASSUME(GetMovePower(MOVE_SEED_BOMB) == 80);
        ASSUME(GetMoveType(MOVE_SEED_BOMB) == TYPE_GRASS);
        ASSUME(GetMoveCategory(MOVE_SEED_BOMB) == DAMAGE_CATEGORY_PHYSICAL);
        PLAYER(SPECIES_CARNIVINE) { Ability(ABILITY_LEVITATE); }
        OPPONENT(species) { HP(9999); MaxHP(9999); }
    } WHEN {
        TURN { MOVE(player, move); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, move, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(2.0), results[1].damage);
        EXPECT_MUL_EQ(results[2].damage, Q_4_12(2.0), results[3].damage);
        EXPECT_EQ(results[4].damage, results[5].damage);
    }
}

// Colossal Claw: -2 Attack voor de gebruiker.
SINGLE_BATTLE_TEST("Colossal Claw harshly lowers the user's Attack")
{
    GIVEN {
        PLAYER(SPECIES_KINGLER);
        OPPONENT(SPECIES_WOBBUFFET) { HP(9999); MaxHP(9999); }
    } WHEN {
        TURN { MOVE(player, MOVE_COLOSSAL_CLAW, hit: TRUE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_COLOSSAL_CLAW, player);
        HP_BAR(opponent);
        ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_STATS_CHANGE, player);
    } THEN {
        EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE - 2);
    }
}

// Bonemerang: raakt ook Flying-types en Levitate, zonder ze te grounden.
SINGLE_BATTLE_TEST("Bonemerang hits Flying types and Levitate users")
{
    u32 species;
    PARAMETRIZE { species = SPECIES_PIDGEY; }
    PARAMETRIZE { species = SPECIES_CARNIVINE; }
    GIVEN {
        PLAYER(SPECIES_MAROWAK);
        OPPONENT(species) { HP(9999); MaxHP(9999); if (species == SPECIES_CARNIVINE) Ability(ABILITY_LEVITATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_BONEMERANG, hit: TRUE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_BONEMERANG, player);
        HP_BAR(opponent);
        HP_BAR(opponent);
        MESSAGE("The Pokémon was hit 2 times!");
    }
}
