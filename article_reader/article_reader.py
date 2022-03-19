""" Skrypt zarządza przepływem programu do odczytu nagłówków artykułów

Ten skrypt uruchamia program i steruje jego przepływem. Skrypt można uruchomić z parametrami. Szczegóły dostępnych
parametrów są dostępne poprzez wywołanie skryptu z parametrem -h (python article_reader.py -h).
Szczegółowy opis przeznaczenia i działania programu jest opisany w README.rst

Ten skrypt wymaga zainstalowanego: szczegółowy opis wymagań znajduje się w pliku README.rst

Uruchomienie skryptu odbywa się poprzez wywołanie:
`python article_reader.py` - uruchomienie programu i odczyt artykułów
`python article_reader.py -h` - informacje o dostępnych opcjach w programie
`python article_reader.py -v` - informacje o wersji programu
`python article_reader.py -i` - informacje o ilości przechowywanych artykułów
`python article_reader.py -r id` - ustawia jako przeczytany artykuł o podanym numerze id
`python article_reader.py -u id` - ustawia jako nieprzeczytany artykuł o podanym numerze id

Skrypt zawiera funkcje:
- main - ...
- get_command_arguments - Pobranie parametrów linii komend
- show_articles_info - Wyświetlenie informacji o ilości artykułów
- show_script_info - Wyświetlenie informacji o skrypcie
- get_page_content - Pobranie zawartości strony www
- get_articles - Pobranie informacji o artykułach
- sen_email - Wysłanie maila z informacją o nowych artykułach
"""

# Standard library imports
import os, smtplib, ssl, sys, pathlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Third party imports
import argparse
import requests
from bs4 import BeautifulSoup

# Local imports
# sys.path.insert(0, str(pathlib.Path(__file__).parent)) # potrzebne do uruchomienia z pliki cli.py
# from . import xml_helper
# from . import common_helper
# from . import logger_helper
import xml_helper
import common_helper
import logger_helper


def get_command_arguments() -> tuple:
    """ Pobranie parametrów linii komend

    Funkcja sprawdza, czy w linii komend podane zostały parametry skryptu. Możliwe parametry:
    - version - Show information about script
    - info - Show information about articles
    - set-read - Set article as read
    - set-unread - Set article as unread
    - show - Show articles: all, read, unread

    :return: Zwracana jest informacja: version (True/False), info (True/False), set-read (None/number),
    set-unread (None/number), show (all, read, unread)
    :rtype: bool, bool, int, int, str, str
    """
    parser = argparse.ArgumentParser(prog='Article reader',
                                     description='Management of articles. If you do not provide arguments, the script'
                                                 'will download articles from the website.')
    parser.add_argument('-v', '--version', help='Show information about script', action='store_true', dest='version',
                        default=False)
    parser.add_argument('-i', '--info', help="Show information about articles", action='store_true', dest='info',
                        default=False)
    parser.add_argument('-r', '--set-read', help="Set article as read", action='store', type=int, dest='set_read')
    parser.add_argument('-u', '--set-unread', help="Set article as unread", action='store', type=int,
                        dest='set_unread')
    parser.add_argument('-s', '--show', help="Show articles: all, read, unread", action='store',
                        choices=['all', 'read', 'unread'], dest='show')
    args = parser.parse_args()
    return args.version, args.info, args.set_read, args.set_unread, args.show


def show_articles_info(xml_file_path: str):
    """ Wyświetlenie informacji o ilości artykułów.

    Funkcja zlicza artykuły przechowywane w lokalnym źródle danych i wyświetla informacje o wszystkich artykułach,
    nowych artykułach, przeczytanych artykułach.

    :param xml_file_path: ścieżka do pliku xml z artykułami (lokalne źródło danych)
    :type xml_file_path: str
    :return: ---
    :rtype: ---
    """
    amount_all, amount_read = xml_helper.xml_find_all_articles(xml_file_path)
    print(f"All articles: {amount_all}\nRead articles: {amount_read}")


def show_script_info(path_xml: str, path_logger: str, url: str) -> str:
    """ Wyświetlenie informacji o skrypcie

    Funkcja wyświetla informacje o skrypcie oraz o jego konfiguracji

    :param path_xml: ścieżka do pliku z informacjami o artykułach
    :type path_xml: str
    :param path_logger: ścieżka do pliku logów
    :type path_logger: str
    :param url: adres url strony z artykułami czytanymi przez skrypt
    :type url: str
    :return: informacje o skrypcie
    :rtype: str
    """
    info = "Version: 4.0\n" \
           "Author: PiotrZET\n" \
           f"Path to save data: {path_xml}\n" \
           f"Path to logger: {path_logger}\n" \
           f"URL to articles: {url}"
    return info


def get_page_content(url: str):
    """ Pobranie zawartości strony www

    Na podstawie podanego adresu url funkcja pobiera i zwraca zawartość strony internetowej.

    :param url: Pełny adres strony internetowej
    :type url: str
    :return: HTML z zawartością strony spod podanego adresu url. Jeżeli pobranie zawartości nie powiodło się, to
    funkcja zwraca pustą wartość i zapisuje informację o błędzie do pliku logu
    :rtype: str
    """
    try:
        response = requests.get(url)
        if not response.ok:
            response.raise_for_status()
        else:
            return response.text
    except requests.exceptions.RequestException:
        logger_helper.log_error(f"Błędny adres URL: {url}")
        return None


