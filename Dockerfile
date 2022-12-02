FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR ./pythonProject1
ADD ./ITSC_BAZA ./
RUN pip install -r requirements.txt