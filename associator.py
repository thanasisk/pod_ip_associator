#!/usr/bin/env python3
import re
import sys
import subprocess
import shutil
import tempfile
import os
import argparse

def has_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return shutil.which(name) is not None

parser = argparse.ArgumentParser()
parser.add_argument("-l","--logfile", help="the logfile we want to transform", default="vault-1")
args = parser.parse_args()
# in case we need more tools from the OS
req_tools = [ "kubectl"]
for tool in req_tools:
    if not has_tool(tool):
        print("%s not found - exiting", tool)
        sys.exit(1)
pod_ips = tempfile.mkstemp(text=True)[1]
kubelet_cmd = ["kubectl", "get",  "pods", "-o", "wide", "--all-namespaces"]
# the shell way to do this is but we are not going to need it
# kubectl get pods -o wide --all-namespaces |gawk '{ print $2 " "  $7 }' |tee pod_ips
kubectl = subprocess.Popen(kubelet_cmd, stdout=subprocess.PIPE)
pods = kubectl.stdout.readlines()
f = open(pod_ips, "wb")
for pod in pods:
    pods = pod.split()
    f.write(pods[1]+ " ".encode("ascii") + pods[6]+"\n".encode("ascii"))
f.close()
with open(pod_ips, "r") as ifile:
    pods = ifile.readlines()
# we do not need it anymore ...
os.unlink(pod_ips)
helper = {}
for pod in pods:
    foo = pod.strip().split()
    helper[foo[1]] = foo[0]

with open(args.logfile,"r") as logfile:
    logs = logfile.readlines()

rexp_ip = r".*\s(\d{1,3}.\d{1,3}\.\d{1,3}\.\d{1,3})"
for logline in logs:
    foo = re.findall(rexp_ip,logline)
    try:
        logline = logline.replace(foo[0],helper[foo[0]])
    except (KeyError, IndexError) as e:
        pass
    finally:
        print(logline)
