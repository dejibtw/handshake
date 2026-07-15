import json
import re
from collections import Counter
from pathlib import Path


ACCESS_LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")
REQUEST_PATTERN = re.compile(
    r'^\S+\s+.*"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (?P<path>\S+) HTTP/\d(?:\.\d)?"'
)


def load_report() -> dict:
    assert REPORT_PATH.is_file(
    ), f"Required output file {REPORT_PATH} was not created."
    try:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise AssertionError(
            f"{REPORT_PATH} must contain valid JSON: {error}") from error
    assert isinstance(
        report, dict), "The top-level JSON value must be an object."
    return report


def expected_report() -> dict:
    total_requests = 0
    unique_ips = set()
    path_counts = Counter()

    for line_number, raw_line in enumerate(
        ACCESS_LOG_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line:
            continue

        match = REQUEST_PATTERN.match(line)
        assert match is not None, f"Unable to parse access.log line {line_number}: {line!r}"
        total_requests += 1
        unique_ips.add(line.split()[0])
        path_counts[match.group("path")] += 1

    assert path_counts, "The access log contains no request paths."
    highest_count = max(path_counts.values())
    top_path = min(path for path, count in path_counts.items()
                   if count == highest_count)

    return {
        "total_requests": total_requests,
        "unique_ips": len(unique_ips),
        "top_path": top_path,
    }


def test_report_schema() -> None:
    """Verifies instruction.md success criterion 1: exact JSON fields and types."""
    report = load_report()
    assert set(report) == {"total_requests", "unique_ips", "top_path"}
    assert isinstance(report["total_requests"], int) and not isinstance(
        report["total_requests"], bool)
    assert isinstance(report["unique_ips"], int) and not isinstance(
        report["unique_ips"], bool)
    assert isinstance(report["top_path"], str)


def test_total_requests() -> None:
    """Verifies instruction.md success criterion 2: exact non-empty request count."""
    report = load_report()
    assert report["total_requests"] == expected_report()["total_requests"]


def test_unique_ips() -> None:
    """Verifies instruction.md success criterion 3: exact distinct client IP count."""
    report = load_report()
    assert report["unique_ips"] == expected_report()["unique_ips"]


def test_top_path() -> None:
    """Verifies instruction.md success criterion 4: most frequent path and tie-break."""
    report = load_report()
    assert report["top_path"] == expected_report()["top_path"]
