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
2.  **CRITICAL RULE: NO ERROR = EMPTY ARRAY:** If the translation is perfect and has no errors, you **MUST** return an empty array `[]`.
    * **ABSOLUTE PROHIBITION:** **절대** "이것은 오류가 아닙니다" 또는 "오류 없음"과 같은 내용을 `reason` 필드에 담은 JSON 객체를 생성하지 마십시오. 오류가 없으면 오직 `[]`만 반환해야 합니다.
3.  **Identify All Errors:** You must identify every single error in the translation, *except* for issues explicitly defined in `RULE 1` (Formatting Exclusion).
4.  **JSON Object Fields (CRITICAL FORMAT):** Each error object in the array **must** contain exactly these six fields:
    * `"error_type"`: The error classification.
    * `"impact_type"`: The impact classification (severity from customer perspective).
    * `"source"`: **The full source sentence** containing the error. The specific error fragment **must** be highlighted with double asterisks (`**error**`).
    * `"target"`: **The full translated sentence** corresponding to the source. The specific incorrect fragment **must** be highlighted with double asterisks (`**오류**`).
    * `"offer"`: The corrected Korean **fragment only**. (e.g., "짧은 이동 시간"). **Do NOT** provide the full sentence or asterisks here.
    * `"reason"`: A brief, professional explanation in **100% Korean** of *why* it is an error. (e.g., "직역이라 어색함", "문맥에 맞지 않음", "원문 병기 누락").
5.  **Language Rule:** The `reason` field must be 100% Korean. No English.
6.  **Context & Highlighting Rule (CRITICAL):**
    * The `source` and `target` fields **must** contain the *entire sentence* where the error occurred to provide context.
    * If the input is just a title (e.g., "How to book"), then that entire phrase is the "sentence".
    * The `offer` field *must* contain *only* the corrected text **fragment**, *without* asterisks or the full sentence.

**Critical Evaluation Rules (MUST FOLLOW):**

1.  **FORMATTING EXCLUSION RULE (CRITICAL):**
    * **Do NOT** report any errors related to:
        * Line breaks (`\n`)
        * Missing/extra spacing
        * Words stuck together (e.g., `...신칸센,아름다운...`)
        * Repetitions that are clearly crawling/formatting errors (e.g., `베이징-상하이베이징-상하이 노선...`)
    * These issues **MUST BE IGNORED**. Focus *only* on semantic and stylistic translation quality.

2.  **Key Variable Context (title/contents):**
    * If the 'key' variable is **`title`**: Titles are short. Brevity, accuracy, and impact are most important.
    * If the 'key' variable is **`contents`**:
        * **CONTEXTUAL FLOW (CRITICAL):** When evaluating segments, *always* check their grammatical role in the full sentence. Do **NOT** flag correct conjunctive endings (e.g., `...예약하고`, `...하며`) as errors.
        * **CONTEXTUAL OVERREACH (PROHIBITED):** The `{item_type}` variable provides context, but it **must not** be used to 'correct' a translation (e.g., changing "Trains" to "High-Speed Trains") if the translation is a *faithful* and *literal* match to the source text.

3.  **Klook 스타일 가이드: 통화, 숫자, 시간 (Strict)**
    * **Currency (Digits):** '150 yen' 등 숫자가 포함된 금액은 **반드시 `JPY150` 형식**이어야 합니다. (`150엔`, `JPY 150` 등은 모두 오류입니다.)
    * **Currency (Words):** 'a few hundred yen' 등 단어로 된 금액은 **반드시 `수백 엔` 등 한글 단어**로 번역해야 합니다.
    * **Time:** **반드시 24시간 표기법**을 사용해야 합니다 (e.g., `08:00`). `AM/PM` 또는 `오전/오후` 표기는 금지됩니다.
    * **Age:** 'ages 0-3' 등 연령대는 **반드시 `만 0-3세` 형식**으로 번역해야 합니다.
    * **Ranges:** 시간 및 숫자 범위는 **반드시 물결표(`~`)**를 사용해야 합니다 (e.g., `4.5~6시간`).

