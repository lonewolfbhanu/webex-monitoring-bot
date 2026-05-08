# Server Health Monitor

A Linux bash script that monitors server health and logs reports automatically.

## What it does
- Monitors CPU usage
- Monitors RAM usage
- Monitors Disk usage
- Checks if critical services are running (sshd, cron)
- Saves timestamped reports to a log file

## How to run
```bash
bash health_monitor.sh
```

## Tech used
- Bash scripting
- Linux core tools: top, free, df, systemctl
- Cron (for scheduling)

