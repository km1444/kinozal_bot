FROM python:3.10.7-slim
RUN mkdir /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY kinozal_20v.py /app
# COPY .env /app
ENV TOKEN=5356493744:AAEl6alOR2-evfUF_0w1TN1w1EkGYwVxA9A
WORKDIR /app
CMD ["python", "kinozal_20v.py"]