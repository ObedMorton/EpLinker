import os
import re
import ctypes

SUPPORTED_EXTENSIONS = [".mkv", ".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"]

def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return ""

def validate_dir(path, must_exist=True):
    if must_exist and not os.path.isdir(path):
        print(f"✗ Directory does not exist: {path}")
        return False
    if not must_exist and os.path.exists(path) and not os.path.isdir(path):
        print(f"✗ Path exists but is not a directory: {path}")
        return False
    return True

def create_hardlinks(source_dir, target_dir, series_title, season_num, auto_episode=True, manual_start=1):
    season_num = int(season_num)
    episode_num = int(manual_start)

    series_title = series_title.strip()
    season_dir = os.path.join(target_dir, f"{series_title}", f"Season {season_num:02d}")
    os.makedirs(season_dir, exist_ok=True)

    files = [f for f in os.listdir(source_dir) if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS]
    files.sort()

    print(f"\nProcessing {len(files)} files...\n")

    for i, file_name in enumerate(files):
        src_path = os.path.join(source_dir, file_name)

        if auto_episode:
            match = re.search(r'(?:S\d{1,2}E(\d{1,2}))|(?:\d{1,2}[xX](\d{1,2}))|(?:[^\d](\d{1,3})[^\d])', file_name)
            if match:
                episode = next(group for group in match.groups() if group)
                try:
                    episode_num = int(episode)
                except ValueError:
                    pass  # fallback to previous value

        episode_str = f"E{episode_num:02d}"
        season_str = f"S{season_num:02d}"
        new_name = f"{series_title} - {season_str}{episode_str}{os.path.splitext(file_name)[1]}"
        dst_path = os.path.join(season_dir, new_name)

        print(f"[{i + 1}/{len(files)}] Linking: {file_name} -> {new_name}")

        try:
            os.link(src_path, dst_path)
        except Exception as e:
            print(f"✗ Failed to create link for {file_name}: {e}")

        if not auto_episode:
            episode_num += 1

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)

    source_dir = ask("Enter the source folder path: ")
    if not validate_dir(source_dir):
        exit()

    target_dir = ask("Enter the target folder path: ")
    if not validate_dir(target_dir, must_exist=False):
        exit()

    series_title = ask("Enter the series title: ")
    season_num = ask("Enter the season number: ")

    auto_choice = ask("Extract episode number from filename? (Y/N): ").upper()
    if auto_choice == 'Y':
        auto_episode = True
        manual_start = 1
    else:
        auto_episode = False
        manual_start = ask("Start episode number from: ")

    create_hardlinks(source_dir, target_dir, series_title, season_num, auto_episode, manual_start)

    ask("\nDone. Press Enter to exit...")
