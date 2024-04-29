from PIL import Image, ImageDraw, ImageFont
import numpy as np


# Функция разбивки изображения на блоки
def split_into_blocks(image, block_size):
    image_width, image_height = image.size
    blocks = []
    for y in range(0, image_height, block_size):
        for x in range(0, image_width, block_size):
            end_x = min(x + block_size, image_width)  # Граничные значения
            end_y = min(y + block_size, image_height)
            block = image.crop((x, y, end_x, end_y))
            blocks.append(((x, y), block))
    return blocks


# Функция нахождения блока с наибольшей изменчивостью цвета
def find_block_with_max_color_change(blocks):
    max_variance = 0
    target_position = None

    for position, block in blocks:
        block_np = np.array(block.convert("L"))  # Преобразуем в черно-белое
        variance = np.var(block_np)  # Измеряем дисперсию

        if variance > max_variance:
            max_variance = variance
            target_position = position

    return target_position


# Функция встраивания видимого водяного знака
def embed_watermark(input_image_path, output_image_path, watermark_text, block_position, block_size):
    image = Image.open(input_image_path).convert("RGBA")
    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    # Используем фиксированный размер шрифта
    font_path = "arial.ttf"
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)

    x, y = block_position
    position = (x + block_size // 2, y + block_size // 2)  # Центрируем текст

    draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))

    # Объединяем оригинальное изображение с водяным знаком
    watermarked_image = Image.alpha_composite(image, watermark_layer)
    watermarked_image.save(output_image_path)