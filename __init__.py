import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd, io, os
from mlxtend.frequent_patterns import apriori, association_rules

def main(myblob: func.InputStream):
    # myblob is the uploaded Parquet with 'items' column
    df = pd.read_parquet(io.BytesIO(myblob.read()))
    if df.empty or "items" not in df.columns:
        return
    exploded = df.explode("items").assign(val=1)
    basket = exploded.pivot_table(index=exploded.index, columns="items", values="val",
                                  fill_value=0, aggfunc="max").astype(bool)
    freq = apriori(basket, min_support=float(os.getenv("MIN_SUPPORT","0.03")), use_colnames=True)
    if freq.empty:
        return
    rules = association_rules(freq, metric="confidence", min_threshold=float(os.getenv("MIN_CONF","0.7")))
    rules = rules[["antecedents","consequents","support","confidence","lift"]].head(200)
    rules = rules.assign(
        antecedents=rules["antecedents"].apply(lambda s: sorted(list(s))),
        consequents=rules["consequents"].apply(lambda s: sorted(list(s)))
    )
    out_csv = io.StringIO(); rules.to_csv(out_csv, index=False)
    conn = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    container = os.environ.get("OUTPUT_CONTAINER","results")
    name = os.environ.get("OUTPUT_NAME","rules_sample.csv")
    blob = BlobServiceClient.from_connection_string(conn).get_container_client(container)
    blob.upload_blob(name=name, data=out_csv.getvalue(), overwrite=True)
