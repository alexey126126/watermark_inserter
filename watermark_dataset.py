import os
from torch.utils.data import Dataset
from PIL import Image


class WatermarkDataset(Dataset):
    def __init__(self, dataset_dir, transform=None):
        # Путь к подкаталогам
        self.with_watermark_dir = os.path.join(dataset_dir, 'with_watermark/cropped')
        self.without_watermark_dir = os.path.join(dataset_dir, 'without_watermark/cropped/')

        # Получаем имена файлов изображений
        self.with_watermark_files = [f for f in os.listdir(self.with_watermark_dir)]
        self.without_watermark_files = [f for f in os.listdir(self.without_watermark_dir)]

        # Убедимся, что количество файлов совпадает
        assert len(self.with_watermark_files) == len(self.without_watermark_files), \
            "Количество изображений с водяным знаком и без них должно быть одинаковым"

        # Проверяем, что имена файлов соответствуют друг другу
        self.with_watermark_files.sort()
        self.without_watermark_files.sort()

        for with_w, without_w in zip(self.with_watermark_files, self.without_watermark_files):
            assert with_w == without_w, \
                f"Имена файлов не совпадают: {with_w} и {without_w}"

        self.transform = transform

    def __len__(self):
        # Возвращаем количество изображений
        return len(self.with_watermark_files)

    def __getitem__(self, idx):
        # Загружаем изображение с водяным знаком
        with_watermark_path = os.path.join(self.with_watermark_dir, self.with_watermark_files[idx])
        with_watermark = Image.open(with_watermark_path)

        # Загружаем оригинальное изображение (без водяного знака)
        without_watermark_path = os.path.join(self.without_watermark_dir, self.without_watermark_files[idx])
        without_watermark = Image.open(without_watermark_path)

        if self.transform:
            with_watermark = self.transform(with_watermark)
            without_watermark = self.transform(without_watermark)

        # Возвращаем оба изображения как кортеж
        return with_watermark, without_watermark
