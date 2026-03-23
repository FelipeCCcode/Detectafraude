from flask import Flask, render_template, jsonify, request
import sqlite3
import pandas as pd
import os

app = Flask(__name__)
DB_PATH = 'transactions.db'

def get_db_connection():
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Banco de dados não encontrado. Execute o create_db.py primeiro."}), 404
        
    try:
        cursor = conn.cursor()
        
        # Total transações
        cursor.execute("SELECT COUNT(*) FROM transactions")
        total = cursor.fetchone()[0]
        
        # Fraudes
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE Class = 1")
        fraudes = cursor.fetchone()[0]
        
        # Legítimas
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE Class = 0")
        legitimas = cursor.fetchone()[0]
        
        # Valor fraudes (se a coluna Amount existir)
        cursor.execute("PRAGMA table_info(transactions)")
        columns = [info[1] for info in cursor.fetchall()]
        
        valor_fraudes = 0
        if 'Amount' in columns:
            cursor.execute("SELECT SUM(Amount) FROM transactions WHERE Class = 1")
            resultado = cursor.fetchone()[0]
            valor_fraudes = resultado if resultado else 0
            
        conn.close()
        
        return jsonify({
            "total_transacoes": total,
            "total_fraudes": fraudes,
            "total_legitimas": legitimas,
            "valor_fraudes": valor_fraudes
        })
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/api/transactions')
def get_transactions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Banco de dados não encontrado."}), 404
        
    # Parâmetros de filtro
    filter_type = request.args.get('filter', 'Todas')
    limit = min(int(request.args.get('limit', 100)), 1000) # Máximo 1000 por requisição
    offset = int(request.args.get('offset', 0))
    
    query = "SELECT * FROM transactions"
    params = []
    
    if filter_type == 'Fraudes':
        query += " WHERE Class = 1"
    elif filter_type == 'Legítimas':
        query += " WHERE Class = 0"
        
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    try:
        # Usar pandas para facilitar a conversão para JSON
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
