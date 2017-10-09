FROM hivesolutions/python:latest

LABEL maintainer="Hive Solutions <development@hive.pt>"

EXPOSE 8080

VOLUME /data

ENV LEVEL INFO
ENV SERVER netius
ENV SERVER_ENCODING gzip
ENV HOST 0.0.0.0
ENV PORT 8080
ENV FORCE_SSL 1
ENV MONGOHQ_URL mongodb://localhost
ENV SCHEDULER 1
ENV SENDER_EMAIL "Shopdesk <no-reply@shopdesk.com>"
ENV LOGO_EMAIL 1
ENV SMTP_HOST SMTP_HOST
ENV SMTP_PORT 25
ENV SMTP_SSL 1
ENV SMTP_USER SMTP_USER
ENV SMTP_PASSWORD SMTP_PASSWORD
ENV SMTP_HELO_HOST SMTP_HELO_HOST
ENV SHOPIFY_API_KEY SHOPIFY_API_KEY
ENV SHOPIFY_PASSWORD SHOPIFY_PASSWORD
ENV SHOPIFY_SECRET SHOPIFY_SECRET
ENV SHOPIFY_STORE SHOPIFY_STORE
ENV EASYPAY_PRODUCTION 1
ENV EASYPAY_CIN EASYPAY_CIN
ENV EASYPAY_ENTITY EASYPAY_ENTITY
ENV EASYPAY_USERNAME EASYPAY_USERNAME
ENV EASYPAY_PATH /data/easypay.shelve
ENV PYTHONPATH /src

ADD requirements.txt /
ADD extra.txt /
ADD src /src

RUN pip3 install -r /requirements.txt && pip3 install -r /extra.txt && pip3 install --upgrade netius

CMD ["/usr/bin/python3", "/src/shopdesk/main.py"]
