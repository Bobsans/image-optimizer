[![Build Status](https://travis-ci.org/Bobsans/image-optimizer.svg?branch=master)](https://travis-ci.org/Bobsans/image-optimizer)
[![Coverage Status](https://coveralls.io/repos/github/Bobsans/image-optimizer/badge.svg?branch=master)](https://coveralls.io/github/Bobsans/image-optimizer?branch=master)
[![PyPI version](https://badge.fury.io/py/image_optimizer.svg)](https://badge.fury.io/py/image_optimizer)

image_optimizer v0.3.2.dev
======================================

Оптимизатор изображений на базе PIL.


Установка
--------------------------------------
```bash
pip install image_optimizer
```


Параметры коммандной строки
--------------------------------------
```
> image_optimizer source -r -t THREADS
    source                # Файл или директория для оптимизации
    -r                    # Рекурсивный поиск изображений в поддиректориях
    -t THREADS            # Установка количества потоков
    -l                    # Отключение вывода статистики
```


Использование
--------------------------------------
```bash
# Оптимизация файла image.jpg
> image_optimizer C:\image.jpg

# Оптимизация изображений в директории images
> image_optimizer C:\images

# Оптимизация изображений в директории images и вложенных директориях
> image_optimizer C:\images -r

# Оптимизация изображений в директории images в 3 потока
> image_optimizer C:\images -t 3

# Оптимизация изображений в директории images и вложенных директориях в 4 потока
> image_optimizer C:\images -r -t 4

# Оптимизация изображений в директории images и вложенных директориях в 4 потока без вывода информации
> image_optimizer C:\images -r -t 4 -n
```


Поддерживаемые типы файлов
--------------------------------------
BMP, EPS, GIF, J2C, J2K, JP2, JPC, JPE, JPEG, JPF, JPG, JPX, MPO, PBM, PCX, PGM, PNG, PPM, TGA


Список изменений
--------------------------------------
* **v0.3.2** \[_dev_\]

    - Добавлен аргумент `-l`, отелючающий вывод статистики.

* **v0.3.1** \[_27.10.2016_\]

    - Убраны аргументы `-f` и `-d`. Теперь можно просто указать путь до файла или папки.
    - Аргумент `--sub` заменен на `-r`.
    - Исправлены некоторые баги.

* **v0.3.0** \[_23.09.2016_\]

    - Добавлена поддержка мультипоточности.
    - Улучшен вывод статистики.

* **v0.2.0** \[_19.09.2016_\]

    - Добавлены аргументы коммандной строки.
    - Добавлена поддержка нестандартных типов изображений.

* **v0.1.0** \[_17.09.2016_\]

    - Начало работы над проектом.


Ссылки
--------------------------------------
- [PyPi](https://pypi.python.org/pypi/image_optimizer)
- [GitHub](https://github.com/Bobsans/image-optimizer)
