import requests
import json

# run `python -m vllm.entrypoints.openai.api_server   --model openai/gpt-oss-20b   --tensor-parallel-size 4   --host 0.0.0.0   --port 8080`


def qwen3_api(
    user_prompt: str,
    system_prompt: str = "",
) -> str:
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "user", "content": user_prompt},
        ],
        # "max_tokens": 1024,
        "chat_template_kwargs": {"enable_thinking": False},
        "seed": 42,
    }

    if system_prompt:
        payload["messages"].insert(0, {"role": "system", "content": system_prompt})

    response = None
    try:
        response = requests.post(
            "http://klook.hufs.jae.one:8080/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=300,
        )

        response_data = response.json()
        return (
            response_data["choices"][0]["message"]["content"]
            .replace("```json", "")
            .replace("```", "")
            .replace("\\n", "\n")
            .replace("\n", " ")
            .strip()
        )

    except requests.exceptions.RequestException as e:
        return response.text if response else str(e)


if __name__ == "__main__":
    system_prompt = "You are a helpful assistant."
    user_prompt = "who are you?"

    response = qwen3_api(user_prompt=user_prompt, system_prompt=system_prompt)
    print(response)
