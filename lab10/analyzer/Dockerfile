FROM python:3
LABEL maintainer="pchen109@my.bcit.ca"

RUN mkdir app.py
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update && apt-get install -y nano
RUN pip3 install -r requirements.txt

COPY . .
RUN mkdir config
RUN mkdir logs
RUN touch logs/analyzer.log

RUN adduser kekw
RUN chown -R kekw:kekw /app
USER kekw

EXPOSE 8110
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]