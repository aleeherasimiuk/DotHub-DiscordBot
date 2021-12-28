FROM python:slim-buster

WORKDIR /usr/src/app

RUN apt update && apt install -y git
RUN git clone https://github.com/Pycord-Development/pycord /tmp/pycord
RUN python -m pip install /tmp/pycord
RUN pip install --no-cache-dir requests aiohttp

COPY ./models/logger.py ./models/logger.py
COPY ./gpt.py .

CMD ["python", "./gpt.py"]


