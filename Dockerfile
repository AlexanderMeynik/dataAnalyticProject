FROM citusdata/citus as database
#COPY ../dumpFile.sql /docker-entrypoint-initdb.d/

FROM python:3.11 as client_env
COPY clientCode/requirements.txt /home/app/
WORKDIR /home/app
RUN pip install -r requirements.txt

FROM python:3.11 as server_env
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

FROM client_env as client_dev
WORKDIR /home/app/code
ENTRYPOINT ["python3","app.py"]
CMD ["bash"]



