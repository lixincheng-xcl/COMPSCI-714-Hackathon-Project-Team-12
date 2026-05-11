import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main():
    api_key = get_required_env("AZURE_OPENAI_API_KEY")
    base_url = get_required_env("AZURE_OPENAI_BASE_URL")
    deployment = get_required_env("AZURE_OPENAI_DEPLOYMENT")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    prompt = (
        "Reply with exactly this sentence: "
        "Azure connection OK for Research Contract Adviser Agent."
    )

    try:
        response = client.responses.create(
            model=deployment,
            input=prompt,
        )

        output_text = getattr(response, "output_text", None)

        if not output_text:
            output_text = str(response)

        print("Azure connection succeeded.")
        print("Deployment:", deployment)
        print("Response:")
        print(output_text)

    except Exception as responses_error:
        print("Responses API failed. Trying chat completions fallback...")
        print("Responses API error:", responses_error)

        try:
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a concise assistant.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            print("Azure chat completion succeeded.")
            print("Deployment:", deployment)
            print("Response:")
            print(response.choices[0].message.content)

        except Exception as chat_error:
            print("Azure connection failed.")
            print("Chat completions error:", chat_error)
            sys.exit(1)


if __name__ == "__main__":
    main()