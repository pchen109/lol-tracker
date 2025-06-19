FROM python:3
LABEL maintainer="pchen109@my.bcit.ca"

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . .
RUN mkdir config
RUN mkdir logs

RUN adduser kekw
RUN chown -R kekw:kekw /app
USER kekw

EXPOSE 8080
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]