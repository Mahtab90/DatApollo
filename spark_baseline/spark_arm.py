import time, psutil, json
from pyspark.sql import SparkSession
from pyspark.ml.fpm import FPGrowth

def main(input_parquet: str, min_support=0.03, min_conf=0.7, out_json="spark_results.json"):
    spark = (SparkSession.builder
             .appName("DatApollo-Spark-Baseline")
             .getOrCreate())
    proc = psutil.Process()
    mem0 = proc.memory_info().rss
    t0 = time.time()

    df = spark.read.parquet(input_parquet)  # expects columns: ts, city, items (array<string>)
    fp = FPGrowth(itemsCol="items", minSupport=min_support, minConfidence=min_conf)
    model = fp.fit(df)

    rules = model.associationRules
    n_rules = rules.count()

    elapsed = time.time() - t0
    mem_delta_mb = (proc.memory_info().rss - mem0) / (1024**2)
    metrics = {
        "engine":"spark",
        "min_support":min_support,
        "min_confidence":min_conf,
        "execution_time_sec":round(elapsed,3),
        "peak_mem_mb_est":round(mem_delta_mb,2),
        "num_rules":int(n_rules)
    }

    sample = rules.limit(30).toPandas().to_dict(orient="records")
    with open(out_json,"w") as f:
        json.dump({"metrics":metrics,"rules_sample":sample}, f, indent=2)

    spark.stop()

if __name__ == "__main__":
    import argparse
    a = argparse.ArgumentParser()
    a.add_argument("--input", required=True)
    a.add_argument("--min_support", type=float, default=0.03)
    a.add_argument("--min_confidence", type=float, default=0.7)
    a.add_argument("--out", default="spark_results.json")
    args = a.parse_args()
    main(args.input, args.min_support, args.min_confidence, args.out)
