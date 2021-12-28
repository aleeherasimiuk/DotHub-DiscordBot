FROM python:slim-buster

WORKDIR /usr/src/app

RUN apt update && apt install -y git
RUN git clone https://github.com/Pycord-Development/pycord /tmp/pycord
RUN python -m pip install /tmp/pycord
RUN pip install stegano xmltodict

COPY ./infobot.py .
COPY ./models/logger.py ./models/logger.py
COPY ./models/metadata/ ./models/metadata/
COPY ./models/embed/ ./models/embed/
COPY ./res/infobot.json ./res/infobot.json

CMD [ "python", "./infobot.py" ]