4.  **Klook 스타일 가이드: 고유명사 및 톤 (Strict)**
    * **Parenthetical English (CRITICAL):**
        * 주요 명소, 서비스명, 지명 등은 **반드시 `한글명(English Name)` 형식**을 사용해야 합니다. (e.g., `자금성(The Forbidden City)`).
        * **CLARIFICATION:** 이 규칙은 원문 병기를 '추가'하는 것입니다. 만약 소스에 `(HSR)`처럼 이미 약어 괄호가 있다면, 타겟도 `(HSR)`을 그대로 따르는 것이 올바르며, 이를 `(China High Speed Rail)`로 "수정"하려 해서는 안 됩니다.
    * **Brand Names:** 'Hilton', 'Universal Studios' 등 글로벌 브랜드명, 호텔 체인명은 번역하지 않고 **영문 그대로 유지**해야 합니다.
    * **Natural Tone (Glossary):**
        * 'fast travel times' -> **'짧은 이동 시간'** (O) / '빠른 이동 시간' (X)
        * 'Reviews' -> **'리뷰'** (O) / '이용후기' (X)

5.  **Klook 스타일 가이드: 기호, 단위,"""

            user_prompt = f"""Please evaluate the following translation based on the rules provided.

**Task Context:**
* The source item type is: **{item_type}**
* This content is used as a **{key}** in the Klook service. (e.g., 'title' or 'contents')

**Error Classifications:**
* ERROR TYPES: {ERROR_TYPE_STR}
* IMPACT TYPES: {IMPACT_TYPE_STR}

**JSON Output Format Example (NEW FORMAT):**
[
  {{
    "error_type": "MISTRANSLATION",
    "impact_type": "Major",
    "source": "**How to book**",
    "target": "**어떻게 사용나요?**",
    "offer": "예약 방법",
    "reason": "'How to book'는 예약 방법을 묻는 표현이므로, '어떻게 사용나요?'는 문맥에 맞지 않음."
  }},
  {{
    "error_type": "LOCALE CONVENTION ISSUE",
    "impact_type": "Major",
    "source": "For example, a JR Kyushu Rail Pass costs from **10,000 to 25,000 yen**.",
    "target": "JR 큐슈 레일 패스 가격은 **JPY10,000-25,000**입니다.",
    "offer": "JPY10,000~25,000",
    "reason": "Klook 스타일 가이드에 따라 '엔'이 아닌 'JPY' 접두사를 사용해야 하며, 범위는 '-' 대신 '~'를 사용해야 함."
  }},
  {{
    "error_type": "MISTRANSLATION",
    "impact_type": "Major",
    "source": "...while longer rides between cities or regions could range from **a few hundred to a couple thousand yen**.",
    "target": "...도시나 지역 사이를 이동할 경우 **요금은 JPY100-1000까지 다양합니다**.",
    "offer": "요금은 수백 엔에서 수천 엔까지 다양합니다",
    "reason": "원문의 'a few hundred'를 'JPY100'로, 'a couple thousand'를 '1000'으로 오역함. 원문이 숫자가 아니므로 '수백 엔' 등으로 번역해야 함."
  }},
  {{
    "error_type": "STYLE GUIDE ISSUE",
    "impact_type": "Minor",
    "source": "Along the way, you can explore iconic attractions like **theForbidden City** in Beijing.",
    "target": "여정을 따라 베이징의 **자금성**과 같은 상징적인 명소를 방문할 수 있습니다.",
    "offer": "자금성(The Forbidden City)",
    "reason": "주요 명소는 고객의 명확한 이해를 위해 원문(영어) 병기가 필요함."
  }},
  {{
    "error_type": "MISTRANSLATION",
    "impact_type": "Major",
    "source": "They offer **fast travel times**, fast travel times, and comfortable seating.",
    "target": "잦은 출발, **빠른 이동 시간**, 편안한 좌석을 제공하여...",
    "offer": "짧은 이동 시간",
    "reason": "직역이라 어색함. 'fast'는 이동 시간의 맥락에서 '짧은'으로 번역하는 것이 자연스러움."
  }},
  {{
    "error_type": "LOCALE CONVENTION ISSUE",
    "impact_type": "Minor",
    "source": "Source: **8:00am**",
    "target": "출처: **오전 8:00**",
    "offer": "08:00",
    "reason": "Klook 스타일 가이드는 24시간 표기법(08:00)을 요구하며, '오전' 또는 'AM' 표기는 금지됨."
  }},
  {{
    "error_type": "STYLE GUIDE ISSUE",
    "impact_type": "Minor",
    "source": "It is perfect **for ages 0-3**.",
    "target": "이것은 **0-3세 대상**으로 완벽합니다.",
    "offer": "만 0-3세 대상",
    "reason": "Klook 연령 표기 규칙에 따라 '만' 접두사가 누락됨."
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
