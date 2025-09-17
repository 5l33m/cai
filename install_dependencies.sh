#!/usr/bin/env bash

# install_dependencies.sh
#
# This script installs the system and Python dependencies required by
# the CAI framework and the supplementary tools added in this fork.
# It should be run on a Debian/Ubuntu based system.  It uses apt
# to install external command‑line utilities and pip to install
# Python libraries.  Run this script with sudo privileges for the
# apt portion, or prefix it with sudo manually.

set -euo pipefail

echo "[+] Updating package lists..."
sudo apt-get update -y

echo "[+] Installing system packages..."
sudo apt-get install -y \
    exploitdb \          # provides searchsploit
    metasploit-framework \ # provides msfconsole and pattern tools
    smbclient \            # SMB file share enumeration
    rsync \                # file synchronisation
    zip unzip \           # archive utilities
    curl \                # HTTP client used in data exfiltration
    wget \                # alternative HTTP client
    nmap \                # network scanner (optional but recommended)
    sshpass \             # non‑interactive SSH password support
    libcap2-bin \         # provides getcap utility
    iputils-ping \        # ping utility
    openssh-client        # ssh client for remote commands and tunnels

echo "[+] System packages installed."

# Install Python dependencies.  Use python3 and pip3 explicitly to avoid
# confusion with system python on some distributions.  If a virtual
# environment is desired, create and activate it before running this
# script.
PYTHON=python3
PIP=pip3

echo "[+] Ensuring pip is up to date..."
$PYTHON -m pip install --upgrade pip

echo "[+] Installing Python dependencies..."

# Base dependencies from CAI's .devcontainer/requirements.txt
if [ -f .devcontainer/requirements.txt ]; then
    $PIP install -r .devcontainer/requirements.txt
fi

# Additional dependencies explicitly required by CAI and these tools
$PIP install \
    openai==1.75.0 \
    pydantic>=2.10,<3 \
    griffe>=1.5.6,<2 \
    typing-extensions>=4.12.2,<5 \
    requests>=2.0,<3 \
    types-requests>=2.0,<3 \
    openinference-instrumentation-openai>=0.1.22 \
    wasabi>=1.1.3 \
    rich>=13.9.4 \
    prompt_toolkit>=3.0.39 \
    python-dotenv>=0.9.0 \
    litellm[proxy]>=1.63.7 \
    mako>=1.3.8 \
    networkx==2.5 \
    pymetasploit3 \
    xmltodict \
    pydot==1.4.2 \
    dnspython \
    flask \
    paramiko \
    PyPDF2

echo "[+] Python dependencies installed."

echo "[+] Dependency installation complete."