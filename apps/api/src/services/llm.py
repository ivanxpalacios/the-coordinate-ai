from groq import AsyncGroq

from config import settings

Message = dict[str, str]

client = AsyncGroq(api_key=settings.groq_api_key)


async def complete(messages: list[Message]) -> str:
    response = await client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
    )
    return response.choices[0].message.content
