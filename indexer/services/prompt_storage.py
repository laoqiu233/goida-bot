class PromptStorage:
    # Ideas:
    # - versioning prompts
    # - get prompts for external source
    # - different prompts based on models

    eng_summarize = (
        "Summarize this articlce using the words from the original text. "
        "The summary should be written in in Russian, using the words "
        "using the words from the original article and use no more "
        "than 2 to 3 sentences."
    )
    eng_full_text = (
        "Extract the original text of the article UNCHANGED. "
        "You should ignore all the headlines and ads that "
        "are not relevant to the main article. The article you "
        "should extract is called %s"
    )

    ru_summarize = (
        "Выведи краткое описание данной новостной статьи. Придерживайся "
        "к словам и темам, использованные в изначальной статье. "
        "Используй не более 2 или 3 предложения."
    )
    ru_full_text = (
        "Выдели только полный и неизмененный текст новостной статьи "
        "на это странице. Отформатируй абзацы. "
        "Необходимо игонрировать все остальные элементы страницы, которые "
        "не относятся к основной статье. Статью которую ты должен выделить "
        "называется %s"
    )

    def summarize_prompt(self) -> str:
        return self.ru_summarize

    def full_text_prompt(self, title: str) -> str:
        return self.ru_full_text % (title)
