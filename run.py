import logging
import os

from lanzl import LanzlOrbiter
from lanzl.modules.suggestions_board import Suggestions

os.chdir("lanzl")
logger = logging.getLogger("lanzl")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)8s [%(name)s] : %(message)s'))
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)
LanzlOrbiter().run()
