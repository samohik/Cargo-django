FROM python:3


# install dependencies
RUN pip install --upgrade pip

COPY requirements.txt Cargo/

RUN pip install -r Cargo/requirements.txt

# env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY ./cargo Cargo/cargo

WORKDIR Cargo/cargo/