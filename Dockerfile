FROM python
RUN apt-get update && apt-get install -y sqlite3 #python3

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY app.py /app/
COPY rank_data.db /app/
COPY resources/ /app/resources/

WORKDIR /app
#RUN python app.py &>/dev/null &

ENTRYPOINT [ "python" ]
CMD ["app.py"]