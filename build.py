#!/usr/bin/python

import pathlib
import glob

COMPONENTS_DIR = pathlib.Path("components")
SOURCE_DIR = pathlib.Path("src")
OUTPUT_DIR = pathlib.Path("out")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COMPONENTS = {}



for c in COMPONENTS_DIR.glob("*"):
    name = pathlib.Path(c)

    if name.is_file() and name.name.endswith(".component.html"):
        COMPONENT_NAME = name.name[0:-len(".component.html")]
        COMPONENTS[COMPONENT_NAME] = name.read_text()
        # print(COMPONENT_NAME)

for file in SOURCE_DIR.rglob("*"):
    name = pathlib.Path(file)
    if name.is_dir(): continue
    p = OUTPUT_DIR / name.relative_to(SOURCE_DIR)

    p.parent.mkdir(parents=True, exist_ok=True)
    if name.name.endswith(".html"):
        data = name.read_text()
        # Apply substitutions
        for k, v in COMPONENTS.items():
            sub = f"{{{{{k}}}}}"

            data = data.replace(sub, v)
        p.write_text(data)

    else:
        # pass
        p.write_bytes(name.read_bytes())
