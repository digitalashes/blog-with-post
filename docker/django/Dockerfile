FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements/
RUN pip install -r /requirements/local.txt

WORKDIR /project

EXPOSE 8000
