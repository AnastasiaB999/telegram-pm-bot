import os
import logging
from openai import OpenAI

class OpenAIHelper:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"

    def generate_response(self, user_message, system_prompt, max_tokens=1000, temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return {
                "success": True,
                "response": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }