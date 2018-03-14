import logging
from SocketServer import BaseServer

logger = logging.getLogger('uvcsite.ukh.schulportal')


def my_handle_error(self, request, client_address):
    return

BaseServer.handle_error = my_handle_error


def log(message, summary='', severity=logging.DEBUG):
    logger.log(severity, '%s %s', summary, message)
