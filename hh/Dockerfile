FROM python:3.8

# set work directory
WORKDIR /home/app/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y netcat gcc libpq-dev python3-dev musl-dev \
    postgresql postgresql-contrib

# install SSL stuff
RUN apt-get install -y libffi-dev

# install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install wheel
RUN pip3 install --upgrade pip setuptools wheel
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# install server dependencies
RUN pip3 install gunicorn

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# copy project
COPY ./ ./

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
