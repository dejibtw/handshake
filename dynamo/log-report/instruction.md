Analyze the Apache-style access log at `/app/access.log` and write the completed JSON report to `/app/report.json`.

Each non-empty line represents one HTTP request. The first whitespace-delimited value is the client IP address. The requested path is the value between the HTTP method and HTTP version inside the quoted request.

Success criteria:

1. `/app/report.json` must contain valid JSON. Its top-level value must be an object with exactly the fields `total_requests`, `unique_ips`, and `top_path`. `total_requests` and `unique_ips` must be integers, and `top_path` must be a string.

2. `total_requests` must equal the number of non-empty request entries in `/app/access.log`.

3. `unique_ips` must equal the number of distinct client IP addresses in the first field of the log entries.

4. `top_path` must be the requested path occurring most frequently. Count paths exactly as they appear in the quoted requests. If multiple paths tie for the highest count, choose the path that comes first in ascending string order.

Do not modify `/app/access.log`. The task requires no network access at runtime.
