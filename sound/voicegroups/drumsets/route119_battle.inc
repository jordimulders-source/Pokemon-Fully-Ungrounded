@ Project Grounded: drumkit voor route119_battle_theme.py (Route 119+-wildthema). Alleen stock-samples, geen PSG.
@ 36 kick, 37 snare, 38 crash, 39 tom laag, 40 tom midden, 41 tom hoog, 42 orkestsnare, 43 orkestbekken, 44 taiko.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group route119_battle_drumset, 36
	voice_directsound 67, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 190
	voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 190
	voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 190
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 200
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216
	voice_directsound 57, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 180
