import config
import requests
import json


def my_open_request(SD_token):
    url = config.url_SD + "requests"
    headers = {"authtoken": SD_token}

    input_data = '''{
        "list_info": {
            "row_count": 20,
            "start_index": 1,
            "sort_field": "id",
            "sort_order": "desc",
            "get_total_count": true,
            "search_fields": {
                "group.name": "IT отдел",
                "status.name": "Open"
            }
            
        }
    }'''
    params = {'input_data': input_data}
    response = requests.get(url,headers=headers,params=params,verify=True)
    if response.status_code == 200:
        result = []
        data = json.loads(response.text)
        row_count = data['list_info']['row_count']
        for i in range(0, row_count):
            result.append([data['requests'][i]['id'], data['requests'][i]['requester']['email_id'], data['requests'][i]['subject'], data['requests'][i]['short_description']])
        return (result)
    else:
        return ("Ошибка получения данных с сервера")



