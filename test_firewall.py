def test_import_firewall():
    import firewall

    assert hasattr(firewall, "block_ip")
    assert hasattr(firewall, "unblock_ip")
    assert hasattr(firewall, "check_ip")

def test_is_valid_ip():
    import firewall

    assert firewall.is_valid_ip("8.8.8.8") is True
    assert firewall.is_valid_ip("192.168.1.1") is True
    assert firewall.is_valid_ip("999.999.999.999") is False
    assert firewall.is_valid_ip("hello") is False