#ifndef GUARD_STADIUM_H
#define GUARD_STADIUM_H
// Project Grounded: Battle Stadium (Pokémon World Tournament, zie STADIUM_DESIGN.md)
//   src/stadium.c          toernooi, gevechten, compagnons, specials
//   src/stadium_screens.c  bracket op papier, wedstrijdkaart, compagnonkeuze, meldingen
//   src/data/stadium_pool.h  pool en compagnons (tools/grounded/stadium/pool.py)

#include "constants/stadium.h"

#define STADIUM_LEVEL           50
// Onzichtbare meter (Jordi): ±100 punten per toernooi = ±1 nieuwe compagnon (drempels elke 100, pool.py)
#define STADIUM_POINTS_TOURNAMENT   70
#define STADIUM_POINTS_WIN          10
#define STADIUM_POINTS_TITLE        20
#define STADIUM_SINGLES_MONS    4
#define STADIUM_DOUBLES_MONS    3
#define STADIUM_MAX_ENTRANTS    32
#define STADIUM_PLAYER          0       // deelnemer 0 = de speler (en compagnon)
#define STADIUM_MAX_POOL        128
#define STADIUM_MAX_COMPANIONS  160     // was 128 (v0.9: Selene/Reginald/Helia); oude saves: lastCompanion/tournaments terug op 0

enum StadiumUnlock
{
    STADIUM_UNLOCK_START,   // vanaf het begin
    STADIUM_UNLOCK_BEAT,    // trainer verslagen in het Stadium (waarde = TRAINER_*)
    STADIUM_UNLOCK_POINTS,  // Stadium-punten (waarde = drempel)
};

struct StadiumEntrant
{
    u16 trainerId;
    u16 rating;         // gem. BST van de singles-keuze (simulatie)
    u8 rivalFor;        // 0 = altijd; 1 = alleen als de speler een jongen is (May), 2 = meisje (Brendan)
    u8 singlesMask;     // teamplekken voor singles (4)
    u8 doublesMask;     // teamplekken voor doubles/compagnon (3)
    u16 gfx;            // overworld-sprite in de arena
};

struct StadiumCompanion
{
    u16 partnerId;      // PARTNER_STADIUM_*
    u16 trainerId;      // bron-trainer (TRAINER_NONE bij trio's); niet tegelijk tegenstander
    bool8 frontPic;     // geen rugplaatje: voorplaatje naast de speler (zoals de Frontier-tag battles)
    u8 unlockType;      // enum StadiumUnlock
    u16 unlockValue;
    u16 gfx;            // overworld-sprite in de arena (naast de speler)
};

// Opslag in SaveBlock2 (STADIUM_SAVE_SIZE)
struct StadiumSave
{
    u16 points;         // onzichtbare meter (STADIUM_POINTS_*)
    u16 matchesWon;
    u16 titles[2];      // gewonnen toernooien singles/doubles
    u32 beaten[STADIUM_MAX_POOL / 32];          // deelnemers ooit verslagen (bit per poolplek)
    u32 seen[STADIUM_MAX_COMPANIONS / 32];      // compagnons waarvan de melding al getoond is
    u8 lastCompanion;
    u8 tournaments;     // toernooien begonnen (max. 255; de omroeper: nieuwkomer of terugkeerder)
    u8 unused[2];
};
#define STADIUM_SAVE (*(struct StadiumSave *)gSaveBlock2Ptr->stadiumData)

extern bool8 gStadiumBattle;

// battle_main.c: team van een tegenstander (keuze uit de pool, level 50)
u8 Stadium_BuildTrainerParty(struct Pokemon *party, u16 trainerNum, bool8 firstTrainer);
bool32 Stadium_PartnerUsesFrontPic(void);
u32 Stadium_CapIvs(u32 ivs);
void Stadium_ScaleCompanionMon(struct Pokemon *mon);
u16 Stadium_CompanionSourceTrainer(void);
const u8 *Stadium_GetWinText(u32 opponent);
const u8 *Stadium_GetDefeatText(u32 trainerId);

// Project Grounded: Battle Casino (src/battle_casino.c)
extern bool8 gCasinoBattle;
u8 Casino_BuildEnemyParty(struct Pokemon *party, u16 trainerNum, bool8 firstTrainer);
const u8 *Casino_GetWinText(u16 trainerId);
const u8 *Casino_GetPlayerSideName(void);
bool32 Casino_HidePlayerTrainerPic(void);
void Casino_HasBp(void);
void Casino_OpenCard(void);
void Casino_StartArenaBattle(void);
void Casino_SetArenaGfx(void);
void Casino_Resolve(void);
void Casino_CheckUnlock(void);
void Casino_DebugUnlockAll(void);

// specials (data/maps/BattleFrontier_StadiumLobby/scripts.inc)
void Stadium_PrepareChooseParty(void);
void Stadium_StartTournament(void);
void Stadium_ShowNextMatch(void);
void Stadium_StartMatch(void);
void Stadium_AfterMatch(void);
void Stadium_EndTournament(void);
void Stadium_ChooseCompanion(void);
void Stadium_ShowUnlocks(void);
void Stadium_HasNewUnlocks(void);
void Stadium_DebugUnlockAll(void);
void Stadium_GetRecord(void);
void Stadium_SetArenaGfx(void);
void Stadium_GetMatchNames(void);
void Stadium_GetBpText(void);
void Stadium_GetAnnouncerLine(void);

// stadium.c -> stadium_screens.c
u32 Stadium_PoolCount(void);
const struct StadiumEntrant *Stadium_GetEntrant(u32 i);
u32 Stadium_CompanionCount(void);
const struct StadiumCompanion *Stadium_GetCompanion(u32 i);
bool32 Stadium_IsCompanionUnlocked(u32 i);
bool32 Stadium_IsCompanionVisible(u32 i);
u16 Stadium_EntrantTrainer(u8 slot, u32 member);    // trainer van bracketplek (lid 0/1 bij doubles)
void Stadium_GetEntrantName(u8 slot, u8 *dst);
u16 Stadium_EntrantPic(u8 slot);
u16 Stadium_EntrantMemberPic(u8 slot, u32 member);
u8 Stadium_GetMode(void);
u8 Stadium_GetRound(void);
u8 Stadium_GetRoundCount(void);
u8 Stadium_GetBracketSlot(u32 round, u32 pos);   // STADIUM_PLAYER, deelnemer, of 0xFE = nog onbekend
u8 Stadium_GetCompanionIndex(void);
void Stadium_SetCompanionIndex(u8 i);
u8 Stadium_TakeNewUnlock(void);                  // volgende nieuwe compagnon (0xFF = geen)
void Stadium_OpenBracket(void (*onDone)(void));
void Stadium_OpenCompanionSelect(void (*onDone)(void));
void Stadium_OpenUnlock(u8 companion, void (*onDone)(void));

#endif // GUARD_STADIUM_H
