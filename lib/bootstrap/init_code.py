__version__ = "1.0.2"

import importlib.util
import inspect
import platform
import sys
import os
from pathlib import Path
from lib.bootstrap.context import context, Context
from lib.bootstrap import cfgyaml
from lib.bootstrap import cfgproperties
from lib.bootstrap import logger
from lib.bootstrap import appenv

def init() -> None:
    # load and instanciate classes in context
    context.cfgyaml = cfgyaml.ConfigYaml(app_home=context.APPLICATION_HOME)
    context.cfgprops = cfgproperties.ConfigProperties(app_home=context.APPLICATION_HOME)
    context.appenv = appenv.AppEnv()
    context.log = logger.Logger(app_home=context.APPLICATION_HOME, app_name=context.APPLICATION_NAME)


# load classes included in /lib/bootstrap
# safe version. introspection of class arguments
def load_epy_cls(epy: Context, app_home: Path , app_name: str) -> None:
    init_dir = Path(app_home) / "lib/bootstrap"

    for file in init_dir.glob("*.py"):
        if file.name in {"__init__.py", "init_code.py", "bootstrap.py", "context.py"}:
            continue

        module_name = f"lib.bootstrap.{file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, file)
        if not spec or not spec.loader:
            print(f"[load_epy_cls] - No specs found for {file.name}")
            continue

        try:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"[load_epy_cls] - Error on loading module {module_name}: {e}")
            continue

        # Nom de classe par défaut : CamelCase du nom du fichier
        default_class_name = ''.join(part.capitalize() for part in file.stem.split('_'))
        cls = getattr(module, default_class_name, None)

        # Si non trouvé, chercher la première classe définie dans le module
        if cls is None:
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type):
                    cls = obj
                    break

        if cls is None:
            print(f"[load_epy_cls] - No class found in {file.name}")
            continue

        # Instanciation sécurisée si possible
        try:
            sig = inspect.signature(cls)
            params = sig.parameters
            if 'app_home' in params and 'app_name' in params:
                instance = cls(app_home=app_home, app_name=app_name)
                alias = getattr(cls, 'alias', file.stem)
                setattr(epy, alias, instance)
            #else:
            #    print(f"[load_epy_cls] Classe {cls.__name__} ne supporte pas app_home/app_name")
        except (ValueError, TypeError):
            print(f"[load_epy_cls] - Class {cls.__name__} can not be introspected (built-in ?)")
        except Exception as e:
            print(f"[load_epy_cls] - Error on instanciating of {cls.__name__}: {e}")


def load_class(module_name: str, class_name: str = None, args: list = []):
    """
    Allow to load and instanciate your own python class (outside of lib/bootstrap)
    Args:
        module_name (str): Module name (without extension) to load. Ex: module_name = 'my_dummy_class'
        class_name (str, optional): Class name to load. Defaults to None.
        args (list, optional): List of arguments required by module. Defaults to [].
    Returns:
        cls (object): a properly loaded module with its class
    """
    # if not module_name and not class_name:
    #     raise ValueError("Au moins 'module_name' ou 'class_name' doit être fourni.")

    # Add lib to python context if not exists
    lib_path = Path(context.APPLICATION_HOME) / "lib"
    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)

    # using importlib.util to loading from absolute path
    module_path = os.path.join(lib_path, f"{module_name}.py")
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Module file not found: {module_path}")

    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if not spec or not spec.loader:
            raise ImportError(f"Spec for '{module_name}' can not be created")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        raise ImportError(f"Module '{module_name}' can not be loaded - {e}")

    # Looking for class
    if class_name:
        cls = getattr(mod, class_name, None)
        if cls is None:
            raise AttributeError(f"Class '{class_name}' is not found in '{module_name}' module")
    else:
        classes = [obj for name, obj in inspect.getmembers(mod, inspect.isclass) if obj.__module__ == mod.__name__]
        if len(classes) == 1:
            cls = classes[0]
        elif len(classes) == 0:
            raise ValueError(f"No class found in module '{module_name}'")
        else:
            raise ValueError(f"More than one class found in '{module_name}'. Use 'class_name'.")

    return cls(*args)


def summarize_context() -> None:
    """
    Summurizing content of context
    """
    def supports_color() -> bool:
        if sys.stdout.isatty():
            return True
        if 'ipykernel' in sys.modules:
            return True  # Notebook Jupyter
        return False

    def color(text: str, code: str) -> str:
        return f"\033[{code}m{text}\033[0m" if supports_color() else text

    python_version = platform.python_version()
    interpreter_path = sys.executable
    is_venv = sys.prefix != sys.base_prefix
    venv_info = "✅ Virtualenv actif" if is_venv else "❌ Pas de virtualenv"

    # Modules dynamically loaded in context
    module_names = [
        name for name in dir(context)
        if not name.startswith("_")
        and name not in {"app_home", "app_name"}
        and not isinstance(getattr(context, name), (str, type(None)))
    ]

    separator = "─" * 50
    print()
    print(color("🔧  Application Context Initialized", "96"))  # cyan clair
    print(color(separator, "90"))  # gris

    print(f"{color('🖥️  SYSTEM', '91')} : {platform.system()} ({platform.platform()})")
    print(f"{color('🐍  PYTHON_VERSION', '92')} : {python_version}")
    print(f"{color('🧪  INTERPRETER_PATH', '92')} : {interpreter_path}")
    print(f"{color('📦  ENVIRONMENT', '92')} : {venv_info}")
    print(f"{color('📦  EPY_MODULES', '92')} : {', '.join(sorted(module_names)) or 'None'}")

    print(f"{color('📁  APPLICATION_HOME', '93')} : {context.APPLICATION_HOME}")
    print(f"{color('📛  APPLICATION_NAME', '93')} : {context.APPLICATION_NAME}")

    # Config files dynamically loaded in context
    if hasattr(context, 'CFGENV_FILE'):
        print(f"📘  ENV file loaded : {context.CFGENV_FILE}")
    if hasattr(context, 'CFGPROPS_FILE'):
        print(f"📘  PROPERTIES file loaded : {context.CFGPROPS_FILE}")
    if hasattr(context, 'CFGYAML_FILE'):
        print(f"📘  YAML file loaded : {context.CFGYAML_FILE}")
    
    print()
    print(color("✅  Context is ready.", "92"))  # vert
    print(color(separator, "90"))