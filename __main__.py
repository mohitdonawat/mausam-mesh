"""
⚡ MausamMesh — Main Package Execution Hook
Allows running `python -m mausam_mesh` from any terminal or virtual environment.
"""

try:
    from .cli import main
except (ImportError, ValueError):
    from cli import main

if __name__ == "__main__":
    main()
