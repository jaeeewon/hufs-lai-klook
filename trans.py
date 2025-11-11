import re, os, pandas as pd
from qwen3 import qwen3_api
from tqdm import tqdm
from evaluate_bleurt import bleurt_score

with open("klook_prompt.txt", "r", encoding="utf-8") as f:
    user_prompt_placeholder = f.read()


def execute_translation(file_path: str):
    resp = []
    data = pd.read_json(file_path, lines=True).to_dict(orient="records")

    eval_path = file_path.replace("testsets", "testsets_evaluated")
    eval_dir = os.path.dirname(eval_path)
    if eval_dir:
        os.makedirs(eval_dir, exist_ok=True)

    with open(eval_path, "w", encoding="utf-8") as f_out:
        for id, dta in tqdm(enumerate(data), total=len(data)):
            user_prompt = user_prompt_placeholder.replace(
                "{{english_text}}", dta["source"]
            ).replace("{{glossary_str}}", dta["glossary"] if dta["glossary"] else "-")
            response = qwen3_api(user_prompt=user_prompt)
            match = re.search(r"<translation>(.*?)</translation>", response)
            assert match is not None, f"failed to extract translation: {response}"
            response = match.group(1).strip()
            f_out.write(response + "\n")
            f_out.flush()

            print(f"==== ID: {id} ====")
            print("SOURCE:", dta["source"])
            print("REFERENCE:", dta["reference"])
            print("TRANSLATION:", response)
            print("BLEURT:", bleurt_score([dta["reference"]], [response]))
    return resp


if __name__ == "__main__":
    testset_file_name = "bleurt_testsets.jsonl"
    executed = execute_translation(testset_file_name)
