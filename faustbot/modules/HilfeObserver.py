"""

This module prints some resources for distressed and suicidal People

September 2025 Skadi Wiesemann

"""

from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class HilfeObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".hilfe"]

    @staticmethod
    def help():
        return ".hilfe - Gibt anlaufstellen für Akute Hilfe aus"

    def update_on_priv_msg(self, data, connection: Connection):
        if data["message"].startswith(".hilfe"):
            _lines = [
                "Wir sind keine ausgebildteten Therapeuten. Bitte wende dich in akuten Fällen von Suizidalität oder psychologischen Ausnahmezuständen an folgende Orte:",
                "Rettungsdienst: Tel: 112",
                "Telefonseelsorge: https://telefonseelsorge.de",
                "Für Kinder und Eltern: https://nummergegenkummer.de, https://dajeb.de",
                "Hilfe bei Gewalt und Straftaten: https://weisser-ring.de/",
            ]
            for help_line in _lines:
                connection.send_back(help_line, data)
