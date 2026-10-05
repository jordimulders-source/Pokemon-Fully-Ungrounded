@ Project Grounded: kit voor Battle! Victini (victini_theme.py): 36 kick, 37 snare, 38 roffelsnare, 39 clap,
@ 40 crash, 41 grote crash, 42 hihat, 43-46 toms laag -> hoog. Alles DirectSound.
voice_group victini_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 160
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 170
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 160
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 140
	voice_directsound_no_resample 60, 50, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 190
	voice_directsound_no_resample 60, 78, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 200
	voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 150
	voice_directsound 45, 40, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 50, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 55, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 60, 88, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180

