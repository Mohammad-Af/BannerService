FROM python:3.8.5
# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
RUN apt-get update -qy
RUN apt-get install -qy gdal-bin python-gdal python3-gdal
RUN apt-get install -qy netcat
RUN apt-get install unzip
ADD . /code/
EXPOSE 8000
RUN chmod +x ./start.sh
RUN export PYTHONPATH=./
CMD ./start.sh
