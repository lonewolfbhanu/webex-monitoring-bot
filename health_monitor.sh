#!/bin/bash
# Tells the OS to use bash to run this script

# Script: Server Health Monitor
# Version 1.0
# Author: BTG
# Date: 2026-03-16

# ---- CONFIG ----

LOGFILE="./health_monitor.log"
# Variable storing the path where the report will be saved

SERVICES=("sshd" "cron")
# Array of services we want to check
# Add or remove services based on what's running on your server

# ---- FUNCTIONS ----

check_cpu()
{
  CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
  # top -bn1        → runs top once as plain text (non interactive)
  # grep "Cpu(s)"   → filters just the CPU line
  # awk '{print $2} → grabs 2nd column (the usage number)
  # $()             → runs the command and stores result in CPU

  echo "CPU Usage     : $CPU%"
}

check_memory()
{
  TOTAL=$(free -m | awk 'NR==2 {print $2}')
  # free -m   → shows memory in megabytes
  # NR==2     → only look at line 2 which is the RAM line
  # {print $2} → 2nd column is total memory

  USED=$(free -m | awk 'NR==2 {print $3}')
  # same but $3 is 3rd column which is used memory

  echo "Memory Usage  : $USED MB used out of $TOTAL MB"
}

check_disk()
{
  DISK=$(df -h / | awk 'NR==2 {print $5}')
  # df -h /    → shows disk usage of the / (root) partition in human readable format
  # NR==2      → skip the header line, look at line 2
  # {print $5} → 5th column is the usage percentage like 45%

  echo "Disk Usage    : $DISK used on /"
}

check_services()
{
  echo "Service Status:"

  for SERVICE in "${SERVICES[@]}"
  do
    # "${SERVICES[@]}" → loops through every item in the SERVICES array

    STATUS=$(systemctl is-active $SERVICE)
    # systemctl is-active → checks if the service is running
    # returns "active" if running, "inactive" if stopped

    if [ "$STATUS" == "active" ]
    then
      echo "  $SERVICE    : RUNNING"
    else
      echo "  $SERVICE    : STOPPED"
    fi
    # if/else → prints RUNNING or STOPPED based on the status
  done
}

print_report()
{
  echo "===== Run: $(date) ====="
  echo "==============================="
  echo "  Server Health Report"
  echo "  $(date)"
  # date → prints current date and time

  echo "==============================="
  check_cpu
  check_memory
  check_disk
  check_services
  # calling all 4 functions inside print_report
  # so we only need to call print_report in main

  echo "==============================="
}

# ---- MAIN ----

print_report | tee -a "$LOGFILE"
# print_report  → calls the function which calls all other functions
# |             → pipe, sends the output to the next command
# tee -a        → prints to terminal AND appends to the log file at the same time
# "$LOGFILE"    → the path we set at the top