class PromptStorage:
    # Ideas:
    # - versioning prompts
    # - get prompts for external source
    # - different prompts based on models

    def summarize_prompt(self) -> str:
        return """Summarize only the main content of the article in this PDF,
        ignoring all the headlines and ads that are not relevant to the main story.
        The summary should be in Russian, using the words from the original article,
        and use no more than 2 to 3 sentences"""

    def full_text_prompt(self) -> str:
        return """Output only the original text of the article UNCHANGED,
        ignoring all the headlines and ads that are not relevant to the main article."""
