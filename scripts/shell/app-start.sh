#!/bin/bash

# USAGES:
# $ ./bin/app-start.sh ${PYTHON_APP.py}

set -e  # Stop the script on error

#############
# FUNCTIONS #
#############
log_message() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ${message}" | tee -a "${LOG_FILE}"
}

###############################
# APPLICATION_HOME AND CONFIG #
###############################

# starting point. current script is launched from this folder
current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# going up folders until we find init_code.py in lib/init/ folder
while [ "$current_dir" != "/" ]; do
    candidate="$current_dir/lib/init/init_code.py"
    if [ -f "$candidate" ]; then
        export APPLICATION_HOME="$current_dir"
        echo "APPLICATION_HOME: $APPLICATION_HOME"
        break
    fi
    current_dir="$(dirname "$current_dir")"
done

# Checking
if [ -z "${APPLICATION_HOME:-}" ]; then
    echo "❌  Error : Fail to find init_code.py"
    exit 1
fi

#APPLICATION_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONF_DIR="${APPLICATION_HOME}/conf"
APP_DIR="${APPLICATION_HOME}/app"

# Logs
LOG_FILE="${APPLICATION_HOME}/log/start.log"
mkdir -p "$(dirname "${LOG_FILE}")"

# Loading file: env.conf
if [ -f ${CONF_DIR}/env.conf ]; then
    . ${CONF_DIR}/env.conf
else
    log_message "❌  Error : Config file '${CONF_DIR}/env.conf' not found."
    exit 1
fi

# ======================================================================== #

# Search for Python exec
if [ -d "${VENV_PYTHON_DIR}" ] && [ -x "${VENV_PYTHON_DIR}/bin/${VENV_PYTHON_EXE}" ]; then
    VENV_PYTHON="${VENV_PYTHON_DIR}/bin/${VENV_PYTHON_EXE}"
    log_message "🟢 Virtual environment found. Using : ${VENV_PYTHON}"
    PYTHON_EXE="${VENV_PYTHON}"
else
    log_message "⚪️ No virtual environment found. Using : ${PARENT_PYTHON_HOME}/bin/${PARENT_PYTHON_EXE}"
    PYTHON_EXE="${PARENT_PYTHON_HOME}/bin/${PARENT_PYTHON_EXE}"
fi

# Checking argument for execution
if [ -z "$1" ]; then
    log_message "❌ Error : You have to provide a program name for launching."
    log_message "Using : $0 <nom_du_python.py>"
    exit 1
fi

APP_NAME="$1"
APP_PATH="${APP_DIR}/${APP_NAME}"

# Check python app exists
if [ ! -f "${APP_PATH}" ]; then
    log_message "❌ Error : No python program '${APP_NAME}' found in '${APP_DIR}'."
    exit 1
fi

# Launching
log_message "Launching : ${APP_NAME}"
${PYTHON_EXE} "${APP_PATH}"

# Check conversion result
if [ $? -eq 0 ]; then
    log_message "✅  Success : ${APP_NAME}"
else
    log_message "❌  Fail : ${APP_NAME}"
    exit 1
fi
log_message "--- END OF PROCESS ---"