FROM swaxtech/pycord2:v2

WORKDIR /usr/src/app

COPY ./moderadot.py .
COPY ./models/logger.py ./models/logger.py
COPY ./models/embed/ ./models/embed/
COPY ./res/moderadot.json ./res/moderadot.json

CMD [ "python", "./moderadot.py" ]