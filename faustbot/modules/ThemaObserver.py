"""

This module prints a random Topic to chat about

September 2025, Skadi Wiesemann

"""

import random
from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from faustbot.extras.themen import Themen

themen = Themen()

class ThemaObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".thema"]

    @staticmethod
    def help():
        return ".thema - gibt ein Thema aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".thema"):
            anfang = ["Gerade geht es um", "Wir reden über", "Das Thema ist"]

            connection.send_back(f"{random.choice(anfang)} {themen.get_random()}", data)
