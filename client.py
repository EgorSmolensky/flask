import requests


def take_info(r):
    print('Status code:', r.status_code)
    print(r.json())
    print('-----------------------------')
    print()


print('создание пользователей')
response = requests.post('http://127.0.0.1:5000/register/', json={"email": "user1@mail.ru", "password": "Password1@"})
take_info(response)

response = requests.post('http://127.0.0.1:5000/register/', json={"email": "user2@mail.ru", "password": "Password2@"})
take_info(response)

response = requests.post('http://127.0.0.1:5000/register/', json={"email": "user3@mail.ru", "password": "Password3@"})
take_info(response)


print('создание объявлений')
advt = {
    "title": "Котята",
    "description": "Отдам котят бесплатно. Ласковые, любят помурчать, к лотку приучены",
    "owner_id": 1,
}
response = requests.post('http://127.0.0.1:5000/ads/', json=advt)
take_info(response)

advt = {
    "title": "Продам квартиру",
    "description": "100 квадратов, в центре города",
    "owner_id": 2,
}
response = requests.post('http://127.0.0.1:5000/ads/', json=advt)
take_info(response)

advt = {
    "title": "Приму непригодный грунт",
    "description": "От 5 кубов",
    "owner_id": 3,
}
response = requests.post('http://127.0.0.1:5000/ads/', json=advt)
take_info(response)

print('список всех объявлений')
response = requests.get('http://127.0.0.1:5000/ads/')
take_info(response)

print('просмотреть объявление')
response = requests.get('http://127.0.0.1:5000/ads/2/')
take_info(response)

print('изменение объявления')
advt = {
    "description": "Двухуровневая, 100 квадратов, в центре города"
}
response = requests.patch('http://127.0.0.1:5000/ads/2/', json=advt)
take_info(response)

print('просмотреть объявление после изменения')
response = requests.get('http://127.0.0.1:5000/ads/2/')
take_info(response)

print('удаление объявления')
response = requests.delete('http://127.0.0.1:5000/ads/3/')
take_info(response)

print('список всех объявлений после удаления')
response = requests.get('http://127.0.0.1:5000/ads/')
take_info(response)
