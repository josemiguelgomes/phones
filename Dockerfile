FROM python:3.10.4-alpine3.16
LABEL maintainer="zem.com"

ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="/scripts:$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN pip install --upgrade pip
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
       build-base postgresql-dev musl-dev \
       zlib zlib-dev linux-headers
RUN pip install -r /tmp/requirements.txt
RUN if [ $DEV = "true" ]; \
        then pip install -r /tmp/requirements.dev.txt ; \
    fi
RUN rm -rf /tmp
RUN apk del .tmp-build-deps
RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN chown -R django-user:django-user /vol
RUN chmod -R 755 /vol
RUN chmod -R +x /scripts

USER django-user

CMD ["run.sh"]