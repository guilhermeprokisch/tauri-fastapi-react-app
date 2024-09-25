import logging
import shutil
import subprocess
from pathlib import Path

import PyInstaller.__main__
from colorama import Fore, Style, init

init()

logging.basicConfig(format="%(message)s")
logger = logging.getLogger(__name__)


def colored_log(message, color=Fore.WHITE):
    logger.info(f"{color}{message}{Style.RESET_ALL}")


def install():
    colored_log("Build Fast Api Binary...", Fore.CYAN)
    path_to_main = str(Path("src-python/main.py").absolute())
    PyInstaller.__main__.run(
        [path_to_main, "--onefile", "--name=api", "--log-level=ERROR"]
    )
    post_install()


def post_install() -> None:
    colored_log("Running post-build steps...", Fore.CYAN)

    # Create src-tauri/binaries directories if they don't exist
    dist_path = Path("src-tauri", "binaries")
    dist_path.mkdir(parents=True, exist_ok=True)

    # Get rustc host information
    try:
        rustc_output = subprocess.check_output(
            ["rustc", "-Vv"], universal_newlines=True
        )
        host_info = next(
            (
                line.split(": ")[1].strip()
                for line in rustc_output.split("\n")
                if line.startswith("host:")
            ),
            "",
        )
    except subprocess.CalledProcessError:
        host_info = ""
        colored_log("Warning: Failed to get rustc host information", Fore.YELLOW)

    colored_log("Moving files to src-tauri...", Fore.CYAN)
    scripts = ["api"]  # Replace with your actual script names
    for script in scripts:
        source = Path("dist")
        destination = Path(dist_path)
        shutil.move(f"{source}/{script}", f"{destination}/{script}-{host_info}")
        shutil.rmtree(f"{source}")
        colored_log(f"Updated {script}", Fore.GREEN)

    colored_log("Cleaning up...", Fore.CYAN)
    shutil.rmtree(Path("build"))
    colored_log("Removed build directory", Fore.GREEN)


if __name__ == "__main__":
    install()
