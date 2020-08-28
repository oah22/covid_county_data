FROM python:3.8.5
# FROM python:2.7.17-slim-buster
LABEL maintainer="drohao@gmail.com"

# # -- Temporary Tools
# RUN apt-get update && apt-get install -y netcat telnet curl

# -- Copy to /app
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app/

RUN chmod +x /app/entrypoint.sh

# -- Main
ENTRYPOINT [ "bash", "-x", "/app/entrypoint.sh"]
