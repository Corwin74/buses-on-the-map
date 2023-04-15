# pylint: disable=C0301

TEST_MESSAGE_1 = '"dd"'
TEST_MESSAGE_2 = '{"msgType": "Buses", "buses": [{"busId": "c790\u0441\u0441", "lat": 55.75, "lng": 37.6, "route": "120"}, {"busId": "a134aa", "lat": 55.7494, "lng": 37.621, "route": "670\u043a"}]}'  # noqa: E501
TEST_MESSAGE_3 = '{"msgType": "Buse"}'
TEST_MESSAGE_4 = '{"msgType": "Buses", "buse": [{"busId": "c790\u0441\u0441", "lat": 55.75, "lng": 37.6, "route": "120"}, {"busId": "a134aa", "lat": 55.7494, "lng": 37.621, "route": "670\u043a"}]}'  # noqa: E501
TEST_MESSAGE_5 = '{"msgType": "Buses", "buses": [{"busId": "c790\u0441\u0441", "lat": 155.75, "long": 37.6, "route": "120"}, {"busId": "a134aa", "lat": 55.7494, "lng": 37.621, "route": "670\u043a"}]}'  # noqa: E501

TEST_REPLY_1 = '{"msgType": "Errors", "errors": ["\'dd\' is not of type \'object\'"]}'  # noqa: E501
TEST_REPLY_2 = 'OK'
TEST_REPLY_3 = '{"msgType": "Errors", "errors": ["\'buses\' is a required property", "\'Buses\' was expected"]}'  # noqa: E501
TEST_REPLY_4 = '{"msgType": "Errors", "errors": ["Additional properties are not allowed (\'buse\' was unexpected)", "\'buses\' is a required property"]}'  # noqa: E501
TEST_REPLY_5 = '{"msgType": "Errors", "errors": ["Additional properties are not allowed (\'long\' was unexpected)", "\'lng\' is a required property", "155.75 is greater than the maximum of 90"]}'  # noqa: E501


TEST_BROWSER_MESSAGE_1 = '{"msgType": "newBounds", "data": {"east_lng": 37.65563964843751, "north_lat": 55.77367652953477, "south_lat": 55.72628839374007, "west_lng": 37.54440307617188} }'  # noqa: E501
TEST_BROWSER_REPLY_1 = '{"msgType": "Buses", "buses": [{"busId": "c790\\u0441\\u0441", "lat": 55.75, "lng": 37.6, "route": "120"}, {"busId": "a134aa", "lat": 55.7494, "lng": 37.621, "route": "670\\u043a"}]}'  # noqa: E501

TEST_BROWSER_MESSAGE_2 = '{"msgType": "newBounds", "data": {"east_lng": 38.1, "north_lat": 55.7495, "south_lat": 53.72628839374007, "west_lng": 37.61} }'  # noqa: E501
TEST_BROWSER_REPLY_2 = '{"msgType": "Buses", "buses": [{"busId": "a134aa", "lat": 55.7494, "lng": 37.621, "route": "670\\u043a"}]}'  # noqa: E501

TEST_BROWSER_MESSAGE_3 = '{"msgType": "newBound", "data": {"eat_lng": 38.1, "north_lat": 155.7495, "south_lat": 53.72628839374007} }'  # noqa: E501
TEST_BROWSER_REPLY_3 = '{"msgType": "Errors", "errors": ["Additional properties are not allowed (\'eat_lng\' was unexpected)", "\'east_lng\' is a required property", "\'west_lng\' is a required property", "155.7495 is greater than the maximum of 90", "\'newBounds\' was expected"]}'  # noqa: E501
