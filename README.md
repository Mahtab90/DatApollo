
# Datapollo: Serverless Association Rule Mining (ARM) Framework

## Overview

**Datapollo** is a lightweight, serverless framework designed for performing **Association Rule Mining (ARM)** at scale using a Function-as-a-Service (FaaS) architecture. This system is especially suitable for cloud environments and supports efficient mining of frequent itemsets and rule generation on transactional datasets.

This repository contains:

- A serverless ARM implementation based on the Apriori algorithm
- An orchestration workflow using Apollo Runtime System
- Preprocessing and output handling utilities
- Benchmark results comparing Datapollo vs. Apache Spark

---

## Architecture Flowchart

```
                          +-----------------------------+
                          |   Datapollo Serverless      |
                          |     ARM Framework           |
                          +--------------+--------------+
                                         |
                +------------------------+-------------------------+
                |                                                  |
       +--------v--------+                                +--------v--------+
       |  Input Dataset  |                                |   Preprocessing  |
       +--------+--------+                                +--------+--------+
                |                                                  |
                +------------------------+-------------------------+
                                         |
                          +--------------v--------------+
                          |   Mining Association Rules   |
                          +--------------+--------------+
                                         |
                          +--------------v--------------+
                          |        Output Rules         |
                          +--------------+--------------+
                                         |
                          +--------------v--------------+
                          |       Export Results        |
                          +-----------------------------+
```

---

## Installation and Setup

### Prerequisites

Install Java, Docker, Python3, and `faas-cli`:

```sh
sudo apt update
sudo apt install default-jre docker.io python3
curl -sSL https://cli.openfaas.com | sudo sh
```

Alias Python 3:

```sh
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

---

## Configuration

Before running, update the following files:

- `deployment/apriori/configs/GARM.xml` — update all file paths
- `deployment/apriori/demoInput/typeMappings.json` — update image IDs
- `FunctionTemplate/openfaas/push_images` — DockerHub image references
- `FunctionTemplate/openfaas/stack.yml` — DockerHub image references
- `FunctionTemplate/openfaas/typeMappings.json` — DockerHub image references

---

## Build and Push Docker Images

```sh
sudo ./build_and_push.sh
```

---

## Execute the Project

```sh
sudo ./main 0.5 1 8
```

Arguments:
- `0.5`: Minimum Support
- `1`: Minimum Confidence
- `8`: Maximum Rule Length

In Apollo GUI, load:
```
deployment/apriori/configs/GARM.xml
```

Results will be saved to:
```
output.json
```

---

## Experimental Highlights

Datapollo was tested on real datasets (COVID-19, Lung Cancer, Meteorological). Key observations:

- **Faster execution** than Apache Spark
- **Similar or better rule quality**
- **Elasticity and cost efficiency** due to serverless FaaS model

---

## License

MIT License.

---

### Introduction

Datapollo is a lightweight, scalable, and serverless framework for performing Association Rule Mining (ARM) on large datasets. It leverages modern Function-as-a-Service (FaaS) architectures to efficiently orchestrate ARM tasks without the overhead of traditional cluster-based platforms like Apache Spark. This project demonstrates how cloud-native paradigms can simplify ARM workflows while improving cost-effectiveness and performance.

---

### Features

- **Serverless Execution**: Fully decoupled Lambda functions for preprocessing, mining, and rule aggregation.
- **Flexible Scheduling**: DAG-based task orchestration using Apollo Scheduler.
- **Stateless Design**: External state management ensures resilience and scalability.
- **Domain-agnostic Application**: Tested on healthcare, climate, and analytics datasets.
- **Lightweight Deployment**: Minimal setup needed using Docker and faas-cli.

---

### Use Cases

This implementation has been tested across the following real-world domains:

- **Healthcare**: Discovering associations in COVID-19 and lung cancer datasets.
- **Meteorology**: Identifying correlations between environmental parameters.
- **Benchmarking**: Comparing performance against Apache Spark in terms of rule quality, runtime, and scalability.

---

### Architecture Breakdown

Each stage of the pipeline runs as an independent Lambda function:

1. **Preprocessing** – Cleans and formats raw inputs.
2. **Data Partitioning** – Splits data across cloud object storage.
3. **Frequent Itemset Mining** – Parallelized support computation using Apriori.
4. **Rule Generation** – Filters by confidence and lift, generates output rules.
5. **Exporting Results** – Outputs JSON and CSV formats to external storage.

This serverless design allows horizontal scaling and fault tolerance while maintaining simplicity.

---

### Performance Insights

- Datapollo consistently outperformed Spark across various datasets (30%, 60%, 80% support thresholds).
- Rules generated by Datapollo were stronger (higher confidence/support).
- Spark occasionally extracted more rules, but at higher cost and runtime.
- Cloud-native execution reduced idle resource costs.

---

