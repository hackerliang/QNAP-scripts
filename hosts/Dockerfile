FROM python:alpine

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && rm -f /requirements.txt

COPY ./hosts-host.py /hosts-host.py

ENV TZ=Asia/Shanghai

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONUNBUFFERED=1

CMD ["python", "/hosts-host.py"]