FROM balenalib/raspberry-pi-debian-python

WORKDIR /usr/src/app

COPY ./main.py .

RUN pip install pyserial prometheus_client

EXPOSE 8000

CMD ["python", "./main.py"]
