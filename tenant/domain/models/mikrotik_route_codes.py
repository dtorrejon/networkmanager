from enum import Enum


class MikrotikRouteCodes(Enum):
    DISABLED = 'X'
    ACTIVE = 'A'
    INACTIVE = 'I'
    DYNAMIC = 'D'
    CONNECT = 'C'
    STATIC = 'S'
    RIP = 'r'
    BGP = 'b'
    OSPF = 'o'
    MME = 'm'
    BLACKHOLE = 'B'
    UNREACHABLE = 'U'
    PROHIBIT = 'P'


    @staticmethod
    def get_names_in_a_list() -> list:
        route_codes_list: list[str] = []
        for member in MikrotikRouteCodes:
            route_codes_list.append(member.name)
        return route_codes_list

    @staticmethod
    def get_names_in_a_string() -> str:
        return " ".join(MikrotikRouteCodes.get_names_in_a_list())

    @staticmethod
    def get_values_in_a_list() -> list:
        route_codes_list: list[str] = []
        for member in MikrotikRouteCodes:
            route_codes_list.append(member.value)
        return route_codes_list

    @staticmethod
    def get_values_in_a_string() -> str:
        return " ".join(MikrotikRouteCodes.get_values_in_a_list())