// Project Grounded: The Spire - de run (zie SPIRE_DESIGN.md).
// De run staat in gSaveBlock2Ptr->spire, dus een gepauzeerde run blijft bewaard na opslaan en uitzetten.
// Verloop: Spire_Enter (special) → draft van twee rentals → act-kaart → kamer → beloning → kaart ...
// Na de baas van act 1 en 2 een nieuwe act (rentals evolueren); na de baas van act 3 is de run gewonnen.
#include "global.h"
#include "battle.h"
#include "battle_main.h"
#include "battle_setup.h"
#include "event_data.h"
#include "main.h"
#include "move.h"
#include "overworld.h"
#include "palette.h"
#include "pokemon.h"
#include "random.h"
#include "script.h"
#include "sound.h"
#include "spire.h"
#include "string_util.h"
#include "task.h"
#include "constants/battle.h"
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/songs.h"
#include "constants/species.h"

#define RUN SPIRE_SAVE

STATIC_ASSERT(sizeof(struct SpireSave) <= SPIRE_SAVE_SIZE, SpireSaveFitsInSaveBlock2);

EWRAM_DATA struct SpireResult gSpireResult = {0};
EWRAM_DATA static struct Pokemon sSavedParty[PARTY_SIZE] = {0};
EWRAM_DATA static u8 sSavedPartyCount = 0;
EWRAM_DATA static u8 sRoomType = 0;
EWRAM_DATA static u8 sDraftStep = 0;
EWRAM_DATA static u8 sEndMessage[160] = {0};

static void StartRoomBattle(u32 type);
static void CB2_EndSpireBattle(void);
static void NextAct(void);

// ---------------------------------------------------------------------------------------------
// Relics

const struct SpireRelicInfo gSpireRelics[SPIRE_RELIC_COUNT] =
{
    [SPIRE_RELIC_LEFTOVERS]   = {ITEM_LEFTOVERS,   COMPOUND_STRING("Leftovers"),   COMPOUND_STRING("Heal 10% more HP\nafter every battle.")},
    [SPIRE_RELIC_AMULET_COIN] = {ITEM_AMULET_COIN, COMPOUND_STRING("Amulet Coin"), COMPOUND_STRING("Earn 50% more money\nin every battle.")},
    [SPIRE_RELIC_KINGS_ROCK]  = {ITEM_KINGS_ROCK,  COMPOUND_STRING("King's Rock"), COMPOUND_STRING("DEFEND gives 30%\nmore Block.")},
    [SPIRE_RELIC_SCOPE_LENS]  = {ITEM_SCOPE_LENS,  COMPOUND_STRING("Scope Lens"),  COMPOUND_STRING("Your Pokémon land\ncritical hits more often.")},
    [SPIRE_RELIC_MUSCLE_BAND] = {ITEM_MUSCLE_BAND, COMPOUND_STRING("Muscle Band"), COMPOUND_STRING("Your Pokémon deal\n10% more damage.")},
    [SPIRE_RELIC_WIDE_LENS]   = {ITEM_WIDE_LENS,   COMPOUND_STRING("Wide Lens"),   COMPOUND_STRING("Your moves that hit\nboth foes lose no power.")},
    [SPIRE_RELIC_SOOTHE_BELL] = {ITEM_SOOTHE_BELL, COMPOUND_STRING("Soothe Bell"), COMPOUND_STRING("Resting heals 80%\ninstead of 50%.")},
    [SPIRE_RELIC_FOCUS_SASH]  = {ITEM_FOCUS_SASH,  COMPOUND_STRING("Focus Sash"),  COMPOUND_STRING("At full HP, survive a\nknockout hit with 1 HP.")},
};

bool32 Spire_RunActive(void)
{
    return RUN.magic == SPIRE_SAVE_MAGIC;
}

bool32 Spire_HasRelic(u32 relic)
{
    return Spire_RunActive() && (RUN.relics & (1u << relic));
}

void Spire_AddRelic(u32 relic)
{
    RUN.relics |= 1u << relic;
}

// Een relic die je nog niet hebt; SPIRE_RELIC_COUNT als je alles al hebt.
u32 Spire_RandomNewRelic(u32 salt)
{
    u32 i, n = 0, pick;

    for (i = 0; i < SPIRE_RELIC_COUNT; i++)
        if (!(RUN.relics & (1u << i)))
            n++;
    if (n == 0)
        return SPIRE_RELIC_COUNT;
    pick = (Random() + salt) % n;
    for (i = 0; i < SPIRE_RELIC_COUNT; i++)
    {
        if (!(RUN.relics & (1u << i)) && pick-- == 0)
            return i;
    }
    return SPIRE_RELIC_COUNT;
}

