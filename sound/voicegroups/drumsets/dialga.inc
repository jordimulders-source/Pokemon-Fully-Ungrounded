@ Project Grounded: drumkit voor dialga_theme.py (Battle! Dialga/Palkia). Alleen stock-samples, geen PSG.
@ 36 kick, 37 snare, 38 clap, 39 tom laag, 40 tom midden, 41 tom hoog, 42 crash.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group dialga_drumset, 36
	voice_directsound 67, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 0, 255, 170
	voice_directsound 45, 52, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 51, 64, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 57, 76, DirectSoundWaveData_unused_sc55_tom, 255, 210, 77, 180
	voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
