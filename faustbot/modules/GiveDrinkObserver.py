from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from faustbot.extras.getraenke import Getraenke

getraenke = Getraenke()

class GiveDrinkObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".drink"]

    @staticmethod
    def help():
        return ".drink - schenkt Getränke aus"

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data["nick"] in connection.details.get_mods() and connection.is_idented(data["nick"])

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".drink"):
            if data["message"].startswith(".drink reload") and self._is_idented_mod(data, connection):
                _old_drink_count = len(getraenke)
                getraenke.reload()
                _new_drink_count = len(getraenke)
                connection.send_back(
                    f"Getränke neu geladen (Alte Anzahl: {_old_drink_count}, Neue Anzahl: {_new_drink_count})",
                    data,
                )
                return

            connection.send_back(
                f"\001ACTION schenkt {data.get('nick')} {getraenke.get_random()} ein.\001",
                data,
            )
