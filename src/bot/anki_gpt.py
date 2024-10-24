import json

from openai import OpenAI

from bot.english import EnglishWord
from bot.settings import settings

JSON_INSTRUCTION = "You are a system that only outputs JSON."

client = OpenAI(api_key=settings.openai_api_key)


def generate(system_prompt: str, user_prompt: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return completion.choices[0].message.content


def generate_json(system_prompt: str, user_prompt: str, examples: str = "") -> dict:
    json_prompt = JSON_INSTRUCTION + system_prompt + examples
    generated_json: str = generate(json_prompt, user_prompt)
    return json.loads(generated_json)


WORD_HELPER_INSTRUCTION = """
You create a JSON object based on an English word or phrase. The JSON should include the following fields:
- 'word': the input word or phrase
- 'meaning': the dictionary meaning of the word or phrase
- 'etymology': Please explain the etymology. The response should only include this content, without any line breaks or additional text.
- 'example': Provide one example sentence using the word or phrase that a native speaker would most likely use.
- 'situation': Explain the context in which the word is used, including specific examples, without any line breaks or additional text.
"""

EXAMPLES_ENG = """
Your JSON should NOT include any keys or fields other than the ones shown in the given examples.

Examples:

User:
breathtaking

You:
{
    "word": "breathtaking",
    "meaning": "extremely exciting, beautiful, or surprising",
    "etymology": "'Breathtaking' comes from 'breathe' and 'take one's breath away,' expressing something so wonderful or impressive that it leaves one speechless.",
    "example": "The view from the top of the mountain is breathtaking.",
    "situation": "'Breathtaking' is used in contexts where something is so beautiful, grand, or surprising that it takes your breath away. For example, it can be used when viewing a stunning landscape or an emotional performance, like 'The view from the top of the mountain was breathtaking' or 'Her performance was absolutely breathtaking.'"
}

User:
take it with a grain of salt

You:
{
    "word": "take it with a grain of salt",
    "meaning": "To view something with skepticism or not to take it literally.",
    "etymology": "'Take it with a grain of salt' is believed to have originated from the idea that a small amount of salt can help make something more palatable, suggesting that one should not take things too seriously.",
    "example": "You should take his advice with a grain of salt.",
    "situation": "This phrase is used when someone suggests being cautious or skeptical about a piece of information or advice. For example, when discussing rumors or unverified claims, one might say, 'I heard he’s leaving the company, but I’d take that with a grain of salt.'"
}

User:
get the ball rolling

You:
{
    "word": "get the ball rolling",
    "meaning": "To start an activity or process.",
    "etymology": "'Get the ball rolling' likely comes from the idea of rolling a ball to initiate a game or activity, emphasizing the importance of starting something.",
    "example": "Let’s get the ball rolling on this project.",
    "situation": "This phrase is often used in professional settings to encourage the initiation of a task or discussion. For instance, someone might say in a meeting, 'We need to get the ball rolling if we want to meet the deadline.'"
}
"""


def generate_note(query: str) -> EnglishWord:
    system_prompt = WORD_HELPER_INSTRUCTION
    note_json = generate_json(system_prompt, query, EXAMPLES_ENG)
    return EnglishWord(
        word=note_json["word"],
        meaning=note_json["meaning"],
        etymology=note_json["etymology"],
        example=note_json["example"],
        situation=note_json["situation"],
    )
