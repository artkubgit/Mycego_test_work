from django.shortcuts import render, redirect
from .forms import PublicLinkForm
from .utils import get_files_from_public_link, download_file
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


def file_list(request):
    """
    Отображает список файлов и папок из публичной ссылки на Яндекс.Диск.

    Args:
        request (HttpRequest): Объект HTTP-запроса.

    Returns:
        HttpResponse: HTTP-ответ с отображением шаблона file_list.html.
    """
    files = []
    error_message = None
    if request.method == "POST":
        form = PublicLinkForm(request.POST)
        if form.is_valid():
            public_key = form.cleaned_data["public_key"]
            try:
                files = get_files_from_public_link(public_key)
            except Exception as e:
                error_message = str(e)
                logger.error(f"Ошибка в file_list view: {e}")
        else:
            logger.warning("Некорректная форма")
            error_message = (
                "Некорректная ссылка. Пожалуйста, проверьте введенные данные."
            )
    else:
        form = PublicLinkForm()

    return render(
        request,
        "file_list.html",
        {"form": form, "files": files, "error_message": error_message},
    )


def download_view(request, file_path):
    """
    Предоставляет файл для скачивания с Яндекс.Диска.

    Args:
        request (HttpRequest): Объект HTTP-запроса.
        file_path (str): Путь к файлу на Яндекс.Диске.

    Returns:
        HttpResponse: HTTP-ответ с файлом для скачивания.
    """
    try:
        response = download_file(file_path)
        return response
    except Exception as e:
        logger.error(f"Ошибка при скачивании файла: {e}")
        return HttpResponse(f"Ошибка при скачивании файла: {e}")
