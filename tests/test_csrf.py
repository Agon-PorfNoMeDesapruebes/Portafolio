import re


def get_token(client, url):
    html = client.get(url).get_data(as_text=True)
    return re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html).group(1)


def login(client):
    token = get_token(client, '/auth/login')
    return client.post(
        '/auth/login',
        data={'username': 'test', 'password': 'test', 'csrf_token': token}
    )


def test_login_sin_token_es_rechazado(csrf_client):
    response = csrf_client.post(
        '/auth/login', data={'username': 'test', 'password': 'test'}
    )
    assert response.status_code == 400


def test_login_con_token_funciona(csrf_client):
    assert login(csrf_client).headers['Location'] == '/'


def test_logout_por_get_no_esta_permitido(csrf_client):
    login(csrf_client)
    assert csrf_client.get('/auth/logout').status_code == 405


def test_logout_sin_token_es_rechazado(csrf_client):
    login(csrf_client)
    assert csrf_client.post('/auth/logout').status_code == 400


def test_delete_sin_token_es_rechazado(csrf_client):
    login(csrf_client)
    assert csrf_client.post('/1/delete').status_code == 400


def test_delete_con_token_funciona(csrf_client):
    login(csrf_client)
    token = get_token(csrf_client, '/1/update')
    response = csrf_client.post('/1/delete', data={'csrf_token': token})
    assert response.headers['Location'] == '/'