struct Pokemon *Spire_GetRunMon(u32 i)
{
    return &RUN.mons[i];
}

// ---------------------------------------------------------------------------------------------
// Pools (zie tools/grounded/spire/balance.py)

// rentals bij de draft: middelste evolutiestap, evolueren na act 1
static const u16 sRentalPool[] =
{
    SPECIES_IVYSAUR, SPECIES_CHARMELEON, SPECIES_WARTORTLE, SPECIES_GROVYLE, SPECIES_COMBUSKEN,
    SPECIES_MARSHTOMP, SPECIES_HAUNTER, SPECIES_MACHOKE, SPECIES_GRAVELER, SPECIES_KADABRA,
    SPECIES_LAIRON, SPECIES_VIBRAVA, SPECIES_SHELGON, SPECIES_GABITE, SPECIES_MONFERNO,
    SPECIES_PRINPLUP, SPECIES_GROTLE, SPECIES_LUXIO, SPECIES_ZWEILOUS, SPECIES_FRAXURE,
    SPECIES_SLIGGOO, SPECIES_KIRLIA, SPECIES_DRAGONAIR, SPECIES_PUPITAR, SPECIES_METANG,
    SPECIES_CORVISQUIRE, SPECIES_RABOOT, SPECIES_DRIZZILE, SPECIES_THWACKEY, SPECIES_HATTREM,
};

static const u16 sNormalFoes[SPIRE_ACTS][18] =
{
    {SPECIES_PIDGEOTTO, SPECIES_NUZLEAF, SPECIES_LOMBRE, SPECIES_ELECTRIKE, SPECIES_GLOOM, SPECIES_FLAAFFY,
     SPECIES_SKIPLOOM, SPECIES_SWABLU, SPECIES_NUMEL, SPECIES_SPOINK, SPECIES_BALTOY, SPECIES_CORPHISH,
     SPECIES_SHUPPET, SPECIES_DUSKULL, SPECIES_SNORUNT, SPECIES_GRAVELER, SPECIES_MACHOKE, SPECIES_LAIRON},
    {SPECIES_PIDGEOT, SPECIES_SHIFTRY, SPECIES_LUDICOLO, SPECIES_MANECTRIC, SPECIES_VILEPLUME, SPECIES_AMPHAROS,
     SPECIES_JUMPLUFF, SPECIES_ALTARIA, SPECIES_CAMERUPT, SPECIES_GRUMPIG, SPECIES_CLAYDOL, SPECIES_CRAWDAUNT,
     SPECIES_BANETTE, SPECIES_DUSCLOPS, SPECIES_GLALIE, SPECIES_GOLEM, SPECIES_MACHAMP, SPECIES_AGGRON},
    {SPECIES_STARAPTOR, SPECIES_BRELOOM, SPECIES_GYARADOS, SPECIES_ROSERADE, SPECIES_TOGEKISS, SPECIES_TORKOAL,
     SPECIES_BRONZONG, SPECIES_SCIZOR, SPECIES_MISMAGIUS, SPECIES_DUSKNOIR, SPECIES_WEAVILE, SPECIES_RHYPERIOR,
     SPECIES_CONKELDURR, SPECIES_LUCARIO, SPECIES_MAMOSWINE, SPECIES_FROSLASS, SPECIES_GLISCOR, SPECIES_HONCHKROW},
};

static const u16 sEliteFoes[SPIRE_ACTS][6] =
{
    {SPECIES_ARCANINE, SPECIES_GYARADOS, SPECIES_SCIZOR, SPECIES_LUCARIO, SPECIES_MAMOSWINE, SPECIES_HERACROSS},
    {SPECIES_SALAMENCE, SPECIES_METAGROSS, SPECIES_GARCHOMP, SPECIES_TYRANITAR, SPECIES_DRAGONITE, SPECIES_VOLCARONA},
    {SPECIES_HYDREIGON, SPECIES_HAXORUS, SPECIES_GOODRA, SPECIES_KINGAMBIT, SPECIES_DRAGAPULT, SPECIES_GHOLDENGO},
};

