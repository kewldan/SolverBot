from kwldn_bot import BasicBotConfig, load_config
from pydantic import BaseModel


class AccountData(BaseModel):
    username: str
    password: str


class WebConfig(BaseModel):
    base_url: str
    port: int


class SolverBotConfig(BasicBotConfig):
    account: AccountData
    web: WebConfig


config: SolverBotConfig = load_config(SolverBotConfig, {
    'account': {
        'username': '',
        'password': ''
    },
    'web': {
        'base_url': 'https://',
        'port': 3036
    }
})
