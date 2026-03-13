import sqlite3
import pandas as pd
import os

def create_database():
    csv_file = 'creditcard.csv'
    db_file = 'transactions.db'
    
    if not os.path.exists(csv_file):
        print(f"Erro: Arquivo '{csv_file}' não encontrado.")
        return

    print(f"Lendo '{csv_file}'... Isso pode demorar alguns segundos.")
    try:
        # Lê o CSV
        df = pd.read_csv(csv_file)
        
        # Limpa os nomes das colunas
        df.columns = df.columns.str.replace('"', '').str.strip()
        
        # Limpa a coluna Class se for texto
        if df['Class'].dtype == object:
            df['Class'] = df['Class'].str.replace('"', '').astype(int)
            
        print(f"Criando o banco de dados '{db_file}'...")
        conn = sqlite3.connect(db_file)
        
        # Filtra as colunas que importam para a visualização
        cols_to_keep = []
        if 'Time' in df.columns:
            cols_to_keep.append('Time')
        if 'Amount' in df.columns:
            cols_to_keep.append('Amount')
        cols_to_keep.append('Class')
        
        df_db = df[cols_to_keep].copy()
        
        # Adiciona rótulos para facilitar a leitura no app
        df_db['is_fraud'] = df_db['Class'].apply(lambda x: "Fraude" if x == 1 else "Legítima")
        
        # Salva o DataFrame no SQLite
        df_db.to_sql('transactions', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Banco de dados '{db_file}' criado com sucesso com {len(df_db)} registros!")
    except Exception as e:
        print(f"Erro ao criar banco de dados: {e}")

if __name__ == '__main__':
    create_database()
