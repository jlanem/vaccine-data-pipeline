  
### COVID-19 Vaccine Coverage Data Pipeline

This Test project for Assessment for Senior Python Backend Engineer by https://savannahtech.io/
This project  is a Python-based data pipeline that fetches,
processes, and visualizes global COVID-19 vaccine coverage data using the disease.sh API.
```sh
🔹 How It Works
1️⃣ Fetches vaccine data from the API.
2️⃣ Parses and processes the data.
3️⃣ Saves it to a CSV file (vaccine_coverage.csv).
4️⃣ Generates a bar chart (vaccine_coverage.png).
5️⃣ Logs execution details for debugging.


### Development

1. Create and start virtual environment
   ```sh
   python3 -m venv env
   source env/bin/activate
1. Git clone `https://github.com/jlanem/vaccine-data-pipeline.git` 
1. cd to vaccine-data-pipeline directory and instal requirements

    ```sh
    cd vaccine_data_pipeline
    pip install requirements.txt
 Run the Pipeline
    ```sh
    python3 vaccine_pipeline.py
