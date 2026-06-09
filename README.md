# StepMania/OutFox Semi-Auto Stepper

[![CI](https://github.com/Johell1NS/StepGenerator/actions/workflows/ci.yml/badge.svg)](https://github.com/Johell1NS/StepGenerator/actions/workflows/ci.yml)

A Python prototype for semi-automatic step creation

https://github.com/user-attachments/assets/2104635c-5360-45b3-b809-677a149d0cf4

---

## ⚠️ DISCLAIMER (READ BEFORE USE)

This software is a prototype. The author is not responsible for any damage resulting from use of the game.

By downloading and using this tool, you agree to the following:

1. The system automatically generates movement patterns. Some steps may be physically uncomfortable or dangerous if performed without caution.
2. The author is not responsible for physical damage or injuries (sprains, falls, etc.) that occur while playing the game.
3. The author is not responsible for hardware damage (Dance Pad, peripherals, PC) resulting from use of the software.

Always play with caution.

---

## 📖 Introduction: Why this tool?

I wanted to create this system because all the generators I've found online have never satisfied me, generating steps that, in my opinion, have nothing to do with the songs I tested.

The system is **semi-automatic** and is divided into two parts:

1. Detection of the song's BPM/Downbeat (Manual).
2. Generation of steps for the Easy, Medium, and Hard difficulty levels (Automatic).

### The problem with other algorithms

The biggest obstacle encountered during development was finding an efficient algorithm capable of detecting the exact BPM and, above all, automatically recognizing the **Downbeat** (the first quarter in 4/4 time, i.e., the loudest beat in each measure).

Currently, nothing exists that gives 100% correct results. Algorithms often fail, especially with songs that have variable BPMs, pauses, or slowdowns. If you get this first step wrong, everything that follows becomes unplayable and unfun.

### The Solution: Integration with ArrowVortex

To address this problem, the only truly efficient solution was to integrate ArrowVortex into the process.
Using ArrowVortex, we can find the exact BPM (including variations and rests) and indicate the correct tempo of the song.
Only after saving the initial `.sm` file with the correct tempo can we launch automatic arrow generation.

---

## ⚙️ Environment Preparation

> **Running on WSL (Windows Subsystem for Linux)?** See the [WSL Setup](#-wsl-setup) section below.

These actions need to be performed **only the first time**.

First install arrowvortex and ffmpeg (by adding it to your Windows Environment Variables/PATH), then do the following:

1. Clone the project.
2. Run the `setup_venv.bat` file to install the virtual environment with all necessary dependencies.
3. Open the `path.txt` file in the project folder.
4. Save the path to the ArrowVortex executable installed on your PC.
* *Example: * `C:\ArrowVortex\ArrowVortex.exe`

---

## 🐧 WSL Setup

This fork runs natively on **WSL (Windows Subsystem for Linux)**. The ArrowVortex dependency has been removed — you provide the pre-timed `.sm` file yourself.

### One-time setup

```bash
# Install system dependencies
sudo apt install python3.12-venv ffmpeg

# Clone and enter the project
git clone https://github.com/zachmichael/StepGenerator
cd StepGenerator

# Create the virtual environment and install Python dependencies
./setup_venv.sh
```

### Running the tool

```bash
./menu.sh
```

That's it. The script activates the virtual environment automatically. You can run it from any directory — it always operates relative to the project root.

### WSL workflow

Instead of ArrowVortex generating the `.sm` timing file, you provide it yourself:

1. **Prepare your song folder** inside `songs/`, following this structure:
   ```
   songs/
   └── Song Title - Artist Name/
       ├── Song Title - Artist Name.mp3
       └── Song Title - Artist Name.sm   ← you provide this
   ```
2. The `.sm` file needs valid `#BPMS` and `#OFFSET` tags set. Any tool that produces a StepMania-compatible `.sm` with correct timing will work (ArrowVortex on Windows, Stepmania's built-in editor, etc.).
3. Run `./menu.sh` → **option 1**, select your file, and the full pipeline runs automatically.

---

## 🚀 Main Operation

### 1. File Preparation

You have two ways to provide the song:

**Option A**: Local MP3 File

Place your `.mp3` file inside the project's `songs` folder.
Important: Rename the file strictly following this format:
`SongTitle - ArtistName.mp3`

**Option B**: YouTube URL

Alternatively, you can paste a YouTube video URL directly into the tool.
The software will then ask you to manually type the Song Title and Artist Name.

⚠️ CAUTION: In both cases, do not use special characters (such as apostrophes `'`, accented letters `à,è`, emojis, etc.). Keep the text simple.

Correct Examples:
* Local File: `The Fate of Ophelia - Taylor Swift.mp3`
* YouTube Input: Song Name: `The Fate of Ophelia` / Artist Name: `Taylor Swift`

### 2. Process Startup and Timing

**Windows:** Run `menu.bat` from the project root, then press **1** to select a local file or **paste a YouTube URL**.

ArrowVortex will open automatically. Use it to find the correct BPM and Downbeat, then save the `.sm` file with `Ctrl+S`. Press **ENTER** in the menu window to start generation.

**WSL:** Run `./menu.sh`, press **1**, and select your pre-timed `.sm` file. Generation starts immediately.

### 3. Generation

The system automatically generates steps for Easy, Medium, and Hard difficulty levels. Background art is also searched and downloaded automatically.

### 4. Installation

You will find the complete song folder in `songs`.
Place this folder in the `Songs` directory of your game (StepMania or Project OutFox).
Have fun!

---

## 🛠️ Other Functions

Other options can be accessed from the menu (`menu.bat` on Windows, `menu.sh` on WSL).

### Option 2: Regenerate Chart

This option regenerates only the steps using cached analysis data, bypassing the timing step.

* **When to use it:** Useful when changes have been made to the generation code (e.g. after a project update).

### Option 3: Change Difficulty

Allows you to change the density of a specific level.

1. Place the entire song folder (already generated) inside the project's `songs` folder.
2. The system will automatically detect the folder(s).
3. Choose the song you want to edit.
4. Choose the difficulty level you want to adjust.
5. Decide whether to **increase** or **decrease** the difficulty (the algorithm will add or remove **20%** of the arrows).

---

## 🔮 Future Updates

I have many ideas in mind to make the algorithm even smarter and generate charts that are increasingly dynamic and fun to play.
However, implementing these advanced features is complex and requires significant development time.
Therefore, **the future roadmap will depend heavily on the interest the community shows in the project.**

If you like the tool and want to see it grow: use it, leave a star ⭐ on the repository, or share your feedback!

In the meantime, I hope you find this first version useful and fun.

### 🎶 Example Song Included!

For your convenience, the `songs` folder includes an example simfile:
**"Walk On Water - Southby, Emily J.sm"**, along with its audio and graphics.

This song is from NoCopyrightSounds (NCS), a great source for royalty-free music perfect for testing.
You can immediately see how the generated charts look and play.

## ☕ Support me

This project is developed entirely in my spare time with the goal of making chart creation accessible to everyone. It is and will always remain free and open source.

If the tool has saved you time and you're enjoying the songs you've created, consider buying me a (virtual) coffee to support the development of future updates!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C21QBS11)