static const u8 sFoeLevel[SPIRE_ACTS] = {48, 50, 52};

struct SpireBoss
{
    u16 species;
    u16 moves[MAX_MON_MOVES];
    u16 lackey;
    u16 lackeyMoves[MAX_MON_MOVES];
};

static const struct SpireBoss sBosses[SPIRE_ACTS][3] =
{
    {
        {SPECIES_MILOTIC, {MOVE_SCALD, MOVE_ICE_BEAM, MOVE_RECOVER, MOVE_DRAGON_PULSE},
         SPECIES_WHIMSICOTT, {MOVE_TAILWIND, MOVE_HELPING_HAND, MOVE_MOONBLAST, MOVE_ENCORE}},
        {SPECIES_AGGRON, {MOVE_IRON_HEAD, MOVE_ROCK_SLIDE, MOVE_EARTHQUAKE, MOVE_IRON_DEFENSE},
         SPECIES_KLEFKI, {MOVE_REFLECT, MOVE_LIGHT_SCREEN, MOVE_THUNDER_WAVE, MOVE_FLASH_CANNON}},
        {SPECIES_FLYGON, {MOVE_EARTHQUAKE, MOVE_DRAGON_CLAW, MOVE_ROCK_SLIDE, MOVE_U_TURN},
         SPECIES_PELIPPER, {MOVE_TAILWIND, MOVE_HURRICANE, MOVE_SCALD, MOVE_PROTECT}},
    },
    {
        {SPECIES_SALAMENCE, {MOVE_DRAGON_DANCE, MOVE_DRAGON_CLAW, MOVE_FIRE_FANG, MOVE_HYPER_VOICE},
         SPECIES_WHIMSICOTT, {MOVE_TAILWIND, MOVE_HELPING_HAND, MOVE_MOONBLAST, MOVE_ENCORE}},
        {SPECIES_METAGROSS, {MOVE_METEOR_MASH, MOVE_ZEN_HEADBUTT, MOVE_BULLET_PUNCH, MOVE_EARTHQUAKE},
         SPECIES_KLEFKI, {MOVE_REFLECT, MOVE_LIGHT_SCREEN, MOVE_THUNDER_WAVE, MOVE_FLASH_CANNON}},
        {SPECIES_TYRANITAR, {MOVE_ROCK_SLIDE, MOVE_CRUNCH, MOVE_DRAGON_DANCE, MOVE_EARTHQUAKE},
         SPECIES_PELIPPER, {MOVE_TAILWIND, MOVE_HURRICANE, MOVE_SCALD, MOVE_PROTECT}},
    },
    {
        {SPECIES_GROUDON, {MOVE_EARTHQUAKE, MOVE_FIRE_PUNCH, MOVE_STONE_EDGE, MOVE_BULK_UP},
         SPECIES_WHIMSICOTT, {MOVE_TAILWIND, MOVE_HELPING_HAND, MOVE_MOONBLAST, MOVE_ENCORE}},
        {SPECIES_KYOGRE, {MOVE_WATER_SPOUT, MOVE_ICE_BEAM, MOVE_THUNDER, MOVE_CALM_MIND},
         SPECIES_KLEFKI, {MOVE_REFLECT, MOVE_LIGHT_SCREEN, MOVE_THUNDER_WAVE, MOVE_FLASH_CANNON}},
        {SPECIES_RAYQUAZA, {MOVE_OUTRAGE, MOVE_EXTREME_SPEED, MOVE_EARTHQUAKE, MOVE_DRAGON_DANCE},
         SPECIES_PELIPPER, {MOVE_TAILWIND, MOVE_HURRICANE, MOVE_SCALD, MOVE_PROTECT}},
    },
};

