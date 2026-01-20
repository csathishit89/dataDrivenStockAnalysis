import psycopg2

conn = psycopg2.connect(
    host="localhost",   # prefer 127.0.0.1 over "localhost" for TCP
    port=5432,
    user="postgres",
    password="Password#1234",
    dbname="stockAnalysis"
)