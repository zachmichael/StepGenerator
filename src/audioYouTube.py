import os
import sys
import shutil
import subprocess
import yt_dlp
import re

# Add the parent directory to sys.path to allow importing modules if needed
# (Though we might not need to import anything from root if we run standalone)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
SONGS_DIR = os.path.join(ROOT_DIR, "songs")

def clean_youtube_url(url):
    """
    Cleans the YouTube URL to keep only the video ID part.
    Removes playlist parameters and other junk.
    """
    if "&" in url:
        url = url.split("&")[0]
    return url

def get_user_input(prompt):
    return input(prompt).strip()

def get_ffmpeg_path():
    """
    Reads path.txt to find ffmpeg path.
    Returns the directory containing ffmpeg (or ffmpeg.exe on Windows).
    """
    config_file = os.path.join(ROOT_DIR, "path.txt")
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip().replace('"', '').replace("'", "")
                    if "ffmpeg" in line.lower():
                        # If it points to the executable itself, return the directory
                        if line.lower().endswith("ffmpeg.exe") or line.lower().endswith("/ffmpeg"):
                            return os.path.dirname(line)
                        return line
        except:
            pass
    return None

def download_audio(url, output_path):
    """
    Downloads audio from YouTube using yt-dlp and converts to MP3.
    Returns the filename of the downloaded file.
    """
    print(f"Downloading from: {url}")
    
    ffmpeg_location = get_ffmpeg_path()
    if ffmpeg_location:
        print(f"FFmpeg path detected: {ffmpeg_location}")
        # Verify if it seems valid
        if not os.path.exists(ffmpeg_location):
             print(f"⚠️  Warning: The specified FFmpeg path does not exist: {ffmpeg_location}")
    else:
        print("FFmpeg path not found in path.txt, relying on system PATH...")
        if not shutil.which("ffmpeg"):
            print("\n❌ CRITICAL ERROR: FFmpeg not found in system or path.txt!")
            print("FFmpeg is required to download audio.")
            print("1. Download it from https://ffmpeg.org/download.html")
            print("2. Add the 'bin' folder path to path.txt (or to your system PATH)")
            raise Exception("FFmpeg not found")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': True,
    }
    
    if ffmpeg_location:
        ydl_opts['ffmpeg_location'] = ffmpeg_location

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # The file is converted to mp3, so the extension changes
        final_filename = os.path.splitext(filename)[0] + ".mp3"
        return final_filename

def main():
    if len(sys.argv) < 2:
        print("Usage: python audioYouTube.py <youtube_url>")
        return

    raw_url = sys.argv[1]
    url = clean_youtube_url(raw_url)
    
    print("\n--- YouTube Audio Downloader ---")
    print(f"Target URL: {url}")
    
    # 1. Ask for details
    print("\nEnter details to rename the file:")
    song_name = get_user_input("Song Name: ")
    artist_name = get_user_input("Artist Name: ")

    if not song_name or not artist_name:
        print("Error: Song Name and Artist Name are required.")
        return

    full_name = f"{song_name} - {artist_name}"
    safe_name = re.sub(r'[<>:"/\\|?*]', '', full_name) # Remove invalid chars
    
    # Create temp dir or just download to songs root first?
    # User said: "lo salva dentro la cartella song"
    # Let's create a specific folder for the song to keep it clean, as per ArrowVortex structure preference
    song_folder = os.path.join(SONGS_DIR, safe_name)
    if not os.path.exists(song_folder):
        os.makedirs(song_folder)
    
    try:
        # Download
        print("\nStarting download and conversion...")
        downloaded_file = download_audio(url, song_folder)
        
        # Rename
        final_mp3_path = os.path.join(song_folder, f"{safe_name}.mp3")
        
        # Check if downloaded file name is different (yt-dlp uses video title)
        if os.path.exists(downloaded_file):
            # Verify we aren't overwriting same name (unlikely if title matches but good to check)
            if downloaded_file != final_mp3_path:
                if os.path.exists(final_mp3_path):
                    os.remove(final_mp3_path)
                os.rename(downloaded_file, final_mp3_path)
            print(f"\n✅ File saved: {final_mp3_path}")
        else:
            print(f"\n❌ Error: Downloaded file not found: {downloaded_file}")
            return

        # 2. Run the generation pipeline directly
        print(f"\n✅ Audio downloaded. Now place a matching .sm file (with BPM/timing)")
        print(f"   in the same folder: {song_folder}")
        print(f"   Then run option 1 from the main menu to generate the chart.")
        print(f"\n   Or run directly: python3 src/stepmania_generator.py")

    except Exception as e:
        print(f"\n❌ Error during process: {e}")
        # Clean up if empty folder
        if os.path.exists(song_folder) and not os.listdir(song_folder):
            os.rmdir(song_folder)

if __name__ == "__main__":
    main()
