# StepGenerator — Claude Context

## What this project is
A semi-automatic StepMania/OutFox chart generator. Given an audio file (.mp3) and a timing file (.sm with BPM/offset already set), it analyzes the audio and generates arrow charts for Easy, Medium, and Hard difficulties.

## How to run (WSL)
```bash
# One-time setup
sudo apt install python3.12-venv ffmpeg
./setup_venv.sh

# Launch menu
./menu.sh
```

## User workflow
1. Place `.mp3` and a pre-timed `.sm` file (BPM/offset set) in the same subfolder under `songs/`
2. Run `./menu.sh` → option **1** (Generate from SM file)
3. Pick the `.sm` — it runs audio analysis and generates all difficulty levels

The `.sm` file the user provides plays the role that ArrowVortex used to fill automatically (setting BPM/offset timing). The user creates this file externally and drops it in.

## WSL adaptations made (vs original Windows repo)
The original repo targeted Windows with `.bat` scripts and ArrowVortex GUI automation. Changes made for WSL:

| Original | WSL replacement |
|---|---|
| `menu.bat` | `menu.sh` |
| `setup_venv.bat` | `setup_venv.sh` |
| Option 1: launch ArrowVortex.exe + wait | Option 1: run `stepmania_generator.py` directly |
| `ctypes.windll` / `pyautogui` window automation | Removed — not functional in WSL |
| `ffmpeg.exe` path detection | Also handles Linux `ffmpeg` binary |
| `arial.ttf` font (Windows-only) | Font search chain: DejaVu → Liberation → FreeSans → PIL default |
| `path.txt` held ArrowVortex + ffmpeg paths | Now only holds optional ffmpeg path |

## Pipeline internals
```
stepmania_generator.py (orchestrator)
  ├── audio_analyzer.py       → analysis_data.json (beat grid, onset, RMS, chroma, holds, etc.)
  ├── 1 easy/{4th,8th,jump,hold}.py   → writes Easy #NOTES block
  ├── 2 medium/{4th,8th,jump,hold}.py → writes Medium #NOTES block
  ├── 3 hard/{4th,8th,jump,hold}.py   → writes Hard #NOTES block
  ├── src/PP_mute.py          → post-process: mute intro/outro
  ├── src/PP_IntroEnd.py      → post-process: intro/end cleanup
  ├── src/add_grafic.py       → downloads BG.png + BN.png (iTunes → Wikipedia → Bing → placeholder)
  └── src/PP_azioniFinali.py  → moves all files into named subfolder under songs/
```

## Key files
- `songs/` — drop song folders here (subfolder per song, each with `.mp3` + `.sm`)
- `path.txt` — optional: path to ffmpeg if not on system PATH
- `src/stepmania_generator.py` — main orchestrator, call directly or via menu option 1
- `src/regenerate_menu.py` — re-run generation using cached `analysis_data.json`
- `src/modifica_steps.py` — adjust difficulty ±20% on an existing chart
- `src/open_in_arrowvortex.py` — legacy file, no longer called by the menu

## Notes
- `pyautogui` and `ctypes` are not installed/used; `open_in_arrowvortex.py` is kept but unused
- The original repo is at https://github.com/zachmichael/StepGenerator (forked from Johell1NS)
