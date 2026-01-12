FROM python:3-slim

RUN pip install Flask==3.1.2
RUN pip install python-dotenv==1.2.1 
RUN pip install pyyaml &&\
    pip install "psycopg[binary]"==3.2.13 &&\
    pip install openai==2.8.0

RUN pip install waitress

WORKDIR /app

COPY src/text2sql/ /app/text2sql/ 
COPY src/text2sql/Text2Sql.py /app/Text2Sql.py 
COPY src/configs.yaml /app/configs.yaml
COPY .env /app/.env 

EXPOSE 5000

ENTRYPOINT ["python", "text2sql/text2sql_service.py"]
