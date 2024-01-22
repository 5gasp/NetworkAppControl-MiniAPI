# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2023-05-22 11:45:25
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-12-31 18:12:21

from enum import Enum
 
class OPERATION(Enum):
    ### NEF
    NEF_AUTHENTICATION = 'Def19Sec9'
    AUTHENTICATION_WITH_5GS = 'Def115G1'
    CREATE_UE = '2'
    GET_UES = '3'
    NEF_LOCATION_SUBSCRIPTION = 'Def115G2'
    UE_PATH_LOSS = 'Def115G5'
    SERVING_CELL_INFO = 'Def115G6'
    HANDOVER = 'Def115G3'
    SUBSCRIBE_QOS_EVENT = "Def115G7"
    E2E_SINGLE_UE_LATENCY_AND_THROUGHPUT = "Def14Perf1"
    E2E_MULTIPLE_UE_LATENCY_AND_THROUGHPUT = "Def14Perf2"
    ### AVAILABILITY
    E2E_UE_PERFORMANCE = '7'
    E2E_UE_RTT_PERFORMANCE = '8'
    MAX_HOPS = "Def14Perf13"
    MAX_CONNECTIONS = "Def14Perf11"
    NEF_CALLBACK_MAX_CONNECTIONS = "Def14Perf7"