// movepools per zeldzaamheid (0 common, 1 uncommon, 2 rare)
static const u16 sCommonMoves[] =
{
    MOVE_HEADBUTT, MOVE_BITE, MOVE_WATER_PULSE, MOVE_MAGICAL_LEAF, MOVE_SHOCK_WAVE, MOVE_ICY_WIND,
    MOVE_ROCK_TOMB, MOVE_AERIAL_ACE, MOVE_MUD_SHOT, MOVE_FLAME_WHEEL, MOVE_PSYBEAM, MOVE_SHADOW_CLAW,
    MOVE_DRAGON_BREATH, MOVE_BRICK_BREAK, MOVE_POISON_JAB, MOVE_BUG_BITE, MOVE_DRAINING_KISS, MOVE_SNARL,
    MOVE_METAL_CLAW, MOVE_PROTECT,
};
static const u16 sUncommonMoves[] =
{
    MOVE_FLAMETHROWER, MOVE_SURF, MOVE_THUNDERBOLT, MOVE_ICE_BEAM, MOVE_ENERGY_BALL, MOVE_EARTH_POWER,
    MOVE_PSYCHIC, MOVE_SHADOW_BALL, MOVE_DRAGON_PULSE, MOVE_DARK_PULSE, MOVE_FLASH_CANNON, MOVE_X_SCISSOR,
    MOVE_ROCK_SLIDE, MOVE_CRUNCH, MOVE_SLUDGE_BOMB, MOVE_AURA_SPHERE, MOVE_FREEZE_DRY, MOVE_TAILWIND,
    MOVE_HELPING_HAND, MOVE_CALM_MIND, MOVE_SWORDS_DANCE, MOVE_WIDE_GUARD, MOVE_DRAIN_PUNCH, MOVE_AIR_SLASH,
};
static const u16 sRareMoves[] =
{
    MOVE_FIRE_BLAST, MOVE_HYDRO_PUMP, MOVE_THUNDER, MOVE_BLIZZARD, MOVE_CLOSE_COMBAT, MOVE_EARTHQUAKE,
    MOVE_OUTRAGE, MOVE_MOONBLAST, MOVE_DRACO_METEOR, MOVE_HEAT_WAVE, MOVE_LEAF_STORM, MOVE_DRAGON_DANCE,
    MOVE_QUIVER_DANCE, MOVE_FOLLOW_ME, MOVE_FAKE_OUT, MOVE_NASTY_PLOT,
};

u16 Spire_RandomMove(u32 rarity, u32 salt)
{
    u32 r = Random() + salt * 7;

    switch (rarity)
    {
    case 2:  return sRareMoves[r % ARRAY_COUNT(sRareMoves)];
    case 1:  return sUncommonMoves[r % ARRAY_COUNT(sUncommonMoves)];
    default: return sCommonMoves[r % ARRAY_COUNT(sCommonMoves)];
    }
}

u16 Spire_RandomRental(u32 salt)
{
    return sRentalPool[(Random() + salt * 13) % ARRAY_COUNT(sRentalPool)];
}

// eerste common-move van dit type uit de pool (startermoves), anders MOVE_NONE
static u16 CommonMoveOfType(enum Type type, u32 skip)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sCommonMoves); i++)
    {
        if (GetMoveType(sCommonMoves[i]) == type && sCommonMoves[i] != skip && !IsBattleMoveStatus(sCommonMoves[i]))
            return sCommonMoves[i];
    }
    return MOVE_NONE;
}

// Rental: lv 50, startermoves = STAB uit de common-pool + Protect, rest uit de level-up-moves.
void Spire_SetRental(u32 slot, u16 species)
{
    struct Pokemon *mon = &RUN.mons[slot];
    u16 moves[MAX_MON_MOVES];
    u32 i, n = 0;

    Spire_CreateMon(mon, species, 50, 31, 84, NULL);
    moves[n] = CommonMoveOfType(GetSpeciesType(species, 0), MOVE_NONE);
    if (moves[n] != MOVE_NONE)
        n++;
    if (GetSpeciesType(species, 1) != GetSpeciesType(species, 0))
    {
        moves[n] = CommonMoveOfType(GetSpeciesType(species, 1), MOVE_NONE);
        if (moves[n] != MOVE_NONE)
            n++;
    }
    moves[n++] = MOVE_PROTECT;
    // aanvullen met de eigen level-up-moves (die CreateMon al gaf), zonder dubbelen
    for (i = 0; i < MAX_MON_MOVES && n < MAX_MON_MOVES; i++)
    {
        u16 m = GetMonData(mon, MON_DATA_MOVE1 + i);
        u32 j;
        bool32 dup = (m == MOVE_NONE);

        for (j = 0; j < n; j++)
            if (moves[j] == m)
                dup = TRUE;
        if (!dup)
            moves[n++] = m;
    }
    while (n < MAX_MON_MOVES)
        moves[n++] = MOVE_NONE;
    for (i = 0; i < MAX_MON_MOVES; i++)
        SetMonMoveSlot(mon, moves[i], i);
    Spire_ScaleMonHp(mon, SPIRE_HP_PLAYER);
}

