"""
Модуль, отвечающий за преобразование обычного текста в форматированный.
"""

import markdown2


def precompile(text: str) -> str:
    """
    Возвращает преобразованный html-текст, преобразованный при помощи правил markdown.
    :param text: Текст, который требуется преобразовать.
    """
    markdowner = markdown2.Markdown(extras=['numbering',
                                            'code-friendly',
                                            'fenced-code-blocks',
                                            'tables',
                                            'strike'])
    result = markdowner.convert(text)
    return result


def assemble(head: str, body_content: str) -> str:
    """
    Собирает html-текст и заголовок в html-файл.
    :param head: Заголовок файла.
    :param body_content: html-текст.
    """
    return f"<html>{head}<body>{body_content}</body></html>"
