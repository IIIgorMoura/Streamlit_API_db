# pip install streamlit
# pip install mysql-connector-python

# conexão
import mysql.connector
import pandas as pd

# função de conexão com o banco de dados
    # parametro define qual tipo de Query vamos fazer
def conexao(query):

    # informações de conexão com o banco
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port='3306',
        user='root',
        password='Senai@134',
        db='db_carro'
    )
    
    dataframe = pd.read_sql(query, conn)
    # Executar o SQL e armazenar o resultado no dataframe

    conn.close()

    return dataframe


