FROM python

WORKDIR /usr/src

COPY ./watcher watcher
COPY ./data data

RUN mkdir -p /usr/output && mkdir -p /urs/input
VOLUME /usr/output /usr/input

RUN python3 -m pip install numpy && \
    python3 -m pip install pandas && \
    python3 -m pip install scikit-learn && \
    python3 -m pip install watchdog

ENTRYPOINT [ "python3", "-m", "watcher.main" ]