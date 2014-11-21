import logging

from app.listener import ClientListener

logging.basicConfig(filename='access.log', level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

proxy = ClientListener()
