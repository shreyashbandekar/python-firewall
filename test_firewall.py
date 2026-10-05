import csv


def test_import_firewall():
    import firewall

    assert hasattr(firewall, "block_ip")
    assert hasattr(firewall, "unblock_ip")
    assert hasattr(firewall, "check_ip")
    assert hasattr(firewall, "list_rules")


def test_is_valid_ip():
    import firewall

    assert firewall.is_valid_ip("8.8.8.8") is True
    assert firewall.is_valid_ip("192.168.1.1") is True
    assert firewall.is_valid_ip("2001:4860:4860::8888") is True
    assert firewall.is_valid_ip("999.999.999.999") is False
    assert firewall.is_valid_ip("hello") is False


def test_block_ip(monkeypatch, tmp_path, capsys):
    import firewall

    monkeypatch.chdir(tmp_path)
    commands = []

    class FakeResult:
        returncode = 0
        stdout = "No rules match the specified criteria."
        stderr = ""

    def fake_run(command, **kwargs):
        commands.append(command)

        if "add" in command:
            result = FakeResult()
            result.stdout = "Rule added successfully."
            return result

        return FakeResult()

    monkeypatch.setattr(firewall.subprocess, "run", fake_run)

    assert firewall.block_ip("8.8.8.8") == "SUCCESS"

    captured = capsys.readouterr()

    assert "8.8.8.8 blocked successfully" in captured.out
    assert commands[0][:4] == [
        "netsh",
        "advfirewall",
        "firewall",
        "show",
    ]
    assert "remoteip=8.8.8.8" in commands[1]


def test_block_ip_already_blocked(monkeypatch, tmp_path, capsys):
    import firewall

    monkeypatch.chdir(tmp_path)

    class FakeResult:
        returncode = 0
        stdout = "Rule Name: PYFW_BLOCK_8.8.8.8"
        stderr = ""

    monkeypatch.setattr(
        firewall.subprocess,
        "run",
        lambda *args, **kwargs: FakeResult(),
    )

    assert firewall.block_ip("8.8.8.8") == "ALREADY_BLOCKED"

    captured = capsys.readouterr()

    assert "already blocked" in captured.out


def test_block_ip_failure(monkeypatch, tmp_path, capsys):
    import firewall

    monkeypatch.chdir(tmp_path)

    calls = []

    class FakeResult:
        returncode = 1
        stdout = "No rules match the specified criteria."
        stderr = "Access is denied."

    def fake_run(command, **kwargs):
        calls.append(command)
        return FakeResult()

    monkeypatch.setattr(firewall.subprocess, "run", fake_run)

    assert firewall.block_ip("8.8.8.8") == "FAILED"

    captured = capsys.readouterr()

    assert "Failed to block IP" in captured.out
    assert "Access is denied." in captured.out


def test_unblock_ip(monkeypatch, tmp_path, capsys):
    import firewall

    monkeypatch.chdir(tmp_path)

    class FakeResult:
        returncode = 0
        stdout = "Deleted 1 rule(s)."
        stderr = ""

    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return FakeResult()

    monkeypatch.setattr(firewall.subprocess, "run", fake_run)

    assert firewall.unblock_ip("8.8.8.8") == "SUCCESS"

    captured = capsys.readouterr()

    assert "8.8.8.8 unblocked successfully" in captured.out
    assert commands[0][:5] == [
        "netsh",
        "advfirewall",
        "firewall",
        "delete",
        "rule",
    ]
    assert "name=PYFW_BLOCK_8.8.8.8" in commands[0]


def test_unblock_ip_not_blocked(monkeypatch, tmp_path, capsys):
    import firewall

    monkeypatch.chdir(tmp_path)

    class FakeResult:
        returncode = 1
        stdout = "No rules match the specified criteria."
        stderr = ""

    monkeypatch.setattr(
        firewall.subprocess,
        "run",
        lambda *args, **kwargs: FakeResult(),
    )

    assert firewall.unblock_ip("8.8.8.8") == "NOT_BLOCKED"

    captured = capsys.readouterr()

    assert "No firewall rule found" in captured.out


def test_check_ip_blocked(monkeypatch, tmp_path, capsys):
    import firewall

    monkeypatch.chdir(tmp_path)

    class FakeResult:
        returncode = 0
        stdout = "Rule Name: PYFW_BLOCK_8.8.8.8"
        stderr = ""

    monkeypatch.setattr(
        firewall.subprocess,
        "run",
        lambda *args, **kwargs: FakeResult(),
    )

    assert firewall.check_ip("8.8.8.8") == "BLOCKED"

    captured = capsys.readouterr()

    assert "8.8.8.8 is currently blocked" in captured.out


def test_check_ip_not_blocked(monkeypatch, tmp_path, capsys):
    import firewall

    monkeypatch.chdir(tmp_path)

    class FakeResult:
        returncode = 0
        stdout = "No rules match the specified criteria."
        stderr = ""

    monkeypatch.setattr(
        firewall.subprocess,
        "run",
        lambda *args, **kwargs: FakeResult(),
    )

    assert firewall.check_ip("8.8.8.8") == "NOT_BLOCKED"

    captured = capsys.readouterr()

    assert "8.8.8.8 is not blocked" in captured.out


def test_list_rules(monkeypatch, capsys):
    import firewall

    class FakeResult:
        returncode = 0
        stdout = (
            "Rule Name: PYFW_BLOCK_8.8.8.8\n"
            "Rule Name: Other Application Rule\n"
            "Rule Name: PYFW_BLOCK_1.1.1.1\n"
        )
        stderr = ""

    monkeypatch.setattr(
        firewall.subprocess,
        "run",
        lambda *args, **kwargs: FakeResult(),
    )

    firewall.list_rules()

    captured = capsys.readouterr()

    assert "PYFW_BLOCK_8.8.8.8" in captured.out
    assert "PYFW_BLOCK_1.1.1.1" in captured.out
    assert "Other Application Rule" not in captured.out


def test_log_csv_event(tmp_path, monkeypatch):
    import firewall

    monkeypatch.chdir(tmp_path)

    firewall.log_csv_event("BLOCK", "8.8.8.8", "SUCCESS")

    with open("firewall_events.csv", "r", newline="", encoding="utf-8") as csv_file:
        rows = list(csv.reader(csv_file))

    assert rows[0] == ["timestamp", "action", "ip", "status"]
    assert rows[1][1:] == ["BLOCK", "8.8.8.8", "SUCCESS"]


def test_view_logs(tmp_path, monkeypatch, capsys):
    import firewall

    monkeypatch.chdir(tmp_path)

    with open("firewall_events.csv", "w", newline="", encoding="utf-8") as csv_file:
        csv_file.write(
            "timestamp,action,ip,status\n"
            "2026-09-13 17:00:00,BLOCK,8.8.8.8,SUCCESS\n"
        )

    firewall.view_logs()

    captured = capsys.readouterr()

    assert "BLOCK" in captured.out
    assert "8.8.8.8" in captured.out
    assert "SUCCESS" in captured.out


def test_view_logs_file_not_found(tmp_path, monkeypatch, capsys):
    import firewall

    monkeypatch.chdir(tmp_path)

    firewall.view_logs()

    captured = capsys.readouterr()

    assert "[!] No firewall event log found." in captured.out
