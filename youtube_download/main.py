import os
import subprocess
import sys

# 颜色定义
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
SKYBLUE = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[m"

# 分隔线
def print_separator():
    print(f"{SKYBLUE}" + "*" * 60 + f"{RESET}")

# 显示菜单
def show_menu():
    print(f"{YELLOW}")
    print("    1: playlist (bestvideo + bestaudio)")
    print("    2: no playlist (bestvideo + bestaudio)")
    print("    3: playlist (videoID + audioID)")
    print("    4: no playlist (videoID + audioID)")
    print("    5: yt-dlp -F url")
    print("    6: yt-dlp -f --list-formats --playlist-items 1,2 url")
    print("    7: only audio")
    print("    8: download thumbnail")
    print("    9: list subs")
    print("    10: download subs")
    print(f"{RESET}")

# 显示格式选项
def show_formats():
    print(f"{BLUE}")
    print("    ID    EXT    RESOLUTION    FPS    MORE INFO")
    print("    140   m4a    audio only                    ")
    print("    312   mp4    1920*1080     60     1080p60  ")
    print("    623   mp4    2560*1440     60     1440p60  ")
    print("    628   mp4    3840*2160     60     2160p60  ")
    print(f"{RESET}")

# 运行 yt-dlp 命令
def run_yt_dlp(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error executing yt-dlp: {e}{RESET}")

# 处理用户选择
def main():
    print_separator()
    show_menu()
    show_formats()
    print_separator()

    # 读取用户输入
    try:
        input_num = int(input(f"{GREEN}Please Enter Num 1~10 for yt-dlp: {RESET}"))
    except ValueError:
        print(f"{BLUE}Enter num error, Please enter again!{RESET}")
        sys.exit(1)

    if input_num in {1, 2, 3, 4, 7}:
        os.chdir(os.path.expanduser("~/Videos"))

    print(f"{RED}")
    url = input("Enter the URL: ")

    if input_num == 1:
        playlist_start = input("Enter the number of playlist-start: ")
        playlist_end = input("Enter the number of playlist-end: ")
        run_yt_dlp(
            f'yt-dlp -f bestvideo+bestaudio --playlist-start {playlist_start} --playlist-end {playlist_end} "{url}"'
        )

    elif input_num == 2:
        run_yt_dlp(f'yt-dlp -f bestvideo+bestaudio "{url}"')

    elif input_num == 3:
        video_id = input("Enter the videoID: ")
        audio_id = input("Enter the audioID: ")
        playlist_start = input("Enter the number of playlist-start: ")
        playlist_end = input("Enter the number of playlist-end: ")
        run_yt_dlp(
            f'yt-dlp -f {video_id}+{audio_id} --playlist-start {playlist_start} --playlist-end {playlist_end} "{url}"'
        )

    elif input_num == 4:
        video_id = input("Enter the videoID: ")
        audio_id = input("Enter the audioID: ")
        run_yt_dlp(f'yt-dlp -f {video_id}+{audio_id} "{url}"')

    elif input_num == 5:
        run_yt_dlp(f'yt-dlp -F "{url}"')

    elif input_num == 6:
        run_yt_dlp(f'yt-dlp -f --list-formats --playlist-items 1,2 "{url}"')

    elif input_num == 7:
        print(f"{YELLOW}")
        print("    1: flac")
        print("    2: m4a")
        print(f"{RESET}")

        try:
            input_format = int(
                input(f"{GREEN}Please Enter Num 1 or 2 for audio format: {RESET}")
            )
        except ValueError:
            print(f"{BLUE}Enter num error, Please enter again!{RESET}")
            sys.exit(1)

        if input_format == 1:
            run_yt_dlp(f'yt-dlp -x --audio-format flac "{url}"')
        elif input_format == 2:
            run_yt_dlp(f'yt-dlp -x --audio-format m4a "{url}"')
        else:
            print(f"{BLUE}Enter num error, Please enter again!{RESET}")

    elif input_num == 8:
        run_yt_dlp(
            f'yt-dlp --skip-download --write-thumbnail --convert-thumbnail png "{url}" -o "%(id)s.%(ext)s"'
        )

    elif input_num == 9:
        run_yt_dlp(f'yt-dlp --list-subs "{url}"')

    elif input_num == 10:
        run_yt_dlp(
            f'yt-dlp --write-auto-sub --sub-lang "zh,zh-Hans,zh-CN,en" --sub-format vtt --convert-subs srt --skip-download "{url}" -o "%(id)s.%(ext)s"'
        )

    else:
        print(f"{BLUE}Enter num error, Please enter again!{RESET}")

if __name__ == "__main__":
    main()
