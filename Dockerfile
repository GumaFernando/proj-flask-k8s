FROM  python:3.9.5

RUN apt-get update -y && \
  apt-get install -y python-pip python-dev

COPY . /app

RUN pip install flask

WORKDIR /app

EXPOSE 80

CMD ["python","app-fii.py"]

