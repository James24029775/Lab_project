FROM python:3.9.10-slim
ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN apt update && apt install dnsutils  -y
RUN mkdir /opt/log
ADD ./api/backend /app

ENV FLASK_APP=/opt/app/main.py
ENV FLASK_ENV=development

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]
