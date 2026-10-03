#ifndef GUARD_SPIRE_H
#define GUARD_SPIRE_H

// Project Grounded: The Spire (roguelike-faciliteit, zie SPIRE_DESIGN.md)
//   src/spire.c         gevechtsmechaniek (×HP, DEFEND/blok, intenties)
//   src/spire_run.c     run-state (SaveBlock2), kaartgeneratie, kamers, relics, acts
//   src/spire_map.c     act-kaart
//   src/spire_cards.c   kaartenscherm (beloning, draft, rust, winkel, events, berichten)

#define B_ACTION_SPIRE_DEFEND   22

// DEFEND-doel (bitmasker per battler aan eigen kant)
#define SPIRE_DEFEND_BOTH       0xFF

// HP-vermenigvuldiger van de speler in procenten (vijanden: per ontmoeting, zie src/data/spire_encounters.h)
#define SPIRE_HP_PLAYER         400
#define SPIRE_LEVEL             100 // Jordi: alles in de Spire is lv 100, level is geen knop

// Blok = 15% van max HP x verdedigingsfactor x act-factor; verdeeld over beide = 60% elk
#define SPIRE_BLOCK_PERCENT     15
#define SPIRE_BLOCK_SPLIT       60

#define SPIRE_SAVE_MAGIC        0x5A
#define SPIRE_ACTS              3
#define SPIRE_FLOORS            7   // verdiepingen per act; daarboven de baas
#define SPIRE_MAX_NODES         4   // kamers per verdieping
#define SPIRE_HEAL_AFTER        10  // procent HP na een gewonnen gevecht (zie SPIRE_BALANS.md)
#define SPIRE_REST_HEAL         40  // procent HP op een rustplek (Chansey)

enum SpireRoom
{
    SPIRE_ROOM_NONE,
    SPIRE_ROOM_FIGHT,
    SPIRE_ROOM_ELITE,
    SPIRE_ROOM_REST,
    SPIRE_ROOM_SHOP,
    SPIRE_ROOM_EVENT,
    SPIRE_ROOM_BOSS,
};

enum SpireRelic
{
    SPIRE_RELIC_LEFTOVERS,     // +10% extra heal na elk gevecht
    SPIRE_RELIC_AMULET_COIN,   // +50% geld
    SPIRE_RELIC_KINGS_ROCK,    // +30% blok bij DEFEND
    SPIRE_RELIC_SCOPE_LENS,    // eigen crits +1 stage
    SPIRE_RELIC_MUSCLE_BAND,   // eigen schade +10%
    SPIRE_RELIC_WIDE_LENS,     // eigen spread-moves zonder 25% verlies
    SPIRE_RELIC_SOOTHE_BELL,   // rustplek heelt 80% i.p.v. 50%
    SPIRE_RELIC_FOCUS_SASH,    // overleef een klap op volle HP met 1 HP
    SPIRE_RELIC_COUNT,
};

enum SpireBiomeId
{
    SPIRE_BIOME_GROVE,
    SPIRE_BIOME_DOCKS,
    SPIRE_BIOME_HIVE,
    SPIRE_BIOME_FROST,
    SPIRE_BIOME_COURT,
    SPIRE_BIOME_ABYSS,
    SPIRE_BIOME_COUNT,
};

enum SpireEncounterKind
{
    SPIRE_ENC_WEAK,
    SPIRE_ENC_NORMAL,
    SPIRE_ENC_ELITE,
    SPIRE_ENC_BOSS,
};

enum SpireGimmick
{
    SPIRE_GIMMICK_NONE,
    SPIRE_GIMMICK_SLEEP,    // begint 3 beurten in slaap
};

struct SpireBiome
{
    u8 act;
    const u8 *name;
    const u8 *desc;
};

// Vijand in een ontmoeting (tools/grounded/spire/encounters.py)
struct SpireFoe
{
    u16 species;
    u16 moves[MAX_MON_MOVES];
    u16 ability;            // ABILITY_NONE = normaal
    u16 item;
    s8 unused;
    u8 hp;                  // HP-vermenigvuldiger in tienden
    u8 gimmick;             // enum SpireGimmick
    s8 boosts[5];           // totem-boosts: Atk, Def, Spe, SpA, SpD
    u8 pattern[8];          // vaste volgorde van moveslots (1-4), 0 = einde; leeg = vrije AI
};

