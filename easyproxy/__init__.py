# -*- coding: UTF-8 -*-
# Copyright©2020 xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

"""
import logging
from .proxy_manager import ProxyManager

logging.basicConfig(
    filename='log.txt',
    format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]',
    level=logging.DEBUG,
    filemode='a',
    datefmt='%Y-%m-%d%I:%M:%S %p'
)

proxy_manager = ProxyManager()
proxy = get_proxy = proxy_manager.get_proxy
