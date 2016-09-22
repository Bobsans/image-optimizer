image_optimizer v0.2.2
======================================

Оптимизатор изображений на базе PIL.

Установка
--------------------------------------
```bash
pip install image_optimizer
```

Использование
--------------------------------------
- Оптимизация отдельных файлов:
```bash
> image_optimizer -f C:\image.jpg
> image_optimizer -f C:\image.jpg C:\image2.png ...
```
- Оптимизация файлов в директории:
```bash
> image_optimizer -d C:\images
> image_optimizer -d C:\images --sub
```

Поддерживаемые типы файлов
--------------------------------------
BMP, EPS, GIF, J2C, J2K, JP2, JPC, JPE, JPEG, JPF, JPG, JPX, MPO, PBM, PCX, PGM, PNG, PPM, TGA

Ссылки
--------------------------------------
- [PyPi](https://pypi.python.org/pypi/image_optimizer)
