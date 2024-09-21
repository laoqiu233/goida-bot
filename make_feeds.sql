TRUNCATE feeds;
INSERT INTO feeds(id, token, feed_name, slug, main_url, feed_url, is_active) VALUES 
(gen_random_uuid(), 0, 'Лента.ру', 'lenta', 'https://lenta.ru/', 'https://lenta.ru/rss', true);