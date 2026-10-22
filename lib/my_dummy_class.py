__version__ = "1.0.0"


class Dummy:
    """
    Just a dummy python class outside of /bootstrap for example.
    """

    def __init__(self, epy, app_name):
        """
        Constructor

        Args:
            epy (_type_): EssencePy instance used in this class
            app_name (_type_): Application name
        """
        self.app_home = epy.APPLICATION_HOME
        self.app_name = f"{app_name}_test"

    
    def dummy_function(self, arg1: str) -> str:
        """
        Just a dummy function.

        Args:
            arg1 (str): A very simple argument attended as function's input

        Returns:
            str: Result of function
        """
        print(f"Hello World from {self.app_home}")

# class Foo:

#     def __init__(self):
#         return None

    
#     def dummy_function(self):
#         print(f"Bye Bye")