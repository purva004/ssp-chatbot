import pandas as pd
from neo4j import GraphDatabase

df = pd.read_csv("occupancy_data.csv")

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "purva@1234"))

def insert_data(tx, row):
    tx.run("""
    CREATE (:Occupancy {
        RecordDate: $RecordDate,
        TimeSlot: $TimeSlot,
        Floor: $Floor,
        WiFiCount: $WiFiCount,
        LocationCode: $LocationCode,
        SiteDetails: $SiteDetails
    })
    """, 
    RecordDate=row.get("RecordDate", ""),
    TimeSlot=row.get("TimeSlot", ""),
    Floor=row.get("Floor", ""),
    WiFiCount=int(row.get("WiFiCount", 0) or 0),
    LocationCode=row.get("LocationCode", ""),
    SiteDetails=row.get("SiteDetails", "")
    )

with driver.session() as session:
    for _, row in df.iterrows():
        session.execute_write(insert_data, row.to_dict())
driver.close()