import tkinter as tk
from tkinter import filedialog, messagebox
import torch
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from torchvision.transforms import transforms

from utils import split_into_blocks, find_block_with_max_color_change, embed_watermark


# Класс приложения на tkinter
class WatermarkApp(tk.Tk):
    def __init__(self, model):
        super().__init__()
        self.title("Watermark App")

        # Компоненты интерфейса
        self.load_button = tk.Button(self, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack(pady=10)

        self.watermark_entry = tk.Entry(self)
        self.watermark_entry.insert(0, "WATERMARK")
        self.watermark_entry.pack(pady=10)

        self.embed_button = tk.Button(self, text="Встроить водяной знак", command=self.embed_watermark)
        self.embed_button.pack(pady=10)

        self.remove_button = tk.Button(self, text="Удалить водяной знак", command=self.remove_watermark)
        self.remove_button.pack(pady=10)

        self.image_path = None
        self.model = model
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor()  # Преобразуем изображение в тензор
        ])

    # Функция загрузки изображения
    def load_image(self):
        self.image_path = filedialog.askopenfilename(title="Выберите изображение",
                                                     filetypes=[("Изображения", "*.png")])
        if not self.image_path:
            messagebox.showwarning("Предупреждение", "Изображение не загружено")

    # Функция встраивания водяного знака
    def embed_watermark(self):
        if self.image_path:
            watermark_text = self.watermark_entry.get()
            image = Image.open(self.image_path)
            block_size = 100
            blocks = split_into_blocks(image, block_size)
            block_position = find_block_with_max_color_change(blocks)

            if block_position is not None:
                output_image_path = "dataset/with_watermark/image_1.png"
                embed_watermark(self.image_path, output_image_path, watermark_text, block_position, block_size)
                messagebox.showinfo("Успех", "Водяной знак встроен")
            else:
                messagebox.showerror("Ошибка", "Не удалось найти блок с наибольшим изменением")
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, загрузите изображение")

    # Функция для удаления водяного знака
    def remove_watermark(self):
        if self.image_path:
            image = Image.open(self.image_path)  # Загружаем изображение
            image_tensor = self.transform(image).unsqueeze(0)  # Преобразуем в тензор с добавлением батча

            # Используем обученную модель для удаления водяного знака
            output_tensor = self.model(image_tensor)
            output_image = transforms.ToPILImage()(output_tensor.squeeze(0))  # Преобразуем обратно в PIL

            output_image_path = "image_without_watermark.ppg"
            output_image.save(output_image_path)

            messagebox.showinfo("Успех", f"Водяной знак удален. Изображение сохранено как '{output_image_path}'")
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, загрузите изображение")
