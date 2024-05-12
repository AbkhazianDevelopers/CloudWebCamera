# CloudWebCamera
Автоматическое создание архива, всех камер для apsny.camera. 

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

После завершения работы, установщик должен вывести "Установка завершена.", теперь CloudWebCamera работает под сервисом cloudwebcamera

Путь к файлу с логами: `data/logs/(дата).log


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