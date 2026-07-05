from faustbot.communication.Connection import Connection
from faustbot.model.Config import Config
from faustbot.model.ConnectionDetails import ConnectionDetails
from faustbot.modules import (
    ActivityObserver,
    AllSeenObserver,
    BaseObserver,
    BastelObserver,
    BlockObserver,
    CharactersCountObserver,
    ComicObserver,
    ConvertObserver,
    DiceObserver,
    DuckObserver,
    First_Greeter,
    FortuneObserver,
    FreeHugsObserver,
    GiveCookieObserver,
    GiveDrinkObserver,
    GiveDrinkToObserver,
    GiveFoodObserver,
    GiveIceObserver,
    Greeter,
    HangmanObserver,
    HelpObserver,
    HilfeObserver,
    ICD11Observer,
    IdentNickServObserver,
    IntroductionObserver,
    JokeObserver,
    Kicker,
    LagObserver,
    LetterObserver,
    LoveAndPeaceObserver,
    MathObserver,
    MathRunObserver,
    ModulePrototype,
    OeisObserver,
    PartyObserver,
    PingAnswerObserver,
    PrideObserver,
    PubmedObserver,
    SeenObserver,
    SnacksObserver,
    TellObserver,
    ThemaObserver,
    TitleObserver,
    UrbanObserver,
    UserList,
    WeatherObserver,
    WhoObserver,
    WikiObserver,
    WordRunObserver,
)
from faustbot.modules.CustomUserModules import (
    GlossaryModule,
    ICDObserver,
    ModmailObserver,
)
from faustbot import logger
from faustbot.extras import (
    bbb,
    module_reloader
)

class FaustBot(object):
    def __init__(self, config_path: str):
        self._config = Config(config_path)
        connection_details = ConnectionDetails(self.config)
        self._connection = Connection(connection_details)

    @property
    def config(self):
        return self._config

    def _setup(self):
        self._connection.establish()
        user_list = UserList.UserList()
        self._connection.priv_msg_observable.define_user_list(user_list)
        self.add_module(user_list)
        self.add_module(ActivityObserver.ActivityObserver())
        self.add_module(WhoObserver.WhoObserver(user_list))
        self.add_module(AllSeenObserver.AllSeenObserver(user_list))
        self.add_module(PingAnswerObserver.ModulePing())
        self.add_module(
            Kicker.Kicker(user_list, self._config.idle_warn, self._config.idle_kick)
        )  # only in #autistenchat
        self.add_module(LagObserver.LagObserver(self._connection))
        self.add_module(SeenObserver.SeenObserver())
        self.add_module(TitleObserver.TitleObserver())
        self.add_module(WikiObserver.WikiObserver())
        self.add_module(ModmailObserver.ModmailObserver())
        self.add_module(ICDObserver.ICDObserver())
        self.add_module(GlossaryModule.GlossaryModule(self._config))
        self.add_module(IdentNickServObserver.IdentNickServObserver())
        self.add_module(GiveDrinkObserver.GiveDrinkObserver())
        self.add_module(GiveCookieObserver.GiveCookieObserver())
        self.add_module(LoveAndPeaceObserver.LoveAndPeaceObserver())
        self.add_module(FreeHugsObserver.FreeHugsObserver())
        self.add_module(GiveFoodObserver.GiveFoodObserver())
        self.add_module(ComicObserver.ComicObserver())
        self.add_module(HangmanObserver.HangmanObserver())
        self.add_module(HelpObserver.HelpObserver())
        self.add_module(IntroductionObserver.IntroductionObserver(user_list))
        self.add_module(DuckObserver.DuckObserver())
        self.add_module(JokeObserver.JokeObserver())
        self.add_module(TellObserver.TellObserver())
        self.add_module(WordRunObserver.WordRunObserver())
        self.add_module(GiveIceObserver.GiveIceObserver())
        self.add_module(GiveDrinkToObserver.GiveDrinkToObserver())
        self.add_module(Greeter.Greeter(self.config.greeting))
        self.add_module(First_Greeter.First_Greeter(self.config.first_greeting))
        self.add_module(MathRunObserver.MathRunObserver())
        self.add_module(PartyObserver.PartyObserver())
        self.add_module(PrideObserver.PrideObserver())
        self.add_module(SnacksObserver.SnacksObserver())
        self.add_module(BlockObserver.BlockObserver())
        self.add_module(LetterObserver.LetterObserver())
        self.add_module(DiceObserver.DiceObserver())
        self.add_module(CharactersCountObserver.CharactersCountObserver())
        self.add_module(BastelObserver.BastelObserver())
        self.add_module(UrbanObserver.UrbanObserver())  # only in #autistenchat-fsk18
        self.add_module(PubmedObserver.PubmedObserver())  # only, maybe in #autistenchat-si
        self.add_module(ThemaObserver.ThemaObserver())
        self.add_module(ICD11Observer.ICD11Observer())
        self.add_module(HilfeObserver.HilfeObserver())
        self.add_module(OeisObserver.OeisObserver())  # only, maybe in #autistenchat-si
        self.add_module(WeatherObserver.WeatherObserver())
        self.add_module(MathObserver.MathObserver())
        self.add_module(BaseObserver.BaseObserver())
        self.add_module(ConvertObserver.ConvertObserver())
        self.add_module(FortuneObserver.FortuneObserver())
        self.add_module(bbb.BBB())
        self.add_module(module_reloader.ModuleReloader())

    def run(self):
        self._setup()
        running = True
        while running:
            if not self._connection.receive():
                return

    def add_module(self, module: ModulePrototype):
        _module_name = str(module.__class__.__name__)
        if _module_name in self._config.blacklist:
            logger.info(f"Module {_module_name} not loaded (blacklisted)")
        else:
            self._add_to_observable_by_function_existence(module)
            module.config = self._config
            logger.info(f"Module {_module_name} loaded.")

    def _add_to_observable_by_function_existence(self, module):
        _module_functions = module.__dir__()
        if "update_on_join" in _module_functions:
            self._connection.join_observable.add_observer(module)
        if "update_on_leave" in _module_functions:
            self._connection.leave_observable.add_observer(module)
        if "update_on_kick" in _module_functions:
            self._connection.kick_observable.add_observer(module)
        if "update_on_priv_msg" in _module_functions:
            self._connection.priv_msg_observable.add_observer(module)
        if "update_on_nick_change" in _module_functions:
            self._connection.nick_change_observable.add_observer(module)
        if "update_on_ping" in _module_functions:
            self._connection.ping_observable.add_observer(module)
        if "update_on_pong" in _module_functions:
            self._connection.pong_observable.add_observer(module)
        if "update_on_notice" in _module_functions:
            self._connection.notice_observable.add_observer(module)
        if "update_on_magic_number" in _module_functions:
            self._connection.magic_number_observable.add_observer(module)
