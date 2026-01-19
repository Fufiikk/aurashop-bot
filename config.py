from dataclasses import dataclass
import os


@dataclass(slots=True)
class Config:
    bot_token: str
    bot_username: str
    admin_ids: list[int]
    channel_id: int

def load_config() -> Config:
    token = "8457065938:AAHxP4qPIyXinWbRhUFslSrpsXSHfVG_JlE"
    bot_username = "testnaxuisuka_bot"  # 👈 БЕЗ @
    channel_id = -1003544547966

    admins = "6630175448"
    admin_ids = [int(x) for x in admins.split(",") if x]

    return Config(
        bot_token=token,
        bot_username=bot_username,
        admin_ids=admin_ids,
        channel_id=channel_id
    )

