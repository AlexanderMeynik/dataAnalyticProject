# Use the official Citus Docker image as the base image
FROM citusdata/citus as database
COPY ../dumpFile.sql /docker-entrypoint-initdb.d/



FROM python:3.11 as server_env
#COPY ../ServerCode/   /home/app/code
COPY requirements.txt /home/app/
WORKDIR /home/app
RUN pip install -r requirements.txt



FROM server_env as server
COPY ../ServerCode/   /home/app/code
WORKDIR /home/app/code
ENTRYPOINT ["python3","flaskApi.py"]
CMD ["bash"]

FROM server_env as server_dev
WORKDIR /home/app/code
ENTRYPOINT ["python3","flaskApi.py"]
CMD ["bash"]


