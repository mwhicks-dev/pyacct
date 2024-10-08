FROM python:3.10-bookworm
ARG TARGET=main
ARG DRIVER=psycopg2

RUN apt install git -y
RUN mkdir /cert

RUN git clone https://github.com/mwhicks-dev/pyacct

WORKDIR /pyacct
RUN git checkout ${TARGET} && git pull
RUN pip install -r src/requirements.txt
RUN pip install ${DRIVER}

WORKDIR /pyacct/src/pyacct
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]
