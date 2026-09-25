from models import Article
import pandas as pd
df = pd.read_json("../data/glycomics.jsonl", lines= True)
print(df.pub_year.value_counts())


