#!/usr/bin/env python
# coding: utf-8

# In[1]:


APPLICATION_NAME = "DEMO_YamlClass"


# In[2]:


import os, sys
from pathlib import Path

### APPLICATION_HOME ###
APPLICATION_HOME = os.getenv("APPLICATION_HOME")
if APPLICATION_HOME is None:
    current_path = Path.cwd()   # get previous folder from current location
    # checking init_code.py is existing in lib/init
    for parent in current_path.parents:
        if (parent / 'lib/init/init_code.py').exists():
            APPLICATION_HOME = str(parent)  # APPLICATION_HOME trouvé
            break
    else:
        # Fallback : using current folder if nothing found
        APPLICATION_HOME = str(current_path)

# ### APPLICATION_NAME ###
if (os.getenv("APPLICATION_NAME") is not None): 
    APPLICATION_NAME = os.getenv("APPLICATION_NAME")
else:
    try: APPLICATION_NAME # APPLICATION_NAME not defined
    except: APPLICATION_NAME = None
    if APPLICATION_NAME is None: 
        APPLICATION_NAME = "Default"

# Load dynamically libraries files
sys.path.append(f"{APPLICATION_HOME}/lib/init")

# Import init_code for loading class included in lib/init
from init_code import load_and_initialize_classes

# Load and initiate classes with globale vars
global_vars={"app_home": APPLICATION_HOME,
             "app_name": APPLICATION_NAME}

instances = load_and_initialize_classes(f"{APPLICATION_HOME}/lib/init", global_vars)


# ## Get simple values from Yaml file

# In[3]:


# Get a yaml dict (with stripping by default)
mydict = cfg_yaml.get("aDictionnary")
print(mydict)
print(type(mydict))


# In[4]:


# Get a yaml dict (without stripping)
mydict = cfg_yaml.get("aDictionnary", strip_values=False)
print(mydict)
print(type(mydict))


# In[5]:


# Get a bloc value
bloc = cfg_yaml.get("specialDelivery")
print(bloc)


# ## Get env vars from OS

# In[6]:


# Get an OS variable environnement (with stripping) from Linux
# "user_linux" is from yaml file but value is from OS env. variables
os_var_env = cfg_yaml.get("user_linux", strip_values=True)
print(f"{os_var_env}:_")


# In[7]:


# Get an OS variable environnement (with stripping) from Windows
# "user_linux" is from yaml file but value is from OS env. variables
os_var_env = cfg_yaml.get("user_windows", strip_values=True)
print(f"{os_var_env}:_")


# In[8]:


# var_env is from yaml file but PWDTEST is user env_vars (set in Windows)
var_env = cfg_yaml.get("var_env")
print(var_env)


# ## Using imbricated values

# In[9]:


# Get a imbricated value
# "customerName" is in yaml file and come from a previous dictionary called "customer"
imb_value = cfg_yaml.get("customerName")
print(imb_value)


# In[ ]:


# Get a simple value with a placehold coming from OS env. vars
print(cfg_yaml.get('placeholder'))

