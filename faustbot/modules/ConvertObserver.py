"""

Module to Convert one Unit to a different Unit

February 2026, Skadi Wiesemann

"""

from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from faustbot import logger

ZENT_INCH = 2.25
GRAMM_POUND = 453.592
FAHR_CEL = 1.8

umrechnung = {
    ("zentimeter", "inch"): 1 / ZENT_INCH,  # cm to inch (divide)
    ("inch", "zentimeter"): ZENT_INCH,       # inch to cm (multiply)
    ("gramm", "pound"): 1 / GRAMM_POUND,    # gram to pound (divide)
    ("pound", "gramm"): GRAMM_POUND,        # pound to gram (multiply)
    ("fahrenheit", "celsius"): 1 / FAHR_CEL, # F to C (divide)
    ("celsius", "fahrenheit"): FAHR_CEL,    # C to F (multiply)
}


class ConvertObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".conv"]

    @staticmethod
    def help():
        return ".conv <von Einheit> <zu Einheit> <Zahl> - Wandelt eine Einheit in die andere um. .conv help für eine liste von Einheiten"

    def update_on_priv_msg(self, data, connection: Connection):
        if data["message"].find(".conv") == -1:
            return

        if data["message"].startswith(".conv"):
            logger.debug(f"{data['message']}")

            array = data["message"].split(" ")  # ['.conf', 'von', 'zu', 'zahl']

            try:
                zahlString = array[3]
                von = array[1]
                zu = array[2]
            except IndexError:
                connection.send_back(
                    "Verfügbare Einheiten sind: gramm, zentimeter, pound, inch, celsius, fahrenheit",
                    data,
                )
                return

            try:
                zahlString = zahlString.replace(",", ".")
                zahl = float(zahlString)
            except ValueError:
                connection.send_back("Keine Zahl", data)
                return
            if von == "fahrenheit" and zu == "celsius":
                faktor = umrechnung.get((von, zu))
                ergebnis = round(((zahl - 32) * faktor), 2)  # (F - 32) * 5/9
            elif von == "celsius" and zu == "fahrenheit":
                faktor = umrechnung.get((von, zu))
                ergebnis = round((zahl * faktor + 32), 2)    # (C * 9/5) + 32

            else:
                try:
                    faktor = umrechnung.get((von, zu))
                    ergebnis = round((zahl * faktor), 2)
                except KeyError:
                    connection.send_back("KE: Keine Umrechnung möglich", data)
                    return
                except TypeError:
                    connection.send_back("TE: Keine Umrechnung möglich", data)
                    return

            connection.send_back(f"{zahlString} {von} sind {ergebnis} {zu}", data)
            return
