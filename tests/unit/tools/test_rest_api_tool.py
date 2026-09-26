import pytest

from griptape.artifacts import BaseArtifact


class TestRestApi:
    @pytest.fixture()
    def client(self):
        from griptape.tools import RestApiTool

        return RestApiTool(base_url="http://www.griptape.ai", description="Griptape website.")

    def test_put(self, client):
        assert isinstance(client.post({"values": {"body": {}}}), BaseArtifact)

    def test_post(self, client):
        assert isinstance(client.post({"values": {"body": {}}}), BaseArtifact)

    def test_get_one(self, client):
        assert isinstance(client.get({"values": {"path_params": ["1"]}}), BaseArtifact)

    def test_get_all(self, client):
        assert isinstance(client.get({"values": {}}), BaseArtifact)

    def test_get_filtered(self, client):
        assert isinstance(client.get({"values": {"query_params": {"limit": 10}}}), BaseArtifact)

    def test_delete_one(self, client):
        assert isinstance(client.delete({"values": {"path_params": ["1"]}}), BaseArtifact)

    def test_delete_multiple(self, client):
        assert isinstance(client.delete({"values": {"query_params": {"ids": [1, 2]}}}), BaseArtifact)

    def test_patch(self, client):
        assert isinstance(client.patch({"values": {"path_params": ["1"], "body": {}}}), BaseArtifact)

    def test_build_url(self, client):
        url = client._build_url("https://foo.bar")

        assert url == "https://foo.bar"

        url = client._build_url("https://foo.bar", path="/foo")

        assert url == "https://foo.bar/foo"

        url = client._build_url("https://foo.bar", path_params=[1, "fizz"])

        assert url == "https://foo.bar/1/fizz"

        url = client._build_url("https://foo.bar", path="foo/", path_params=["fizz", "buzz", 1, 2, 3])

        assert url == "https://foo.bar/foo/fizz/buzz/1/2/3"

        url = client._build_url("https://foo.bar", path_params=["fizz", "buzz", 1, 2, 3])

        assert url == "https://foo.bar/fizz/buzz/1/2/3"

    def test_activity_descriptions_include_param_schemas(self):
        from griptape.tools import RestApiTool

        tool = RestApiTool(
            base_url="https://foo.bar",
            description="Foo API.",
            request_path_params_schema="PATH-SCHEMA",
            request_query_params_schema="QUERY-SCHEMA",
        )

        for activity in (tool.get, tool.delete):
            description = tool.activity_description(activity)
            assert "The request path parameters must follow this JSON schema: PATH-SCHEMA" in description
            assert "The request query parameters must follow this JSON schema: QUERY-SCHEMA" in description
        assert "The request path parameters must follow this JSON schema: PATH-SCHEMA" in tool.activity_description(
            tool.patch
        )
