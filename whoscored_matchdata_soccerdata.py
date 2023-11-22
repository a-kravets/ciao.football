# https://soccerdata.readthedocs.io/en/latest/intro.html

import soccerdata as sd
import pandas as pd

ws = sd.WhoScored(leagues="ITA-Serie A", seasons=2023)

events = ws.read_events(match_id=1746142)
df = pd.DataFrame(events)

df.to_csv("match_data.csv")

#print(events.head())