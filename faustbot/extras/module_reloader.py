from importlib import reload
from random import choice
from faustbot import logger
from faustbot.communication.Connection import Connection
from sys import modules


class ModuleReloader(object):
    def reload(self):
        self.__init__()

    def get_random(self):
        return choice(self)

    @staticmethod
    def cmd():
        return [".module"]

    @staticmethod
    def help():
        return ".module - Module Manipulation For Mods."

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data["nick"] in connection.details.get_mods() and connection.is_idented(
            data["nick"]
        )

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if (
            data["message"].startswith(".module")
            and self._is_idented_mod(data, connection)
            and connection.details.get_channel() == "#faust-bot"
        ):
            _args = data["message"].count(" ")
            if _args >= 2:
                _cmd, _mod = data["message"].split(" ", 2)[1:]
            elif _args == 1:
                _cmd = data["message"].split(" ", 1)[1]
            else:
                _cmd = "ls"

            _active_modules = {
                str(type(_active_module)): _active_module
                for _active_module in connection.priv_msg_observable._observers
            }
            _reloadable_mods = {
                "bbb": "<class 'faustbot.extras.bbb.BBB'>",
                "module_reloader": "<class 'faustbot.extras.module_reloader.ModuleReloader'>",
                "comic": "<class 'faustbot.modules.ComicObserver.ComicObserver'>",
                "urban": "<class 'faustbot.modules.UrbanObserver.UrbanObserver'>",
                "title": "<class 'faustbot.modules.TitleObserver.TitleObserver'>",
            }

            if _cmd == "list" or _cmd == "ls":
                connection.send_back(
                    f"\001ACTION kann die folgenden Module verwalten (rm, reload): {', '.join(list(_reloadable_mods.keys()))}.\001",
                    data,
                )

            if _cmd == "remove" or _cmd == "rm":
                if _mod in _reloadable_mods:
                    if _reloadable_mods[_mod] in _active_modules:
                        while (
                            _active_modules[_reloadable_mods[_mod]]
                            in connection.priv_msg_observable._observers
                        ):
                            connection.priv_msg_observable._observers.remove(
                                _active_modules[_reloadable_mods[_mod]]
                            )
                        connection.send_back(
                            f"\001ACTION hat das Modul {_mod} entfernt.\001",
                            data,
                        )
                    else:
                        connection.send_back(
                            f"\001ACTION hat das Modul {_mod} garnicht geladen. :(\001",
                            data,
                        )
                else:
                    connection.send_back(
                        f"\001ACTION kennt das Modul nicht (in Bezug zum Reloader), aber die hier {list(_reloadable_mods.keys())} wären möglich.\001",
                        data,
                    )

            if _cmd == "reload":
                if _mod in _reloadable_mods:
                    if _reloadable_mods[_mod] in _active_modules:
                        while (
                            _active_modules[_reloadable_mods[_mod]]
                            in connection.priv_msg_observable._observers
                        ):
                            connection.priv_msg_observable._observers.remove(
                                _active_modules[_reloadable_mods[_mod]]
                            )

                    _has_reloaded_mod = True
                    match _mod:
                        case "bbb":
                            import faustbot.extras.bbb as _new_mod

                            _new_mod = reload(_new_mod)
                            connection.priv_msg_observable._observers.append(_new_mod.BBB())

                        case "module_reloader":
                            import faustbot.extras.module_reloader as _new_mod

                            _new_mod = reload(_new_mod)
                            connection.priv_msg_observable._observers.append(
                                _new_mod.ModuleReloader()
                            )

                        case "comic":
                            import faustbot.modules.ComicObserver as _new_mod

                            _new_mod = reload(_new_mod)
                            connection.priv_msg_observable._observers.append(
                                _new_mod.ComicObserver()
                            )

                        case "urban":
                            import faustbot.modules.UrbanObserver as _new_mod

                            _new_mod = reload(_new_mod)
                            connection.priv_msg_observable._observers.append(
                                _new_mod.UrbanObserver()
                            )

                        case "title":
                            import faustbot.modules.TitleObserver as _new_mod

                            _new_mod = reload(_new_mod)
                            connection.priv_msg_observable._observers.append(
                                _new_mod.TitleObserver()
                            )

                        case _:
                            _has_reloaded_mod = False

                    if _has_reloaded_mod:
                        connection.send_back(
                            f"\001ACTION hat das Modul {_mod} neu eingeladen.\001",
                            data,
                        )
                else:
                    connection.send_back(
                        f"\001ACTION ist ratlos wie eins {_mod} neu einlädt.\001",
                        data,
                    )

            # connection.send_back(
            #     f"\001ACTION schenkt {data.get('nick')} {choice(_response_bean_list)}.\001",
            #     data,
            # )
