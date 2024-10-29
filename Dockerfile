FROM python:3.11-slim

WORKDIR /

ENV CONTAINER=True

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . ./

CMD ["python","app.py"]