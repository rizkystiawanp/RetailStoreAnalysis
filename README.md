# Retail Store Analysis
### This project aims to analyze sales data across various product categories and regions during the 2022-2023 period. Using Docker, Apache Airflow, PostgreSQL, Elasticsearch, and Kibana, I automated the data pipeline and visualized key business insights.
### The analysis focuses on sales trends, product distribution, competitor price impact, seasonal demand patterns, and strategic recommendations for inventory and promotions.

[View the presentation as PDF](RetailStoreAnalysis.pdf)

## Dataset Source
```
Dataset is taken from :

Retail Store Inventory Forecasting Dataset
By Anirudh Singh Chauhan

```
<a href="https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset">DATASET LINK</a>

## Role in the Project
As a Data Analyst, my responsibilities included
- Analyzing sales trends and demand patterns by region & product category.
- Identifying external factors affecting sales, such as weather & competitor pricing.
- Developing an interactive dashboard to help business teams make data-driven decisions. 

## Background
For retail companies operating across multiple regions and product lines, understanding sales patterns, competitor pricing, and external factors is crucial for marketing strategies & inventory management.
The primary goal of this analysis is to provide data-driven insights to improve business strategy and profitability.

## Project Objectives
✅ Analyze sales performance and profitability by product category & region.
✅ Identify demand trends and customer purchasing patterns.
✅ Evaluate the impact of competitor pricing on unit sales.
✅ Assess how weather and seasonal patterns affect demand.
✅ Provide business recommendations for inventory and marketing optimization.

## Target Users
- Sales & Marketing Teams → To plan promotions and data-driven marketing campaigns.
- Logistics & Supply Chain Teams → To optimize inventory management based on demand trends.
- Executive Management → To support strategic decision-making for business expansion & pricing optimization.

## Tools & Technologies Used
```
🔹 Docker → Running Airflow, PostgreSQL, Elasticsearch, and Kibana in containerized environments.
🔹 Apache Airflow → Automating the ETL (Extract, Transform, Load) pipeline to keep data up-to-date.
🔹 PostgreSQL → Storing structured sales data for analysis.
🔹 Elasticsearch → Enabling high-performance data search & analysis.
🔹 Kibana → Creating interactive dashboards for data exploration.
```

## Data Pipeline Workflow
```
This project automates data extraction, transformation, and analysis as follows:

1️⃣ Extract Data from PostgreSQL → Raw data is pulled from the database.
2️⃣ Clean & Transform Data → Data is processed and formatted using Python & Pandas.
3️⃣ Index Data into Elasticsearch → Processed data is uploaded to Elasticsearch for efficient analysis.
4️⃣ Visualize Insights in Kibana → Dashboards display key insights such as:

- Sales trends by season & region
- Competitor pricing impact on unit sales
- Analysis of promotion effectiveness & product inventory
```

## Installation Instructions
To set up this project locally, follow these steps:

1. Clone this repository:
2. Install Docker if you haven't already.
3. Build and start the Docker environment:
```
docker-compose -f .\airflow\airflow.yaml up -d
```
The following services will be started:

- Airflow (for orchestrating the pipeline)
- PostgreSQL (for storing cleaned data)
- Elasticsearch (for indexing data)
- Kibana (for visualizing the data)

Access the services:
- Airflow UI: http://localhost:8080
- Kibana UI: http://localhost:5601

Once the pipeline is running, it will automatically extract, clean, process, and load the data into PostgreSQL and Elasticsearch. You can then explore the data in Kibana.