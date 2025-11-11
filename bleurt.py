import torch, pandas as pd
from bleurt_pytorch import (
    BleurtConfig,
    BleurtForSequenceClassification,
    BleurtTokenizer,
)
from collections import Counter

ds = pd.read_excel("res.xlsx")

config = BleurtConfig.from_pretrained("lucadiliello/BLEURT-20")
model = BleurtForSequenceClassification.from_pretrained("lucadiliello/BLEURT-20")
tokenizer = BleurtTokenizer.from_pretrained("lucadiliello/BLEURT-20")

references = ds["Reference Target"].tolist()
candidates = ds["Model Predicted Target"].tolist()

model.eval()
with torch.no_grad():
    inputs = tokenizer(references, candidates, padding="longest", return_tensors="pt")
    ds["bleurt_score"] = model(**inputs).logits.flatten().tolist()

counter = Counter()

for index, row in ds.iterrows():
    if row["bleurt_score"] != row["BLEURT Score"]:
        counter["incorrect"] += 1
        counter["delta"] += abs(row["bleurt_score"] - row["BLEURT Score"])
        print(f"Reference: {row['Reference Target']}")
        print(f"Candidate: {row['Model Predicted Target']}")
        print(
            f"Computed BLEURT: {row['bleurt_score']}, Given BLEURT: {row['BLEURT Score']}"
        )
        print("-----")
    else:
        counter["correct"] += 1

print(counter)
if counter["incorrect"] > 0:
    print(f"average delta: {counter['delta'] / counter['incorrect']}")
print(f"average bleurt: {sum(ds['bleurt_score']) / len(ds):.4f}")

"""
Counter({'correct': 44, 'incorrect': 42, 'delta': 2.9951333999078678e-06})
average delta: 7.131269999780638e-08
average bleurt: 0.7035
"""

testsets = ds[["Source", "Reference Target", "Glossary"]]
testsets.rename(
    columns={
        "Source": "source",
        "Reference Target": "reference",
        "Glossary": "glossary",
    },
    inplace=True,
)
testsets.to_json(
    "bleurt_testsets.jsonl", orient="records", lines=True, force_ascii=False
)
