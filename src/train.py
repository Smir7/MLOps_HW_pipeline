import os
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("titanic_local_experiment")

train_df = pd.read_csv("../data/train.csv")
test_df = pd.read_csv("../data/test.csv")


def prepare_data(df):
    df_numeric = df.select_dtypes(include=['number']).dropna()

    target_col = [col for col in df_numeric.columns if col.lower() == 'survived']

    if not target_col:
        y = df_numeric.iloc[:, 0]
        X = df_numeric.iloc[:, 1:]
    else:
        y = df_numeric[target_col[0]]
        X = df_numeric.drop(columns=[target_col[0]])

    return X, y


X_train, y_train = prepare_data(train_df)
X_test, y_test = prepare_data(test_df)

with mlflow.start_run():
    mlflow.sklearn.autolog()

    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)

    mlflow.log_metric("accuracy", acc)

    print(f" Модель обучена! Accuracy: {acc:.3f}")
    print(" Проверка результатов: http://147.45.147.94:5000")