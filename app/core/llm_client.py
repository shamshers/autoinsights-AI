# app/llm/claude_api.py

import anthropic
import os

from dotenv import load_dotenv
load_dotenv()


# main.py
from fastapi.middleware.cors import CORSMiddleware


# app/llm/claude_api.py
class ClaudeClient:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("❌ Claude API key is missing. Set ANTHROPIC_API_KEY.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
        print(f"[ClaudeClient] Model: {self.model}")


    def generate(self, prompt, max_tokens=800, temperature=0.3):
        try:
            print(f"[ClaudeClient] Sending prompt (first 200 chars):\n{prompt[:200]}...\n")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text.strip() if response.content else None
            print(f"[ClaudeClient] Response: {content}")
            return content or "⚠️ No response received from Claude."
        except Exception as e:
            error_message = f"Claude API Error: {str(e)}"
            print(f"[ClaudeClient] {error_message}")
            return error_message
