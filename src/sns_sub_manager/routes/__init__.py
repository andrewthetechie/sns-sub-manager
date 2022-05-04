import glob
import importlib
import os.path
from pathlib import Path

from fastapi import APIRouter


ROUTERS = list()

package_path = Path(__file__)
plugin_file_paths = glob.glob(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "*.py")
)

for plugin_file_path in plugin_file_paths:
    plugin_file_name = os.path.basename(plugin_file_path)

    module_name = os.path.splitext(plugin_file_name)[0]

    if module_name.startswith("__"):
        continue

    # -----------------------------
    # Import python file
    module = importlib.import_module(
        "." + module_name,
        package=f"{package_path.parents[1].name}.{package_path.parents[0].name}",
    )
    for item in dir(module):
        value = getattr(module, item)
        if not value:
            continue

        if type(value) == APIRouter:
            if getattr(value, "routes", None) is not None:
                ROUTERS.append(value)
