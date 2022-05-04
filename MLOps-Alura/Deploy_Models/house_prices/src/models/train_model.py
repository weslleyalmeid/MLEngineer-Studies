import pandas as pd
import os.path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

ROOT_DIR = os.path.abspath('.')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
MODELS_DIR = os.path.join(ROOT_DIR, 'models')

data = os.path.join(DATA_DIR, 'processed', 'casas.csv')
df = pd.read_csv(data)

X = df.drop(labels=['preco'], axis=1)
y = df['preco']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo = LinearRegression()
# modelo.fit(X_train.values, y_train.values)
modelo.fit(X_train, y_train)

model = os.path.join(MODELS_DIR, 'model.pkl')
pickle.dump(modelo, open(model, 'wb'))