struct SpireEncounter
{
    u8 biome;               // bij bazen: de act
    u8 kind;                // enum SpireEncounterKind
    u8 field;               // STARTING_STATUS_*
    const u8 *name;
    const u8 *hint;
    struct SpireFoe foes[2];
};

// Rentals en evoluties (tools/grounded/spire/spire_pool.py)
struct SpireRental
{
    u16 species;
    u8 tier;                // 0 C - 3 S
    u16 moves[MAX_MON_MOVES];
};

struct SpireEvolution
{
    u16 species;
    u16 targets[3];
};

// Lopende run, in gSaveBlock2Ptr->spireData: een gepauzeerde run overleeft opslaan en uitzetten.
struct SpireSave
{
    u8 magic;           // SPIRE_SAVE_MAGIC = er loopt een run
    u8 act;             // 1-3
    u8 floor;           // aantal afgeronde verdiepingen in deze act (SPIRE_FLOORS = baas aan de beurt)
    u8 node;            // gekozen kamer op die verdieping
    u32 seed;           // seed van de kaart van deze act
    u16 path;           // gekozen kamers per verdieping (2 bits per verdieping)
    u16 bp;             // BP van deze run (gaan naar je totaal als de run eindigt)
    u16 gold;           // geld voor de winkel
    u8 inRoom:1;        // kamer gestart maar nog niet klaar (gevecht gepauzeerd)
    u8 unused:7;
    u8 runsWon;
    u32 relics;         // bitveld met relics
    u8 biome;           // biome van deze act (enum SpireBiomeId)
    u8 relearns;        // aantal keer Move Relearner gebruikt (prijs stijgt)
    u16 usedEncounters; // gevechten die deze act al geweest zijn (index binnen de biome)
    u8 toxicFights;     // events: zoveel gevechten nog Toxic Spikes-risico
    u8 fungalMask;      // events: deze rentals (bit 0/1) zijn het volgende gevecht besmet
    s8 hpBonus[2];      // events: blijvende max-HP-verandering in procentpunten (bijv. -10)
    u32 eventsSeen;     // events die deze run al geweest zijn
    struct Pokemon mons[2];
};

#define SPIRE_SAVE (*(struct SpireSave *)gSaveBlock2Ptr->spireData)

struct SpireRelicInfo
{
    u16 item;           // icoon
    const u8 *name;
    const u8 *desc;
};

struct SpireMapNode
{
    u8 type;            // enum SpireRoom
    u8 x;               // pixelpositie op de kaart
    u8 links;           // bitmasker naar kamers op de volgende verdieping
};

struct SpireActMap
{
    u8 count[SPIRE_FLOORS];
    struct SpireMapNode nodes[SPIRE_FLOORS][SPIRE_MAX_NODES];
};

// uitkomst van de laatste kamer, voor de kop van het beloningsscherm
struct SpireResult
{
    u16 bp;
    u16 gold;
    u8 healPercent;
};

extern bool8 gSpireBattle;
extern u8 gSpireAct;
extern u16 gSpireBlock[MAX_BATTLERS_COUNT];
extern u16 gSpireBlockAbsorbed[MAX_BATTLERS_COUNT];
extern u8 gSpireDefendTarget[MAX_BATTLERS_COUNT];
extern u16 gSpireEnemyHp[PARTY_SIZE];
extern struct SpireResult gSpireResult;
extern const struct SpireRelicInfo gSpireRelics[SPIRE_RELIC_COUNT];
extern const struct SpireBiome gSpireBiomes[SPIRE_BIOME_COUNT];
extern u8 gSpirePattern[PARTY_SIZE][8];
extern u8 gSpireStartingStatus;
extern u8 gSpireEnvironment;
extern u8 gSpireEvolveMon;
extern u8 gSpirePatternStep[PARTY_SIZE];

