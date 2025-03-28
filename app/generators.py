from openai import AsyncOpenAI
from config import ORTOKEN

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=ORTOKEN
)

async def ai_generate(text: str):
    completion = await client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            # {
            #     "role": "system",
            #     "content": '',
            # },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    print(completion)
    return completion.choices[0].message.content