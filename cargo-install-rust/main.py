import os
import shutil
import subprocess

def is_rust_installed():
    return shutil.which("rustc") is not None

def install_rust():
    print("正在安装 Rust...")
    command = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
    try:
        subprocess.run(command, shell=True, check=True, executable="/bin/bash")
        print("Rust 安装完成！")
    except subprocess.CalledProcessError as e:
        print(f"安装失败，错误码：{e.returncode}")
        return False
    return True

def load_rust_env():
    env_script = os.path.expanduser("~/.cargo/env")
    if os.path.exists(env_script):
        command = f"source {env_script} && rustc --version"
        try:
            # 使用 login shell 加载 .cargo/env 并运行 rustc
            result = subprocess.run(
                ["bash", "-lc", command], check=True, capture_output=True, text=True
            )
            print(f"Rust 安装成功: {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print("Rust 安装后环境变量加载失败。你可能需要手动执行：")
            print(f"  source {env_script}")
    else:
        print(f"未找到环境变量文件：{env_script}，请检查安装是否完整")

def main():
    if is_rust_installed():
        version = subprocess.run(["rustc", "--version"], capture_output=True, text=True)
        print(f"Rust 已安装: {version.stdout.strip()}")
    else:
        if install_rust():
            load_rust_env()

if __name__ == "__main__":
    main()
