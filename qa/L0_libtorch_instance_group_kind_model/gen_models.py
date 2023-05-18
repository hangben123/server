#!/usr/bin/python
# Copyright 2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import torch
import torch.nn as nn
from torch.nn.parallel import DataParallel


class TestModel(nn.Module):

    def __init__(self, device1, device2):
        super(TestModel, self).__init__()
        self.device1 = device1
        self.device2 = device2
        self.layers1 = nn.Sequential(nn.Linear(16, 4),).to(self.device1)
        self.layers2 = nn.Sequential(nn.Linear(16, 4)).to(self.device2)

    def forward(self, INPUT0, INPUT1):
        INPUT0 = INPUT0.to(self.device1)
        INPUT1 = INPUT1.to(self.device2)
        print('INPUT0 device: {}, INPUT1 device: {}\n'.format(
            INPUT0.device, INPUT1.device))

        op0 = self.layers1(INPUT0 + INPUT0)
        op1 = self.layers2(INPUT1 + INPUT1)
        return op0, op1


devices = [("cuda:2", "cuda:0"), ("cpu", "cuda:3")]
model_names = ["libtorch_multi_gpu", "libtorch_multi_devices"]

for device_pair, model_name in zip(devices, model_names):
    model = TestModel(device_pair[0], device_pair[1])
    model_path = "models/" + model_name + "/1/model.pt"
    scripted_model = torch.jit.script(model)
    scripted_model.save(model_path)
