import pandas as pd

df = pd.read_csv("clothes.csv")
print(df)
df.drop(["name", "img_route"], axis=1, inplace=True)
df.to_csv("clothes.csv", index=False)