FROM python:3.6

RUN  mkdir mang-system

ENV DIR /mang-system

COPY . $DIR

RUN apt-get update \
    && cd /mang-system \
    && pip3 install django==2.1 \
    && pip3 install boto3  \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate 

WORKDIR $DIR

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]