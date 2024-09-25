import shutil
import subprocess
from pathlib import Path


def post_build(interface) -> None:
    """
    Pyinstaller post build hook. Version built directory, remove generated folders.
    Include rustc host information in the final binary name.
    """
    # Create src-tauri/binaries directories if they don't exist
    dist_path = Path("src-tauri", "binaries")
    dist_path.mkdir(parents=True, exist_ok=True)
    version = interface.pyproject_data["tool"]["poetry"]["version"]

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
        interface.write_line(
            "  - <warning>Failed to get rustc host information</warning>"
        )

    interface.write_line("  - <b>Moving to src-tauri</b>")
    for script in interface.pyproject_data["tool"]["poetry-pyinstaller-plugin"][
        "scripts"
    ]:
        source = Path("dist", "pyinstaller", interface.platform)
        destination = Path(dist_path)
        shutil.move(f"{source}/{script}", f"{destination}/{script}-{host_info}")
        shutil.rmtree(f"{source}")
        interface.write_line(
            f"    - Updated "
            f"<success>{script}</success> -> "
            f"<success>{script}_{version}_{host_info}</success>"
        )

    interface.write_line("  - <b>Cleaning</b>")
    shutil.rmtree(Path("build"))
    interface.write_line("    - Removed build directory")
