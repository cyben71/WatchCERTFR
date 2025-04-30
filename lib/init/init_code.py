import sys
import importlib
import inspect
from pathlib import Path
from typing import Dict
import __main__

            
def build_simple_classname() -> Dict[str, str]:
    """
    Dictionary allow you to use an alias for calling a class
    Example:
    Logger => log.<function>
    """
    aliases = {
    "Logger": "log",
    "ConfigProperties": "cfg_prop",
    "AppEnv": "app_env",
    "ConfigYaml": "cfg_yaml"
    }
    return aliases

#def load_and_initialize_classes(init_dir, global_vars=None) -> dict:
def load_and_initialize_classes(init_dir: str, 
                                global_vars: Dict[str, str]
                                ) -> Dict[str, str]:
    """
    Load dynamically Python classes included in lib/init folder. 
    Classes are instancied and load their own loading variables by reading their constructor.
    Args:
        init_dir (str): Emplacement des classes Python (default: lib/init/)
        global_vars (str, optional): _description_. Defaults to None.
    Returns:
        dict: Dictionnaire des classes Python chargées
    """
    instances: Dict[str, str] = {}
    # Set lib folder
    init_path = Path(init_dir).resolve()

    if not init_path.exists() or not init_path.is_dir():
        raise FileNotFoundError(f"Folder '{init_dir}' not found or not available.")

    # Add lib folder to PYTHONPATH
    if str(init_path) not in sys.path:
        sys.path.append(str(init_path))

    instances: Dict[str, str] = {}
    aliases = build_simple_classname()
    #custom_args = custom_args or {}
    
    # Find Python files (.py) into folder
    for file in Path(init_dir).glob("*.py"):
        module_name = file.stem
        module = importlib.import_module(module_name)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                try:
                    # Get constructor parameters (__init__)
                    init_signature = inspect.signature(obj.__init__)
                    init_params = init_signature.parameters

                    # Filtering global_vars to keep only required
                    required_args = {
                        key: value
                        for key, value in global_vars.items()
                        if key in init_params and key != "self"
                    }
                    
                    # Instanciating classes with filtered args
                    instance = obj(**required_args)
                    #instance = obj(**args_to_use)
                    instances[name] = instance
                    
                    # Find & Push instance into global namespace                    
                    alias = aliases.get(name, name)  # If alias exists, use it
                    setattr(__main__, alias, instance)
                except Exception as err:
                    raise err                 
    return instances


    