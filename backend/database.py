import mysql.connector


def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="nandhu@55",
        database="gene_cancer_db"
    )