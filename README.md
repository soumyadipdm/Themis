Themis
======

An OS resource-limit based load-balancer written in Python

Objective
=========

Every node in the cluster will have an agent running at a frequency depending upon the overall load of the cluster. The agent deducts (initial score is 100) scores the node based on available resources like CPU wait time, load-average, available RAM, swapiness etc. These can be tunable by predefining thresholds like 20% of the total CPU time is acceptible as a normal wait time for a particular node. The better the score is, the lower the load on that particular node. There is a plan to keep heuristics as well, to make the scoring process a bit smarter over the time by manipulating the thresholds automatically.

After the agent assigns a score to a particular node, it sends that score (along with the trend data, but probably less frequently) over to the load balancer through ZeroMQ messaging as JSON string

The load-balancer keeps a queue of all the nodes reverse-sorted based on their scores, i.e the node with highest score will be put in front of the queue and will be scheduled for the next connection, in case this node does not respond, next node in the queue will be considered.

Load-balancer will also keep track of a "participation-score" i.e how many times a particular node has been selected by the load-balancer. The lowest scorers will be reported by the load-balancer along with the different resource-limit/load data pin-pointing the reason why that node was not selected so frequently, thusgiving a hint to the sysadmins on the bottlenecks
