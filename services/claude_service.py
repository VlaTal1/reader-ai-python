import os

import anthropic

client = anthropic.Anthropic()


def claude_generate_answer(prompt: str):
    response = client.messages.create(
        model=os.getenv("MODEL_NAME", "claude-3-5-sonnet-20241022"),
        max_tokens=2000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    return response
