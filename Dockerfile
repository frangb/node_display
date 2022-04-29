FROM python:3

ADD docs /
ADD fonts /
ADD config.txt /
ADD node_display.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./node_display.py" ]