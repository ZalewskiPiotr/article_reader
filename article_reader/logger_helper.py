"""
Moduł zawiera funkcje do obsługi logowania komunikatów.

Klasy:
- brak klas

Funkcje:
- init_logging - Konfiguracja modułu logowania komunikatów
- start_script - Logowanie informacji o uruchomieniu skryptu
- end_script - Logowanie informacji o zakończeniu skryptu
- log_error - Logowanie informacji o błędzie w programie
- log_exception - Logowanie informacji o aktualnym wyjątku
- log_warning - Logowanie informacji

Wyjątki (exceptions):
- brak

Inne obiekty:
- brak
"""
# Standard library imports
import logging


def init_logging(file_path: str) -> None:
    """ Konfiguracja modułu logowania komunikatów

    Funkcja ustawia konfigurację modułu logowania. Wykorzystywany jest mechanizm z modułu logging.py ze standardowej
    biblioteki Pythona

    :param file_path: Ścieżka do pliku z logami
    :type file_path: str
    :return: ---
    :rtype: ---
    """
    logging.basicConfig(filename=file_path,
                        filemode='a',
                        level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')


def start_script() -> None:
    """ Logowanie informacji o uruchomieniu skryptu

    Funkcja loguje informację o dacie i czasie uruchomienia skryptu.

    :return: ---
    :rtype: ---
    """
    logging.info('-' * 45)
    logging.info('-' * 10 + f" Article Reader started" + '-' * 10)


def end_script() -> None:
    """ Logowanie informacji o zakończeniu skryptu

    Funkcja loguje datę i czas zakończenia działania skryptu

    :return: ---
    :rtype: ---
    """
    logging.info('-' * 10 + f" Article Reader ended" + '-' * 10)
    logging.info('-' * 45)


def log_error(msg: str) -> None:
    """ Logowanie informacji o błędzie w programie

    Funkcja loguje informację w formacie błędu. Funkcja nie zapisze zawartości traceback, tylko sam komunikat i oznaczy
    go w pliku logu jako błąd.

    :param msg: Komunikat o błędzie
    :type msg: str
    :return: ---
    :rtype: ---
    """
    logging.error(msg)


def log_exception(msg: str) -> None:
    """ Logowanie informacji o aktualnym wyjątku

    Funkcja loguje informację o wyjątku. Do pliku zapisywany jest cały aktualny traceback.

    :param msg: Komunikat o błędzie
    :type msg: str
    :return: ---
    :rtype: ---
    """
    logging.exception(msg)


def log_warning(msg: str) -> None:
    """ Logowanie informacji

    Funkcja loguje podaną informację

    :param msg: Tekst do zalogowania
    :type msg: str
    :return: ---
    :rtype: ---
    """
    logging.info(msg)
