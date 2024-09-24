class PromptStorage:
    # Ideas:
    # - versioning prompts
    # - get prompts for external source
    # - different prompts based on models

    def summarize_prompt(self) -> str:
        return (
            "Summarize this articlce using the words from the original text. "
            "The summary should be written in in Russian, using the words "
            "using the words from the original article and use no more "
            "than 2 to 3 sentences."
        )

    def full_text_prompt(self, title: str) -> str:
        return (
            "Extract the original text of the article UNCHANGED. "
            "You should ignore all the headlines and ads that "
            "are not relevant to the main article. The article you "
            "should extract is called {title}"
        )
