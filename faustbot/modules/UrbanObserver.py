"""

This module takes a term and Queries Urban Dictionary for results. Prints the first one to the Chat

September 2025, Skadi Wiesemann

"""

import requests
from re import search as re_search
from json import loads as json_loads

from faustbot.modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class UrbanObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".urban"]

    @staticmethod
    def help():
        return ".urban <term> - fragt Urban Dictionary zu <term> ab"

    def update_on_priv_msg(self, data, connection):
        if data["messageCaseSensitive"].find(".urban") == -1:
            return

        if data["message"].startswith(".urban "):
            # split incoming message in '.urban' and '<term>'
            message = data["messageCaseSensitive"].split(" ", 1)

            # request content from Urban Dict with <term>
            search = message[1]

            def not_found():
                connection.send_back(
                    f"Ich konnte leider keine Definition für {search} finden", data
                )

            contents = requests.get(
                f"https://www.urbandictionary.com/define.php?term={search}"
            )

            # use build in tools to extract content and status code for further processing

            status = int(contents.status_code)

            if status != 200:
                not_found()
            else:
                for line in contents.content.decode(encoding="utf-8").split("\n"):
                    if "mainEntity" in line:
                        groups = re_search("({.*mainEntity.*})", line).groups()
                        if len(groups) == 1:
                            break
                        else:
                            continue
                else:
                    not_found()

                answer = (
                    json_loads(groups[0])
                    .get("mainEntity", {})
                    .get("description", False)
                )
                if answer:
                    connection.send_back(f"{data['nick']}: {search} - {answer}", data)
                else:
                    not_found()
        else:
            return
