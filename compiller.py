"""
Модуль, отвечающий за преобразование обычного текста в форматированный.
"""

import markdown2


def precompile(text: str) -> str:
    markdowner = markdown2.Markdown(extras=['numbering',
                                            'code-friendly',
                                            'fenced-code-blocks',
                                            'tables',
                                            'strike'])
    result = markdowner.convert(text)
    return result


def assemble(head: str, body_content: str) -> str:
    return f"<html>{head}<body>{body_content}</body></html>"
