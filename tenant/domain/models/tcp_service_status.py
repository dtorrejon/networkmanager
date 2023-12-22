import socket

from tenant.domain.ports.interface_service_status import IServiceStatus


class TCPServiceStatus(IServiceStatus):
    @staticmethod
    def status(hostname: str, port: int) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            if sock.connect_ex((hostname, port)) == 0:
                return True
            return False
        except socket.error as error:
            return False
