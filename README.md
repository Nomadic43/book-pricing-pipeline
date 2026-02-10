# Pricing Intelligence Data Pipeline

This project implements a production-ready data engineering pipeline that scrapes product data from the web, put it with currency exchange rates, transforms it into an analytics ready format, and loads it into PostgreSQL.  
The entire pipeline is orchestrated using **Apache Airflow** and runs in a fully **Dockerized environment**.

## What This Pipeline Do

1. **Scrapes product data** from `books.toscrape.com`
   - Product title
   - Price (GBP)
   - Category
   - Availability

2. **Fetches daily GBP to INR exchange rate**
   - Uses a public exchange rate API
   - Stores rates in a staging table for reuse

3. **Transforms raw data**
   - Cleans and normalizes text fields
   - Converts prices from GBP to INR
   - Derives price tiers like cheap, moderate, expensive
   - Generates a stable product ID using hashing

4. **Loads final data**
   - Writes clean, analytics ready data into PostgreSQL
   - Designed to be idempotent and rerunnable

---

## Tech Stack

- **Python**
- **Apache Airflow** (orchestration)
- **PostgreSQL** (data storage)
- **Docker & Docker Compose** (containerization)
- **BeautifulSoup & Requests** (web scraping)

---

## Project Structure

pricing-intelligence-pipeline/
>> dags/ # Airflow DAG definitions
>> scripts/ # Python scripts for each pipeline step
>> sql/ # SQL initialization scripts
>> Dockerfile # Airflow image customization
>> docker-compose.yml # Services orchestration
>> requirements.txt # Python dependencies
>> README.md

## How to Run the Pipeline Locally

### 1. Prerequisites
- Docker Desktop installed and running
- Docker Compose available

---

### 2. Start the services

From the project root:

```bash
docker-compose up -d

for airflow UI:

http://localhost:8080

## Airflow Login (Local)

For local development, Airflow is configured with a default admin user:

- **Username:** airflow
- **Password:** airflow

These credentials are intended for local testing only.