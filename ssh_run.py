#!/usr/bin/env python3
"""Run a command on a remote host over ssh. Usage: ssh_run.py HOST CMD [-i KEY] [-u USER]"""
import argparse, os, subprocess, sys


def ssh_run(host, command, key=None, user="root", port=22, timeout=20):
    """Returns (exit_code, stdout, stderr). exit_code 255 = ssh/connection failure."""
    cmd = ["ssh", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=no",
           "-o", "UserKnownHostsFile=/dev/null", "-o", f"ConnectTimeout={timeout}",
           "-p", str(port)]
    if key:
        cmd += ["-i", os.path.expanduser(key)]
    cmd += [f"{user}@{host}", command]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 15)
    return p.returncode, p.stdout, p.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("host")
    ap.add_argument("command")
    ap.add_argument("-i", "--key")
    ap.add_argument("-u", "--user", default="root")
    ap.add_argument("-p", "--port", type=int, default=22)
    a = ap.parse_args()
    rc, out, err = ssh_run(a.host, a.command, a.key, a.user, a.port)
    sys.stdout.write(out)
    sys.stderr.write(err)
    return rc


if __name__ == "__main__":
    sys.exit(main())
