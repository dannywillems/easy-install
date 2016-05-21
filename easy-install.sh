#!/bin/bash - 
#===============================================================================
#
#          FILE: easy-install.sh
# 
#         USAGE: ./easy-install.sh
# 
#   DESCRIPTION: Clone and install easy-install with requirements.
# 
#  REQUIREMENTS: git, python, pip
#        AUTHOR: Danny Willems
#       CREATED: 05/21/16 11:45
#      REVISION: v0.1
#===============================================================================

set -o nounset                              # Treat unset variables as an error

################################################################################
## Variables
EASY_INSTALL_HOME=$HOME/.easy-install
################################################################################

git clone https://github.com/dannywillems/easy-install $EASY_INSTALL_HOME
cd $EASY_INSTALL_HOME
pip install -r requirements.txt
chmod u+x easy-install.py
# echo "export PATH=$EASY_INSTALL_HOME:$PATH" >> $HOME/.${SHELL##*/}rc
