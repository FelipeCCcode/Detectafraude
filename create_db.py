import sqlite3
import pandas as pd
import os

def create_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_name = 'creditcard.csv' if os.path.exists(os.path.join(script_dir, 'creditcard.csv')) else 'creditcard_sample.csv'
    csv_file = os.path.join(script_dir, dataset_name)
    db_file = os.path.join(script_dir, 'transactions.db')

    if not os.path.exists(csv_file):
        print(f"Erro: Arquivo '{csv_file}' não encontrado. Verifique se o arquivo está na mesma pasta do script.")
        return

    print(f"Lendo '{csv_file}'... Isso pode demorar alguns segundos.")
    try:
        #lê o CSV de forma robusta, mesmo com possiveis separadores ou aspas
        df = pd.read_csv(csv_file, sep=',', quotechar='"', low_memory=False)
        
        #limpa os nomes das colunas
        df.columns = df.columns.str.replace('"', '').str.strip()
        
        #limpa a coluna Class se for texto
        if df['Class'].dtype == object:
            df['Class'] = df['Class'].str.replace('"', '').astype(int)
            
        print(f"Criando o banco de dados '{db_file}'...")
        conn = sqlite3.connect(db_file)
        
        #filtra as colunas que importam para a visualização
        cols_to_keep = []
        if 'Time' in df.columns:
            cols_to_keep.append('Time')
        if 'Amount' in df.columns:
            cols_to_keep.append('Amount')
        cols_to_keep.append('Class')
        
        df_db = df[cols_to_keep].copy()
        
        #adiciona rótulos para facilitar a leitura no app
        df_db['is_fraud'] = df_db['Class'].apply(lambda x: "Fraude" if x == 1 else "Legítima")
        
        #salva o DataFrame no SQLite
        df_db.to_sql('transactions', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Banco de dados '{db_file}' criado com sucesso com {len(df_db)} registros!")
    except Exception as e:
        print(f"Erro ao criar banco de dados: {e}")

if __name__ == '__main__':
    create_database()
