# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   2023-05-22 11:40:10
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-05-22 16:39:58
import requests
import json 

def login (ip, port, username, password):

    login_url = f"http://{ip}:{port}/api/v1/login/access-token"
    headers = {}
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }

    response = requests.post(
        url=login_url,
        headers=headers,
        data=data
    )
    
    # Check if the login was successful
    if response.status_code not in [200, 201, 409]:
        response.raise_for_status()


    print("Login Response:", response.text)
    resp_content = response.json()
    token = resp_content["access_token"]

    return token


def get_ues(ip, port, token):

    url = f"http://{ip}:{port}/api/v1/UEs"
        
    headers = {}
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + token
    headers["Content-Type"] = "application/json"
    

    response = requests.get(
        url=url,
        headers=headers, 
    )
    
    print("Get UEs Response:", response.text)
    if response.status_code not in [200, 201, 409]:
        response.raise_for_status()


def subscribe_event (ip, port, callback_url, monitoring_type,
                     monitoring_expire_time, token):

    url = f"http://{ip}:{port}/nef/api/v1/3gpp-monitoring-event/" \
        "v1/netapp/subscriptions"
        
    headers = {}
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + token
    headers["Content-Type"] = "application/json"
    
    monitoring_payload = {
        "externalId": "123456789@domain.com",
        "notificationDestination": callback_url,
        "monitoringType": monitoring_type,
        "maximumNumberOfReports": 1,
        "monitorExpireTime": monitoring_expire_time,
        "maximumDetectionTime": 1,
        "reachabilityType": "DATA"
    }

    response = requests.post(
        url=url,
        headers=headers, 
        data=json.dumps(monitoring_payload)
    )
    
    print("Monitoring Subscription Response:", response.text)
    if response.status_code not in [200, 201, 409]:
        response.raise_for_status()

    


def create_ue(ip, port, ue_name, ue_description, 
              ue_ipv4, ue_ipv6, ue_mac, ue_supi, token):
    
    url = f"http://{ip}:{port}/api/v1/UEs"
        
    headers = {}
    headers["accept"] = "application/json"
    headers["Authorization"] = "Bearer " + token
    headers["Content-Type"] = "application/json"
    
    payload = {
        "name": ue_name,
        "description": ue_description,
        "ip_address_v4": ue_ipv4,
        "ip_address_v6": ue_ipv6,
        "mac_address": ue_mac,
        "supi": ue_supi,
    }
    
    response = requests.post(
        url=url,
        headers=headers, 
        data=json.dumps(payload)
    )
    
    print("Create UE Response:", response.text)
    if response.status_code not in [200, 201, 409]:
        response.raise_for_status()