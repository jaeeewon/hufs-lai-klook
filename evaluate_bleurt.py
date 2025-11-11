import torch, pandas as pd
from bleurt_pytorch import (
    BleurtConfig,
    BleurtForSequenceClassification,
    BleurtTokenizer,
)
from collections import Counter

testsets = pd.read_json("bleurt_testsets.jsonl", lines=True)

config = BleurtConfig.from_pretrained("lucadiliello/BLEURT-20")
model = BleurtForSequenceClassification.from_pretrained("lucadiliello/BLEURT-20")
tokenizer = BleurtTokenizer.from_pretrained("lucadiliello/BLEURT-20")

model.eval()


def bleurt_score(references: list[str], candidates: list[str]):
    with torch.no_grad():
        inputs = tokenizer(
            references, candidates, padding="longest", return_tensors="pt"
        )
        return model(**inputs).logits.flatten().tolist()


counter = Counter()

if __name__ == "__main__":
    bleurt_scores = bleurt_score(
        references=testsets["reference"].tolist(),
        candidates=testsets["source"].tolist(),
    )

    for index, row in testsets.iterrows():
        print(f"reference: {row['reference']}")
        print(f"candidate: {row['source']}")
        print(f"calculated BLEURT: {bleurt_scores[index]}")
        print("-----")

    print(sum(bleurt_scores) / len(bleurt_scores))

    # testsets = ds[["Source", "Reference Target"]]
    # testsets.rename(
    #     columns={"Source": "source", "Reference Target": "reference"}, inplace=True
    # )
    # testsets.to_json(
    #     "bleurt_testsets.jsonl", orient="records", lines=True, force_ascii=False
    # )
