---
name: hagnben
about: Create a report to help us improve
title: 'Triton will initialize logging twice when starting'
labels: ''
assignees: ''

---

**Description**

Logger::Logger() constructor in logging.cc is executed twice, if I add logs in the destructor, it can clearly show，
![image](https://github.com/triton-inference-server/server/assets/127070080/abc2a72a-c965-4691-a477-92cdfb666596)
![image](https://github.com/triton-inference-server/server/assets/127070080/dd0c64f6-d091-403a-892d-f928294d484c)
As shown in the above figure, I printed the log in the destructor and found that it was initialized twice。

**Triton Information**

triton 23.04 

**To Reproduce**

Add logs to the destructor of the logger, and compile and run them to discover

**Expected behavior**

initialized once
