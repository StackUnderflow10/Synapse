class LLMService:

    def generate(self, system_prompt, user_prompt):

        """
        Provider-specific implementation will go here.

        Possible implementations:
        - Ollama
        - Hugging Face Inference
        - API-based LLM
        """

        raise NotImplementedError(
            "Configure your LLM provider first."
        )