#ifndef GUARD_CONSTANTS_MAP_COMPAT_H
#define GUARD_CONSTANTS_MAP_COMPAT_H

// Gegenereerd door tools/grounded/maptools/map_compat.py, niet met de hand bewerken.
// Fully Ungrounded: verdwenen Hoenn-kaarten die de code nog noemt. Elke kaart heeft een eigen waarde in een
// groep die niet bestaat (0x40 + oude groep), dus een test erop is nooit waar. Opruimen per systeem
// (PLAN_HOENN_ERUIT.md, stap 7) laat deze lijst krimpen tot hij leeg is en weg kan.
// 64 kaarten, 16 layouts, 0 heal locations, 35 local ids.

// kaarten en layouts: sinds expansion 1.17 maakt tools/mapjson (required_map_defines.json) die zelf aan.

// local ids
enum {
    LOCALID_APPRENTICE = 0xF0,
    LOCALID_BLEND_MASTER = 0xF0,
    LOCALID_CONTESTANT_1 = 0xF0,
    LOCALID_CONTESTANT_2 = 0xF0,
    LOCALID_CONTESTANT_3 = 0xF0,
    LOCALID_CONTESTANT_4 = 0xF0,
    LOCALID_CONTEST_ARTIST = 0xF0,
    LOCALID_CONTEST_AUDIENCE_1 = 0xF0,
    LOCALID_CONTEST_AUDIENCE_2 = 0xF0,
    LOCALID_CONTEST_AUDIENCE_3 = 0xF0,
    LOCALID_CONTEST_AUDIENCE_4 = 0xF0,
    LOCALID_CONTEST_AUDIENCE_5 = 0xF0,
    LOCALID_CONTEST_AUDIENCE_6 = 0xF0,
    LOCALID_CONTEST_AUDIENCE_7 = 0xF0,
    LOCALID_CONTEST_JUDGE = 0xF0,
    LOCALID_CONTEST_LOBBY_BLENDER_2_LEADER = 0xF0,
    LOCALID_CONTEST_LOBBY_BLENDER_2_PARTICIPANT = 0xF0,
    LOCALID_CONTEST_LOBBY_BLENDER_3_LEADER = 0xF0,
    LOCALID_CONTEST_LOBBY_BLENDER_3_PARTICIPANT_1 = 0xF0,
    LOCALID_CONTEST_LOBBY_BLENDER_3_PARTICIPANT_2 = 0xF0,
    LOCALID_CONTEST_MC = 0xF0,
    LOCALID_CONTEST_POKEBALL = 0xF0,
    LOCALID_LILYCOVE_LADY = 0xF0,
    LOCALID_LILYCOVE_LADYS_MON = 0xF0,
    LOCALID_PIKE_ROOM_NPC_1 = 0xF0,
    LOCALID_PIKE_ROOM_NPC_2 = 0xF0,
    LOCALID_TOWER_LOBBY_REPORTER = 0xF0,
    LOCALID_UNION_ROOM_PLAYER_1 = 0xF0,
    LOCALID_UNION_ROOM_PLAYER_2 = 0xF0,
    LOCALID_UNION_ROOM_PLAYER_3 = 0xF0,
    LOCALID_UNION_ROOM_PLAYER_4 = 0xF0,
    LOCALID_UNION_ROOM_PLAYER_5 = 0xF0,
    LOCALID_UNION_ROOM_PLAYER_6 = 0xF0,
    LOCALID_UNION_ROOM_PLAYER_7 = 0xF0,
    LOCALID_UNION_ROOM_PLAYER_8 = 0xF0,
};


#endif // GUARD_CONSTANTS_MAP_COMPAT_H
