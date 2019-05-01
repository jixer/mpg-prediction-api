FROM python

WORKDIR /usr/src

COPY ./api api
COPY ./data data

RUN mkdir -p /urs/output
VOLUME /usr/output

RUN python3 -m pip install numpy && \
    python3 -m pip install pandas && \
    python3 -m pip install scikit-learn && \
    python3 -m pip install flask

ENTRYPOINT [ "python3" ]
CMD [ "-m", "api.app" ]