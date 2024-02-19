import pandas as pd
import requests

url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
data = requests.get(url).json()

df = []
for v in data["vulnerabilities"]:
    value = next(d["value"] for d in v["cve"]["descriptions"] if d["lang"] == "en")
    refs = [r["url"] for r in v["cve"]["references"]]
    df.append((value, refs))

df = pd.DataFrame(df, columns=["value", "url"]).explode("url")
print(df)
