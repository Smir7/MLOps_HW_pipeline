import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("../data/titanic.csv")
train, test = train_test_split(df, test_size=0.2, random_state=42)
train.to_csv("train.csv", index=False)
test.to_csv("test.csv", index=False)

print(" Готово! Файлы train.csv и test.csv созданы.")