// ---------------------------------------------------------------------------------------------
// Kaart van een act: SPIRE_FLOORS verdiepingen met 2-4 kamers, daarboven de baas.

static u32 Lcg(u32 *state)
{
    *state = *state * 1103515245 + 12345;
    return (*state >> 16) & 0x7FFF;
}

void Spire_GenerateMap(struct SpireActMap *map, u32 seed)
{
    u32 f, i, j, st = seed;

    for (f = 0; f < SPIRE_FLOORS; f++)
    {
        u32 n = (f == 0) ? 3 : (f == SPIRE_FLOORS - 1) ? 2 : 2 + Lcg(&st) % 3;

        map->count[f] = n;
        for (i = 0; i < n; i++)
        {
            struct SpireMapNode *node = &map->nodes[f][i];
            u32 r = Lcg(&st) % 100;

            node->x = 18 + (132 * (2 * i + 1)) / (2 * n) + (Lcg(&st) % 9) - 4;
            node->links = 0;
            if (f == 0)
                node->type = SPIRE_ROOM_FIGHT;
            else if (f == SPIRE_FLOORS - 1)
                node->type = SPIRE_ROOM_REST;
            else if (r < 45)
                node->type = SPIRE_ROOM_FIGHT;
            else if (r < 65)
                node->type = SPIRE_ROOM_EVENT;
            else if (r < 80 && f >= 2)
                node->type = SPIRE_ROOM_ELITE;
            else if (r < 90)
                node->type = SPIRE_ROOM_SHOP;
            else if (f >= 3)
                node->type = SPIRE_ROOM_REST;
            else
                node->type = SPIRE_ROOM_FIGHT;
        }
    }
    // verbindingen zonder kruisingen: kamer i gaat naar j0(i) (oplopend met i) en soms ook naar j0(i)+1,
    // maar alleen als de volgende kamer daar niet onder begint. Losse kamers krijgen een buur van links.
    for (f = 0; f + 1 < SPIRE_FLOORS; f++)
    {
        u32 n0 = map->count[f], n1 = map->count[f + 1];
        u8 j0s[SPIRE_MAX_NODES];
        u8 incoming = 0;

        for (i = 0; i < n0; i++)
            j0s[i] = (n0 == 1) ? 0 : (i * (n1 - 1) + (n0 - 1) / 2) / (n0 - 1);
        for (i = 0; i < n0; i++)
        {
            map->nodes[f][i].links |= 1u << j0s[i];
            if (j0s[i] + 1 < n1 && (i + 1 >= n0 || j0s[i + 1] > j0s[i]) && Lcg(&st) % 2)
                map->nodes[f][i].links |= 1u << (j0s[i] + 1);
            incoming |= map->nodes[f][i].links;
        }
        for (j = 0; j < n1; j++)
        {
            if (!(incoming & (1u << j)))
            {
                // de laatste kamer links van j (j0 < j) neemt hem erbij; anders de eerste
                u32 from = 0;

                for (i = 0; i < n0; i++)
                    if (j0s[i] < j)
                        from = i;
                map->nodes[f][from].links |= 1u << j;
            }
        }
    }
}

static u32 PathNode(u32 floor)
{
    return (RUN.path >> (2 * floor)) & 3;
}

// Kun je deze kamer nu kiezen? RUN.floor = aantal afgeronde verdiepingen in deze act.
bool32 Spire_IsReachable(const struct SpireActMap *map, u32 floor, u32 node)
{
    if (floor != RUN.floor || node >= map->count[floor])
        return FALSE;
    if (floor == 0)
        return TRUE;
    return (map->nodes[floor - 1][PathNode(floor - 1)].links & (1u << node)) != 0;
}

// ---------------------------------------------------------------------------------------------
// Run starten, pauzeren, beëindigen

static void SaveParty(void)
{
    u32 i;

    for (i = 0; i < PARTY_SIZE; i++)
        sSavedParty[i] = gPlayerParty[i];
    sSavedPartyCount = gPlayerPartyCount;
}

static void RestoreParty(void)
{
    u32 i;

    for (i = 0; i < PARTY_SIZE; i++)
        gPlayerParty[i] = sSavedParty[i];
    gPlayerPartyCount = sSavedPartyCount;
}

