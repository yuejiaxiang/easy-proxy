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
from typing import Dict, Union, List, Any
from .xila_proxy.xila_proxy import XiLaProxy
from aitool import singleton
from random import choice
from .proxy_base import ProxyBase
import time
import logging


@singleton
class ProxyManager(ProxyBase):
    def __init__(
            self,
            expiration_data: int = 1000,
            proxies_bare_minimum: int = 1
    ):
        self._available = False
        self.proxy_collectors = [
            XiLaProxy(),
        ]
        self._expiration_data = expiration_data
        self._proxies_bare_minimum = proxies_bare_minimum
        self._http_proxy_storage = []
        self._https_proxy_storage = []
        self._update_time = None

    def get_proxy(self):
        if not self._update_time or time.time() - self._update_time > self._expiration_data:
            self._update_proxy_storage()
        if not self._available:
            return None
        return {
            'http': choice(self._http_proxy_storage),
            'https': choice(self._https_proxy_storage),
        }

    def _update_proxy_storage(self):
        self._update_time = time.time()
        set_http_proxy_storage = set()
        set_https_proxy_storage = set()
        for proxy_collector in self.proxy_collectors:
            for proxy in proxy_collector.http_proxy_storage:
                set_http_proxy_storage.add(proxy)
            for proxy in proxy_collector.https_proxy_storage:
                set_https_proxy_storage.add(proxy)
        self._http_proxy_storage = list(set_http_proxy_storage)
        self._https_proxy_storage = list(set_https_proxy_storage)
        logging.info('The http proxies collected by {}: {}'.format(__class__, self._http_proxy_storage))
        logging.info('The https proxies collected by {}: {}'.format(__class__, self._https_proxy_storage))
        if len(self._http_proxy_storage) >= self._proxies_bare_minimum and \
                len(self._https_proxy_storage) >= self._proxies_bare_minimum:
            print('{} is available'.format(__class__))
            logging.info('{} is available'.format(__class__))
            self._available = True
