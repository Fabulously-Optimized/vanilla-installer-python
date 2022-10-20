FROM gitpod/workspace-python-3.10

RUN sudo upgrade-packages \
    && sudo install-packages python-tk
