import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings

warnings.filterwarnings('ignore')

def main():
    print("Carregando os dados...")
    # Lê o dataset
    df = pd.read_csv('creditcard.csv')
    
    # Caso as colunas tenham aspas no nome (como visto no Get-Content)
    df.columns = df.columns.str.replace('"', '').str.strip()

    print("Pré-processando os dados...")
    # Se a coluna 'Class' foi lida como string contendo aspas, removemos
    if df['Class'].dtype == object:
        df['Class'] = df['Class'].str.replace('"', '').astype(int)

    # Separação entre features (X) e a variável alvo (y)
    X = df.drop('Class', axis=1)
    y = df['Class']

    # Padronização dos dados (Importante para a Regressão Logística convergir corretamente)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Divisão em conjuntos de treino e teste (mantendo a proporção de fraudes com stratify=y)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Configurando a Regressão Logística e a busca de hiperparâmetros...")
    # Define o modelo
    # Utilizamos class_weight='balanced' pois a base de fraudes normalmente é muito desbalanceada
    log_reg = LogisticRegression(max_iter=1000, random_state=42)

    # Grade de hiperparâmetros para buscar a melhor acurácia
    param_dist = {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],  # Inverso da força de regularização
        'penalty': ['l1', 'l2'],             # Tipos de penalidade
        'solver': ['liblinear', 'saga']      # Solvers que suportam l1 e l2
    }

    # Utilizamos RandomizedSearchCV para otimizar os hiperparâmetros (é mais rápido que GridSearchCV)
    # A métrica de avaliação ('scoring') é a acurácia, conforme solicitado
    search = RandomizedSearchCV(
        log_reg, 
        param_distributions=param_dist, 
        n_iter=5,             # Número de combinações a testar
        scoring='accuracy',   # Focando na melhor acurácia
        cv=3,                 # Validação cruzada com 3 folds
        random_state=42, 
        n_jobs=-1,            # Usa todos os núcleos do processador disponíveis
        verbose=1
    )

    print("Iniciando o treinamento e ajuste... Isso pode levar alguns minutos devido ao tamanho do dataset.")
    search.fit(X_train, y_train)

    print("\n================ RESULTADOS ================")
    print("\nTreinamento concluído!")
    print(f"Melhores hiperparâmetros encontrados: {search.best_params_}")
    
    # Avaliando o melhor modelo no conjunto de teste
    best_model = search.best_estimator_
    y_pred = best_model.predict(X_test)

    # Calculando a acurácia
    acc = accuracy_score(y_test, y_pred)
    print(f"\nMelhor Acurácia no conjunto de teste: {acc:.4f} ({(acc*100):.2f}%)")
    
    # Exibindo métricas detalhadas (Precision, Recall, F1-Score)
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred))

    print("Matriz de Confusão:")
    print(confusion_matrix(y_test, y_pred))

if __name__ == '__main__':
    main()
