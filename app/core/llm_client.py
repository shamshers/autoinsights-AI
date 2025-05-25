import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient:
    def __init__(self):
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            raise RuntimeError("CLAUDE_API_KEY not set in environment or .env file")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-opus-20240229"  # Or "claude-3-sonnet-20240229"

    def generate_summary(self, data_stats, columns, business_question=None,rag_context=None):
        prompt = (
            f"You are a business data analyst AI.\n"
            f"Columns: {columns}\n"
            f"Summary statistics: {data_stats}\n"
        )
        if business_question:
            prompt += f"Business question: {business_question}\n"
        prompt += "Provide a concise, business-friendly summary of insights and patterns."
        if rag_context:
            prompt += f"\nRelevant enterprise context:\n{rag_context}\n"
        prompt += "Provide a concise, business-friendly summary of insights and patterns."

        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Claude v3: response.content is a list of message blocks
        return response.content[0].text.strip()
