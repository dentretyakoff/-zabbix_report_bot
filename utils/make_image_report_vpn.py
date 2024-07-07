"""Генерирует изображение из полученных данных."""
from PIL import Image, ImageDraw, ImageFont

from configs.logs import logger
from configs.base import VPN_IMAGE


def make_image(pretty_text: dict):
    """Создает файл отчета."""
    # Вычисление количества строк и столбцов в таблице
    num_rows = len(pretty_text) + 1
    num_columns = len(next(iter(pretty_text.values()))) + 1

    # Размеры ячейки таблицы и запасы
    cell_width = 200
    cell_height = 50
    padding = 10

    # Размеры изображения
    image_width = (num_columns * cell_width) + (padding * 2)
    image_height = (num_rows * cell_height) + (padding * 2)

    # Создание изображения
    image = Image.new('RGB', (image_width, image_height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', 16)

    # Рисование заголовков
    header_color = (0, 0, 255)
    header_text_color = (255, 255, 255)
    headers = ['account'] + list(next(iter(pretty_text.values())).keys())
    for i, header in enumerate(headers):
        x = (i * cell_width) + padding
        y = padding
        draw.rectangle(
            [(x, y), (x + cell_width, y + cell_height)],
            fill=header_color
        )
        draw.text(
            (x + padding, y + padding),
            header,
            fill=header_text_color,
            font=font
        )

    # Рисование данных
    row_colors = [(240, 240, 240), (255, 255, 255)]
    for i, (key, values) in enumerate(pretty_text.items()):
        row_values = [key] + list(values.values())
        for j, value in enumerate(row_values):
            x = (j * cell_width) + padding
            y = ((i + 1) * cell_height) + padding
            color = row_colors[i % len(row_colors)]

            draw.rectangle(
                [(x, y), (x + cell_width, y + cell_height)],
                fill=color
            )
            draw.text(
                (x + padding, y + padding),
                value,
                fill=(0, 0, 0),
                font=font
            )

    # Сохранение изображения
    image.save(f'{VPN_IMAGE}')
    logger.debug('Изображение успешно сохранено.')
