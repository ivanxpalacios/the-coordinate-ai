from collections.abc import AsyncIterator

from groq import AsyncGroq, GroqError

from config import settings

Message = dict[str, str]

client = AsyncGroq(api_key=settings.groq_api_key)


class LlmError(Exception):
    pass


async def complete(messages: list[Message]) -> str:
    try:
        response = await client.chat.completions.create(
            model=settings.groq_model,
            messages=messages,
        )
    except GroqError as e:
        raise LlmError(str(e)) from e
    return response.choices[0].message.content


async def stream_complete(messages: list[Message]) -> AsyncIterator[str]:
    try:
        stream = await client.chat.completions.create(
            model=settings.groq_model,
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except GroqError as e:
        raise LlmError(str(e)) from e
