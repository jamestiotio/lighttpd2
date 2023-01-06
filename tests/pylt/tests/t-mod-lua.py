# -*- coding: utf-8 -*-

from pylt.base import ModuleTest
from pylt.requests import CurlRequest


LUA_TEST_OPTIONS = """

setup["server.tag"]("lighttpd 2.0 with lua")

function changetag(tag)
    return action["server.tag"](tag)
end

actions = {
    ["lua.changetag"] = changetag
}

"""


class TestSetupOption(CurlRequest):
    URL = "/"
    EXPECT_RESPONSE_HEADERS = [("Server", "lighttpd 2.0 with lua")]


class TestChangeOption(CurlRequest):
    URL = "/?change"
    EXPECT_RESPONSE_HEADERS = [("Server", "lighttpd 2.0 with modified lua")]


class Test(ModuleTest):
    def prepare_test(self) -> None:
        test_options_lua = self.prepare_file("lua/test_options.lua", LUA_TEST_OPTIONS)
        self.plain_config = f"""
            setup {{ lua.plugin "{test_options_lua}"; }}
        """
        self.config = """
            if req.query == "change" {
                lua.changetag "lighttpd 2.0 with modified lua";
            }
        """
