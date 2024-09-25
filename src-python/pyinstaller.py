import shutil
import subprocess
from pathlib import Path

import PyInstaller.__main__

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "main.py")


def install():
    PyInstaller.__main__.run(
        [
            path_to_main,
            "--onefile",
            "--name=api",
        ]
    )

    post_build()


def post_build() -> None:
    """
    Pyinstaller post build hook. Version built directory, remove generated folders.
    Include rustc host information in the final binary name.
    """
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
        print("Warning: Failed to get rustc host information")

    print("Moving to src-tauri")

    scripts = ["api"]  # Replace with your actual script names

    for script in scripts:
        source = Path("dist")
        destination = Path(dist_path)
        shutil.move(f"{source}/{script}", f"{destination}/{script}-{host_info}")
        shutil.rmtree(f"{source}")
        print(f"Updated {script}")

    print("Cleaning")
    shutil.rmtree(Path("build"))
    print("Removed build directory")


if __name__ == "__main__":
    install()