// spire.c: gevecht
void Spire_OnEnemyPartyCreated(void);
void Spire_ClearBlocks(void);
u32 Spire_BlockAmount(u32 battler);
u32 Spire_BlockPercent(u32 amount, u32 target);
void Spire_AbsorbDamage(u32 battlerDef);
void HandleAction_SpireDefend(void);
bool32 Spire_TryPrintBlockAbsorbed(void);
u8 *Spire_GetIntentText(u8 *dst, u32 battler);
void Spire_ScaleMonHp(struct Pokemon *mon, u32 percent);
void Spire_CreateMon(struct Pokemon *mon, u16 species, u8 level, u8 iv, u32 ev, const u16 *moves);
void Spire_ApplyPattern(u32 battler);
void Spire_EndTurn(void);
bool32 Spire_IsMoveBanned(u16 move);

// spire_run.c: run
bool32 Spire_RunActive(void);
struct Pokemon *Spire_GetRunMon(u32 i);
bool32 Spire_HasRelic(u32 relic);
void Spire_AddRelic(u32 relic);
u32 Spire_RandomNewRelic(u32 salt);
void Spire_GenerateMap(struct SpireActMap *map, u32 seed);
bool32 Spire_IsReachable(const struct SpireActMap *map, u32 floor, u32 node);
void Spire_EnterRoom(u32 floor, u32 node);
void Spire_RoomFinished(void);
void Spire_SuspendRun(void);
void Spire_GiveUpRun(void);
void Spire_HealRun(u32 percent);
void Spire_RestorePP(void);
bool32 Spire_CanEvolve(u32 i);
void Spire_Evolve(u32 i);
void Spire_SetRental(u32 i, u16 species);
u16 Spire_RandomRental(u32 salt);
u16 Spire_RandomMove(u32 rarity, u32 salt);
u16 Spire_RandomMoveOfType(u32 rarity, u32 type, u32 salt);
u32 Spire_GetEvolutions(u16 species, u16 *targets);
void Spire_EvolveTo(u32 i, u16 target);
u32 Spire_PlayerHpPercent(u32 i);
const struct SpireRental *Spire_FindRental(u16 species);
void Spire_ReturnToField(void);
u16 Spire_GetBossSpecies(void);
void Spire_Enter(void);
void Spire_ResetRun(void);
void Spire_DebugOpen(void);

// spire_map.c
void Spire_OpenMap(void);

// spire_rest.c: Snorlax-kamp en upgrades ("+")
void Spire_OpenRest(void (*onDone)(void));
bool32 Spire_IsSlotUpgraded(struct Pokemon *mon, u32 slot);
void Spire_UpgradeSlot(struct Pokemon *mon, u32 slot);
void Spire_ClearSlotUpgrade(struct Pokemon *mon, u32 slot);
u32 Spire_GetBiomeEnvironment(void);
void Spire_LoadBiomeBackground(u16 tint, u32 amount);
bool32 Spire_IsMoveUpgraded(u32 battler, u32 move);
uq4_12_t Spire_UpgradeDamageModifier(u32 battlerAtk, u32 move);

// spire_cards.c
enum SpireCardMode
{
    SPIRE_CARDS_MOVES,      // beloning: kies een move en leer hem aan
    SPIRE_CARDS_RELICS,     // beloning: kies een relic
    SPIRE_CARDS_DRAFT,      // start van een run: kies een rental (twee keer)
    SPIRE_CARDS_REST,       // rustplek
    SPIRE_CARDS_SHOP,       // winkel
    SPIRE_CARDS_EVENT,      // event
    SPIRE_CARDS_MESSAGE,    // alleen een bericht (einde run, nieuwe act)
    SPIRE_CARDS_EVOLVE,     // nieuwe act: kies de evolutie van gSpireEvolveMon (vertakking)
};
void Spire_OpenCards(u32 mode, void (*onDone)(void));
void Spire_OpenMessage(const u8 *title, const u8 *text, void (*onDone)(void));

#endif // GUARD_SPIRE_H
