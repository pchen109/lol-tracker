FROM python:3
LABEL maintainer = "pchen109@my.bcit.ca"

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . .
RUN mkdir config
# RUN touch config/processing_config.yml
# RUN touch config/logging_config.yml
RUN mkdir -p data/processing
RUN mkdir logs
RUN touch logs/processing.log

RUN adduser kekw
RUN chown -R kekw:kekw /app
USER kekw

EXPOSE 8100
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]