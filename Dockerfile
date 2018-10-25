FROM python:3
ENV PYTHONUNBUFFERED 1

# to install NPM
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -

RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat nodejs

RUN pip install -U pip pipenv
ADD Pipfile* /code/

ADD https://s3-us-west-1.amazonaws.com/fasttext-vectors/supervised_models/lid.176.bin /

WORKDIR /code
RUN pipenv install --system --ignore-pipfile

ADD misc/dokku/CHECKS /app/
ADD misc/dokku/* /code/


COPY . /code/

RUN cd static/frontend && npm install && cd ../..

RUN /code/manage.py collectstatic --noinput
