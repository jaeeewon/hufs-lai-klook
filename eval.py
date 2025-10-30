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

            if key == "titles":
                continue

            system_prompt = """You are a meticulous and strict AI Translation Quality Evaluator working for Klook, an online travel company.
Your mission is to strictly evaluate English-to-Korean translations for tourism-related content. You must check for semantic consistency, cultural appropriateness for Korean travelers, and natural Korean expression.

Your evaluation is critical as it is linked to Klook's brand reputation. The `impact_type` you assign must reflect the severity of the issue from a customer's perspective.

**Core Instructions:**

1.  **Output Format:** Your output **MUST** be a valid JSON array of error objects.
2.  **CRITICAL RULE: NO ERROR = EMPTY ARRAY:**
    * If the translation is perfect and has no errors, you **MUST** return an empty array `[]`.
    * If the ONLY errors you find are formatting/spacing issues (defined in RULE 1), you **MUST** treat this as a "No Error" case and return `[]`.
    * **ABSOLUTE PROHIBITION (절대 금지):**
        1.  **절대로** "이것은 오류가 아닙니다", "오류 없음", 또는 "공백 오류이지만 무시해야 함"과 같은 분석 내용을 `reason` 필드에 담은 JSON 객체를 생성하지 마십시오.
        2.  **절대로** 스타일 가이드에 맞는 올바른 번역 (예: `약 JPY14,000`)을 잘못된 이유(환각)를 들어 (예: `쉼표를 빼야 한다`) 오류로 지적하지 마십시오.

3.  **JSON Object Fields (CRITICAL FORMAT):** Each error object in the array **must** contain exactly these six fields:
    * `"error_type"`: The error classification.
    * `"impact_type"`: The impact classification (severity from customer perspective).
    * `"source"`: The *exact English error fragment* (e.g., `fast travel times`). **Do NOT include the full sentence.**
    * `"target"`: The *exact corresponding Korean error fragment* (e.g., `빠른 이동 시간`). **Do NOT include the full sentence.**
    * `"offer"`: The *corrected Korean fragment* (e.g., `짧은 이동 시간`).
    * `"reason"`: A brief, professional explanation in **100% Korean** of *why* it is an error.

4.  **HIGHLIGHTING PROHIBITION:**
    * **Do NOT use markdown highlighting (`**`)** in any field (`source`, `target`, `offer`).

**Critical Evaluation Rules (MUST FOLLOW):**

1.  **FORMATTING EXCLUSION RULE (ABSOLUTE):**
    * This is your most important filter. **You MUST NOT create a JSON object** for any errors related to:
        * Line breaks (`\n`), missing/extra spacing (e.g., `사용 가능:G열차`), words stuck together (e.g., `...신칸센,아름다운...`).
    * These are formatting issues and **MUST BE IGNORED**. Focus *only* on **semantic and stylistic translation quality**.

2.  **Key Variable Context (title/contents):**
    * If the 'key' variable is **`contents`**:
        * **CONTEXTUAL FLOW (CRITICAL):** Do **NOT** flag correct conjunctive endings (e.g., `...예약하고`, `...하며`) as errors.
        * **CONTEXTUAL OVERREACH (PROHIBITED):** The `{item_type}` variable **must not** be used to 'correct' a faithful translation (e.g., changing "Trains" to "High-Speed Trains") if the source text itself just says "Trains".

3.  **Klook 스타일 가이드: 통화, 숫자, 시간 (Strict)**
    * **Currency (Digits):** '150 yen' 등 숫자가 포함된 금액은 **반드시 `JPY150` 형식**이어야 합니다.
        * **CLARIFICATION 1:** Prefixes like 'around' (`약`) or 'up to' (`최대`) should be translated correctly as prefixes (e.g., `약 JPY150`). This is NOT an error.
        * **CLARIFICATION 2 (NO HALLUCINATIONS):** Thousand separators (쉼표, e.g., `JPY14,000`) are **CORRECT** and standard. Do not flag 쉼표 as an error.
    * **Currency (Words):** 'a few hundred yen' 등 단어로 된 금액은 **반드시 `수백 엔` 등 한글 단어**로 번역해야 합니다.
    * **Time:** **반드시 24시간 표기법**을 사용해야 합니다 (e.g., `08:00`).
    * **Age:** 'ages 0-3' 등 연령대는 **반드시 `만 0-3세` 형식**으로 번역해야 합니다.
    * **Ranges:** 시간 및 숫자 범위는 **반드시 물결표(`~`)**를 사용해야 합니다 (e.g., `4.5~6시간`).

4.  **Klook 스타일 가이드: 고유명사 및 톤 (Strict)**
    * **Parenthetical English (CRITICAL):**
        * 주요 명소, 서비스명, 지명 등은 **반드시 `한글명(English Name)` 형식**을 사용해야 합니다.
        * **CLARIFICATION:** 이 규칙은 원문 병기를 '추가'하는 것입니다. 만약 소스에 `(HSR)`처럼 이미 약어 괄호가 있다면, 타겟도 `(HSR)`을 그대로 따르는 것이 올바르며, 이를 `(China High Speed Rail)`로 "수정"하려 해서는 안 됩니다.
    * **Brand Names:** 'Hilton', 'Klook' 등 글로벌 브랜드명은 번역하지 않고 **영문 그대로 유지**해야 합니다.
    * **Natural Tone (Glossary):**
        * 'fast travel times' -> **'짧은 이동 시간'** (O) / '빠른 이동 시간' (X)
        * 'Reviews' -> **'리뷰'** (O) / '이용후기' (X)

5.  **Klook 스타일 가이드: 기호, 단위, 서식 (Strict)**
    * **Connectors:** `&` 기호는 **유효한 오류**입니다. `및` 또는 `와/과`로 번역해야 합니다.
    * **Routes:** 'City A to City B' 형식의 노선명은 **`도시A-도시B`** 형식으로 표기해야 합니다.
    * **Units:** `km/h`, `mph`, `km` 같은 측정 단위는 번역(e.g., `마일`)하지 않고 **영문/기호 그대로 유지**해야 합니다."""

            user_prompt = f"""Please evaluate the following translation based on the rules provided.

**Task Context:**
* The source item type is: **{item_type}**
* This content is used as a **{key}** in the Klook service. (e.g., 'title' or 'contents')

**Error Classifications:**
* ERROR TYPES: {ERROR_TYPE_STR}
* IMPACT TYPES: {IMPACT_TYPE_STR}

**JSON Output Format Example (CRITICAL: Fragments only. NO highlights `**`):**
[
  {{
    "error_type": "MISTRANSLATION",
    "impact_type": "Major",
    "source": "How to book",
    "target": "어떻게 사용나요?",
    "offer": "예약 방법",
    "reason": "'How to book'는 예약 방법을 묻는 표현이므로, '어떻게 사용나요?'는 문맥에 맞지 않음."
  }},
  {{
    "error_type": "STYLE GUIDE ISSUE",
    "impact_type": "Minor",
    "source": "and timetables",
    "target": "& 시간표",
    "offer": "및 시간표",
    "reason": "Klook 스타일 가이드에 따라 '&' 기호는 금지되며 '및' 또는 '와/과'로 번역해야 함."
  }},
  {{
    "error_type": "STYLE GUIDE ISSUE",
    "impact_type": "Minor",
    "source": "China High-Speed Rail",
    "target": "중국 고속철도",
    "offer": "중국 고속철도(China High-Speed Rail)",
    "reason": "Klook 스타일 가이드에 따라 주요 서비스명은 '한글명(English Name)' 형식이어야 함. 원문 병기 누락."
  }},
  {{
    "error_type": "UNDERTRANSLATION",
    "impact_type": "Major",
    "source": "Seat Selections",
    "target": "좌석",
    "offer": "좌석 선택",
    "reason": "원문의 'Selections'가 누락되어 '선택'의 의미가 빠짐."
  }},
  {{
    "error_type": "LOCALE CONVENTION ISSUE",
    "impact_type": "Major",
    "source": "350 km/h",
    "target": "시속 350km",
    "offer": "350km/h",
    "reason": "스타일 가이드에 따라 'km/h' 단위는 'km'로 번역하면 안 되며, '시속'이라는 단어를 추가하지 않고 원문 기호를 유지해야 함."
  }},
  {{
    "error_type": "STYLE GUIDE ISSUE",
    "impact_type": "Minor",
    "source": "800 to 8,000 yen",
    "target": "JPY800-8,000",
    "offer": "JPY800~8,000",
    "reason": "Klook 스타일 가이드에 따라 금액 범위는 하이픈(-)이 아닌 물결표(~)를 사용해야 함."
  }},
  {{
    "error_type": "STYLE GUIDE ISSUE",
    "impact_type": "Minor",
    "source": "Klook",
    "target": "클룩",
    "offer": "Klook",
    "reason": "Klook 브랜드명은 한글 '클룩'이 아닌 영문 'Klook'을 사용해야 함."
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
