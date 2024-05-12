import asyncio
import os
import aiohttp
import schedule
import time

from datetime import datetime, timedelta
from transliterate import translit
from data.requests import get_locations, get_camera, get_timelapse
from loguru import logger

def get_date():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def start_logging():
    logger.add(f"data/logs/{get_date()}.log", rotation="00:00", retention="7 days", level="INFO") 

start_logging()

async def start():
    logger.info(f"Запуск от {get_date()}")

    locations_data = await get_locations()
    if locations_data:
        for location in locations_data.get('response', []):
            location_id = location["location_id"]
            location_name = location["location_name"]
            location_name_latin = translit(location_name, 'ru', reversed=True)
            location_folder = f'data/archive/{location_name_latin}'

            os.makedirs(location_folder, exist_ok=True)

            os.makedirs(location_folder, exist_ok=True)

            cameras = await get_camera(location_id)
            for camera in cameras['response'].get('cams', []):
                channel = camera['channel']
                channel_folder = os.path.join(location_folder, channel)
                os.makedirs(channel_folder, exist_ok=True)

                timelapses = await get_timelapse(channel)
                if isinstance(timelapses, dict) and 'response' in timelapses:
                    timelapse_link = timelapses['response'].get('link')
                    if timelapse_link:
                        date_str = get_date()

                        async with aiohttp.ClientSession() as session:
                            async with session.get(timelapse_link) as response:
                                if response.status == 200:
                                    filename = os.path.join(channel_folder, f"{date_str}.mp4")
                                    with open(filename, 'wb') as f:
                                        f.write(await response.read())
                                    logger.info(f"Записи с камеры {channel} за {date_str} успешно архивированы")
                                else:
                                    logger.error(f"Произошла ошибка при скачивании timelaps за {date_str} с камеры {channel}, ошибка: {response.status}")
                else:
                    logger.error(f"Не смог найти timelaps с камеры {channel}")
    else:
        logger.error(f"Не удалось получить данные о локациях")

def start_and_schedule():
    asyncio.run(start())

    schedule.every().day.at("01:00").do(asyncio.run, start_and_schedule)

if __name__ == '__main__':
    start_and_schedule()
    while True:
        schedule.run_pending()
        time.sleep(1)
