# 🛡️ DetectaFraude

Um sistema completo de detecção e visualização de transações financeiras fraudulentas.

Este projeto contém um modelo de Regressão Logística para identificar potenciais fraudes em transações de cartão de crédito e um Dashboard Web moderno para visualização dos registros no banco de dados.

## 📁 Estrutura do Projeto

- `creditcard.csv`: Dataset original com as transações (não incluído por restrições de tamanho, coloque-o na pasta raiz).
- `logistic_regression_fraud.py`: Script para treinar o modelo de Machine Learning que detecta fraudes.
- `create_db.py`: Script que lê o CSV e converte em um banco de dados SQLite (`transactions.db`) mais leve e limpo para o sistema Web.
- `app.py`: Servidor Backend feito em Python (Flask) que fornece a API de comunicação com o banco de dados.
- `templates/` e `static/`: Contém os arquivos responsáveis pela interface gráfica do Dashboard no navegador (HTML, CSS premium dark-mode e JavaScript dinâmico usando Chart.js).

## 🚀 Como Executar o Projeto

Siga os passos abaixo, abrindo o seu Terminal/Prompt de Comando na pasta do projeto:

### 1. Criar o Banco de Dados (Uma única vez)
Para popular os dados e poder visualizá-los, execute o seguinte script:
```bash
python create_db.py
```
Isso criará o arquivo `transactions.db`.

### 2. Iniciar o Painel de Controle (Dashboard)
Para ligar o seu site, digite:
```bash
python app.py
```
O servidor ficará rodando. Abra o seu navegador favorito e acesse a página: **[http://localhost:5000](http://localhost:5000)**

### 3. (Opcional) Testar/Treinar o Modelo Analítico
Se quiser rodar o modelo de Machine Learning para ver as métricas de acurácia da Regressão Logística, abra um novo terminal e digite:
```bash
python logistic_regression_fraud.py
```
# Detectafraude
