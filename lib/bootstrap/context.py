__version__ = "1.0.2"

# Use real name of Class (not filename !)
from typing import Any, List, Type, TypeVar, overload
from types import SimpleNamespace
from lib.bootstrap.cfgyaml import ConfigYaml        
from lib.bootstrap.cfgproperties import ConfigProperties
from lib.bootstrap.appenv import AppEnv
from lib.bootstrap.calendar import Calendar
from lib.bootstrap.logger import Logger
from lib.bootstrap.docgenerator import DocGenerator

T = TypeVar('T')

class Context(SimpleNamespace):
    """
    Allow to display properly modules or main variables into a context called 'epy'.
    Usefull for IDE like Vscode.
    """

    # Add here all classes needed
    APPLICATION_HOME: str
    APPLICATION_NAME: str
    cfgyaml: ConfigYaml  
    cfgprops: ConfigProperties
    appenv: AppEnv
    cal: Calendar
    log: Logger
    doc: DocGenerator
    CFGYAML_FILE: str
    CFGENV_FILE: str
    CFGPROPS_FILE: str


    # it's just function signature to help IDE to display args... etc
    @overload
    def load_class(self, module_name: str, class_name: str = "", args: List[Any] = [], *, cls_type: Type[T]) -> T: 
        ...
    @overload
    def load_class(self, module_name: str, class_name: str = "", args: List[Any] = [], *, cls_type: None = None) -> Any: 
        ...

    # def load_class(self, module_name: str, class_name: str, args: list[Any] = [], cls_type: Type[T] | None = None) -> T | Any:
    def load_class(self, module_name: str, class_name: str = "", args: List[Any] = [], *, cls_type: Type[T] | None = None) -> T | Any:
        """
        Allow to load and instanciate your own python class (outside of lib/bootstrap).

        Args:
            module_name (str): Module name (without extension) to load. Ex: module_name = 'my_dummy_class'
            class_name (str, optional): Class name to load. Defaults to None.
            args (list, optional): List of arguments required by module. Defaults to [].
            cls_type (Type[T], optional): Expected class type for static analysis. Defaults to None.

        Returns:
            cls (object): a properly loaded module with its class

        Example:
            # Load my custom class
            cls: MyDummyClass = epy.load_class(
                module_name='my_dummy_class', 
                args=[epy, APPLICATION_NAME]
                cls_type=MyDummyClass
                )
        """
        ...


# Unique instance of global context
context = Context()