# app/services/gpt.py
import openai
from config.settings.base import settings

openai.api_key = settings.OPENAI_API_KEY


def generate_text(prompt):

    # model = "davinci"
    model = "text-davinci-003"
    completions = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text.strip()
    return message
