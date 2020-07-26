import cx_Freeze
import re
base = "Console"
executables = [cx_Freeze.Executable("main.py", base=base)]
cx_Freeze.setup(
    name="Super Dogeee",
    options={"build_exe": { "includes": ["pygame", "scipy.sparse.csgraph._validation"],
            "include_files":["img/", "classes/", "entities/", "levels/", "sfx/", "sprites/", "traits/"]}},
    executables = executables
)
