FROM swaxtech/pycord2:v1

WORKDIR /usr/src/app

RUN pip install stegano xmltodict

COPY ./museum.py ./museum.py
COPY ./models/embed/ ./models/embed/
COPY ./models/artwork.py ./models/artwork.py
COPY ./models/metadata/ ./models/metadata/
COPY ./models/logger.py ./models/logger.py

CMD [ "python", "./museum.py" ]