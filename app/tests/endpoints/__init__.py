def handle_data(response, data, message_not_found, single_check_data, type='single'):
    assert response.status_code in [200, 404]
    # If you have specific expectations for the response content in each case, you can add further assertions
    if response.status_code == 200:
        if type == "multiple":
            # Assert specific content expectations for a successful response
            assert len(data['data']) > 0
        elif type == "single":
            assert data['data'][single_check_data] is not None
    elif response.status_code == 404:
        # Assert specific content expectations for a 404 response
        assert data['data']['message'] == message_not_found

def handle_data_user(response, data, type='single'):
    handle_data(response, data, "Users not found", 'username', type)

def handle_data_article(response, data, type='single'):
    handle_data(response, data, "Article not found", 'slug', type)
