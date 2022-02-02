import pytest

from datagateway_api.src.common.config import Config


class TestSearchAPISearchEndpoint:
    @pytest.mark.parametrize(
        "endpoint_name, request_filter, expected_json",
        [
            pytest.param(
                "datasets",
                '{"limit": 2}',
                [
                    {
                        "pid": "0-449-78690-0",
                        "title": "DATASET 1",
                        "creationDate": "2002-11-27T06:20:36+00:00",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                    {
                        "pid": "0-8401-1070-7",
                        "title": "DATASET 2",
                        "creationDate": "2013-04-01T10:56:52+00:00",
                        "isPublic": True,
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                ],
                id="Basic /datasets request",
            ),
            pytest.param(
                "documents",
                '{"limit": 1}',
                [
                    {
                        "pid": "0-449-78690-0",
                        "isPublic": True,
                        "type": "INVESTIGATIONTYPE 2",
                        "title": "INVESTIGATION 1",
                        "summary": "Season identify professor happen third. Beat"
                        " professional blue clear style have. Light final summer.",
                        "doi": "0-449-78690-0",
                        "startDate": "2000-04-03T00:00:00+00:00",
                        "endDate": "2000-07-09T00:00:00+00:00",
                        "releaseDate": "2000-07-05T00:00:00+00:00",
                        "license": None,
                        "keywords": [
                            "read123",
                            "boy129",
                            "out253",
                            "hour326",
                            "possible449",
                            "west566",
                            "scene948",
                            "who1253",
                            "capital1526",
                            "dream1989",
                            "front2347",
                            "inside2465",
                            "surface2851",
                            "learn2953",
                            "hot3053",
                            "just3159",
                            "population3261",
                            "cup3366",
                            "another3451",
                            "environmental3632",
                            "require3858",
                            "rock3952",
                            "determine4048",
                            "space4061",
                            "big4229",
                            "why4243",
                            "public4362",
                            "election4641",
                            "measure4996",
                            "often5014",
                            "develop5135",
                            "than5310",
                            "floor5312",
                            "check5327",
                            "cost5487",
                            "information6130",
                            "guy6180",
                            "admit6235",
                            "market6645",
                            "law6777",
                            "close7336",
                            "billion7597",
                            "product7964",
                            "American8041",
                            "language8246",
                            "school8277",
                            "specific8539",
                            "position8670",
                            "grow8702",
                            "time8899",
                            "weight9086",
                            "catch9129",
                            "speak9559",
                            "strong9621",
                            "development9757",
                            "best9786",
                            "identify10039",
                            "give10497",
                            "life10854",
                            "century11040",
                            "fire11580",
                            "leg11744",
                            "past11935",
                            "bar12034",
                            "do12108",
                            "prove12224",
                            "body12251",
                            "data12288",
                            "at12640",
                            "star12706",
                            "customer12795",
                            "small13058",
                            "event13141",
                            "now13193",
                            "magazine13415",
                            "policy13601",
                            "black13996",
                            "American14654",
                        ],
                        "datasets": [],
                        "members": [],
                        "parameters": [],
                    },
                ],
                id="Basic /documents request",
            ),
            pytest.param(
                "instruments",
                '{"limit": 2}',
                [
                    {
                        "datasets": [],
                        "facility": "LILS",
                        "name": "INSTRUMENT 1",
                        "pid": "1",
                    },
                    {
                        "datasets": [],
                        "facility": "LILS",
                        "name": "INSTRUMENT 2",
                        "pid": "2",
                    },
                ],
                id="Basic /instruments request",
            ),
            pytest.param(
                "datasets",
                '{"limit": 1, "skip": 5}',
                [
                    {
                        "pid": "0-468-20341-9",
                        "title": "DATASET 6",
                        "isPublic": True,
                        "creationDate": "2008-06-30T08:30:58+00:00",
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                ],
                id="Search datasets with skip filter",
            ),
            pytest.param(
                "instruments",
                '{"limit": 2, "where": {"name": "INSTRUMENT 10"}}',
                [
                    {
                        "datasets": [],
                        "facility": "LILS",
                        "name": "INSTRUMENT 10",
                        "pid": "10",
                    },
                ],
                id="Search instruments with name condition",
            ),
            pytest.param(
                "datasets",
                '{"limit": 1, "where": {"creationDate": {"gt":'
                ' "2007-06-30 08:30:58+00:00"}}}',
                [
                    {
                        "pid": "0-8401-1070-7",
                        "title": "DATASET 2",
                        "isPublic": True,
                        "creationDate": "2013-04-01T10:56:52+00:00",
                        "size": None,
                        "documents": [],
                        "techniques": [],
                        "instrument": None,
                        "files": [],
                        "parameters": [],
                        "samples": [],
                    },
                ],
                id="Search datasets with creation date filter (operator specified)",
            ),
            pytest.param(
                "datasets",
                '{"include": [{"relation": "documents"}, {"relation": "techniques"},'
                ' {"relation": "instrument"}, {"relation": "files"},'
                ' {"relation": "parameters"}, {"relation": "samples"}], "limit": 1}',
                [{}],
                id="Search datasets including all possible related entities",
                # Skipped because ICAT 5 mapping on techniques and instrument
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "documents",
                '{"include": [{"relation": "datasets"}, {"relation": "members"},'
                ' {"relation": "parameters"}], "limit": 1}',
                [{}],
                id="Search documents including all possible related entities",
                # TODO - issue with parameters include
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "instruments",
                '{"include": [{"relation": "datasets"}], "limit": 1}',
                {
                    "description": "Former outside source play nearly Congress before"
                    " necessary. Allow want audience test laugh. Economic body person"
                    " general attorney. Effort weight prevent possible.",
                    "modId": "user",
                    "createTime": "2019-02-19 05:57:03+00:00",
                    "pid": None,
                    "createId": "user",
                    "type": "2",
                    "name": "INSTRUMENT 2",
                    "modTime": "2019-01-29 23:33:20+00:00",
                    "id": 2,
                    "fullName": "With piece reason late model. House office fly."
                    " International scene call deep answer audience baby true.\n"
                    "Indicate education across these. Opportunity design too.",
                    "url": "https://moore.org/",
                },
                id="Search instruments including all possible related entities",
                # Skipped due to ICAT 5 mapping
                marks=pytest.mark.skip,
            ),
            pytest.param(
                "datasets",
                '{"limit": 1, "where": {"isPublic": true}}',
                [{}],
                id="Search datasets with isPublic condition",
                # Skipped because the where for isPublic doesn't work
                marks=pytest.mark.skip,
            ),
        ],
    )
    def test_valid_search_endpoint(
        self, flask_test_app_search_api, endpoint_name, request_filter, expected_json,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/{endpoint_name}?filter="
            f"{request_filter}",
        )

        assert test_response.json == expected_json

    @pytest.mark.parametrize(
        "request_filter, expected_status_code",
        [
            pytest.param('{"where": []}', 400, id="Bad where filter"),
            pytest.param('{"limit": -1}', 400, id="Bad limit filter"),
            pytest.param('{"skip": -100}', 400, id="Bad skip filter"),
            pytest.param('{"include": ""}', 400, id="Bad include filter"),
        ],
    )
    def test_invalid_search_endpoint(
        self, flask_test_app_search_api, request_filter, expected_status_code,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/instruments?filter={request_filter}",
        )

        assert test_response.status_code == expected_status_code
