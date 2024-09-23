# GOIDA-BOT
## News aggregator with GPT

Project for "Wireless networks" discipline.

## TODOs
- [x] Скачиваем новости из нескольких заданных RSS источников
- [x] Конвертируем скачанные html в pdf
- [x] Передаем pdf на вход LLM (GPT4All)
- [x] Задать промпт, например "Какие сегодня есть события (новости) упоминающие о ФИО" (спортсмен, политик, киноактер и т.п.)
Или просим "Выведи полный текст новостей о ФИО" (чтобы не пересказ а оригинальный текст новости был)
- [x] Автоматизировать предыдущие пункты
- [ ] Индексировать и использовать в поисках full_text и summary вместо изначальной PDF
- [x] Занести векторное хранилище в постгрес
- [ ] Название статьей хранить в БД
- [ ] Время публикации протянуть в БД
- [ ] Подумать про подписки на поиски
- [ ] Улучшить результат с помощью различных моделей (Mistral, Deepseek, Snoozy), подпираем формулировку запроса новостей
- [ ] Доработать документацию по запуску