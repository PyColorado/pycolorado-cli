import pkgutil
import os
import importlib
from inspect import getmembers, isfunction

commands = {}

for _, module_name, _ in pkgutil.iter_modules([os.path.split(__file__)[0]]):
    if module_name != "__init__":

        def function_is_local(object):
            return isfunction(object) and getattr(object, "__module__", None) == "commands." + module_name

        module = importlib.import_module("." + module_name, __package__)

        # By default, all local function members of the module should be included as potential commands
        commands[module_name] = dict(getmembers(module, function_is_local))
