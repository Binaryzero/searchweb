import json
import pprint

import pandas as pd

with open("mirror/1999/CVE-1999-0001.json", "r") as f_in:
    data = json.load(f_in)
pprint(data)
# df = []
# /for v in data["vulnerabilities"]:
#    value = next(d["value"] for d in v["cve"]["descriptions"] if d["lang"] == "en")
#    refs = [r["url"] for r in v["cve"]["references"]]
#    df.append((value, refs))
#
# df = pd.DataFrame(df, columns=["value", "url"]).explode("url")
# print(df)
