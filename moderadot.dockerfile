FROM python:slim-buster

WORKDIR /usr/src/app

RUN apt update && apt install -y git
RUN git clone https://github.com/Pycord-Development/pycord /tmp/pycord
RUN python -m pip install /tmp/pycord

COPY ./moderadot.py .
COPY ./models/logger.py ./models/logger.py
COPY ./models/embed/ ./models/embed/
COPY ./res/moderadot.json ./res/moderadot.json

CMD [ "python", "./moderadot.py" ]