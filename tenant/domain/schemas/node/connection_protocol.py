from enum import Enum, verify, UNIQUE


@verify(UNIQUE)
class ConnectionProtocol(str, Enum):
    SSH = "ssh"
    TELNET = "telnet"
    NETCONF = "netconf"
    API_HTTPS = "api_https"
    API_HTTP = "api_http"
    API = "api"


class ConnectionProtocolDefaultPort(Enum):
    SSH = 22
    TELNET = 23
    NETCONF = 830
    API_HTTPS = 443
    API_HTTP = 80
    API = 443


if __name__ == '__main__':
    pass
