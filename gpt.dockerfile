FROM swaxtech/pycord2:v1

WORKDIR /usr/src/app

RUN pip install --no-cache-dir requests aiohttp

COPY ./models/logger.py ./models/logger.py
COPY ./gpt.py .

CMD ["python", "./gpt.py"]


