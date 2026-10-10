@ Project Grounded: drumkit voor legendary_theme.py (Battle! Legendary Pokémon). Alleen stock-samples, geen PSG.
@ 36 taiko, 37 orkestsnare, 38 tom laag, 39 tom midden, 40 tom hoog, 41 orkestbekken, 42 crash.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group legendary_drumset, 36
	voice_directsound 57, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 200
	voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204
	voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204
	voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 204
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216
	voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
