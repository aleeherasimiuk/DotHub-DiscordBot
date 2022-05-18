FROM swaxtech/pycord2:v2

WORKDIR /usr/src/app

COPY ./dotesting.py .
COPY ./models/logger.py ./models/logger.py
COPY ./res/dotesting.json ./res/dotesting.json

CMD [ "python", "./dotesting.py" ]
