import random
import time

from faustbot.communication.Connection import Connection
from faustbot.model.UserProvider import UserProvider
from faustbot.modules.UserList import UserList
from faustbot.extras.getraenke import Getraenke
from faustbot.extras.essen import essen
from faustbot.extras.icecreamlist import icecream

from faustbot.modules.PingObserverPrototype import PingObserverPrototype
from faustbot.modules.PongObserverPrototype import PongObserverPrototype
from faustbot import logger

getraenke = Getraenke()

class Kicker(PingObserverPrototype, PongObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self, user_list: UserList, idle_warn: int, idle_kick: int):
        logger.debug(f"Initialized with idle_warn: {idle_warn} and idle_kick {idle_kick}")
        super().__init__()
        self.idle_warn = idle_warn
        self.idle_kick = idle_kick
        self.user_list = user_list
        self.warned_users = {}

    def update_on_ping(self, data, connection: Connection):
        for user in self.user_list.userList.keys():
            offline_time = Kicker.get_offline_time(user)

            # Skip Statt and 'self'
            host = self.user_list.userList.get(user).host
            if "libera/staff/" in host or user == connection.details.get_nick():
                continue
            logger.debug(f"Kicker-Debug: {user} is inactive for {offline_time}s")

            if user in self.warned_users:
                if offline_time < self.idle_warn:
                    self.warned_users.pop(user)
                    logger.debug(
                        f"Kicker-Debug: {user} is active again, warning-state deleted."
                    )
                elif (offline_time - self.warned_users.get(user, 0)) > self.idle_kick:
                    # connection.send_channel(
                    #     f"\001ACTION würde jetzt eigentlich {user} kicken weil {offline_time}.\001"
                    # )
                    connection.raw_send(
                        f"KICK {connection.details.get_channel()} {user} :Zu lang geidlet, komm gerne wieder!"
                    )
                    self.warned_users.pop(user)
                    logger.debug(f"Kicker-Debug: {user} has been kicked.")
            elif user not in self.warned_users:
                if offline_time > self.idle_warn:
                    connection.send_channel(
                        f"\001ACTION serviert {user} {random.choice(getraenke + essen + icecream)}.\001"
                    )
                    self.warned_users.update({user: offline_time})
                    logger.debug(f"Kicker-Debug: {user} has been warned.")

    def update_on_pong(self, data, connection):
        self.update_on_ping(data, connection)

    @staticmethod
    def get_offline_time(nick):
        who = nick
        user_provider = UserProvider()
        activity = user_provider.get_activity(who)
        delta = time.time() - activity
        return delta
