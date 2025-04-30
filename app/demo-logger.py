#!/usr/bin/env python
# coding: utf-8

# In[1]:


APPLICATION_NAME = "DEMO_LoggerClass"


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


# ## Testing log functions

# In[3]:


log.info(f"Testing INFO message : {app_env.get_current_date()} {app_env.get_current_time()}")


# In[4]:


log.warning(f"Testing WARN message : {app_env.get_current_date()} {app_env.get_current_time()}")


# In[5]:


log.error(f"Testing ERROR message : {app_env.get_current_date()} {app_env.get_current_time()}")


# ## Testing other functions

# In[6]:


log.get_log_file


# In[7]:


log.get_log_folder

