#!/bin/bash

# First arg ($1) is the extras_require to install, optional second arg
# ($2) is an extra dependency (currently just nox on one run)
set -eo pipefail
export PYTHONUTF8=1
if [[ "$SPHINX_VERSION" == "" ]]; then
    SPHINX_INSTALL=""
elif [[ "$SPHINX_VERSION" == "dev" ]]; then
    SPHINX_INSTALL="git+https://github.com/sphinx-doc/sphinx"
    if [[ "$1" == "doc" ]]; then
        # Until they release a new version that undoes the max sphinx pin...
        DEP_EXTRA="git+https://github.com/executablebooks/MyST-NB"
    fi
elif [[ "$SPHINX_VERSION" == "old" ]]; then
    SPHINX_INSTALL="sphinx==5.0"
else  # not used currently but easy enough
    SPHINX_INSTALL="sphinx==$SPHINX_VERSION"
fi
set -x  # print commands
python -m pip install --upgrade pip wheel setuptools
python -m pip install -e .["$1"] ${SPHINX_INSTALL} $2 $DEP_EXTRA
