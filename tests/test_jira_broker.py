"""Exercise attachment uploads against a local Jira stand-in."""

import json
import os
import subprocess
import threading
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

BROKER = (
    Path(__file__).resolve().parents[1]
    / "private_dot_agents/skills/jira-broker/scripts/executable_jira-broker"
)


@pytest.fixture
def jira(tmp_path):
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = self.rfile.read(int(self.headers["Content-Length"]))
            requests.append((self.path, self.headers, body))
            failed = self.path.endswith("/FAIL-1/attachments")
            self.send_response(403 if failed else 200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {"errorMessages": ["Attachments forbidden"]}
                    if failed
                    else [
                        {
                            "filename": "notes.md",
                            "id": "123",
                            "content": "https://jira.example/attachment/123/notes.md",
                        }
                    ]
                ).encode()
            )

        def log_message(self, *_args):
            pass

    token = tmp_path / "pat"
    token.write_text("local-test-token\n")
    token.chmod(0o600)
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    def run(*args):
        return subprocess.run(
            ["bash", str(BROKER), *args],
            cwd=tmp_path,
            env={
                **os.environ,
                "JIRA_PAT_FILE": str(token),
                "JIRA_BASE_URL": f"http://127.0.0.1:{server.server_port}",
            },
            capture_output=True,
            check=False,
            text=True,
            timeout=10,
        )

    try:
        yield run, requests, tmp_path
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


@pytest.mark.parametrize(
    ("filename", "wire_filename"),
    [
        ("notes.md", "notes.md"),
        ("notes,semi;.md", "notes,semi;.md"),
        # curl percent-encodes quotes; the MIME parser unescapes backslashes.
        ('notes,semi;quote"slash\\.md', "notes,semi;quote%22slash.md"),
    ],
)
def test_attach_uploads_unchanged_file(jira, filename, wire_filename):
    run, requests, root = jira
    content = b"# Notes\n\nBritish English: \xc2\xa3\n"
    (root / filename).write_bytes(content)
    result = run("--yes", "attach", "IFS-1234", filename)
    assert result.returncode == 0, result.stderr
    assert "attached notes.md to IFS-1234 (attachment 123)" in result.stdout
    assert "https://jira.example/attachment/123/notes.md" in result.stdout
    assert len(requests) == 1
    path, headers, body = requests[0]
    assert path == "/rest/api/2/issue/IFS-1234/attachments"
    assert headers["Authorization"] == "Bearer local-test-token"
    assert headers["X-Atlassian-Token"] == "no-check"
    message = BytesParser(policy=policy.default).parsebytes(
        f"Content-Type: {headers['Content-Type']}\r\n\r\n".encode() + body
    )
    parts = list(message.iter_parts())
    assert len(parts) == 1
    assert parts[0].get_param("name", header="content-disposition") == "file"
    assert parts[0].get_filename() == wire_filename
    assert parts[0].get_payload(decode=True) == content
    assert "local-test-token" not in result.stdout + result.stderr


@pytest.mark.parametrize("target", ["missing.md", "."])
def test_attach_rejects_invalid_files(jira, target):
    run, requests, _ = jira
    result = run("--yes", "attach", "IFS-1234", target)
    assert result.returncode != 0
    assert "not a readable regular file" in result.stderr
    assert not requests


def test_attach_requires_confirmation(jira):
    run, requests, root = jira
    (root / "notes.md").write_text("# Notes\n")
    result = run("attach", "IFS-1234", "notes.md")
    assert result.returncode != 0
    assert "write refused without confirmation" in result.stderr
    assert not requests


def test_attach_reports_http_failure(jira):
    run, requests, root = jira
    (root / "notes.md").write_text("# Notes\n")
    result = run("--yes", "attach", "FAIL-1", str(root / "notes.md"))
    assert result.returncode != 0
    assert "Attachments forbidden" in result.stderr
    assert "attached " not in result.stdout
    assert len(requests) == 1


def test_attach_rejects_extra_arguments(jira):
    run, requests, _ = jira
    result = run("--yes", "attach", "IFS-1234", "one.md", "two.md")
    assert result.returncode != 0
    assert "usage: attach <KEY> <file>" in result.stderr
    assert not requests
