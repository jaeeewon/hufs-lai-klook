import json, os
from qwen3 import qwen3_api
from tqdm import tqdm

ERROR_TYPE = [
    "MISTRANSLATION",
    "OVERTRANSLATION",
    "UNDERTRANSLATION",
    "WRONG VARIABLE",
    "GRAMMAR",
    "SPELLING/TYPO",
    "PUNCTUATION & FORMATTING",
    "LOCALE CONVENTION ISSUE",
    "CULTURAL RELEVANCE ISSUE",
    "GLOSSARY ISSUE",
    "STYLE GUIDE ISSUE",
    "AWKWARD STYLE & REPETITIONS",
    "INCONSISTENCY",
    "LENGTH",
]
ERROR_TYPE_STR = json.dumps(ERROR_TYPE)

IMPACT_TYPE = [
    "Critical",
    "Major",
    "Minor",
]
IMPACT_TYPE_STR = json.dumps(IMPACT_TYPE)


def evaluate_translation(file_path: str):
    resp = []
    with open(file_path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    eval_path = file_path.replace("translations", "evaluations")
    eval_dir = os.path.dirname(eval_path)
    os.makedirs(eval_dir, exist_ok=True)

    with open(eval_path, "w", encoding="utf-8") as f_out:
        for id, dta in tqdm(enumerate(data), total=len(data)):
            key = dta["key"]
            item_type = dta["item_type"]
            source = dta["src"]
            translation = dta["tgt"]

            system_prompt = """You are a meticulous and strict AI Translation Quality Evaluator working for Klook, an online travel company.
Your mission is to strictly evaluate English-to-Korean translations for tourism-related content. You must check for semantic consistency, cultural appropriateness for Korean travelers, and natural Korean expression.

Your evaluation is critical as it is linked to Klook's brand reputation. The `impact_type` you assign must reflect the severity of the issue from a customer's perspective.

**Core Instructions:**

1.  **Output Format:** Your output **MUST** be a valid JSON array of error objects.
2.  **No Errors:** If the translation is perfect and has no errors, return an empty array `[]`.
3.  **Identify All Errors:** You must identify every single error in the translation, *except* for whitespace or line break issues.
4.  **JSON Object Fields:** Each error object in the array **must** contain exactly these six fields:
    * `"error_type"`: The error classification.
    * `"impact_type"`: The impact classification (severity from customer perspective).
    * `"source"`: The *exact* English phrase segment from the source that has an error.
    * `"target"`: The *exact* corresponding Korean phrase segment from the translation that is incorrect.
    * `"offer"`: The single, corrected Korean phrase for that segment. **Do not include explanations here.**
    * `"reason"`: A brief, professional explanation in **100% Korean** of *why* it is an error. **Do not include the correction here.** (e.g., "직역이라 어색함", "문맥에 맞지 않음", "용어 불일치", "불필요한 반복", "핵심 의미('선택') 누락").
5.  **Language Rule:** The `reason` field must be 100% Korean. No English.
6.  **Scoping Rule:** The `source` and `target` fields must contain *only* the specific phrases that are wrong, not the entire sentence.

**Critical Evaluation Rules (MUST FOLLOW):**

1.  **FORMATTING EXCLUSION RULE (IMPORTANT):**
    * **Do NOT** report any errors related to line breaks (`\n`), missing/extra spacing, or other whitespace issues. These are considered crawling issues and **must be ignored**.

2.  **Key Variable Context (title/contents):**
    * If the 'key' variable is **`title`**: Titles are short. Brevity, accuracy, and impact are most important.
    * If the 'key' variable is **`contents`**: Content is longer. Focus on the flow between sentences and semantic accuracy, but *ignore* line break formatting.

3.  **Currency & Number Rule:**
    * **Source has Digits (e.g., "150 yen"):** The translation **MUST** use the format `JPY150`. All other formats (`150엔`, `JPY 150`, `150 JPY`, `150원`) are **incorrect**. A range like "150-300 yen" should be `JPY150~300`.
    * **Source has Words (e.g., "a few hundred yen"):** The translation **MUST** use Korean words (e.g., "수백 엔"). Translating this as `JPY100` is a `MISTRANSLATION`."""

            user_prompt = f"""Please evaluate the following translation based on the rules provided.

**Task Context:**
* The source item type is: **{item_type}**
* This content is used as a **{key}** in the Klook service. (e.g., 'title' or 'contents')

**Error Classifications:**
* ERROR TYPES: {ERROR_TYPE_STR}
* IMPACT TYPES: {IMPACT_TYPE_STR}

**JSON Output Format Example:**
[
  {{
    "error_type": "MISTRANSLATION",
    "impact_type": "Major",
    "source": "How to book",
    "target": "어떻게 사용하나요?",
    "offer": "예약 방법",
    "reason": "'How to book'는 예약 방법을 묻는 표현이므로, '어떻게 사용하나요?'는 문맥에 맞지 않음."
  }},
  {{
    "error_type": "AWKWARD STYLE & REPETITIONS",
    "impact_type": "Major",
    "source": "The Tokaido Shinkansen",
    "target": "도카이도 신칸센도카이도 신칸센은",
    "offer": "도카이도 신칸센",
    "reason": "원본에 해당하지 않는 불필요한 텍스트가 반복 삽입됨."
  }},
  {{
    "error_type": "MISTRANSLATION",
    "impact_type": "Major",
    "source": "A basic fare... costs around 150-300 yen",
    "target": "요금은 약 JPY150-300가 발생하며",
    "offer": "기본 요금은 약 JPY150~300입니다",
    "reason": "번역이 부자연스럽고 문맥이 끊어짐. 또한 'JPY150-300'가 아닌 'JPY150~300' 형식이 권장됨."
  }},
  {{
    "error_type": "MISTRANSLATION",
    "impact_type": "Major",
    "source": "...a few hundred to a couple thousand yen",
    "target": "요금은 JPY100-1000까지 다양합니다",
    "offer": "요금은 수백 엔에서 수천 엔까지 다양합니다",
    "reason": "원문의 'a few hundred'를 'JPY100'로, 'a couple thousand'를 '1000'으로 오역함. 원문이 숫자가 아니므로 '수백 엔' 등으로 번역해야 함."
  }}
]

**Evaluate Now:**

<source>
{source}
</source>

<translation>
{translation}
</translation>"""

            response = qwen3_api(user_prompt=user_prompt, system_prompt=system_prompt)

            # print("Source:", source)
            # print("Translation:", translation)
            # print("Evaluation:", response)
            # print("-" * 50)

            try:
                res_json = json.loads(response)
            except json.JSONDecodeError:
                print("JSONDecodeError for", dta)
                print("LLM output:", response)
                res_json = []

            resp.extend(res_json)
            for r in res_json:
                r["key"] = key
                r["item_type"] = item_type
                r["orig_source"] = source
                r["orig_translation"] = translation
                f_out.write(json.dumps(r, ensure_ascii=False) + "\n")
            f_out.flush()
    return resp


if __name__ == "__main__":
    translation_file_name = "translations/klook_trains_translations.jsonl"
    evaled = evaluate_translation(translation_file_name)

    error_types = {}
    impact_types = {}
    for ev in evaled:
        etype = ev["error_type"]
        itype = ev["impact_type"]
        error_types[etype] = error_types.get(etype, 0) + 1
        impact_types[itype] = impact_types.get(itype, 0) + 1
    print("ERROR TYPES:", error_types)
    print("IMPACT TYPES:", impact_types)

    result_file_name = translation_file_name.replace("translations", "results")

    with open(result_file_name, "w", encoding="utf-8") as f:
        summary = {
            "total_evaluations": len(evaled),
            "error_types": error_types,
            "impact_types": impact_types,
        }
        f.write(json.dumps(summary, ensure_ascii=False, indent=4))
