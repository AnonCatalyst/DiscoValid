import os
import platform
import subprocess
import sys

def install_dependencies():
    try:
        os.system("pip3 install --upgrade colorama tqdm requests pygments fake_useragent beautifulsoup4")
    except Exception as e:
        print(f"Error installing Python dependencies: {e}")
        sys.exit(1)

def install_linux_dependencies():
    try:
        os.system("sudo apt-get update")
        os.system("sudo apt-get install -y python3 python3-pip libxml2 libxml2-dev libxslt1-dev zlib1g-dev")
    except Exception as e:
        print(f"Error installing Linux dependencies: {e}")
        sys.exit(1)

def install_macos_dependencies():
    try:
        os.system("brew install python")
    except Exception as e:
        print(f"Error installing macOS dependencies: {e}")
        sys.exit(1)

def install_windows_dependencies():
    print("Please install Python and required dependencies manually.")
    sys.exit(1)

def install_termux_dependencies():
    try:
        os.system("pkg install -y python clang make libffi-dev")
    except Exception as e:
        print(f"Error installing Termux dependencies: {e}")
        sys.exit(1)

def main():
    system = platform.system().lower()

    if system == "linux":
        install_linux_dependencies()
    elif system == "darwin":
        install_macos_dependencies()
    elif system == "windows":
        install_windows_dependencies()
    elif "termux" in system:
        install_termux_dependencies()
    
    install_dependencies()
    print("Installation completed successfully.")

if __name__ == "__main__":
    main()
