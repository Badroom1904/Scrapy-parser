import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class PepParsePipeline:
    """Pipeline для подсчёта статусов PEP и сохранения сводки в CSV."""

    def __init__(self):
        """Инициализация без структур данных."""
        self.status_count = None
        self.results_dir = None

    def open_spider(self, spider):
        """Инициализация структур и создание папки для результатов."""
        spider.logger.info('Pipeline открыт. Начинаем сбор статусов PEP.')

        self.status_count = defaultdict(int)

        feeds = spider.crawler.settings.get('FEEDS')
        if feeds:
            feed_path = list(feeds.keys())[0]
            self.results_dir = Path(feed_path).parent
        else:
            self.results_dir = Path('results')

        self.results_dir.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        """Подсчёт статусов PEP."""
        status = item.get('status')
        if status:
            self.status_count[status] += 1
        return item

    def close_spider(self, spider):
        """Сохранение сводки по статусам после завершения паука."""
        if self.results_dir is None:
            self.results_dir = Path('results')
            self.results_dir.mkdir(exist_ok=True)

        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{now}.csv'
        file_path = self.results_dir / file_name

        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            for status, count in sorted(self.status_count.items()):
                writer.writerow([status, count])
            total = sum(self.status_count.values())
            writer.writerow(['Total', total])

        spider.logger.info(f'Сводка сохранена в {file_path}')
