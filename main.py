import asyncio
import os
import aiohttp
import schedule
import time
import boto3
import ntplib

from datetime import datetime, timedelta
from transliterate import translit
from data.requests import get_locations, get_camera, get_timelapse
from loguru import logger
from config import Config

def get_ntp_time():
    c = ntplib.NTPClient()
    response = c.request('pool.ntp.org')
    return datetime.utcfromtimestamp(response.tx_time)

def get_system_time():
    return datetime.utcnow()

def check_time_difference():
    ntp_time = get_ntp_time()
    system_time = get_system_time()
    difference = abs((ntp_time - system_time).total_seconds())

    if difference > 300:  # 300 секунд это 5 минут
        logger.error(f"Разница между системным временем ({system_time}) и NTP временем ({ntp_time}) больше пяти минут. Пожалуйста, исправьте системное время.")
        exit(1)

def get_date():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def start_logging():
    logger.add(f"data/logs/{get_date()}.log", rotation="00:00", retention="7 days", level="INFO")

check_time_difference()

start_logging()

s3_client = boto3.client(
    's3',
    endpoint_url=Config.endpoint_url,
    aws_access_key_id=Config.aws_access_key_id,
    aws_secret_access_key=Config.aws_secret_access_key,
    region_name=Config.region_name
)

async def start():
    logger.info(f"Запуск от {get_date()}")

    locations_data = await get_locations()
    if locations_data:
        for location in locations_data.get('response', []):
            location_id = location["location_id"]
            location_name = location["location_name"]
            location_name_latin = translit(location_name, 'ru', reversed=True)

            cameras = await get_camera(location_id)
            for camera in cameras['response'].get('cams', []):
                channel = camera['channel']

                timelapses = await get_timelapse(channel)
                if isinstance(timelapses, dict) and 'response' in timelapses:
                    timelapse_link = timelapses['response'].get('link')
                    if timelapse_link:
                        date_str = get_date()

                        async with aiohttp.ClientSession() as session:
                            async with session.get(timelapse_link) as response:
                                if response.status == 200:
                                    s3_key = f"archive/{location_name_latin}/{channel}/{date_str}.mp4"
                                    content = await response.read()
                                    s3_client.put_object(Bucket=Config.bucket_name, Key=s3_key, Body=content)
                                    
                                    logger.info(f"Записи с камеры {channel} за {date_str} успешно архивированы в S3")
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
