import os
import requests
from databricks.connect import DatabricksSession
from pyspark.sql.types import StructType, StructField, StringType
from dotenv import load_dotenv

load_dotenv()

# Conecta ao workspace via Databricks Connect
# Configure DATABRICKS_CONFIG_PROFILE no arquivo .env
profile = os.getenv("DATABRICKS_CONFIG_PROFILE")
if not profile:
    raise EnvironmentError("DATABRICKS_CONFIG_PROFILE não definido. Configure o arquivo .env.")
spark = DatabricksSession.builder.profile(profile).serverless(True).getOrCreate()

TARGET_TABLE = "star_wars_api_wender.landing.characters"
SWAPI_URL = "https://swapi.dev/api/people/"
MAX_RECORDS = 10_000


def fetch_all_characters(url: str, limit: int = MAX_RECORDS) -> list[dict]:
    records = []
    while url and len(records) < limit:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        for person in data["results"]:
            if len(records) >= limit:
                break
            records.append({
                "name": person.get("name"),
                "height": person.get("height"),
                "mass": person.get("mass"),
                "birth_year": person.get("birth_year"),
                "homeworld": person.get("homeworld"),
            })
        url = data.get("next")
        print(f"Fetched {len(records)} characters so far (limit: {limit})...")
    return records


schema = StructType([
    StructField("name", StringType(), True),
    StructField("height", StringType(), True),
    StructField("mass", StringType(), True),
    StructField("birth_year", StringType(), True),
    StructField("homeworld", StringType(), True),
])

print("Fetching Star Wars characters from SWAPI (running locally)...")
characters = fetch_all_characters(SWAPI_URL)
print(f"Total characters fetched: {len(characters)}")

df = spark.createDataFrame(characters, schema=schema)
df.write.format("delta").mode("overwrite").saveAsTable(TARGET_TABLE)

print(f"Successfully loaded {df.count()} characters into {TARGET_TABLE}")
