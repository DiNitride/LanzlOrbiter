import os
import logging

from lanzl import LanzlOrbiter

os.chdir("lanzl")
logger = logging.getLogger("lanzl")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)8s [%(name)s] : %(message)s'))
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)
LanzlOrbiter().run()