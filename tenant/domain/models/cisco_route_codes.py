from enum import Enum


class CiscoRouteCodes(Enum):
    LOCAL = 'L'
    CONNECTED = 'C'
    STATIC = 'S'
    RIP = 'R'
    MOBILE = 'M'
    BGP = 'B'
    EIGRP = 'D'
    EIGRP_EXTERNAL = 'EX'
    OSPF = 'O'
    INTER_AREA = 'IA'
    NSSA_EXTERNAL_TYPE_1 = 'N1'
    NSSA_EXTERNAL_TYPE_2 = 'N2'
    EXTERNAL_TYPE_1 = 'E1'
    EXTERNAL_TYPE_2 = 'E2'
    IS_IS = 'i'
    IS_IS_SUMMARY = 'su'
    IS_IS_LEVEL_1 = 'L1'
    IS_IS_LEVEL_2 = 'L2'
    IS_IS_INTER_AREA = 'ia'
    CANDIDATE_DEFAULT = '*'
    PER_USER_STATIC_ROUTE = 'U'
    ODR = 'o'
    PERIODIC_DOWNLOADED_STATIC_ROUTE = 'P'
    NHRP = 'H'
    LISP = 'l'
    APPLICATION_ROUTE = 'a'
    REPLICATED_ROUTE = '+'
    NEXT_HOP_OVERRIDE = '%'
    PFR_OVERRIDES = 'p'
    IGRP = 'I'
    EGP = 'E'
    LOCAL_CANDIDATE_DEFAULT = 'L*'
    CONNECTED_CANDIDATE_DEFAULT = 'C*'
    STATIC_CANDIDATE_DEFAULT = 'S*'
    RIP_CANDIDATE_DEFAULT = 'R*'
    MOBILE_CANDIDATE_DEFAULT = 'M*'
    BGP_CANDIDATE_DEFAULT = 'B*'
    EIGRP_CANDIDATE_DEFAULT = 'D*'
    EIGRP_EXTERNAL_CANDIDATE_DEFAULT = 'EX*'
    OSPF_CANDIDATE_DEFAULT = 'O*'
    INTER_AREA_CANDIDATE_DEFAULT = 'IA*'
    NSSA_EXTERNAL_TYPE_1_CANDIDATE_DEFAULT = 'N1*'
    NSSA_EXTERNAL_TYPE_2_CANDIDATE_DEFAULT = 'N2*'
    EXTERNAL_TYPE_1_CANDIDATE_DEFAULT = 'E1*'
    EXTERNAL_TYPE_2_CANDIDATE_DEFAULT = 'E2*'
    IS_IS_CANDIDATE_DEFAULT = 'i*'
    IS_IS_SUMMARY_CANDIDATE_DEFAULT = 'su*'
    IS_IS_LEVEL_1_CANDIDATE_DEFAULT = 'L1*'
    IS_IS_LEVEL_2_CANDIDATE_DEFAULT = 'L2*'
    IS_IS_INTER_AREA_CANDIDATE_DEFAULT = 'ia*'
    PER_USER_STATIC_ROUTE_CANDIDATE_DEFAULT = 'U*'
    ODR_CANDIDATE_DEFAULT = 'o*'
    PERIODIC_DOWNLOADED_STATIC_ROUTE_CANDIDATE_DEFAULT = 'P*'
    NHRP_CANDIDATE_DEFAULT = 'H*'
    LISP_CANDIDATE_DEFAULT = 'l*'
    APPLICATION_ROUTE_CANDIDATE_DEFAULT = 'a*'
    REPLICATED_ROUTE_CANDIDATE_DEFAULT = '+*'
    NEXT_HOP_OVERRIDE_CANDIDATE_DEFAULT = '%*'
    PFR_OVERRIDES_CANDIDATE_DEFAULT = 'p*'
    IGRP_CANDIDATE_DEFAULT = 'I*'
    EGP_CANDIDATE_DEFAULT = 'E*'

    @staticmethod
    def get_names_in_a_list() -> list:
        route_codes_list: list[str] = []
        for member in CiscoRouteCodes:
            route_codes_list.append(member.name)
        return route_codes_list

    @staticmethod
    def get_names_in_a_string() -> str:
        return " ".join(CiscoRouteCodes.get_names_in_a_list())

    @staticmethod
    def get_values_in_a_list() -> list:
        route_codes_list: list[str] = []
        for member in CiscoRouteCodes:
            route_codes_list.append(member.value)
        return route_codes_list

    @staticmethod
    def get_values_in_a_string() -> str:
        return " ".join(CiscoRouteCodes.get_values_in_a_list())
