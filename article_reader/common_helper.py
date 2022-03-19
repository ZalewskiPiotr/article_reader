"""
Moduł zawiera różne funkcje do realizacji różnych, wspólnych działań wykorzystywanych w wielu miejscach.

Klasy:
- brak klas

Funkcje:
- complete_link - Uzupełnienie linku do artykułu
- remove_characters - Usuwanie zbędnych znaków z tekstu

Wyjątki (exceptions):
- brak

Inne obiekty:
- brak
"""


def complete_link(link):
    """ Uzupełnienie linku do artykułu.

    Funkcja kompletuje podany link względny do artykułu. Dodaje do niego przedrostek z adresem strony
    'https://www2.deloitte.com'.

    :param link: Względny link do artykułu
    :type link: str
    :return: Pełny link do artykułu
    :rtype: str
    """
    return "https://www2.deloitte.com" + link


def remove_characters(string: str) -> str:
    """ Usuwanie zbędnych znaków z tekstu

    Funkcja usuwa znak u'\xa0' (No-Break Space - &nbsp) oraz białe znaki z podanego ciągu znaków.

    :param string: Ciąg znaków, z którego usuwane są znaki
    :type string: str
    :return: Ciąg znaków po usunięciu wskazanych znaków
    :rtype: str
    """
    string = string.strip()
    return string.replace(u'\xa0', ' ')
