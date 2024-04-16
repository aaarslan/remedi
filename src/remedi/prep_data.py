import pandas as pd

genetic_data = pd.read_csv("./data/aa.tsv", sep="\t")
pgx_data = pd.read_json("./data/pharmacogenomics/combined.json")

genetic_data = genetic_data[genetic_data["rsid"].isin(pgx_data["variantRsId"].values)]

print(genetic_data.head())