def get_articles(html: str) -> list:
    """ Pobranie informacji o artykułach.

    Funkcja wyszukuje w otrzymanym html-u artykuły i zwraca informacje o nich. Każdy artykuł zawiera tytuł oraz link do
    strony www

    :param html: Html, w którym zawarte są artykuły
    :type html: str
    :return: Lista z informacjami o artykułach
    :rtype: list[[tytuł,link], [tytuł,link]]
    :exception: W przypadku, gdy w podanym html-u nie było artykułów to generowany jest wyjątek typu Exception
    """
    list_articles = []
    soup = BeautifulSoup(html, features="lxml")

    for tag in soup.find_all('h2'):
        parent = tag.find_parent('a')
        link = parent.get('href')
        list_articles.append([common_helper.remove_characters(tag.text), link])

    for tag in soup.find_all(class_='standard-promo perspective-color'):
        parent = tag.find_parent('a')
        link = parent.get('href')
        list_articles.append([common_helper.remove_characters(tag.h3.text), link])

    if len(list_articles) == 0:
        raise Exception("ERROR: I did not find the articles")

    return list_articles


def send_email():
    """ Wysłanie maila z informacją o nowych artykułach

    Funkcja wysyła e-mail na podany adres. Wysyłanie maili bazuje na koncie gmail zgodnie z opisem ze strony:
    https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
    :return: None
    :rtype: brak
    """
    port = 465
    password = '*****'  # może kiedyś do poprawy aby to hasło nie było trzymane na GitHubie
    sender_email = "*****"  # może kiedyś do poprawy aby ten adres nie był trzymany na GitHubie
    receiver_email = "*****"  # na razie i tak niepotrzebne. Wyłączyłem funkcję wysyłania maili

    message = MIMEMultipart("alternative")
    message["Subject"] = "Masz nowe artykuły do przeczytania"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = """Cześć Piotr,
    Na stronie Deloittle pojawiły się nowe artykuły do przeczytania """

    part1 = MIMEText(text, "plain")
    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def main():
    """ Sterowanie przebiegiem programu

    Funkcja ustawia konfigurację programu, zarządza pobraniem parametrów linii komend, zarządza odczytem artykułów
    ze strony www oraz ich zapisem do lokalnego źródła danych

    :return: ---
    :rtype: ---
    """
    # ---------- Konfiguracja programu ----------
    # Poniższa kombinacja z parentPath powoduje, że folder do zapisu danych programu zawsze jest szukany w tym samym
    # miejscu na dysku - niezależnie od folderu, z którego został uruchomiony program
    script_parent_folder = pathlib.Path(__file__).parent.parent
    xml_file_path = os.path.join(f"{script_parent_folder}/data/saved_articles", 'articles.xml')
    logger_file_path = f"{script_parent_folder}/data/app.log"

    url = 'https://www.deloitte.com/pl/pl/pages/technology/topics/blog-agile.html'
    logger_helper.init_logging(logger_file_path)
    # -------------------------------------------

    logger_helper.start_script()

    try:
        get_data_from_web = True
        # Parser parametrów linii komend
        version, info, set_read, set_unread, show = get_command_arguments()
        if version:
            print('-' * 50, "ABOUT SCRIPT:", '-' * 50)
            print(show_script_info(xml_file_path, logger_file_path, url))
            get_data_from_web = False
        if info:
            print('-' * 50, "ARTICLES INFORMATION:", '-' * 50)
            show_articles_info(xml_file_path)
            get_data_from_web = False
        if set_read:
            print('-' * 50, "SET READ:", '-' * 50)
            xml_helper.xml_set_article_as_read(xml_file_path, set_read, True)
            get_data_from_web = False
        if set_unread:
            print('-' * 50, "SET UNREAD:", '-' * 50)
            xml_helper.xml_set_article_as_read(xml_file_path, set_unread, False)
            get_data_from_web = False
        if show:
            print('-' * 50, f"SHOW {show} ARTICLES:", '-' * 50)
            xml_helper.xml_show_articles(show, xml_file_path)
            get_data_from_web = False

        if get_data_from_web:
            # Pobranie zawartości strony www, odczyt nagłówków artykułów, zapis do lokalnego źródła danych
            print('-' * 50, f"READ ARTICLES FROM WWW PAGE:", '-' * 50)
            content = get_page_content(url=url)
            if content:
                articles = get_articles(html=content)
                added_articles = xml_helper.xml_save_articles(articles, xml_file_path)
                if added_articles:
                    send_email()
                print(f"Dodano {added_articles} nowych artykułów.\nDziałanie programu zakończone.")
            else:
                print(f"Błąd ładowania strony www !!! Zajrzyj do pliku logu: {logger_file_path} !!!")
    except Exception:
        logger_helper.log_exception("!!! Niespodziewany wyjątek !!!")
        print(f"Program zakończony nieprawidłowo. Pojawił się niespodziewany wyjątek. Zajrzyj do pliku logu.")
    finally:
        logger_helper.end_script()


if __name__ == '__main__':
    main()
