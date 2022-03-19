"""
Moduł zawiera funkcje do obsługi danych w formacie xml.

Klasy:
- brak klas

Funkcje:
- xml_get_max_id - Pobranie maksymalnej wartości id artykułu z xml-a
- xml_get_new_id - Ustalenie kolejnego wolnego identyfikatora dla artykułu
- xml_save_to_file - Zapis do pliku xml-a z informacjami o artykułach
- xml_create_article - Utworzenie xml-a z informacjami o artykule.
- xml_load_tree - Załadowanie xml-a z danymi o artykułach
- xml_create_tree - Utworzenie głównego węzła xml
- xml_modify_tree - Modyfikacja zawartości xml-a z informacjami o artykułach
- xml_find_all_articles - Obliczenie ilości artykułów
- xml_save_articles - Modyfikacja artykułów i zapis do lokalnego pliku xml
- xml_show_articles - Wyświetlenie listy artykułów

Wyjątki (exceptions):
- brak

Inne obiekty:
- brak
"""
# Standard library imports
import os
from typing import Tuple, List
import xml.etree.ElementTree as ElementTree

# Third party imports

# Local application import
# from . import common_helper
# from . import logger_helper
import common_helper
import logger_helper


def xml_get_max_id(xml_root) -> int:
    """ Pobranie maksymalnej wartości id artykułu z xml-a

    Funkcja przeszukuje podany xml i zwraca największy znaleziony identyfikator artykułu

    :param xml_root: Obiekt xml z danymi o artykułach, które zapisane są w pliku xml. Potrzebny jest do wyszukania
    max_id w xml-u
    :type xml_root: xml.etree.ElementTree.Element
    :return: Największy identyfikator artykułu znajdujący się w pliku
    :rtype: int
    """
    max_id = 0
    for node in xml_root.findall("article"):
        current_id = int(node.get('id'))
        if current_id > max_id:
            max_id = current_id
    return max_id


def xml_get_new_id(xml_root) -> int:
    """ Ustalenie kolejnego wolnego identyfikator dla artykułu

    Funkcja zwraca kolejny wolny identyfikator artykułu w xml-u

    :param xml_root: Obiekt xml z danymi o artykułach, które zapisane są w pliku xml. Potrzebny jest do wyszukania
    max_id w xml-u
    :type xml_root: xml.etree.ElementTree.Element
    :return: Kolejny identyfikator artykułu
    :rtype: int
    """
    max_id = xml_get_max_id(xml_root)
    return max_id + 1


def xml_save_to_file(tree: ElementTree.ElementTree, filename) -> None:
    """ Zapis do pliku xml-a z informacjami o artykułach.

    Funkcja zapisuje do pliku pod podaną nazwą zawartość xml-a z danymi o artykułach

    :param tree: Obiekt xml z danymi o artykułach
    :type tree: xml.etree.ElementTree.ElementTree
    :param filename: Nazwa pliku xml
    :type filename: str
    :return: ---
    :rtype: ---
    """
    tree.write(file_or_filename=filename, xml_declaration=True, encoding='utf-8', method='xml',
               short_empty_elements=False)


def xml_create_article(title, link, root_node) -> ElementTree.Element:
    """ Utworzenie xml-a z informacjami o artykule.

    Funkcja na podstawie otrzymanych parametrów generuje obiekt xml z informacjami o artykule.

    :return:
    :param title: Tytuł artykułu
    :type title: str
    :param link: Link do artykułu
    :type link: str
    :param root_node: Obiekt xml z danymi o artykułach, które zapisane są w pliku xml. Potrzebny jest do wyszukania
    max_id w xml-u
    :type root_node: xml.etree.ElementTree.Element
    :return: Obiekt xml z informacjami o artykule
    :rtype: xml.etree.ElementTree.Element
    """
    node_article = ElementTree.Element('article')
    node_article.set('id', str(xml_get_new_id(root_node)))
    node_article.set('read', str(False).lower())

    node_title = ElementTree.SubElement(node_article, 'title')
    node_title.text = title

    node_link = ElementTree.SubElement(node_article, 'link')
    node_link.text = common_helper.complete_link(link)

    return node_article


def xml_load_tree(file_name: str) -> ElementTree.ElementTree:
    """ Załadowanie xml-a z danymi o artykułach

    Funkcja ładuje dane o artykułach z podanego pliku xml. Jeżeli plik nie istnieje to funkcja tworzy nowy plik z
    podstawowymi informacjami xml oraz węzłem root.

    :param file_name: Nazwa pliku xml z danymi o artykułach
    :type file_name: str
    :return: Obiekt xml z zawartością podanego pliku xml.
    :rtype: xml.etree.ElementTree.Element
    """
    if not os.path.exists(file_name):
        xml_create_tree(file_name)
    return ElementTree.parse(file_name)


def xml_create_tree(file_name):
    """ Utworzenie głównego węzła xml

    Funkcja tworzy główny węzeł w pliku xml i zapisuje utworzony xml do podanego pliku.

    :param file_name: Nazwa pliku xml
    :type file_name: str
    :return: ---
    :rtype: ---
    """
    doc = ElementTree.Element('articles')
    tree = ElementTree.ElementTree(doc)
    xml_save_to_file(tree, file_name)


