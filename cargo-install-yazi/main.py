import argparse
import shutil
import subprocess
import sys
from pathlib import Path

def is_command_available(cmd):
    return shutil.which(cmd) is not None

def configure_cargo_mirror():
    cargo_config = Path.home() / ".cargo" / "config.toml"
    cargo_config.parent.mkdir(parents=True, exist_ok=True)

    mirror_content = """
[source.crates-io]
replace-with = "ustc"

[source.ustc]
registry = "https://mirrors.ustc.edu.cn/crates.io-index"
"""
    cargo_config.write_text(mirror_content)
    print("✅ 已配置 USTC cargo 镜像源")

def install_yazi(force=False):
    if not is_command_available("cargo"):
        print("❌ 未找到 cargo，请先安装 Rust：https://www.rust-lang.org/tools/install")
        sys.exit(1)

    # NOTE: sudo chown -R se7en:se7en ~/.cargo/config.toml
    configure_cargo_mirror()

    cmd = ["cargo", "install", "yazi-fm"]
    if force:
        cmd.append("--force")

    try:
        subprocess.run(cmd, check=True)
        print("✅ Yazi 安装成功！你可以运行 `yazi` 启动它。")
    except subprocess.CalledProcessError:
        print("❌ 安装失败，请检查 cargo 的输出。")
        sys.exit(1)

def uninstall_yazi():
    if not is_command_available("cargo"):
        print("❌ 未找到 cargo，请先安装 Rust。")
        sys.exit(1)

    try:
        subprocess.run(["cargo", "uninstall", "yazi-fm"], check=True)
        print("🗑️  Yazi 已卸载。")
    except subprocess.CalledProcessError:
        print("⚠️ 卸载失败，可能未安装 yazi-fm 或 cargo 出错。")

def check_yazi_version():
    if not is_command_available("yazi"):
        print("⚠️ 未检测到 Yazi。")
        return

    try:
        result = subprocess.run(["yazi", "--version"], capture_output=True, text=True)
        print("📦 Yazi 当前版本：", result.stdout.strip())
    except Exception:
        print("⚠️ 无法获取 Yazi 版本。")

def main():
    parser = argparse.ArgumentParser(description="Yazi 安装/卸载/查询脚本")
    parser.add_argument(
        "--install", action="store_true", help="安装或更新 Yazi（默认）"
    )
    parser.add_argument("--uninstall", action="store_true", help="卸载 Yazi")
    parser.add_argument("--version", action="store_true", help="显示已安装的 Yazi 版本")

    args = parser.parse_args()

    # 默认行为：安装
    if not (args.install or args.uninstall or args.version):
        args.install = True

    if args.uninstall:
        uninstall_yazi()
    elif args.version:
        check_yazi_version()
    elif args.install:
        already_installed = is_command_available("yazi")
        if already_installed:
            print("🔁 检测到已安装 Yazi，准备更新...")
            install_yazi(force=True)
        else:
            print("📦 Yazi 未安装，开始安装...")
            install_yazi(force=False)

if __name__ == "__main__":
    main()
