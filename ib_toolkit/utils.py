import ipaddress

import requests
import json
import os
from django.core.validators import RegexValidator

infoblox = os.environ.get("INFOBLOX_GRIDMASTER", default='10.0.0.241')
ib_username = os.environ.get("INFOBLOX_USERNAME", default='admin'),
ib_password = os.environ.get("INFOBLOX_PASSWORD", default='infoblox')




alphanumeric_and_underscore_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_]+$',
    message='Only alphanumeric characters and underscores are allowed.',
    code='invalid_character'
)

cidr_validator = RegexValidator(
    regex=r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$',  # Regular expression for CIDR notation validation
    message='Enter a valid CIDR notation (e.g., 192.168.0.0/24).',
    code='invalid_cidr'
)


def err_res(message, details=None, error_code=None):
    return {'status': False, 'message': message, 'details': details, 'error_code': error_code}


def create_next_avail_network_container(parent_network: str, new_network_size: int, new_network_name):
    url = f"https://{infoblox}/wapi/v2.11.2/request"
    payload = [
        {
            "method": "GET",
            "object": "networkcontainer",
            "data": {
                # "*SifLoc:": "Texas",
                "network": parent_network,
                "network_view": "default"
            },
            "assign_state": {
                "netw_ref": "_ref"
            },
            "discard": True
        },
        {
            "method": "POST",
            "object": "networkcontainer",
            "data": {
                "network": {
                    "_object_function": "next_available_network",
                    "_result_field": "networks",
                    "_parameters": {
                        "cidr": new_network_size
                    },
                    "_object_ref": "##STATE:netw_ref:##"
                },
                "network_view": "default",
                "comment": new_network_name,
                # "extattrs": {
                #     "Test1": {
                #         "value": "dg11"
                #     },
                #     "Test2": {
                #         "value": "vince"
                #     }
                # }
            },
            "enable_substitution": True
        }
    ]
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False, auth=("admin", "infoblox"))
    except requests.exceptions.HTTPError as http_err:
        message = f'HTTP error occurred connecting to Infoblox: {http_err}'
        print(message)
        return err_res(message, error_code="ib_connection_error")
    except requests.exceptions.ConnectionError as conn_err:
        message = f'Error connecting to Infoblox: {conn_err}'
        print(message)
        return err_res(message, error_code="ib_connection_error" )
    except requests.exceptions.Timeout as timeout_err:
        message = f'Timeout to Infoblox error: {timeout_err}'
        print(message)
        return err_res(message, error_code="ib_connection_error")
    except Exception as err:
        message = f'An error occurred sending request to infoblox: {err}'
        print(message)
        return err_res(message, error_code="ib_connection_error")
    print(response.text)
    # print(response.status_code)
    # print(response)

    if response.status_code == 201:
        # Network Container was created
        network = json.loads(response.text)[0].split('/')

        message = f"Network {network[1].split(':')[1]}/{network[2]}  was assigned"
        return {'status': True, 'message': message, 'details': {
            'network': f"{network[1].split(':')[1]}/{network[2]}",
            'infoblox_ref': f"{network[1]}"
        }}
    elif response.status_code == 401:
        # Credentials for infoblox grid master is incorrect
        message = f"Unable to authenticate to Infoblox grid master ({infoblox})"
        return err_res(message)
    elif response.status_code == 400:
        message = json.loads(response.text)['Error']
        print(message)
        return err_res(message)
    else:
        message = response.text
        return err_res(message)


def create_host_record(fqdn: str, ip_address: ipaddress.IPv4Address):
    url = f"https://{infoblox}/wapi/v2.11.2/record:host"

    # define parameters
    params = {
        "_return_fields+": "name,network_view",
        "_return_as_object": 1
    }

    # Headers
    headers = {
        "Content-Type": "application/json",
    }

    # Data
    data = {
        "name": f'{fqdn}',
        "ipv4addrs": [
            {
                "ipv4addr": f'{ip_address}'
            }
        ],
        "view": "default"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), params=params, auth=('admin', 'infoblox'), verify=False)
    except requests.exceptions.HTTPError as http_err:
        message = f'HTTP error occurred connecting to Infoblox: {http_err}'
        print(message)
        return err_res(message)
    except requests.exceptions.ConnectionError as conn_err:
        message = f'Error connecting to Infoblox: {conn_err}'
        print(message)
        return err_res(message)
    except requests.exceptions.Timeout as timeout_err:
        message = f'Timeout to Infoblox error: {timeout_err}'
        print(message)
        return err_res(message)
    except Exception as err:
        message = f'An error occurred sending request to infoblox: {err}'
        print(message)
        return err_res(message)
    print(response.text)
    # print(response.status_code)
    # print(response)

    if response.status_code == 201:
        # Network Container was created
        host = json.loads(response.text)

        # message = f"Network {network[1].split(':')[1]}/{network[2]}  was assigned"
        message = response.text
        return {'status': True, 'message': message}
    elif response.status_code == 401:
        # Credentials for infoblox grid master is incorrect
        message = f"Unable to authenticate to Infoblox grid master ({infoblox})"
        return err_res(message)
    elif response.status_code == 400:
        message = json.loads(response.text)['Error']
        print(message)
        return err_res(message)
    else:
        message = response.text
        return err_res(message)

