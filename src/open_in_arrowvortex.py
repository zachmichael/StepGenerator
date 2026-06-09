import os
import subprocess
import sys
import time
import glob

# Console Color Configuration
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Dynamic Path for ArrowVortex
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
CONFIG_FILE = os.path.join(ROOT_DIR, "path.txt")
ARROW_VORTEX_PATH = None

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                raw_line = line.strip()
                clean_line = raw_line.replace('"', '').replace("'", "")
                if "arrowvortex" in clean_line.lower() and clean_line.lower().endswith(".exe"):
                    ARROW_VORTEX_PATH = clean_line
                    break
    except Exception:
        pass


def to_windows_path(linux_path):
    """Convert a Linux/WSL path to a Windows path using wslpath."""
    try:
        result = subprocess.run(
            ["wslpath", "-w", linux_path],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception:
        return linux_path


def resolve_av_path(raw_path):
    """
    Resolve ArrowVortex executable path.
    In WSL, a Windows path like C:\\... can be mounted at /mnt/c/...
    Try to convert it to the WSL mount equivalent so we can check existence,
    but pass the original Windows path to the process.
    """
    if not raw_path:
        return None, None

    # If it's already a Linux path that exists, use it directly
    if raw_path.startswith("/") and os.path.exists(raw_path):
        return raw_path, raw_path

    # Windows-style path: try to convert to WSL mount path for existence check
    wsl_equivalent = raw_path
    if len(raw_path) >= 2 and raw_path[1] == ":":
        drive = raw_path[0].lower()
        rest = raw_path[2:].replace("\\", "/")
        wsl_equivalent = f"/mnt/{drive}{rest}"

    return raw_path, wsl_equivalent


def find_songs():
    """
    Finds all MP3 files in 'songs' directory (root and 1 level deep).
    Returns a list of dicts: {'name': display_name, 'mp3_path': full_path, 'sm_path': full_path_or_none}
    """
    songs_dir = os.path.join(ROOT_DIR, "songs")
    if not os.path.exists(songs_dir):
        songs_dir = os.path.join(os.getcwd(), "songs")

    if not os.path.exists(songs_dir):
        return []

    found_songs = []

    for file in os.listdir(songs_dir):
        if file.lower().endswith(".mp3"):
            full_path = os.path.join(songs_dir, file)
            sm_path = os.path.splitext(full_path)[0] + ".sm"
            if not os.path.exists(sm_path):
                sm_path = None
            found_songs.append({'name': file, 'mp3_path': full_path, 'sm_path': sm_path})

    for entry in os.scandir(songs_dir):
        if entry.is_dir():
            mp3s = glob.glob(os.path.join(entry.path, "*.mp3"))
            for mp3 in mp3s:
                sm_path = os.path.splitext(mp3)[0] + ".sm"
                if not os.path.exists(sm_path):
                    sm_path = None
                display_name = os.path.basename(mp3)
                if entry.name != os.path.splitext(display_name)[0]:
                    display_name = f"{entry.name} / {display_name}"
                found_songs.append({'name': display_name, 'mp3_path': mp3, 'sm_path': sm_path})

    return found_songs


def main():
    if not ARROW_VORTEX_PATH:
        print(f"\n{Colors.WARNING}⚠️  ARROWVORTEX PATH MISSING{Colors.ENDC}")
        print("To use this feature, you need to specify where ArrowVortex is located.")
        print(f"1. Open the {Colors.BOLD}path.txt{Colors.ENDC} file in the main folder.")
        print("2. Paste the full Windows path to the ArrowVortex executable.")
        print("   (You can also add the FFmpeg path on a new line)")
        print(f"\nExample for WSL:\n{Colors.BLUE}C:\\Program Files\\ArrowVortex\\ArrowVortex.exe\nC:\\ffmpeg\\bin{Colors.ENDC}")
        input("\nPress ENTER to go back to the menu...")
        return

    av_launch_path, av_check_path = resolve_av_path(ARROW_VORTEX_PATH)

    if not os.path.exists(av_check_path):
        print(f"{Colors.FAIL}Error: ArrowVortex not found.{Colors.ENDC}")
        print(f"Path read: {ARROW_VORTEX_PATH}")
        print(f"WSL check path: {av_check_path}")
        print("Check that the path in 'path.txt' is correct and exists.")
        input("\nPress ENTER to go back to the menu...")
        return

    # --- AUTO MODE (Argument provided) ---
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if not os.path.exists(input_path):
            print(f"{Colors.FAIL}Error: File not found: {input_path}{Colors.ENDC}")
            return

        if input_path.lower().endswith(".mp3"):
            mp3_path = input_path
            sm_path = os.path.splitext(mp3_path)[0] + ".sm"
            target_file = sm_path if os.path.exists(sm_path) else mp3_path
            sm_path_for_generation = sm_path
        elif input_path.lower().endswith(".sm"):
            sm_path = input_path
            mp3_path = os.path.splitext(sm_path)[0] + ".mp3"
            target_file = sm_path
            sm_path_for_generation = sm_path
        else:
            print(f"{Colors.FAIL}Error: Unsupported file type.{Colors.ENDC}")
            return

    # --- INTERACTIVE MODE ---
    else:
        songs = find_songs()

        if not songs:
            print(f"{Colors.FAIL}No MP3 files found in the 'songs' folder (or subfolders).{Colors.ENDC}")
            input("\nPress ENTER to go back to the menu...")
            return

        print(f"\n{Colors.HEADER}--- OPEN WITH ARROWVORTEX ---{Colors.ENDC}")
        print(f"{Colors.BLUE}Select a song to open or create:{Colors.ENDC}")

        for i, song in enumerate(songs):
            status = " [Existing SM]" if song['sm_path'] else " [New]"
            print(f"{i+1}. {song['name']}{Colors.GREEN}{status}{Colors.ENDC}")

        print("-" * 50)
        print("0. Cancel / Exit")

        try:
            choice_input = input(f"\n{Colors.BLUE}Enter number: {Colors.ENDC}")
            choice = int(choice_input)

            if choice == 0:
                return

            if choice < 1 or choice > len(songs):
                raise ValueError

            selected = songs[choice - 1]
            target_file = selected['sm_path'] if selected['sm_path'] else selected['mp3_path']
            mp3_path = selected['mp3_path']
            sm_path_for_generation = selected['sm_path'] if selected['sm_path'] else os.path.splitext(mp3_path)[0] + ".sm"

        except ValueError:
            print(f"{Colors.FAIL}Invalid choice.{Colors.ENDC}")
            return

    # --- PRE-ANALYSIS AND GRAPHICS IN BACKGROUND ---
    print(f"\n{Colors.BLUE}🔄 Starting pre-analysis and graphics search in background...{Colors.ENDC}")
    try:
        audio_analyzer_path = os.path.join(SRC_DIR, "audio_analyzer.py")
        subprocess.Popen([sys.executable, audio_analyzer_path, mp3_path, "--pre-analyze"])

        song_dir = os.path.dirname(mp3_path)
        if not (os.path.exists(os.path.join(song_dir, "BG.png")) and os.path.exists(os.path.join(song_dir, "BN.png"))):
            add_grafic_path = os.path.join(SRC_DIR, "add_grafic.py")
            subprocess.Popen([sys.executable, add_grafic_path, sm_path_for_generation])
    except Exception as e:
        print(f"{Colors.WARNING}Unable to start background processes: {e}{Colors.ENDC}")

    # Convert target file path to Windows format for ArrowVortex
    win_target = to_windows_path(os.path.abspath(target_file))
    print(f"Launching ArrowVortex: {os.path.basename(target_file)}")
    print(f"{Colors.BLUE}(Windows path: {win_target}){Colors.ENDC}")

    subprocess.Popen([av_launch_path, win_target])

    # Window automation is not available in WSL — skip it and prompt manually
    print("\n" + "="*60)
    print(f"{Colors.BOLD}INSTRUCTIONS:{Colors.ENDC}")
    print("1. ArrowVortex should open in Windows.")
    print("   If it doesn't, open the file manually from Windows.")
    print("2. Work on ArrowVortex (BPM, Offset, Notes).")
    print("3. Save the file (Ctrl+S).")
    print("4. Close ArrowVortex.")
    print("="*60 + "\n")

    input(f"{Colors.BLUE}Press ENTER when done to START GENERATION (or Ctrl+C to exit)...{Colors.ENDC}")

    if os.path.exists(sm_path_for_generation):
        print(f"\n{Colors.GREEN}.sm file detected. Starting Pipeline...{Colors.ENDC}")
        try:
            stepmania_generator_path = os.path.join(SRC_DIR, "stepmania_generator.py")
            cmd_pipeline = [sys.executable, stepmania_generator_path, "--from-sm", "--pipeline", sm_path_for_generation]
            subprocess.run(cmd_pipeline, check=True)
        except subprocess.CalledProcessError as e:
            print(f"{Colors.FAIL}Pipeline error: {e}{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}.sm file not found. Generation cancelled.{Colors.ENDC}")
        input("Press Enter...")


if __name__ == "__main__":
    main()
