def test_import_firewall():
    import firewall

    assert hasattr(firewall, "block_ip")
    assert hasattr(firewall, "unblock_ip")
    assert hasattr(firewall, "check_ip")