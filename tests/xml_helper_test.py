"""
Moduł zawiera testy jednostkowe funkcji znajdujących się w module xml_helper.py

Klasy:
- brak

Funkcje:
- create_xml_from_string - Utworzenie xml-a na potrzeby testów
- create_node_from_string - Utworzenie jednego artykułu na potrzeby testów
- test_xml_get_max_id - Sprawdzenie czy funkcja zwraca maksymalny numer id z pliku xml
- test_xml_get_new_id - Sprawdzenie czy funkcja zwraca identyfikator o jeden większy od aktualnego
- test_xml_modify_tree - Sprawdzenie czy funkcja zwraca ilość nowych artykułów
- test_xml_modify_tree_2 - Sprawdzenie czy funkcja dodała nowe artykuły do istniejącego xml-a
- test_xml_find_all_articles - Sprawdzenie czy funkcja zwraca prawidłową liczbę wszystkich i przeczytanych artykułów
- test_xml_save_articles - Sprawdzenie czy funkcja zwraca prawidłową liczbę nowo dodanych artykułów
- test_xml_create_article - Sprawdzenie czy funkcja generuje węzeł xml z prawidłową strukturą

Wyjątki (exceptions):
- brak

Inne obiekty:
- brak
"""

# Standard library imports
import xml.etree.ElementTree as ElementTree
from unittest.mock import patch

# Third party imports
import pytest

# Local application import
import article_reader.xml_helper as helper


def create_xml_from_string() -> ElementTree.Element:
    """ Utworzenie xml-a na potrzeby testów

    Funkcja tworzy xml-a z artykułami na potrzeby testów jednostkowych.

    :return: Główny element (root) xml-a z danymi o artykułach
    :rtype: ElementTree.Element
    """
    xml_str = '<?xml version=\'1.0\' encoding=\'utf-8\'?>' \
              '<articles>' \
              ' <article id="1" read="false">' \
              '     <title>Tytuł artykułu 1</title>' \
              '     <link>Link artykułu 1</link>' \
              ' </article>' \
              ' <article id="2" read="true">' \
              '     <title>Tytuł artykułu 2</title>' \
              '     <link>Link artykułu 2</link>' \
              ' </article>' \
              ' <article id="3" read="false">' \
              '     <title>Tytuł artykułu 3</title>' \
              '     <link>Link artykułu 3</link>' \
              ' </article>' \
              ' <article id="4" read="false">' \
              '     <title>Tytuł artykułu 4</title>' \
              '     <link>Link artykułu 4</link>' \
              ' </article>' \
              '</articles>'
    return ElementTree.fromstring(xml_str)


def create_node_from_string() -> ElementTree.Element:
    """ Utworzenie jednego artykułu na potrzeby testów

    Funkcja tworzy xml z informacjami o jednym artykule na potrzeby testów jednostkowych.

    :return: Element xml z danymi o artykule
    :rtype: ElementTree.Element
    """
    xml_str = '<article id="1" read="false">' \
              '    <title>Tytuł artykułu 1</title>' \
              '    <link>Link artykułu 1</link>' \
              '</article>'
    return ElementTree.fromstring(xml_str)


def test_xml_get_max_id():
    """ Sprawdzenie czy funkcja zwraca maksymalny numer id z pliku xml """
    elem = create_xml_from_string()
    assert helper.xml_get_max_id(elem) == 4


@patch('article_reader.xml_helper.xml_get_max_id')
def test_xml_get_new_id(mock_get_max_id):
    """ Sprawdzenie czy funkcja zwraca identyfikator o jeden większy od aktualnego.

    Test używa mocka i sprawdza czy mock został wywołany.
    """
    mock_get_max_id.return_value = 5
    elem = create_xml_from_string()
    assert helper.xml_get_new_id(elem) == 6
    mock_get_max_id.assert_called_once()


@patch('article_reader.xml_helper.xml_create_article')
def test_xml_modify_tree(mock_xml_create_article):
    """ Sprawdzenie czy funkcja zwraca ilość nowych artykułów

    Test używa mocka i sprawdza czy mock został wywołany.
    """
    article_list = [['tytuł 1', 'link 1'], ['tytuł 2', 'link 2']]
    elem = create_xml_from_string()

    mock_xml_create_article.return_value = create_node_from_string()

    assert helper.xml_modify_tree(article_list, elem) == 2
    assert mock_xml_create_article.call_count == 2


@patch('article_reader.xml_helper.xml_create_article')
def test_xml_modify_tree_2(mock_xml_create_article):
    """ Sprawdzenie czy funkcja dodała nowe artykuły do istniejącego xml-a

    Test używa mocka i sprawdza czy mock został wywołany.
    """
    article_list = [['tytuł 1', 'link 1'], ['tytuł 2', 'link 2']]
    elem = create_xml_from_string()
    mock_xml_create_article.return_value = create_node_from_string()

    helper.xml_modify_tree(article_list, elem)
    count = 0
    for elem in elem.iter():
        if elem.tag == 'article':
            count += 1
    assert count == 6
    mock_xml_create_article.assert_called()


@patch('article_reader.xml_helper.xml_load_tree')
def test_xml_find_all_articles(mock_xml_load_tree):
    """ Sprawdzenie czy funkcja zwraca prawidłową liczbę wszystkich i przeczytanych artykułów

    Test używa mocka i sprawdza czy mock został wywołany.
    """
    elem = create_xml_from_string()
    tree = ElementTree.ElementTree(elem)
    mock_xml_load_tree.return_value = tree

    amount, read = helper.xml_find_all_articles('something path')
    assert amount == 4
    assert read == 1
    mock_xml_load_tree.assert_called_once()


@patch('article_reader.xml_helper.xml_load_tree')
@patch('article_reader.xml_helper.xml_modify_tree')
@patch('article_reader.xml_helper.xml_save_to_file')
def test_xml_save_articles(mock_save_to_file, mock_xml_modify_tree, mock_xml_load_tree):
    """ Sprawdzenie czy funkcja zwraca prawidłową liczbę nowo dodanych artykułów

    Test używa trzech mocków i sprawdza czy zostały one wywołane. Ważna jest tutaj kolejność mocków w @patch oraz
    w parametrach funkcji. Kolejność musi być taka, że @patch najbliżej definicji funkcji jest jednocześnie pierwszym
    parametrem funkcji. W przeciwnym wypadku mocki się pomieszają. Widać to w trybie debug, w podglądzie zmiennych
    """
    mock_save_to_file.return_value = None
    mock_xml_load_tree.return_value = ElementTree.ElementTree(create_xml_from_string())
    mock_xml_modify_tree.return_value = 8

    new_list = [['tyt', 'link'], ['tyt2', 'link2']]

    assert helper.xml_save_articles(new_list, '') == 8
    mock_xml_modify_tree.assert_called_once()
    mock_xml_load_tree.assert_called_once()
    mock_save_to_file.assert_called_once()


def test_xml_create_article():
    """ Sprawdzenie czy funkcja generuje węzeł xml z prawidłową strukturą """
    title = "tytuł"
    link = "http:\\localhost"
    elem = create_xml_from_string()
    tree = ElementTree.ElementTree(elem)

    new_node = helper.xml_create_article(title, link, tree.getroot())

    assert new_node.tag == 'article'
    assert len(new_node.attrib) == 2
    assert new_node.attrib.get('id')
    assert new_node.attrib.get('read')

    assert len(new_node.items()) == 2
    assert type(new_node.find('title')) is ElementTree.Element
    assert type(new_node.find('link')) is ElementTree.Element