void Spire_ReturnToField(void)
{
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

static void AwardBP(void)
{
    u32 bp = gSaveBlock2Ptr->frontier.battlePoints + RUN.bp;

    gSaveBlock2Ptr->frontier.battlePoints = bp > 9999 ? 9999 : bp;
}

static void EndRun(bool32 won)
{
    u32 bp = RUN.bp;

    AwardBP();
    if (won)
        RUN.runsWon++;
    RUN.magic = 0;
    ConvertIntToDecimalStringN(gStringVar1, bp, STR_CONV_MODE_LEFT_ALIGN, 4);
    ConvertIntToDecimalStringN(gStringVar2, RUN.act, STR_CONV_MODE_LEFT_ALIGN, 1);
    if (won)
        StringExpandPlaceholders(sEndMessage, COMPOUND_STRING("You conquered the Spire!\nYou earned {STR_VAR_1} BP."));
    else
        StringExpandPlaceholders(sEndMessage, COMPOUND_STRING("Your run ended in act {STR_VAR_2}.\nYou earned {STR_VAR_1} BP. The tower keeps the rest."));
    Spire_OpenMessage(won ? COMPOUND_STRING("THE SPIRE IS YOURS!") : COMPOUND_STRING("RUN OVER"), sEndMessage, Spire_ReturnToField);
}

static void NewRun(void)
{
    memset(&RUN, 0, offsetof(struct SpireSave, runsWon));
    RUN.relics = 0;
    ZeroMonData(&RUN.mons[0]);
    ZeroMonData(&RUN.mons[1]);
    RUN.magic = SPIRE_SAVE_MAGIC;
    RUN.act = 1;
    RUN.floor = 0;
    RUN.seed = Random32();
    sDraftStep = 0;
}

static void DraftDone(void)
{
    if (++sDraftStep < 2)
        Spire_OpenCards(SPIRE_CARDS_DRAFT, DraftDone);
    else
        Spire_OpenMap();
}

// special: vanuit een script (lockall; special Spire_Enter; waitstate; releaseall)
void Spire_Enter(void)
{
    CleanupOverworldWindowsAndTilemaps();
    if (!Spire_RunActive())
    {
        NewRun();
        Spire_OpenCards(SPIRE_CARDS_DRAFT, DraftDone);
    }
    else if (RUN.inRoom)
    {
        Spire_EnterRoom(RUN.floor, RUN.node);
    }
    else
    {
        Spire_OpenMap();
    }
}

void Spire_ResetRun(void)
{
    RUN.magic = 0;
}

void Spire_SuspendRun(void)
{
    Spire_OpenMessage(COMPOUND_STRING("RUN PAUSED"),
                      COMPOUND_STRING("Your run is waiting for you.\nSave the game to keep it."), Spire_ReturnToField);
}

void Spire_GiveUpRun(void)
{
    EndRun(FALSE);
}

// ---------------------------------------------------------------------------------------------
// Rentals: heal, PP, evolutie

void Spire_HealRun(u32 percent)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Pokemon *mon = &RUN.mons[i];
        u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP);

        hp = (hp == 0) ? 1 : min(maxHp, hp + maxHp * percent / 100);
        SetMonData(mon, MON_DATA_HP, &hp);
        if (percent >= SPIRE_REST_HEAL)
        {
            u32 status = 0;
            SetMonData(mon, MON_DATA_STATUS, &status);
        }
    }
}

void Spire_RestorePP(void)
{
    u32 i, j;

    for (i = 0; i < 2; i++)
    {
        for (j = 0; j < MAX_MON_MOVES; j++)
        {
            u32 move = GetMonData(&RUN.mons[i], MON_DATA_MOVE1 + j);
            u32 pp = CalculatePPWithBonus(move, GetMonData(&RUN.mons[i], MON_DATA_PP_BONUSES), j);
            SetMonData(&RUN.mons[i], MON_DATA_PP1 + j, &pp);
        }
    }
}

static u16 EvolutionOf(u16 species)
{
    const struct Evolution *evo = GetSpeciesEvolutions(species);

    if (evo == NULL || evo[0].method == EVOLUTIONS_END)
        return SPECIES_NONE;
    return evo[0].targetSpecies;
}

bool32 Spire_CanEvolve(u32 i)
{
    return EvolutionOf(GetMonData(&RUN.mons[i], MON_DATA_SPECIES)) != SPECIES_NONE;
}