def xml_modify_tree(articles_list, root_node: ElementTree.Element) -> int:
    """ Modyfikacja zawartości xml-a z informacjami o artykułach

    Funkcja otrzymuje listę artykułów odczytaną ze strony www oraz xml z artykułami zapisany na dysku. Następnie
    porównuje zawartość obu źródeł i dodaje do xml-a artykuły odczytane ze strony www, których nie ma w xml-u.
    Funkcja modyfikuje zawartość podanego xml-a.

    :param articles_list: Lista artykułów odczytana ze strony www w postaci list[[tytuł,link], [tytuł,link]]
    :type articles_list: list[[str,str], [str,str]]
    :param root_node: Obiekt xml z danymi o artykułach, które zapisane są w pliku xml
    :type root_node: xml.etree.ElementTree.Element
    :return: Ilość nowo dodanych artykułów
    :rtype: int
    """
    new_articles_count = 0  # type: int
    for article in articles_list:
        article_already_exists = False  # type: bool
        for node in root_node.iter(tag='title'):
            if node is not None:
                if node.text == article[0]:
                    article_already_exists = True
                    break
        if not article_already_exists:
            new_article_node = xml_create_article(title=article[0], link=article[1], root_node=root_node)
            root_node.append(new_article_node)
            new_articles_count += 1
    return new_articles_count


def xml_find_all_articles(xml_file_path: str) -> Tuple[int, int]:
    """ Obliczenie ilości artykułów

    Funkcja oblicza ilość artykułów zawartych w podanym źródle danych. Zliczana jest ilość wszystkich, nowych oraz
    przeczytanych artykułów.

    :param xml_file_path: Ścieżka do pliku xml z danymi
    :type xml_file_path: str
    :return: Ilość artykułów: wszystkich, przeczytanych
    :rtype: int, int
    """
    xml_tree_local = xml_load_tree(xml_file_path)
    xml_root = xml_tree_local.getroot()
    amount, read = 0, 0
    for node in xml_root.findall("article"):
        amount += 1
        if node.get("read").lower() == 'true':
            read += 1
    return amount, read


def xml_save_articles(articles: List[List[str]], xml_file_path: str) -> int:
    """ Modyfikacja artykułów i zapis do lokalnego pliku xml

    Funkcja modyfikuje lokalny plik xml z artykułami na podstawie otrzymanej listy artykułów. Następnie wykonywany jest
    zapis zmodyfikowanego pliku na dysk.

    :param articles: Lista artykułów odczytanych ze strony web w postaci list[[tytuł,link], [tytuł,link], ...]
    :type articles: list[list[str]]
    :param xml_file_path: Ścieżka do lokalnego pliku xml
    :type xml_file_path: str
    :return: Ilość nowo dodanych artykułów
    :rtype: int
    """
    xml_tree = xml_load_tree(xml_file_path)
    added_articles = xml_modify_tree(articles, xml_tree.getroot())
    xml_save_to_file(xml_tree, xml_file_path)
    return added_articles


def xml_set_article_as_read(xml_file_path: str, article_id: int, read: bool):
    """ Ustawienie artykułu jako przeczytanego

    Funkcja ustawia jako przeczytany artykuł o podanym identyfikatorze

    :param read: True - artykuł został już przeczytany. False - artykuł jeszcze nie był czytany
    :type read: bool
    :param xml_file_path: Ścieżka do pliku xml z danymi
    :type xml_file_path: str
    :param article_id: identyfikator artykułu
    :type article_id: int
    :return: None
    :rtype: ---
    """
    xml_tree_local = xml_load_tree(xml_file_path)
    xml_root = xml_tree_local.getroot()
    nodes = xml_root.findall(f"article[@id='{article_id}']")
    if len(nodes) == 1:
        nodes[0].set('read', str(read).lower())
        xml_save_to_file(xml_tree_local, xml_file_path)
        if read:
            print(f"Article {article_id} was set as read")
        else:
            print(f"Article {article_id} was set as unread")
    elif len(nodes) == 0:
        msg = f"Node with the identifier {article_id} was not found"
        logger_helper.log_error(msg)
        print(msg)
    else:
        msg = f"Too many nodes found: {len(nodes)}. Expected one node"
        logger_helper.log_error(msg)
        print(msg)


def xml_show_articles(article_type: str, xml_file_path: str):
    """ Wyświetlenie listy artykułów

    Funkcja wyświetla listę artykułów w zależności od podanych parametrów. Mogą być wyświetlone: wszystkie artykuły,
    przeczytane lub nieprzeczytane artykuły.

    :param article_type: all - wszystkie; read - przeczytane; unread - nieprzeczytane
    :type article_type: str
    :param xml_file_path: Ścieżka do pliku z artykułami
    :type xml_file_path: str
    :return: None
    :rtype: ---
    """
    if article_type == 'all':
        query = "article"
    if article_type == 'read':
        query = "article[@read='true']"
    if article_type == 'unread':
        query = "article[@read='false']"
    else:
        logger_helper.log_warning(f'Podano błędny typ artykułów: {article_type}')

    xml_tree_local = xml_load_tree(xml_file_path)
    xml_root = xml_tree_local.getroot()
    for node in xml_root.findall(query):
        print(f"Artykuł o id: {node.attrib.get('id')}")
        print(node.find('title').text.strip())
        print(node.find('link').text.strip())
