import pandas as pd

print("Lendo o arquivo original...")
df = pd.read_csv('creditcard.csv')

print(f"Tamanho original: {len(df)} linhas")

# Pegando 10% de amostra
df_sample = df.sample(frac=0.1, random_state=42)

print(f"Tamanho da amostra: {len(df_sample)} linhas")

print("Salvando a amostra em 'creditcard_sample.csv'...")
df_sample.to_csv('creditcard_sample.csv', index=False)

print("Concluído sucesso!")
