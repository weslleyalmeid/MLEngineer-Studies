import mlflow
logged_model = 'runs:/c7b551614b3948168e762214e896c2a7/model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.
import pandas as pd
import os.path

ROOT_DIR = os.path.abspath('.')
BASE_DIR = os.path.join(ROOT_DIR, 'data')

data = os.path.join(BASE_DIR, 'processed', 'casas_X.csv')
data = pd.read_csv(data)


predicted = loaded_model.predict(data)
data['predicted'] = predicted
data.to_csv('precos.csv')