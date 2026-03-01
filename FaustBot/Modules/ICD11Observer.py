"""

This module takes a ICD11 Code as input and prints the corresponding Entry

September 2025, Skadi Wiesemann

"""


import csv
import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class ICD11Observer(PrivMsgObserverPrototype):
    with open('FaustBot/Modules/txtfiles/icd11_codes.csv') as icd11_codes:
        icd11_dict = {
            row[0]: row[1]
            for row in csv.reader(icd11_codes, delimiter=',')
        }
    icd11_codes.close()

    @staticmethod
    def cmd():
        return ['.icd11']

    @staticmethod
    def help():
        return '.icd11 <Code> - Gibt einen icd11 code aus. Ein leerer Befehl gibt einen zufälligen code aus'

    def update_on_priv_msg(self, data, connection: Connection):

        #' ' after .icd11 so that .icd11xxx doesnt trigger an IndexError at code = arr[1] !!Solved with try: except:
        if data['message'].startswith('.icd11'):
            #split message
            message = data['messageCaseSensitive']
            arr = message.split(' ', 1)


            if len(arr) == 1:
                # Convert dict keys to a list so random.choice can pick one
                code = random.choice(list(self.icd11_dict.keys()))

                # Get Description
                beschreibung = self.icd11_dict.get(code).strip(' ')

                connection.send_back(f'{code} - {beschreibung}', data)
                return

            #capitalize icdCode
            try:
                code = arr[1].upper()
            except IndexError:
                connection.send_back("Leerzeichen vergessen?", data)
                return

            #when there is no key a attribute error is raised
            try:
                text = self.icd11_dict.get(code).strip(' ')
            except AttributeError:
                connection.send_back('Code nicht gefunden', data)
                return

            #send back data
            connection.send_back(f'{code} - {text}', data)
            return