// Evolueren met behoud van HP-verhouding (×4 HP blijft).
void Spire_Evolve(u32 i)
{
    struct Pokemon *mon = &RUN.mons[i];
    u16 target = EvolutionOf(GetMonData(mon, MON_DATA_SPECIES));
    u32 hp = GetMonData(mon, MON_DATA_HP), maxHp = GetMonData(mon, MON_DATA_MAX_HP), newHp;

    if (target == SPECIES_NONE)
        return;
    SetMonData(mon, MON_DATA_SPECIES, &target);
    CalculateMonStats(mon);
    Spire_ScaleMonHp(mon, SPIRE_HP_PLAYER);
    newHp = GetMonData(mon, MON_DATA_MAX_HP) * hp / (maxHp ? maxHp : 1);
    if (newHp == 0 && hp != 0)
        newHp = 1;
    SetMonData(mon, MON_DATA_HP, &newHp);
}

// ---------------------------------------------------------------------------------------------
// Kamers

void Spire_EnterRoom(u32 floor, u32 node)
{
    struct SpireActMap map;
    u32 type;

    Spire_GenerateMap(&map, RUN.seed);
    if (floor >= SPIRE_FLOORS)
        type = SPIRE_ROOM_BOSS;
    else
        type = map.nodes[floor][node].type;
    RUN.floor = floor;
    RUN.node = node;
    RUN.inRoom = TRUE;
    sRoomType = type;

    switch (type)
    {
    case SPIRE_ROOM_FIGHT:
    case SPIRE_ROOM_ELITE:
    case SPIRE_ROOM_BOSS:
        StartRoomBattle(type);
        break;
    case SPIRE_ROOM_REST:
        Spire_OpenCards(SPIRE_CARDS_REST, Spire_RoomFinished);
        break;
    case SPIRE_ROOM_SHOP:
        Spire_OpenCards(SPIRE_CARDS_SHOP, Spire_RoomFinished);
        break;
    default:
        Spire_OpenCards(SPIRE_CARDS_EVENT, Spire_RoomFinished);
        break;
    }
}

void Spire_RoomFinished(void)
{
    RUN.inRoom = FALSE;
    if (RUN.floor < SPIRE_FLOORS)
        RUN.path = (RUN.path & ~(3u << (2 * RUN.floor))) | (RUN.node << (2 * RUN.floor));
    RUN.floor++;
    if (RUN.floor > SPIRE_FLOORS)
        NextAct();
    else
        Spire_OpenMap();
}

static void NextAct(void)
{
    u32 i;

    if (RUN.act >= SPIRE_ACTS)
    {
        EndRun(TRUE);
        return;
    }
    RUN.act++;
    RUN.floor = 0;
    RUN.path = 0;
    RUN.seed = Random32();
    // na act 1 evolueren de rentals
    StringCopy(sEndMessage, COMPOUND_STRING("The tower shakes. A new act begins!"));
    for (i = 0; i < 2; i++)
    {
        if (Spire_CanEvolve(i))
        {
            u8 nick[POKEMON_NAME_LENGTH + 1];

            GetMonData(&RUN.mons[i], MON_DATA_NICKNAME, nick);
            Spire_Evolve(i);
            StringAppend(sEndMessage, COMPOUND_STRING("\n"));
            StringAppend(sEndMessage, nick);
            StringAppend(sEndMessage, COMPOUND_STRING(" became "));
            StringAppend(sEndMessage, GetSpeciesName(GetMonData(&RUN.mons[i], MON_DATA_SPECIES)));
            StringAppend(sEndMessage, COMPOUND_STRING("!"));
        }
    }
    Spire_HealRun(SPIRE_REST_HEAL);
    Spire_RestorePP();
    ConvertIntToDecimalStringN(gStringVar1, RUN.act, STR_CONV_MODE_LEFT_ALIGN, 1);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("ACT {STR_VAR_1}"));
    Spire_OpenMessage(gStringVar4, sEndMessage, Spire_OpenMap);
}

// ---------------------------------------------------------------------------------------------
// Gevechten

static const struct SpireBoss *GetBoss(void)
{
    return &sBosses[RUN.act - 1][(RUN.seed >> 8) % 3];
}

u16 Spire_GetBossSpecies(void)
{
    return GetBoss()->species;
}

