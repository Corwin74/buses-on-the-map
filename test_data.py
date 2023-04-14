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
