from kwldn_bot import BasicBotConfig, load_config
from pydantic import BaseModel


class AccountData(BaseModel):
    username: str
    password: str


class SolverBotConfig(BasicBotConfig):
    account: AccountData


config: SolverBotConfig = load_config(SolverBotConfig, {
    'account': {
        'username': '',
        'password': ''
    }
})
