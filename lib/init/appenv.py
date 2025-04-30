__version__ = "1.0.0"

import os
import socket
from datetime import datetime
from cfgproperties import ConfigProperties
from cfgyaml import ConfigYaml
from typing import Optional, Dict

class AppEnv:
    """
    A tool class to get simple information about environnement.
    """    

    def __init__(self, app_home: str, app_name: str):
        """Constructor
        Args:
            app_home (str): Parent location for this app
            app_name (str): Application name ("Default", by default)
        """
        
        # instance variables (hidden for more clarety in IDE)
        self._application_home = app_home
        self._application_name = app_name
        
        # Loading config files (conf, yaml or properties)
        self._config = ConfigProperties(self._application_home)
        self._yaml = ConfigYaml(self._application_home)
                
        # Getting env variables and display
        env_config = self._setup_environment()
        print(">> Configuration actuelle : <<")
        for k, v in env_config.items():
            print(f"{k}: {v}")


    #####################################
    ##### PUBLIC METHOD & FUNCTIONS #####
    #####################################
    
    # @property => use @property for getting an object from constructor (self)
    # @staticmethod => use @property for getting an objecty from an imported lib. no instance needed
 
    @property
    def get_application_home(self) -> str:
        """
        Return parent location for this app
        """
        return self._application_home

    @property
    def get_application_name(self) -> str:
        """
        Return application name
        """
        return self._application_name
    

    @staticmethod
    def get_hostname() -> str:
        """
        Return host name
        """
        return socket.gethostname()
    
    
    @staticmethod
    def get_current_date(pattern: Optional[str] = None) -> str:
        """
        Return current date (default format: %Y-%m-%d)
        format example: 
            %Y-%m-%d
            %d/%m/%Y
        Args:
            pattern (str, optional): Pattern for diplaying date
        Return:
            current_date (str): Current date displaying with chosen pattern
        """
        today = datetime.now()
        if pattern is None:
            pattern = "%Y-%m-%d"
        
        current_date = today.strftime(pattern)
        
        return current_date
    
    @staticmethod
    def get_current_time(pattern:  Optional[str] = None) -> str:
        """
        Return current time (default format: %H:%M:%S)
        Args:
            pattern (str, optional): Pattern for diplaying time
        Return:
           current_time (str): Current time displaying with chosen pattern
        """
        today = datetime.now()
        if pattern is None:
            pattern = "%H:%M:%S"
            
        current_time = today.strftime(pattern)
        
        return current_time

    @staticmethod
    def is_folder_exists(location: str) -> bool:
        """
        Checking folder exists from specified location
        Args:
            location (str): Folder location
        Return:
            exists (bool): True / False if folder exists
        """
        if not os.path.exists(location):
            exists = False
        else:
            exists = True
        return exists
    
    @staticmethod
    def is_file_exists(location: str) -> bool:
        """
        Checking file exists from specified location
        Args:
            file (str): File location
        Return:
            exists (bool): True / False if file exists
        """
        if os.path.isfile(location):
            exists = True
        else:
            exists = False
        return exists
    
    @staticmethod
    def rm_file(location: str) -> bool:
        """
        Delete a file if exists in location
        Args:
            location (str): File location
        Return:
            deleted (bool): True / False if file is sucessfully deleted
        """
        if os.path.isfile(location):
            try: os.remove(location)
            except Exception: 
                print(f"File ({location}) not deleted")
                deleted = False
            else: deleted = True
        else:
            print(f"File {location} is not found or is not available")
            deleted = False
        return deleted
    
    @staticmethod
    def mkdir(location: str) -> bool:
        """
        Create a folder from a location
        Args:
            location (str): Folder location to create
        Return:
            created (bool): True / False if folder is successfully created
        """
        try:
            os.makedirs(location)
        except Exception:
            print(f"Folder {location} not created")
            created = False
        else:
            print(f"Folder {location} successfully created")
            created = True
        return created
        
    
    ######################################
    ##### PRIVATE METHOD & FUNCTIONS #####
    ######################################

    def _setup_environment(self) -> Dict[str, str]:
        """
        Set project variables from environment variables or from file env.conf for executing project 
        Args:
            None
        Return:
            env_config (dict): dictionary of environment variables for current project
        """
        
        # Loading variables as environment variables (linked to current python context)
        os.environ["APPLICATION_HOME"] = self._application_home
        os.environ["APPLICATION_NAME"] = self._application_name
        os.environ["PYTHONHOME"] = self._config.get_venv_python_home
        os.environ["PYTHONPATH"] = self._config.get_parent_python_home
        
        # store variables in a dict "env_config"
        env_config = {
            "APPLICATION_HOME": self._application_home,
            "APPLICATION_NAME": self._application_name,
            "PARENT_PYTHON_HOME": self._config.get_venv_python_home,
            "PYTHON_HOME": self._config.get_venv_python_home,
            "ENV_CONF": self._config.get_env_file,
            "PROPERTIES_FILE": self._config.get_properties_file,
            "YAML_FILE": self._yaml.get_yaml_file
        }
        return env_config
    