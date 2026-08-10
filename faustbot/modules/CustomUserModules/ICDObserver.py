import csv
import re
from random import choice

from faustbot.communication.Connection import Connection
from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class ICDObserver(PrivMsgObserverPrototype):
    with open(
        "faustbot/modules/txtfiles/care_icd10_de.csv", "r", encoding="utf8"
    ) as icd10_codes:
        icd10_dict = {
            row[0]: row[1] for row in csv.reader(icd10_codes, delimiter=";", quotechar='"')
        }

    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_priv_msg(self, data, connection: Connection):
        if data["message"].startswith(".icd "):
            if data["channel"] == connection.details.get_channel():
                regex = r"\b(\w\d{2}\.?\d?\d?)\b"
                codes = re.findall(regex, data["message"])
                if codes:
                    for code in codes[:5]:
                        code = code.capitalize()
                        text = self.icd10_dict.get(code, False)
                        if not text:
                            if "." in code:
                                code += "-"
                            else:
                                code += ".-"
                        text = self.icd10_dict.get(code, False)
                        if text:
                            connection.send_back(f"{code} - {text}", data)
                else:
                    code = choice(list(self.icd10_dict.items()))
                    connection.send_channel(code[0] + " : " + code[1])
                    return
