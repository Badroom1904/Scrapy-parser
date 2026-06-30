from datetime import datetime
from pathlib import Path


class PepParsePipeline:
    """Pipeline для подсчёта статусов PEP и сохранения сводки в CSV."""

    def __init__(self):
        self.status_count = {}

    @classmethod
    def from_crawler(cls, crawler):
        """Инициализация с доступом к настройкам."""
        pipeline = cls()
        pipeline.crawler = crawler
        return pipeline

    def open_spider(self, spider):
        """Действия при открытии паука."""
        spider.logger.info('Pipeline открыт. Начинаем сбор статусов PEP.')

    def process_item(self, item, spider):
        """Подсчёт статусов PEP."""
        status = item.get('status')
        if status:
            self.status_count[status] = self.status_count.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        """Сохранение сводки по статусам после завершения паука."""
        feeds = spider.crawler.settings.get('FEEDS')
        if feeds:
            feed_path = list(feeds.keys())[0]
            results_dir = Path(feed_path).parent
        else:
            results_dir = Path('results')

        results_dir.mkdir(exist_ok=True)

        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{now}.csv'
        file_path = results_dir / file_name

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status, count in sorted(self.status_count.items()):
                f.write(f'{status},{count}\n')
            total = sum(self.status_count.values())
            f.write(f'Total,{total}\n')

        spider.logger.info(f'Сводка сохранена в {file_path}')
