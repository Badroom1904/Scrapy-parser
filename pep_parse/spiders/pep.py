import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Собирает ссылки на все PEP."""
        # Находим все таблицы с PEP
        tables = response.css('table.pep-zero-table')
        for table in tables:
            # В каждой таблице пропускаем заголовок и берём строки
            rows = table.css('tr')[1:]  # Пропускаем заголовок
            for row in rows:
                # Ссылка на PEP находится во второй колонке (индекс 1)
                link = row.css('td a::attr(href)').get()
                if link:
                    # Переходим на страницу PEP
                    yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсит страницу PEP и извлекает номер, название и статус."""
        # Извлекаем номер PEP из заголовка
        title = response.css('h1.page-title::text').get()
        if title:
            # Извлекаем номер из заголовка (например, "PEP 8 – Style Guide...")
            number = title.split()[1] if len(title.split()) > 1 else ''
        else:
            number = ''

        # Извлекаем название
        # Второй вариант, если заголовок не подходит
        if not number:
            # Пробуем найти номер в другом месте
            pep_tag = response.css('dt:contains("PEP") + dd::text').get()
            if pep_tag:
                number = pep_tag.strip()

        # Извлекаем название PEP
        name = response.css('h1.page-title::text').get()
        if name:
            # Убираем "PEP X – " из названия
            if ' – ' in name:
                name = name.split(' – ', 1)[1]
            else:
                name = name.strip()

        # Извлекаем статус
        status = response.css('dt:contains("Status") + dd abbr::text').get()
        if not status:
            # Если abbr нет, берём просто текст
            status = response.css('dt:contains("Status") + dd::text').get()
        if status:
            status = status.strip()

        # Возвращаем Item с данными
        yield PepParseItem(
            number=number,
            name=name,
            status=status,
        )
