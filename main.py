import re
from collections import defaultdict
import statistics


def parse_log_line(line):
    # Updated regex to include response time (last number before referrer)
    pattern = r'(?P<ip>\S+) \S+ \S+ \[(?P<datetime>.*?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<time>\S+)'
    match = re.match(pattern, line)
    if match:
        return match.groupdict()
    else:
        return None


def analyze_log(file_path):
    total_requests = 0
    status_counts = defaultdict(int)
    ip_counts = defaultdict(int)
    url_counts = defaultdict(int)
    #user_agents = defaultdict(int)
    times = []  # Store response times for calculations

    with open(file_path, 'r') as f:
        for line in f:
            total_requests += 1
            parsed = parse_log_line(line)

            if not parsed:
                print("can't parse")
                continue

            # Update counters
            ip_counts[parsed['ip']] += 1
            url_counts[parsed['url']] += 1

            status_counts[parsed['status']] += 1
            #user_agents[parsed['user_agent']] += 1

            # Collect response times (handle invalid values)
            try:
                time = float(parsed['time'])
                times.append(time)
            except (ValueError, KeyError):
                pass

    # Calculate time statistics
    time_stats = {}
    if times:
        time_stats['avg'] = sum(times) / len(times)
        time_stats['median'] = statistics.median(times)
    else:
        time_stats['avg'] = "N/A"
        time_stats['median'] = "N/A"

    # Update report
    report = f'''
    NGINX LOG ANALYSIS REPORT
    ========================
    Total Requests: {total_requests}

    Unique Visitors: {len(ip_counts)}
    Average Response Time: {time_stats['avg']:.4f}s
    Median Response Time: {time_stats['median']:.4f}s

    Top 10 IPs:
    {dict(sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10])}

    Top 10 Requested URLs:
    {dict(sorted(url_counts.items(), key=lambda x: x[1], reverse=True)[:10])}

    Status Code Distribution:
    {dict(status_counts)}
'''


    return report

print(analyze_log('access.log'))
