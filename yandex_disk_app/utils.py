import requests
from django.http import HttpResponse
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


def extract_file_path_from_public_key(public_key):
    """
    Извлекает публичный ключ из публичной ссылки на Яндекс.Диск.

    Args:
        public_key (str): Публичная ссылка на файл или папку в Яндекс.Диске.

    Returns:
        str: Публичный ключ, если ссылка валидна, иначе None.
    """
    parsed_url = urlparse(public_key)
    if parsed_url.netloc == "yadi.sk" and parsed_url.path.startswith("/d/"):
        path_parts = parsed_url.path.split("/")
        public_key = path_parts[2] if len(path_parts) > 2 else None
        return public_key
    return None


def get_files_from_public_link(public_key):
    """
    Получает список файлов и папок из публичной ссылки на Яндекс.Диск.

    Args:
        public_key (str): Публичная ссылка на файл или папку в Яндекс.Диске.

    Returns:
        list: Список словарей, где каждый словарь содержит информацию о файле/папке
              (name, path, type).

    Raises:
        Exception: В случае ошибок при взаимодействии с API Яндекс.Диска.
    """
    public_key = extract_file_path_from_public_key(public_key)
    if not public_key:
        raise ValueError("Invalid public link format")

    url = (
        f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        files = []

        if "items" in data:
            for item in data["items"]:
                files.append(
                    {
                        "name": item["name"],
                        "path": item["path"],
                        "type": item["type"],
                    }
                )
        return files
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        raise Exception("Ошибка при подключении к API Яндекс.Диска.")
    except ValueError as e:
        logger.error(f"Ошибка при обработке ответа API: {e}")
        raise Exception("Ошибка при обработке ответа API Яндекс.Диска.")
    except Exception as e:
        logger.exception("Неизвестная ошибка при получении списка файлов.")
        raise Exception("Неизвестная ошибка при получении списка файлов.")


def download_file(file_path):
    """
    Скачивает файл с Яндекс.Диска по указанному пути.

    Args:
        file_path (str): Путь к файлу на Яндекс.Диске.

    Returns:
        HttpResponse: HTTP-ответ с содержимым файла для скачивания.

    Raises:
        Exception: В случае ошибок при взаимодействии с API Яндекс.Диска.
    """
    url = f"https://cloud-api.yandex.net/v1/disk/resources/download?path={file_path}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        download_url_data = response.json()
        download_url = download_url_data.get("href")

        if download_url:
            download_response = requests.get(download_url, stream=True)
            download_response.raise_for_status()

            filename = file_path.split("/")[-1]
            response = HttpResponse(
                download_response.iter_content(chunk_size=8192),
                content_type=download_response.headers["Content-Type"],
            )
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
        else:
            raise Exception("Не удалось получить ссылку для скачивания файла.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе на скачивание: {e}")
        raise Exception("Ошибка при подключении к API Яндекс.Диска.")
    except ValueError as e:
        logger.error(f"Ошибка при обработке ответа API: {e}")
        raise Exception("Ошибка при обработке ответа API Яндекс.Диска.")
    except Exception as e:
        logger.exception("Неизвестная ошибка при скачивании файла.")
        raise Exception("Неизвестная ошибка при скачивании файла.")
