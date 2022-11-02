FROM gitpod/workspace-python

RUN sudo upgrade-packages \
    && sudo install-packages python-is-python3 \
    && curl -sSL https://install.python-poetry.org | python3 -
