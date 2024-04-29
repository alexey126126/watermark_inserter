import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision.utils import make_grid
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import WatarmarkDataset


# Определение архитектуры U-Net
class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        # Слои U-Net
        self.encoder1 = self.double_conv(3, 64)
        self.encoder2 = self.double_conv(64, 128)
        self.encoder3 = self.double_conv(128, 256)

        self.middle = self.double_conv(256, 512)

        self.decoder3 = self.up_conv(512, 256)
        self.decoder2 = self.up_conv(256, 128)
        self.decoder1 = self.up_conv(128, 64)

        self.final_conv = nn.Conv2d(64, 3, 1)  # Конечный слой, вывод 3-канальное изображение

    def double_conv(self, in_channels, out_channels):
        # Два последовательных свёрточных слоя
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.ReLU(inplace=True)
        )

    def up_conv(self, in_channels, out_channels):
        # Обратная свёртка для увеличения размера
        return nn.Sequential(
            nn.ConvTranspose2d(in_channels, out_channels, 2, stride=2),
            self.double_conv(out_channels, out_channels)
        )

    def forward(self, x):
        # Прохождение через U-Net
        e1 = self.encoder1(x)
        e2 = self.encoder2(self.max_pool(e1))
        e3 = self.encoder3(self.max_pool(e2))

        middle = self.middle(self.max_pool(e3))

        d3 = self.decoder3(middle)
        d2 = self.decoder2(d3 + e3)  # Смешиваем с энкодером
        d1 = self.decoder1(d2 + e2)

        out = self.final_conv(d1 + e1)
        return out

    def max_pool(self, x):
        return nn.MaxPool2d(2)(x)


# Инициализация модели и загрузка данных
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Путь к директории с изображениями (с водяным знаком и без)
images_dir = "dataset"

# Создание трансформаций
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

# Создание датасета и загрузчика данных
dataset = WatarmarkDataset.WatermarkDataset(images_dir, transform=transform)
data_loader = DataLoader(dataset, batch_size=16, shuffle=True)

# Инициализация модели
model = UNet().to(device)

# Оптимизатор и функция потерь
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()  # MSELoss для восстановления изображений

# Обучение модели
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for images in data_loader:
        images = images.to(device)

        # Модель пытается восстановить изображение без водяного знака
        output = model(images)

        # Считаем потери
        loss = criterion(output, images)  # Потери между оригиналом и восстановленным изображением

        # Оптимизация
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}")

# Отображение образцов
model.eval()
with torch.no_grad():
    sample_images = next(iter(data_loader))
    sample_images = sample_images.to(device)

    output_images = model(sample_images)
    output_images = output_images.cpu()  # Переместить обратно на CPU для отображения

    # Используем make_grid для отображения нескольких изображений
    grid = make_grid(output_images, nrow=4)
    plt.imshow(transforms.ToPILImage()(grid))
    plt.show()
