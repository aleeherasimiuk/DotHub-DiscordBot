FROM swaxtech/pycord2:v2

WORKDIR /usr/src/app

RUN pip install stegano xmltodict

COPY ./infobot.py .
COPY ./models/logger.py ./models/logger.py
COPY ./models/metadata/ ./models/metadata/
COPY ./models/embed/ ./models/embed/
COPY ./res/infobot.json ./res/infobot.json

CMD [ "python", "./infobot.py" ]