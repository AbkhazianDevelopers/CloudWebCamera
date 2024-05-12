# CloudWebCamera

CloudWebCamera - это инструмент, разработанный для автоматического архивирования всех timelapse-видео с камер провайдера ООО "Система", доступных на их сайте apsny.camera. Этот проект обеспечивает удобный способ сохранения и хранения timelapse-видео для последующего просмотра или анализа. 

## Установка скрипта

Для начала, требуется клонировать репозиторий с помощью `git clone`:

```
git clone https://github.com/reques6e/CloudWebCamera.git
cd CloudWebCamera
```

Дальше, требуется выдать права установщику и запустить его:

```
chmod +x install.bash
./install.bash
```

После завершения работы, установщик должен вывести "Установка завершена.", теперь CloudWebCamera работает под сервисом `cloudwebcamera`

Путь к файлу с логами: `data/logs/(дата).log`


## Архитектура:

```
data/
│
├─── archive/
│    ├─── Suhum/
│    ├─── ├─── sukhum_ardzinba_leona/
│    ├─── ├─── ├───2024-05-12.mp4
│    ├─── ├─── ...
│    └─── ...
├─── logs/
│    ├─── 2024-05-12.log
│    ├─── ...
├─── requests.py
│install.bash
│LICENSE
│main.py
│README.md
│requirements.txt
```
