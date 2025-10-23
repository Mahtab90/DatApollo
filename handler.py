import json, io, boto3, pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

s3 = boto3.client("s3")

def _read_parquet_s3(s3_uri: str) -> pd.DataFrame:
    assert s3_uri.startswith("s3://")
    # s3://bucket/key
    no_scheme = s3_uri[5:]
    bucket, _, key = no_scheme.partition("/")
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_parquet(io.BytesIO(obj["Body"].read()))

def lambda_handler(event, context):
    """
    event = {"s3_uri":"s3://YOURBUCKET/shards/tx_000.parquet","min_support":0.03,"min_confidence":0.7}
    """
    s3_uri = event["s3_uri"]
    min_support = float(event.get("min_support", 0.03))
    min_conf = float(event.get("min_confidence", 0.7))

    df = _read_parquet_s3(s3_uri)  # expects column: items (list of strings)
    if "items" not in df.columns or df.empty:
        return {"num_rules":0, "rules":[]}

    # one-hot encode transactions
    exploded = df.explode("items").assign(val=1)
    basket = exploded.pivot_table(index=exploded.index, columns="items", values="val",
                                  fill_value=0, aggfunc="max").astype(bool)

    freq = apriori(basket, min_support=min_support, use_colnames=True)
    if freq.empty:
        return {"num_rules":0, "rules":[]}

    rules = association_rules(freq, metric="confidence", min_threshold=min_conf)
    rules = rules[["antecedents","consequents","support","confidence","lift"]].head(200)
    rules = rules.assign(
        antecedents=rules["antecedents"].apply(lambda s: sorted(list(s))),
        consequents=rules["consequents"].apply(lambda s: sorted(list(s)))
    )
    out = rules.to_dict(orient="records")
    return {"num_rules":len(out), "rules":out}
