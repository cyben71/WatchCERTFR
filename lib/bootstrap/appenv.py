__version__ = "1.1.0"

import os
import sys
import getpass
import platform
import re
# from datetime import datetime
from typing import Optional, Dict
from pathlib import Path
import shutil

try:
    from dotenv import dotenv_values, find_dotenv
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False

class AppEnv:
    """
    A tool class to get information about the execution environment.
    Handles OS detection, date/time utilities, file system helpers,
    and user environment variable loading for any context:
    local, remote, interactive or non-interactive (JupyterLab, VS Code remote, systemd).

    On Linux  : parses ~/.bash_env, ~/.bashrc, ~/.bash_profile, ~/.profile
                and injects ALL exported variables into os.environ (overwrite enabled).
    On Windows: captures full os.environ snapshot (already populated by the OS).

    Calling load() or relaunching init_env() always produces a fresh, complete snapshot.
    """
    alias = "appenv"

    _LINUX_PROFILE_FILES = [
        ".bash_env",
        ".bashrc",
        ".bash_profile",
        ".profile",
    ]

    def __init__(self):
        """Constructor — triggers a full environment load immediately."""
        self._loaded_vars: Dict[str, str] = {}
        self._dotenv_path: Optional[str] = None
        self.load()

    #####################################
    ##### PUBLIC METHOD & FUNCTIONS #####
    #####################################

    @property
    def loaded_vars(self) -> Dict[str, str]:
        """
        Return the full snapshot of environment variables loaded by AppEnv.

        On Linux  : variables parsed from shell profile files (including updates).
        On Windows: full os.environ snapshot.

        Returns:
            Dict[str, str]: {key: value} of all loaded variables.
        """
        return self._loaded_vars

    # def load(self) -> Dict[str, str]:
    def load(self) -> Dict[str, str]:
        """
        Load (or reload) all environment variables into os.environ.

        Always performs a full reload — existing values in os.environ
        are overwritten if a newer value is found in the profile files
        and/or in the .env file.

        Loading order (each step can overwrite the previous one):
            1. OS baseline   : full os.environ snapshot (Windows) or
                               ~/.bash_env, ~/.bashrc, ~/.bash_profile,
                               ~/.profile (Linux).
            2. .env file     : loaded LAST, values always win over the
                               OS baseline above (override enabled).

        Call this after modifying ~/.bash_env, any shell profile, or your
        .env file, without restarting the kernel.

        Args:
            The .env file is auto-discovered by walking up
            from the current working directory (same principle as
            locating APPLICATION_HOME). If no .env file is found,
            this step is silently skipped.

        Returns:
            Dict[str, str]: Full snapshot of loaded variables.

        Example:
            # Initial load (called automatically at init)
            epy = init_env()

            # After modifying ~/.bash_env or your .env file:
            epy.appenv.load()
            print(epy.appenv.loaded_vars)
        """
        self._loaded_vars = {}

        if os.name == "nt":
            self._load_windows()
        else:
            self._load_linux()

        # .env is always loaded last so its values take precedence over
        # anything already present in os.environ (OS vars, shell profile vars).
        self._load_dotenv()

        return self._loaded_vars

    @staticmethod
    def get_system() -> str:
        """Return type of system."""
        return f"{platform.system()} ({platform.platform()})"

    @staticmethod
    def get_hostname() -> str:
        """
        Return hostname.
        You can bypass device hostname by setting your own HOSTNAME variable with a .env file
        """
        # if os.environ["HOSTNAME"] is not None:
        if "HOSTNAME" in os.environ.keys():
            return os.environ["HOSTNAME"]
        else:
            return platform.node()

    @staticmethod
    def get_username() -> str:
        """
        Retrieves the name of the current user logged into the system.

        This function first checks the environment variables 'USERNAME' (Windows) and 'USER' (Linux/macOS).
        If neither is available or is empty, it falls back to `getpass.getuser()`.
        Compatible with Linux, Windows, and macOS.

        Returns:
            str: The username of the current user.
        """

        # Check OS variables first
        username = os.getenv('USERNAME') or os.getenv('USER')

        # Default value by getpass.getuser() if username is null
        if not username:
            username = getpass.getuser()

        return username

    @staticmethod
    def is_folder_exists(location: str) -> bool:
        """
        Check if a folder exists at specified location.

        Args:
            location (str): Folder location.

        Returns:
            bool: True if folder exists, False otherwise.
        """
        return os.path.exists(location)

    @staticmethod
    def is_file_exists(location: str) -> bool:
        """
        Check if a file exists at specified location.

        Args:
            location (str): File location.

        Returns:
            bool: True if file exists, False otherwise.
        """
        return os.path.isfile(location)

    @staticmethod
    def rm_file(location: str) -> bool:
        """
        Delete a file if it exists.

        Args:
            location (str): File location.

        Returns:
            bool: True if successfully deleted, False otherwise.
        """
        if os.path.isfile(location):
            try:
                os.remove(location)
                return True
            except Exception:
                print(f"File ({location}) not deleted")
                return False
        print(f"File {location} is not found or is not available")
        return False

    @staticmethod
    def mkdir(location: str) -> bool:
        """
        Create a folder at specified location.

        Args:
            location (str): Folder location to create.

        Returns:
            bool: True if successfully created, False otherwise.
        """
        try:
            os.makedirs(location)
            print(f"Folder {location} successfully created")
            return True
        except Exception:
            print(f"Folder {location} not created")
            return False

    @staticmethod
    def mv_file(source: str, destination: str) -> bool:
        """
        Move a file to a given destination (equivalent to `mv` on Linux).
        If the destination folder tree does not exist, it is created automatically.

        Args:
            source (str): Path of the file to move.
            destination (str): Destination path (file or folder).
                - If `destination` ends with a folder separator or matches
                an existing folder, the file is moved into that folder,
                keeping its original name.
                - Otherwise, `destination` is treated as the full path of
                the destination file (allows renaming on the fly).

        Returns:
            bool: True if the move succeeded, False otherwise.

        Example:
            epy.appenv.mv_file("data/report.csv", "archive/2026/report.csv")
            epy.appenv.mv_file("data/report.csv", "archive/2026/")
        """
        if not AppEnv.is_file_exists(source):
            print(f"File {source} is not found or is not available")
            return False

        dest_path = Path(destination)

        # Determine whether the destination should be treated as a folder
        # (existing folder, or trailing separator notation)
        is_dir_target = destination.endswith(("/", "\\")) or dest_path.is_dir()

        if is_dir_target:
            target_dir = dest_path
            target_file = target_dir / Path(source).name
        else:
            target_dir = dest_path.parent
            target_file = dest_path

        # Create the missing folder tree by reusing AppEnv.mkdir
        if str(target_dir) and not AppEnv.is_folder_exists(str(target_dir)):
            if not AppEnv.mkdir(str(target_dir)):
                return False

        try:
            shutil.move(source, str(target_file))
            print(f"File {source} successfully moved to {target_file}")
            return True
        except Exception as e:
            print(f"File {source} not moved: {e}")
            return False

    @staticmethod
    def cp_file(source: str, destination: str) -> bool:
        """
        Copy a file to a given destination (equivalent to `cp` on Linux).
        If the destination folder tree does not exist, it is created automatically.

        Args:
            source (str): Path of the file to copy.
            destination (str): Destination path (file or folder).
                - If `destination` ends with a folder separator or matches
                an existing folder, the file is copied into that folder,
                keeping its original name.
                - Otherwise, `destination` is treated as the full path of
                the destination file (allows renaming on the fly).

        Returns:
            bool: True if the copy succeeded, False otherwise.

        Example:
            epy.appenv.cp_file("data/report.csv", "backup/2026/report.csv")
            epy.appenv.cp_file("data/report.csv", "backup/2026/")
        """
        if not AppEnv.is_file_exists(source):
            print(f"File {source} is not found or is not available")
            return False

        dest_path = Path(destination)

        # Determine whether the destination should be treated as a folder
        # (existing folder, or trailing separator notation)
        is_dir_target = destination.endswith(("/", "\\")) or dest_path.is_dir()

        if is_dir_target:
            target_dir = dest_path
            target_file = target_dir / Path(source).name
        else:
            target_dir = dest_path.parent
            target_file = dest_path

        # Create the missing folder tree by reusing AppEnv.mkdir
        if str(target_dir) and not AppEnv.is_folder_exists(str(target_dir)):
            if not AppEnv.mkdir(str(target_dir)):
                return False

        try:
            # copy2 preserves metadata (timestamps, permissions), like cp -p
            shutil.copy2(source, str(target_file))
            print(f"File {source} successfully copied to {target_file}")
            return True
        except Exception as e:
            print(f"File {source} not copied: {e}")
            return False
    

    @property
    def dotenv_path(self) -> Optional[str]:
        """Chemin absolu du .env chargé, ou None si aucun trouvé."""
        return self._dotenv_path


    @staticmethod
    def find_files(location: str, pattern: str, recursive: bool = False) -> List[str]:
        """
        Rechercher dans un dossier les fichiers dont le nom correspond à un motif
        de type SQL LIKE, où le caractère '%' représente une chaîne de caractères
        quelconque (équivalent du '*' en shell).

        Le motif permet de combiner les deux critères habituels :
            1) le nom commence par une chaîne donnée   -> "XXX%"
            2) l'extension correspond à un motif donné -> "%.ext" ou "%.%"

        Args:
            location (str): Dossier dans lequel effectuer la recherche.
            pattern (str): Motif de recherche avec '%' comme joker.
                Exemples :
                    "XXX%.%"        -> fichiers commençant par "XXX", extension quelconque
                    "%.pdf"         -> tous les fichiers avec l'extension .pdf
                    "rapport_%.csv" -> fichiers "rapport_..." avec extension .csv
            recursive (bool): Si True, recherche aussi dans les sous-dossiers.
                Par défaut False (recherche seulement dans `location`).

        Returns:
            List[str]: Liste des chemins (str) des fichiers trouvés.
                Cette liste peut être directement utilisée comme `source`
                dans les méthodes mv_file() ou cp_file().

        Example:
            # Fichiers commençant par "XXX" quelle que soit l'extension
            files = epy.appenv.find_files("data/", "XXX%.%")

            # Déplacer tous les fichiers trouvés vers un dossier d'archive
            for f in files:
                epy.appenv.mv_file(f, "archive/2026/")
        """
        if not AppEnv.is_folder_exists(location):
            print(f"Folder {location} is not found or is not available")
            return []

        # Conversion du motif SQL LIKE ('%') vers un motif glob ('*')
        glob_pattern = pattern.replace("%", "*")
        base = Path(location)

        try:
            matches = base.rglob(glob_pattern) if recursive else base.glob(glob_pattern)
            files = [str(f) for f in matches if f.is_file()]
            return files
        except Exception as e:
            print(f"Search failed in {location} with pattern {pattern}: {e}")
            return []

    ######################################
    ##### PRIVATE METHOD & FUNCTIONS #####
    ######################################

    def _load_windows(self) -> None:
        """
        Capture full os.environ snapshot on Windows.
        os.environ is already populated by the OS at session startup —
        this method records it into _loaded_vars for display and access.
        """
        for key, value in os.environ.items():
            self._loaded_vars[key] = value

    def _load_linux(self) -> None:
        """
        Parse user shell profile files and inject ALL exported variables
        into os.environ, overwriting existing values.
        Files are processed in priority order: .bash_env first.
        """
        for filename in self._LINUX_PROFILE_FILES:
            profile = Path.home() / filename
            if profile.is_file():
                self._parse_export_file(profile)

    def _parse_export_file(self, file_path: Path) -> None:
        """
        Parse 'export KEY=value' lines from a shell file and inject
        them into os.environ (overwrite enabled).

        Handles:
            export KEY=value
            export KEY="value"
            export KEY='value'
            export KEY=$OTHER_VAR      (resolved via os.path.expandvars)
            export KEY="${OTHER_VAR}"  (resolved via os.path.expandvars)

        Skips silently:
            export KEY=$(command)      (subshell expression)

        Args:
            file_path (Path): Shell file to parse.
        """
        pattern = re.compile(r"^export\s+([A-Za-z_][A-Za-z0-9_]*)=(.*)$")

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                match = pattern.match(line)
                if not match:
                    continue

                key   = match.group(1)
                value = match.group(2).strip().strip("'\"")

                if value.startswith("$("):
                    continue

                value = os.path.expandvars(value)
                self._inject(key, value)

    def _inject(self, key: str, value: str) -> None:
        """
        Inject a variable into os.environ and record it in _loaded_vars.
        Overwrites existing values to ensure a fresh state on every load().

        Args:
            key (str): Variable name.
            value (str): Variable value.
        """
        if key:
            os.environ[key] = value
            self._loaded_vars[key] = value

    def _load_dotenv(self) -> None:
        """
        Load a ".env" file and inject ALL its variables into os.environ,
        UNCONDITIONALLY overwriting any existing value (OS env var, shell
        profile var, previously loaded .env, ...).

        Works identically on Windows and Linux (unlike _load_windows /
        _load_linux above), so behaviour is guaranteed to be the same in
        VS Code, JupyterLab, a plain terminal, or a systemd service.

        Lookup order for the .env file:
            Auto-discovery: starting from the current working directory,
            walk up parent folders until a ".env" file is found
            (delegated to python-dotenv's find_dotenv(usecwd=True)).

        If python-dotenv is not installed, or no .env file can be found,
        this step is silently skipped (no exception raised).

        Args:
            dotenv_path (str, optional): Explicit path to a .env file.
        """
        self._dotenv_path = None

        if _DOTENV_AVAILABLE:
            path = find_dotenv(filename=".env", usecwd=True)
            if not path or not Path(path).is_file():
                return
            else:
                self._dotenv_path = path
                for key, value in dotenv_values(path).items():
                    if value is not None:
                        self._inject(key, value)

            # Publishing resolved path of .env file to context.CFGENV_FILE (same pattern as ConfigYaml)
            context_module = sys.modules.get("lib.bootstrap.context")
            if context_module and hasattr(context_module, "context"):
                context_module.context.CFGENV_FILE = self._dotenv_path
