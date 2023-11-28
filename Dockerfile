# Use the official Citus Docker image as the base image
FROM citusdata/citus as database
COPY ../dumpFile.sql /docker-entrypoint-initdb.d/



FROM python:3.11 as server
COPY flaskApi.py dbService.py requirements.txt /home/app/
WORKDIR /home/app
RUN pip install -r requirements.txt
#todo try to copy existing enviroment
ENTRYPOINT ["python3","flaskApi.py"]
CMD ["bash"]


