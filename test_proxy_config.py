import unittest
import sys
import types
from unittest import mock

import auto_scheduler

fake_curl_cffi = types.ModuleType("curl_cffi")
fake_curl_cffi.requests = types.SimpleNamespace()
sys.modules.setdefault("curl_cffi", fake_curl_cffi)

import ncs_register


class ProxyNormalizationTests(unittest.TestCase):
    def test_ncs_register_default_proxy_is_disabled(self):
        self.assertEqual(ncs_register._normalize_proxy_value(""), "")
        self.assertEqual(ncs_register._normalize_proxy_value("填入您自己的代理地址"), "")
        self.assertEqual(ncs_register._normalize_proxy_value("direct"), "")

    def test_auto_scheduler_placeholder_proxy_is_disabled(self):
        self.assertEqual(auto_scheduler._normalize_proxy_value(""), "")
        self.assertEqual(auto_scheduler._normalize_proxy_value("填写你的代理"), "")
        self.assertEqual(auto_scheduler._normalize_proxy_value("http://127.0.0.1:7890"), "http://127.0.0.1:7890")

    def test_ncs_register_load_config_supports_env_name_mapping(self):
        fake_config = {
            "lamail_api_key": "",
            "lamail_api_key_env": "MY_LAMAIL_KEY",
            "lamail_domain": "",
            "lamail_domain_env": "MY_LAMAIL_DOMAIN",
        }
        with mock.patch.dict("os.environ", {
            "MY_LAMAIL_KEY": "secret-key",
            "MY_LAMAIL_DOMAIN": "mail.example.com",
        }, clear=False):
            with mock.patch("ncs_register.os.path.exists", return_value=True):
                with mock.patch("builtins.open", mock.mock_open(read_data="{}")):
                    with mock.patch("ncs_register.json.load", return_value=fake_config):
                        config = ncs_register._load_config()

        self.assertEqual(config["lamail_api_key"], "secret-key")
        self.assertEqual(config["lamail_domain"], "mail.example.com")

    def test_auto_scheduler_load_account_count_config_supports_env_name_mapping(self):
        fake_config = {
            "upload_api_url": "",
            "upload_api_url_env": "MY_UPLOAD_URL",
            "upload_api_token": "",
            "upload_api_token_env": "MY_UPLOAD_TOKEN",
        }
        with mock.patch.dict("os.environ", {
            "MY_UPLOAD_URL": "https://upload.example.com",
            "MY_UPLOAD_TOKEN": "upload-token",
        }, clear=False):
            with mock.patch("auto_scheduler.os.path.exists", return_value=True):
                with mock.patch("builtins.open", mock.mock_open(read_data="{}")):
                    with mock.patch("auto_scheduler.json.load", return_value=fake_config):
                        config = auto_scheduler._load_account_count_config()

        self.assertEqual(config["upload_api_url"], "https://upload.example.com")
        self.assertEqual(config["upload_api_token"], "upload-token")


if __name__ == "__main__":
    unittest.main()
