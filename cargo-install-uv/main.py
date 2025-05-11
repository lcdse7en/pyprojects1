import argparse
import shutil
import subprocess
import sys
from pathlib import Path

def is_command_available(cmd):
    return shutil.which(cmd) is not None

def is_uv_installed():
    return is_command_available("uv")

def install_uv(force=False):
    if is_uv_installed() and not force:
        print("✅ uv 已安装，跳过安装。")
        return

    try:
        print("📦 正在使用官方安装脚本安装 uv ...")
        subprocess.run(
            "curl -LsSf https://astral.sh/uv/install.sh | sh",
            shell=True,
            check=True,
        )
        print("✅ uv 安装完成，你可以运行 `uv` 来使用它。")
    except subprocess.CalledProcessError:
        print("❌ 安装 uv 失败，请检查网络连接或 curl 输出。")
        sys.exit(1)

def uninstall_uv():
    uv_path = shutil.which("uv")
    if not uv_path:
        print("⚠️ 未检测到 uv，无需卸载。")
        return

    try:
        print(f"🗑️ 正在卸载 uv：{uv_path}")
        Path(uv_path).unlink()
        print("✅ uv 已卸载。")
    except Exception as e:
        print(f"❌ 卸载失败：{e}")

def check_uv_version():
    if not is_uv_installed():
        print("⚠️ 未检测到 uv。")
        return

    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        print("📦 uv 当前版本：", result.stdout.strip())
    except Exception:
        print("⚠️ 无法获取 uv 版本。")

def main():
    parser = argparse.ArgumentParser(description="uv 安装/卸载/版本检查脚本")
    parser.add_argument(
        "--install", action="store_true", help="安装或更新 uv（默认行为）"
    )
    parser.add_argument("--uninstall", action="store_true", help="卸载 uv")
    parser.add_argument("--version", action="store_true", help="查看已安装版本")
    parser.add_argument("--force", action="store_true", help="强制重新安装")

    args = parser.parse_args()

    if not (args.install or args.uninstall or args.version):
        args.install = True  # 默认行为是安装

    if args.uninstall:
        uninstall_uv()
    elif args.version:
        check_uv_version()
    elif args.install:
        install_uv(force=args.force)

if __name__ == "__main__":
    main()