static void CreateFoe(struct Pokemon *mon, u16 species, u8 level)
{
    Spire_CreateMon(mon, species, level, 20, 0, NULL);
}

static void StartRoomBattle(u32 type)
{
    u32 act = RUN.act - 1;
    u32 lv = sFoeLevel[act];
    u32 i, song;

    ZeroEnemyPartyMons();
    for (i = 0; i < PARTY_SIZE; i++)
        gSpireEnemyHp[i] = SPIRE_HP_NORMAL;

    if (type == SPIRE_ROOM_BOSS)
    {
        const struct SpireBoss *boss = GetBoss();

        Spire_CreateMon(&gEnemyParty[0], boss->species, lv + 2, 31, 84, boss->moves);
        Spire_CreateMon(&gEnemyParty[1], boss->lackey, lv - 4, 20, 0, boss->lackeyMoves);
        gSpireEnemyHp[0] = SPIRE_HP_BOSS;
        song = MUS_VS_FRONTIER_BRAIN;
    }
    else if (type == SPIRE_ROOM_ELITE)
    {
        CreateFoe(&gEnemyParty[0], sEliteFoes[act][Random() % 6], lv);
        CreateFoe(&gEnemyParty[1], sNormalFoes[act][Random() % 18], lv);
        gSpireEnemyHp[0] = SPIRE_HP_ELITE;
        song = MUS_VS_ELITE_FOUR;
    }
    else
    {
        u32 a = Random() % 18;
        u32 b = (a + 1 + Random() % 17) % 18;

        CreateFoe(&gEnemyParty[0], sNormalFoes[act][a], lv);
        CreateFoe(&gEnemyParty[1], sNormalFoes[act][b], lv);
        song = MUS_VS_WILD;
    }

    SaveParty();
    ZeroPlayerPartyMons();
    gPlayerParty[0] = RUN.mons[0];
    gPlayerParty[1] = RUN.mons[1];
    CalculatePlayerPartyCount();

    gSpireBattle = TRUE;
    gSpireAct = RUN.act;
    Spire_ClearBlocks();
    gBattleTypeFlags = BATTLE_TYPE_DOUBLE;
    gMain.savedCallback = CB2_EndSpireBattle;
    PlayMapChosenOrBattleBGM(song);
    SetMainCallback2(CB2_InitBattle);
}

static void RewardMoves(void)
{
    Spire_OpenCards(SPIRE_CARDS_MOVES, Spire_RoomFinished);
}

static void CB2_EndSpireBattle(void)
{
    u32 i, gold, heal;

    for (i = 0; i < 2; i++)
        RUN.mons[i] = gPlayerParty[i];
    gSpireBattle = FALSE;
    Spire_ClearBlocks();
    RestoreParty();
    PlayNewMapMusic(MUS_B_TOWER);

    if (gBattleOutcome == B_OUTCOME_RAN || gBattleOutcome == B_OUTCOME_PLAYER_TELEPORTED)
    {
        // RUN in een gevecht = pauzeren; de kamer begint opnieuw als je terugkomt
        Spire_SuspendRun();
        return;
    }
    if (gBattleOutcome != B_OUTCOME_WON)
    {
        EndRun(FALSE);
        return;
    }

    heal = SPIRE_HEAL_AFTER + (Spire_HasRelic(SPIRE_RELIC_LEFTOVERS) ? 10 : 0);
    Spire_HealRun(heal);
    switch (sRoomType)
    {
    case SPIRE_ROOM_BOSS:  gold = 80; gSpireResult.bp = 10; break;
    case SPIRE_ROOM_ELITE: gold = 35 + Random() % 11; gSpireResult.bp = 3; break;
    default:               gold = 15 + Random() % 11; gSpireResult.bp = 1; break;
    }
    if (Spire_HasRelic(SPIRE_RELIC_AMULET_COIN))
        gold = gold * 3 / 2;
    gSpireResult.bp *= RUN.act;
    gSpireResult.gold = gold;
    gSpireResult.healPercent = heal;
    RUN.gold = min(9999, RUN.gold + gold);
    RUN.bp += gSpireResult.bp;

    if (sRoomType == SPIRE_ROOM_ELITE || sRoomType == SPIRE_ROOM_BOSS)
        Spire_OpenCards(SPIRE_CARDS_RELICS, RewardMoves);
    else
        RewardMoves();
}
