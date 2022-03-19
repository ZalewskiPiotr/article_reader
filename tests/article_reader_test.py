"""
Moduł zawiera testy jednostkowe funkcji znajdujących się w module common_helper.py

Klasy:
- brak

Funkcje:
- test_get_page_content - Sprawdzenie czy funkcja zwraca jakąś zawartość
- test_get_articles_amount - Sprawdzenie czy funkcja zwraca prawidłową liczbę artykułów.
- test_get_articles_empty_html - Sprawdzenie czy pojawia się wyjątek przy podaniu pustego HTML-a do funkcji

Wyjątki (exceptions):
- brak

Inne obiekty:
- brak
"""
# Standard library imports
from unittest.mock import patch

# Third party imports
import pytest

# Local application import
import article_reader.article_reader as ar


@patch('article_reader.article_reader.requests')
def test_get_page_content(mock_get):
    """ Sprawdzenie czy funkcja zwraca jakąś wartość, w przypadku gdy połączy się z podanym adresem.
    Test używa mocka
    """
    template_value = "<!DOCTYPE HTML>" \
                     "<html lang='pl'>" \
                     "<head prefix='og: http://ogp.me//ns# fb: http://ogp.me//ns//fb#'>" \
                     "<meta http-equiv='X-UA-Compatible' content='IE=Edge,chrome=1'/>"
    mock_get.get().text = template_value
    mock_get.get().status_code = 200
    mock_get.get().ok = True
    return_value = ar.get_page_content("https://www.deloitte.com/pl/pl/pages/technology/topics/blog-agile.html")
    assert return_value == template_value


@patch('article_reader.article_reader.requests')
def test_get_page_content_no_content(mock_get):
    """ Sprawdzenie czy funkcja zwraca pustą wartość, w przypadku nie uda się pobrać danych spod podanego adresu.
    Test używa mocka
    """
    template_value = None
    mock_get.get().text = template_value
    mock_get.get().status_code = 400
    mock_get.get().ok = False
    return_value = ar.get_page_content("https://www.deloitte.com/pl/pl/pages/technology/topics/blog-agile.html")
    assert return_value == template_value


def test_get_articles_amount():
    """ Sprawdzenie czy funkcja zwraca prawidłową liczbę artykułów. W danych wzorcowych jest ich 59. """

    with open('./data/test_data_get_articles.txt', 'r') as data_file:
        html = data_file.read()
    with open('./data/test_resultdata_get_articles.txt', 'r') as result_data_file:
        expected_value = list(result_data_file.read().split(';'))

    result = ar.get_articles(html)

    expected_length = len(expected_value)
    length = len(result)
    assert length == expected_length


def test_get_articles_empty_html():
    """ Sprawdzenie czy pojawia się wyjątek przy podaniu pustego HTML-a do funkcji"""
    html = ''
    with pytest.raises(Exception):
        ar.get_articles(html)
