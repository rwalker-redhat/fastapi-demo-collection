FROM ubi8/python-39

LABEL maintainer="Richard Walker"

USER root

WORKDIR /opt/app-root/src

COPY . /opt/app-root/src

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chown -R 1001:1001 /opt/app-root/src

USER 1001

EXPOSE 8000

CMD python main.py

