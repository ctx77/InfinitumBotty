from os import scandir
from random import choice
from faustbot import logger
from faustbot.communication.Connection import Connection


class BBB(list):
    def _read_file(self, _entry):
        _color = _entry.name.replace('.txt', '')
        with open(_entry) as txt:
            return {_color: [b.strip() for b in txt.readlines()]}

    def __init__(self):
        self.bbb_normal = {}
        self.bbb_special = {}
        self._bbb_give_word = ["schenkt", "überreicht"]
        for _entry in scandir('faustbot/modules/txtfiles/bbb'):
            if _entry.is_file():
                self.bbb_normal.update(self._read_file(_entry))
        for _entry in scandir('faustbot/modules/txtfiles/bbb/special'):
            if _entry.is_file():
                self.bbb_special.update(self._read_file(_entry))
        

        _as_list = []
        for _color in self.bbb_normal.keys():
            _as_list.extend(self.bbb_normal[_color])
        for _color in self.bbb_special.keys():
            _as_list.extend(self.bbb_special[_color])
        super().__init__(_as_list)

    def reload(self):
        self.__init__()
    def get_random(self):
        return choice(self)
    
    @staticmethod
    def cmd():
        return [".bbb"]

    @staticmethod
    def help():
        return ".bbb - und du bekommst eine womöglich schmackhafte Bohne."

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data["nick"] in connection.details.get_mods() and connection.is_idented(data["nick"])

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data["message"].startswith(".bbb"):
            if data["message"].startswith(".bbb reload") and self._is_idented_mod(data, connection):
                _old_bean_count = len(self)
                self.reload()
                _new_bean_count = len(self)
                connection.send_back(
                    f"Bohnen neu geladen (Alte Anzahl: {_old_bean_count}, Neue Anzahl: {_new_bean_count})",
                    data,
                )
                return

            _response_bean_list = self
            if data["message"].startswith(".bbb "):
                _color = str(data["message"].split(" ", 1)[1]).replace('ü', 'ue').replace('ä', 'ae').replace('ö', 'oe').replace('ß', 'ss').lower()
                for available_color in self.bbb_normal.keys():
                    if _color.startswith(available_color):
                        _response_bean_list = self.bbb_normal[available_color]
                        break
            
            connection.send_back(
                f"\001ACTION {choice(self._bbb_give_word)} {data.get('nick')} {choice(_response_bean_list)}.\001",
                data,
            )
