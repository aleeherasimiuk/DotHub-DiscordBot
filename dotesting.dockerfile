FROM python:slim-buster

WORKDIR /usr/src/app

RUN apt update && apt install -y git
RUN git clone https://github.com/Pycord-Development/pycord /tmp/pycord
RUN python -m pip install /tmp/pycord

COPY ./dotesting.py .
COPY ./models/logger.py ./models/logger.py
COPY ./res/dotesting.json ./res/dotesting.json

CMD [ "python", "./dotesting.py" ]
