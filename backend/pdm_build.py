import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import tomllib


@contextmanager
def temporary_venv(venv_path):
    """Context manager to ensure venv_dir is cleaned up even if an error occurs."""
    try:
        yield venv_path
    finally:
        print(f"Cleaning up temporary venv at {venv_path}...")
        shutil.rmtree(venv_path, ignore_errors=True)


def pdm_build_initialize(context):
    project_root = Path(context.root)
    package_static_dest = project_root / "django_sp_admin" / "static"
    source_static = project_root / "static"

    print(
        f"\n--- PDM Build Hook: Starting in {project_root} (target: {context.target}) ---"
    )

    # For wheel builds (built from sdist), static files are already present
    # in django_sp_admin/static so nothing to do
    if context.target == "wheel":
        print("Wheel build detected, skipping Tailwind build.")
        return

    # --- sdist build only from here ---
    venv_dir = project_root / ".build-venv"
    venv_python = venv_dir / "bin" / "python"

    # 1. Read dependencies from pyproject.toml
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text())
    dependencies = pyproject["project"]["dependencies"]
    dev_dependencies = pyproject["dependency-groups"]["dev"]

    with temporary_venv(venv_dir):
        # 2. Create a temporary venv
        print("Creating temporary build venv...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

        # 3. Install all dependencies into the venv
        print("Installing project and dev dependencies...")
        subprocess.run(
            [
                str(venv_python),
                "-m",
                "pip",
                "install",
                "--quiet",
                *dependencies,
                *dev_dependencies,
            ],
            check=True,
            cwd=project_root,
        )

        # 4. Run tailwind build using the venv's Python
        print("Building Tailwind CSS...")
        try:
            subprocess.run(
                [str(venv_python), "manage.py", "tailwind", "build", "--force"],
                check=True,
                cwd=project_root,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error: Tailwind build failed with exit code {e.returncode}")
            sys.exit(1)

        # 5. Copy static assets into the package
        package_static_dest.mkdir(parents=True, exist_ok=True)
        if source_static.exists():
            print(f"Copying assets from {source_static} to {package_static_dest}")
            shutil.copytree(
                source_static,
                package_static_dest,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("images"),
            )
        else:
            print("Error: 'static' directory not found after tailwind build.")
            sys.exit(1)

    print("--- PDM Build Hook: Finished Successfully ---\n")


def pdm_build_finalize(context, artifact):
    """Clean up the static files copied into the package after the build."""
    # Only clean up after sdist build, wheel is built from sdist in a temp dir
    if context.target != "sdist":
        return

    project_root = Path(context.root)
    package_static_dest = project_root / "django_sp_admin" / "static"

    if package_static_dest.exists():
        print(f"\n--- PDM Build Hook: Cleaning up {package_static_dest} ---")
        shutil.rmtree(package_static_dest)
        print("--- PDM Build Hook: Cleanup done ---\n")
