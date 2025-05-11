import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    try:
        subprocess.run(command, check=True, cwd=cwd)
    except subprocess.CalledProcessError:
        print(f"命令执行失败: {' '.join(command)}")
        sys.exit(1)

def cargo_exists():
    return shutil.which("cargo") is not None

def install_rust():
    print("Rust 未安装，正在安装 Rust 工具链...")
    try:
        subprocess.run(
            [
                "curl",
                "--proto",
                "=https",
                "--tlsv1.2",
                "-sSf",
                "https://sh.rustup.rs",
                "-o",
                "rustup.sh",
            ],
            check=True,
        )
        subprocess.run(["sh", "rustup.sh", "-y"], check=True)
        os.remove("rustup.sh")
        print(
            "Rust 安装完成，请重新打开终端或运行 `source $HOME/.cargo/env` 以加载环境变量。"
        )
    except subprocess.CalledProcessError:
        print("Rust 安装失败，请手动安装 Rust。")
        sys.exit(1)

def install_binary():
    binary_path = Path("typst/target/release/typst")
    target_dir = Path.home() / ".cargo" / "bin"
    target_path = target_dir / "typst"

    if not binary_path.exists():
        print("未找到构建产物，无法安装。")
        return

    # 创建 ~/.cargo/bin（如果不存在）
    target_dir.mkdir(parents=True, exist_ok=True)

    # 拷贝文件
    shutil.copy2(binary_path, target_path)
    print(f"已将 typst 安装到 {target_path}")

    # 检查 ~/.cargo/bin 是否在 PATH 中
    if str(target_dir) not in os.environ.get("PATH", ""):
        print(
            "警告：~/.cargo/bin 不在你的 PATH 中。你可能需要手动添加到你的 shell 配置文件中。"
        )

def parse_args():
    parser = argparse.ArgumentParser(description="安装并构建 Typst")
    parser.add_argument("--force", action="store_true", help="强制重新克隆和构建")
    return parser.parse_args()

def main():
    args = parse_args()

    repo_url = "https://github.com/typst/typst"
    repo_name = "typst"

    # 检查 cargo 是否存在
    if not cargo_exists():
        choice = input("未检测到 cargo，是否安装 Rust？[Y/n]: ").strip().lower()
        if choice in ["", "y", "yes"]:
            install_rust()
        else:
            print("未安装 Rust，无法继续。")
            sys.exit(1)

    # 强制清理已有仓库
    if args.force and os.path.exists(repo_name):
        print("正在删除已有 typst 仓库...")
        shutil.rmtree(repo_name)

    # 克隆仓库
    if not os.path.exists(repo_name):
        print("正在克隆 Typst 仓库...")
        run_command(["git", "clone", repo_url])
    else:
        print("Typst 仓库已存在，跳过克隆。")

    # 构建 release 版本
    print("正在构建 release 版本...")
    run_command(["cargo", "build", "--release"], cwd=repo_name)

    # 安装到 ~/.cargo/bin
    install_binary()

    print("所有步骤完成！可以直接使用 typst（如果 ~/.cargo/bin 在 PATH 中）。")

if __name__ == "__main__":
    main()
