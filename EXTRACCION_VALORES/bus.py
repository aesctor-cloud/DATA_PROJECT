import pandas as pd

import conexion_mongo

# Bus
bus = conexion_mongo["bus"]

df_bus = pd.DataFrame([
        {
            "id": record["coddistbar"],
            "paradas_bus": record["paradas_bus"]
        }
        for record in bus["results"]
    ])