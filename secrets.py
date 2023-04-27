import dotenv
from dotenv import load_dotenv
import os
import dataclasses

dotenv.load_dotenv()


@dataclasses.dataclass
class SecretInfo:
    DATABASE_NAME: str
    DATABASE_LOGIN: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str


secret = SecretInfo(DATABASE_NAME=os.getenv('DATABASE_NAME'),
                    DATABASE_LOGIN=os.getenv('DATABASE_LOGIN'),
                    DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD'),
                    DATABASE_HOST=os.getenv('DATABASE_HOST'),
                    DATABASE_PORT=os.getenv('DATABASE_PORT')
                    )