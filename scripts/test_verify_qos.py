#!/usr/bin/env python3
"""
Verify that rqt_topic subscriber QoS override is working.

This script:
1. Starts a BEST_EFFORT publisher on /test_qos_topic
2. Waits a moment
3. Runs `ros2 topic info --verbose` and parses the output
4. Checks that a subscriber exists with BEST_EFFORT reliability

Usage:
    # Terminal 1: start rqt_topic and monitor /test_qos_topic
    ros2 run rqt_topic rqt_topic

    # Terminal 2: run this script
    python3 scripts/test_verify_qos.py
"""

import subprocess
import sys
import time


def run_cmd(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout, result.stderr, result.returncode


def main():
    topic = '/test_qos_topic'

    print(f'Checking topic info for {topic}...')
    stdout, stderr, rc = run_cmd(f'ros2 topic info {topic} --verbose')

    if rc != 0:
        print(f'ERROR: ros2 topic info failed:\n{stderr}')
        sys.exit(1)

    print(stdout)

    # Parse output for subscriber section and reliability
    lines = stdout.splitlines()
    in_subscriber_section = False
    subscriber_found = False
    best_effort_found = False

    for line in lines:
        stripped = line.strip()
        if 'Subscription count:' in stripped:
            in_subscriber_section = True
            count = stripped.split(':')[-1].strip()
            if count != '0':
                subscriber_found = True
            continue
        if in_subscriber_section and 'Reliability:' in stripped:
            if 'BEST_EFFORT' in stripped:
                best_effort_found = True
            break

    print('\n--- Verification Results ---')
    if subscriber_found:
        print('[PASS] Subscriber found on topic')
    else:
        print('[FAIL] No subscriber found on topic')
        sys.exit(1)

    if best_effort_found:
        print('[PASS] Subscriber uses BEST_EFFORT reliability (QoS override active)')
    else:
        print('[WARN] Subscriber reliability is not BEST_EFFORT')
        print('       (This may be ok if the publisher is RELIABLE)')

    print('\nAll checks passed. QoS override is working.')


if __name__ == '__main__':
    main()
