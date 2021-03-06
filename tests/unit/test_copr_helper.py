import pytest
from flexmock import flexmock

import packit
from packit.copr_helper import CoprHelper


class TestCoprHelper:
    @pytest.mark.parametrize(
        # copr_client.mock_chroot_proxy.get_list() returns dictionary
        "get_list_keys, expected_return",
        [
            pytest.param(["chroot1", "_chroot2"], ["chroot1"], id="chroot_list"),
            pytest.param([], [], id="empty_list"),
        ],
    )
    def test_get_avilable_chroots(self, get_list_keys, expected_return):
        copr_client_mock = flexmock(mock_chroot_proxy=flexmock())
        copr_client_mock.mock_chroot_proxy.should_receive("get_list.keys").and_return(
            get_list_keys
        )
        flexmock(packit.copr_helper.CoprClient).should_receive(
            "create_from_config_file"
        ).and_return(copr_client_mock)

        copr_helper = CoprHelper("_upstream_local_project")
        copr_helper.get_available_chroots.cache_clear()

        assert copr_helper.get_available_chroots() == expected_return
