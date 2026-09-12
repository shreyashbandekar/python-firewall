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

def test_block_ip(monkeypatch, capsys):
    import firewall

    commands = []

    class FakeResult:
        returncode = 0
        stdout = "Rule added successfully."
        stderr = ""

    def fake_run(command, **kwargs):
        commands.append(command)

        if "show rule" in command:
            result = FakeResult()
            result.stdout = "No rules match the specified criteria."
            return result

        return FakeResult()

    monkeypatch.setattr(firewall.subprocess, "run", fake_run)

    firewall.block_ip("8.8.8.8")

    captured = capsys.readouterr()

    assert "8.8.8.8 blocked successfully" in captured.out
    assert any("remoteip=8.8.8.8" in command for command in commands)


    
def test_unblock_ip(monkeypatch, capsys):
    import firewall

    commands = []

    class FakeResult:
        returncode = 0
        stdout = "Deleted 1 rule(s)."
        stderr = ""

    def fake_run(command, **kwargs):
        commands.append(command)
        return FakeResult()

    monkeypatch.setattr(firewall.subprocess, "run", fake_run)

    firewall.unblock_ip("8.8.8.8")

    captured = capsys.readouterr()

    assert "8.8.8.8 unblocked successfully" in captured.out
    assert any("delete rule" in command for command in commands)
    assert any('name="PYFW_BLOCK_8.8.8.8"' in command for command in commands)

def test_check_ip(monkeypatch, capsys):
    import firewall

    class FakeResult:
        returncode = 0
        stdout = "Rule Name: PYFW_BLOCK_8.8.8.8"
        stderr = ""

    def fake_run(command, **kwargs):
        return FakeResult()

    monkeypatch.setattr(firewall.subprocess, "run", fake_run)

    firewall.check_ip("8.8.8.8")

    captured = capsys.readouterr()

    assert "8.8.8.8 is currently blocked" in captured.out

def test_log_event(tmp_path, monkeypatch):
    import firewall

    log_file = tmp_path / "firewall.log"

    monkeypatch.chdir(tmp_path)

    firewall.log_event("BLOCK", "8.8.8.8", "SUCCESS")

    assert log_file.read_text() == "BLOCK | 8.8.8.8 | SUCCESS\n"