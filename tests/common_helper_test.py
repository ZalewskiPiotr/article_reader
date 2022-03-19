"""
Moduł zawiera testy jednostkowe funkcji znajdujących się w module common_helper.py

Klasy:
- brak

Funkcje:
- test_remove_characters - Sprawdzenie usunięcia znaków specjalnych
- test_complete_link - Sprawdzenie skompletowania linku do strony WEB

Wyjątki (exceptions):
- brak

Inne obiekty:
- brak
"""
import article_reader.common_helper as ch


def test_complete_link():
    """ Sprawdzenie skompletowania linku do strony WEB

    Test sprawdza czy funkcja prawidłowo połączyła dwie osobne części linku do strony WEB
    """
    prefix = "https://www2.deloitte.com"
    part_link = "/page_example_index.html"

    result_link = ch.complete_link(part_link)

    assert result_link == prefix + part_link


def test_remove_characters():
    """ Sprawdzenie usunięcia znaków specjalnych

    Test sprawdza, czy z podanego ciągu znaków zostały usunięte znaki specjalne oraz białe spacje.
    """
    src_string = "Something \xa0 is in our garden "

    result_string = ch.remove_characters(src_string)

    assert result_string.find("\xa0") == -1
    assert len(result_string) == len(result_string.strip())
