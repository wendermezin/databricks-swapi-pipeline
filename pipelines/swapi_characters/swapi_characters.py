from pyspark import pipelines as dp
from pyspark.sql.types import StructType, StructField, StringType
import requests


@dp.table(
    name="characters",
    comment="Star Wars characters ingested from SWAPI API (https://swapi.dev/api/people)"
)
def characters():
    url = "https://swapi.dev/api/people/"
    records = []

    while url:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        for person in data["results"]:
            records.append({
                "name": person.get("name"),
                "height": person.get("height"),
                "mass": person.get("mass"),
                "birth_year": person.get("birth_year"),
                "homeworld": person.get("homeworld"),
            })

        url = data.get("next")

    schema = StructType([
        StructField("name", StringType(), True),
        StructField("height", StringType(), True),
        StructField("mass", StringType(), True),
        StructField("birth_year", StringType(), True),
        StructField("homeworld", StringType(), True),
    ])

    return spark.createDataFrame(records, schema=schema)
