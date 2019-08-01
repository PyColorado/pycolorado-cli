import fire
from dotenv import load_dotenv

from commands import commands

load_dotenv()

fire.Fire(commands)
