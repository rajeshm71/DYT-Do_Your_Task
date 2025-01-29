# agents/summarize_agent.py

from .agent_base import AgentBase

class SummarizeTool(AgentBase):
    def __init__(self, max_retries=3, verbose=True):
        super().__init__(name="SummarizeTool", max_retries=max_retries, verbose=verbose)
        self.length_options = {
            "Short": "3-5 bullet points",
            "Medium": "2-3 concise paragraphs",
            "Detailed": "comprehensive summary preserving key details"
        }
        self.technical_levels = {
            "Patient-Friendly": "non-medical language for general audience",
            "Clinical": "standard medical terminology for healthcare professionals",
            "Research": "technical language including biochemical terms and study references"
        }

    def execute(self, text, length="Medium", technical_level="Clinical"):
        system_prompt = f"""You are a medical summarization expert. Create summaries that are:
        - Length: {self.length_options[length]}
        - Technical level: {self.technical_levels[technical_level]}
        - Always preserve critical medical information
        - Highlight diagnoses, treatments, and outcomes
        - Maintain original context and meaning"""

        user_prompt = f"""Original medical text:
        {text}

        Create a summary that:
        1. Extracts key clinical information
        2. Structures findings logically
        3. Uses {technical_level} terminology
        4. Maintains {length.lower()} format
        5. Preserves all numerical values and measurements"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        summary = self.call_openai(
            messages,
            max_tokens=400 if length == "Detailed" else 300,
            temperature=0.2  # For more factual responses
        )
        return summary