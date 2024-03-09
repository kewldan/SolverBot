from kwldn_bot import BasicBotConfig
from pydantic import BaseModel


class AccountData(BaseModel):
    username: str = ''
    password: str = ''


class WebConfig(BaseModel):
    base_url: str = 'https://'
    port: int = 3036


class SolverBotConfig(BasicBotConfig):
    account: AccountData = AccountData()
    web: WebConfig = WebConfig()


config = SolverBotConfig()
