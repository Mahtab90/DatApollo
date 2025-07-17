# DatApollo: Serverless Association Rule Mining Framework

## Overview

DatApollo is a scalable, cloud-native framework designed to perform **Association Rule Mining (ARM)** using a serverless Function-as-a-Service (FaaS) model. It decomposes the ARM process into stateless micro-functions orchestrated through the **Apollo Runtime System**, enabling highly efficient, fault-tolerant, and cost-effective mining of frequent patterns across large-scale transactional datasets.

This repository provides:
- A serverless implementation of Apriori-based ARM
- Adaptive DAG orchestration with Apollo
- Preprocessing, partitioning, and rule export utilities
- Dockerized function templates and OpenFaaS integration
- Benchmark comparisons against Apache Spark



## Architecture Flow

                      +-----------------------------+
                      |   DatApollo Serverless      |
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


---

## Prerequisites

Ensure the following tools are installed on your system:

-sudo apt update
-sudo apt install default-jre docker.io python3 -y
-curl -sSL https://cli.openfaas.com | sudo sh


Alias Python 3:
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc

(Configuration)
Before execution, modify configuration files appropriately:
deployment/apriori/configs/GARM.xml — Update dataset and output paths
deployment/apriori/demoInput/typeMappings.json — Specify input data mapping
FunctionTemplate/openfaas/push_images — Edit DockerHub image references
FunctionTemplate/openfaas/stack.yml — Configure function stack for deployment
FunctionTemplate/openfaas/typeMappings.json — Update image metadata


(Build and Push Docker Images)
To build and publish your Docker images for OpenFaaS:
cd FunctionTemplate/openfaas
sudo ./build_and_push.sh


Execution
To execute the ARM pipeline with DatApollo: sudo ./main 0.5 1 8

Arguments:
0.5 — Minimum Support Threshold
1 — Minimum Confidence Threshold
8 — Maximum Rule Length

Open Apollo GUI and load: deployment/apriori/configs/GARM.xml
Results will be saved to: output/output.json


(Repository Structure)
.
├── deployment/
│   ├── apriori/
│   │   ├── configs/
│   │   └── demoInput/
├── FunctionTemplate/
│   └── openfaas/
│       ├── build_and_push.sh
│       ├── push_images
│       ├── stack.yml
│       └── typeMappings.json
├── output/
│   └── output.json
├── scripts/
│   └── preprocessing, rule generation, etc.
└── README.md


(Features)
Serverless Execution: Functions run independently via OpenFaaS or AWS Lambda.
Apollo DAG Orchestration: Latency-aware scheduling, checkpointing, and retries.
Lightweight Deployment: Fully containerized pipeline deployable with faas-cli.
Domain-Agnostic ARM: Supports various domains including healthcare and meteorology.
Cloud Storage Integration: Uses S3-compatible storage for state persistence.

(Use Cases)
DatApollo has been applied to several real-world datasets:
COVID-19 Dataset: Symptom correlation analysis.
Lung Cancer Dataset: Risk pattern discovery from PLCO study.
Meteorological Dataset: Weather pattern identification using ECAD/CMIP6 data.

(Performance Highlights)
Up to 5x speedup over Apache Spark for large ARM tasks
Higher support and confidence in extracted rules
Serverless autoscaling leads to lower infrastructure costs
Handles high-throughput workloads with fine-grained fault recovery

(Further Reading)
Apollo Runtime on YouTube: https://www.youtube.com/@apolloruntimesystem6686/featured


(Contact)
Mahtab Shahin
Postdoctoral Researcher, Tallinn University of Technology
mahtab.shahin@taltech.ee


