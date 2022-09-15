import requests

url = 'https://yandex.ru/dev/id/doc/dg/oauth/reference/auto-code-client.html#auto-code-client__get-token'
url = 'https://oauth.yandex.ru/authorize'

params = {
    'response_type': 'token',
    'redirect_uri': 'https://oauth.yandex.ru/verification_code',
    'client_id': 'bb153a621888486bbd37256bbe8a1430',
}

resp = requests.request(method='GET',
                        url=url,
                        params=params)

print(resp)


# y0_AgAAAABkg3QaAAhoPQAAAADOpVkAeppIeFiZSxCE65_ZSvsjnx-2CgE