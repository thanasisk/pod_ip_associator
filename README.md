# pod_ip_associator

## A small utility to associate IPs with pod names.

Sometimes, when examining pod logs only the numerical IPs are saved. This simple
utility will perform a lookup of all pod/IP pairs in the cluster and perform a 
simple regex replace on IPs with the pod name.

(C) Athanasios Kostopoulos 2020
