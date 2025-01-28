import json
import requests

def check_imei(imei: str):
    url = 'https://api.imeicheck.net/v1/checks'
    token = 'e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'
    # token_my_live = 'kFeytFznfuSBxLqcOoz44sy3nvN4fsbxMKNTvm3Q75917e15'
    # token_my_sandbox = '52PDPPN1t72bNRBmorGP0nJUA3yqkD1CsyoZ4N1E8096e161'

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    access_status = False
    body = json.dumps({
        "deviceId": imei,
        # Тестовый сервис дающий смешанный результат - N15
        "serviceId": 15
    })
    response = requests.post(url, headers=headers, data=body)
    data = response.json()
    response_code = response.status_code
    if response_code == 403:
        print('Нет доступа к api')

    if 'errors' in data:
        try:
            data = {'check_result': data['errors']['deviceId'][0]}
            print('Device is invalid.')
            return data
        except Exception as e:
            print(data['errors'])
            print('Service is invalid for you model.')
            data = {'check_result': 'Service is invalid for you model'}
            return data

    elif 'code' in data:
        print(data['code'])
        data = {'check_result': data['code']}
        return data

    elif 'message' in data:
        print(data['message'])
        data = {'check_result': data['code']}
        return data

    for j in data:
        print(j, ': ', data[j])

    try:
        if data['status'] == 'successful':
            print('Thats ok.')
            data['check_result'] = 'PHONE IS VALID'
            # Флаг какого нибудь разрешения доступа к чему нибудь
            access_status = True
        elif data['status'] == 'failed':
            print('Something went wrong')
            data = {'check_result': 'Something went wrong'}
        else:
            print('You phone is a not valid.')
            data = {'check_result': 'You phone is a not valid.'}
            access_status = False

    except Exception as exc:
        print(exc)
        res = {'error': 'Something went wrong'}
        return res
    print('---------------------------------------------------')
    if response.status_code == 200:
        return response.json().get("result", "Ответ от сервиса не содержит данных.")
    elif response.status_code == 201:
        return data
    else:
        return f"Ошибка при запросе к сервису: {response.status_code}"

def format_dict_to_string(data, indent=0):
    result = ""
    for key, value in data.items():
        # Если значение — словарь
        if isinstance(value, dict):
            result += " " * indent + f"{key}:\n"
            result += format_dict_to_string(value, indent + 4)
        # Если значение — список
        elif isinstance(value, list):
            result += " " * indent + f"{key}:\n"
            for item in value:
                result += " " * (indent + 4) + f"- {item}\n"
        else:
            result += " " * indent + f"{key}: {value}\n"
    return result

#format_dict_to_string(check_imei('350356670657487'))