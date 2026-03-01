"""

This module ouputs a random quote

February 2026, Skadi Wiesemann

"""


import random
import os

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from FaustBot.Model.GoodQuotesProvider import GoodQuotesProvider

def convert_to_arr():

    """
    Convert the badquotes.txt file in a array, separated on \n
    """

    with open('FaustBot/Modules/txtfiles/badquotes.txt', 'rt') as file:
        zitate = file.read()
    file.close()
    badquotes = zitate.split('\n')
    return badquotes

def get_quote():

    """
    Get random Quote from the files in FaustBot/Modules/txtfiles/zitate. First choose one random file, then read said file
    split on % and print out the resulting quote
    """

    file = random.choice(os.listdir('FaustBot/Modules/txtfiles/zitate'))

    with open(f'FaustBot/Modules/txtfiles/zitate/{file}', 'r') as f:
        zitate = f.read()
    f.close()

    arr_zitate = zitate.split('%')
    out = ""
    for zitat in random.sample(arr_zitate, k=1):
        out = zitat.replace('\n', ' ')
        out = out.replace('\t', '')

    return out

def check_for_bad(out):

    """
    Check for matches in badquotes.txt, returns true if badquotes matches
    """

    badquotes = convert_to_arr()
    for zitat in badquotes:
        if out == zitat:
            return True
        else:
            continue

    return False

def num_badquotes():

    """
    Reurns number of badquotes
    """

    badquotes = convert_to_arr()
    laenge = len(badquotes)

    # - 1 because of trailing newline
    return laenge - 1

class FortuneObserver(PrivMsgObserverPrototype):

    @staticmethod
    def cmd():
        return ['.fortune']

    @staticmethod
    def help():
        return '.fortune - Gibt ein zufälliges Zitat aus. .bad setzt das Zitat auf eine Blacklist. .good setzt ein \
                Zitat auf eine gute Liste, .topquote ruft das am hoechsten bewertete Zitat auf'

    def update_on_priv_msg(self, data, connection: Connection):

        global lastQuote

        if data['message'].startswith('.fortune'):

            out = get_quote()
            badquote = check_for_bad(out)

            while len(out) > 433:
                while badquote:
                    out = get_quote()

            connection.send_back(out, data)

            lastQuote = out

            return

        if data['message'].startswith('.bad') and data['message'].find('num') != -1:

            # check if idented mod
            if data['nick'] in self._config.mods and connection.is_idented(data['nick']):
                laenge = num_badquotes()
                connection.send_back(f'Die Anzahl der Zitate auf der Blacklist betraegt {laenge}', data)

        elif data['message'] == '.bad':
            with open('FaustBot/Modules/txtfiles/badquotes.txt', 'at') as f:
                f.write(f'{lastQuote}\n')
                connection.send_back('Zitat zur Blacklist hinzugefuegt', data)
            f.close()
            return

        if data['message'] == '.good':
            quotes_provider = GoodQuotesProvider()
            votes = quotes_provider.get_votes(lastQuote)
            existing = quotes_provider.get_quote(lastQuote)
            if existing:
                quotes_provider.update_votes(lastQuote)
                connection.send_back('Hochwaehlis um eins erhoeht', data)
                return
            else:
                quotes_provider.save_or_replace(lastQuote, votes)
                connection.send_back("Zitat hochgewaehlt", data)
                return

        if data['message'] == '.topquote':
            quotes_provider = GoodQuotesProvider()
            votes, quote = quotes_provider.get_top_quote()

            if votes is not None:
                connection.send_back(f'Top Zitat mit {votes} Hochwaehlis ist', data)
                connection.send_back(quote, data)
                return
            else:
                connection.send_back("Noch kein Zitat gespeichert", data)
                return

