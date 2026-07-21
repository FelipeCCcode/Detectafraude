import os
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings

# limitação de threads para evitar deadlocks de execução paralela no windows (joblib/openblas)
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('NUMEXPR_NUM_THREADS', '1')

warnings.filterwarnings('ignore')

def main():
    # selecao do dataset (prioriza a base completa se disponivel)
    dataset_file = 'creditcard.csv' if os.path.exists('creditcard.csv') else 'creditcard_sample.csv'
    df = pd.read_csv(dataset_file)
    
    # tratamento nos nomes das colunas
    df.columns = df.columns.str.replace('"', '').str.strip()

    # conversao do tipo da variavel alvo
    if df['Class'].dtype == object:
        df['Class'] = df['Class'].str.replace('"', '').astype(int)

    # separacao das features e do target
    X = df.drop('Class', axis=1)
    y = df['Class']

    # divisao treino/teste mantendo a proporção de classes (stratify)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # padronizacao das features apos o split para evitar data leakage
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # regressao logistica com ponderacao de peso por classe
    log_reg = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)

    # espaco de busca de hiperparametros
    param_dist = {
        'C': [0.01, 0.1, 1, 10],
        'penalty': ['l2'],
        'solver': ['liblinear', 'lbfgs']
    }

    # otimizacao via randomized search com foco em f1-score
    search = RandomizedSearchCV(
        log_reg, 
        param_distributions=param_dist, 
        n_iter=4,
        scoring='f1',
        cv=3,
        random_state=42, 
        n_jobs=1,
        verbose=0
    )

    search.fit(X_train_scaled, y_train)

    # avaliacao no conjunto de teste
    best_model = search.best_estimator_
    y_pred = best_model.predict(X_test_scaled)

    acc = accuracy_score(y_test, y_pred)

    print(f"Melhores parametros: {search.best_params_}")
    print(f"Acuracia teste: {acc:.4f}\n")
    print("Relatorio de Classificacao:")
    print(classification_report(y_test, y_pred))
    print("Matriz de Confusao:")
    print(confusion_matrix(y_test, y_pred))

if __name__ == '__main__':
    main()
