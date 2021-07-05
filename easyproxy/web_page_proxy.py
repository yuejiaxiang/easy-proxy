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
Get proxy from http://www.xiladaili.com/
"""

from typing import Dict, Union, List, Any, NoReturn
from abc import ABCMeta, abstractmethod
import time
import os
import requests
from threading import Thread, Lock
from random import choice
from aitool import file_exist, save_json, load_json
from .proxy_base import ProxyBase
import logging

URL = str
Path = str


class WebPageProxy(ProxyBase, metaclass=ABCMeta):
    def __init__(
            self,
            time_interval: float = 5.0,
            record_file_path: Path = 'record.json',
            expiration_data: int = 100000,
            proxies_bare_minimum: int = 1
    ):
        logging.info('initializing {}'.format(self.__class__))
        self._available = False
        self._time_interval = time_interval
        self._record_file_path = record_file_path
        self._expiration_data = expiration_data
        self._proxies_bare_minimum = proxies_bare_minimum

        self._update_time = None
        self._http_proxy_storage = []
        self._https_proxy_storage = []
        self._confirm_proxy_availability()
        Thread(target=self._automatic_update_monitor).start()

    def _confirm_proxy_availability(self) -> NoReturn:
        if file_exist(self._record_file_path):
            self._http_proxy_storage, self._https_proxy_storage, self._update_time = load_json(self._record_file_path)
        if not self._update_time or time.time() - self._update_time > self._expiration_data:
            self._update_proxy_storage()

    def _update_proxy_storage(self) -> NoReturn:
        print('updating proxy storage of {}'.format(__class__))
        logging.info('updating proxy storage of {}'.format(__class__))
        print('This step will cost several minutes, please be patient')
        self._update_time = time.time()
        self._tmp_http_proxy_storage = set()
        self._tmp_https_proxy_storage = set()
        lock = Lock()
        threads = []
        for results in self._analysis_homepage():
            for proxy, tag in results:
                if 'HTTP' in tag:
                    t = Thread(target=self._check_proxy_available, args=(proxy, 'HTTP', lock,))
                    t.start()
                    threads.append(t)
                if 'HTTPS' in tag:
                    t = Thread(target=self._check_proxy_available, args=(proxy, 'HTTPS', lock,))
                    t.start()
                    threads.append(t)
            time.sleep(self._time_interval)
        for t in threads:
            t.join()
        print('{} http proxies have been collected by {}'.format(__class__, len(self._tmp_http_proxy_storage)))
        print('{} https proxies have been collected by {}'.format(__class__, len(self._tmp_https_proxy_storage)))
        logging.info('The http proxies collected by {}: {}'.format(__class__, self._http_proxy_storage))
        logging.info('The https proxies collected by {}: {}'.format(__class__, self._https_proxy_storage))
        self._http_proxy_storage = list(self._tmp_http_proxy_storage)
        self._https_proxy_storage = list(self._tmp_https_proxy_storage)
        save_json(self._record_file_path, [self._http_proxy_storage, self._https_proxy_storage, self._update_time])
        if len(self._tmp_http_proxy_storage) >= self._proxies_bare_minimum and \
                len(self._tmp_https_proxy_storage) >= self._proxies_bare_minimum:
            print('{} is available'.format(__class__))
            logging.info('{} is available'.format(__class__))
            self._available = True
        else:
            print('{} is not available while the number of http proxies or https proxies is little than {}'.
                  format(__class__, self._proxies_bare_minimum))
            logging.info('{} is not available while the number of http proxies or https proxies is little than {}'.
                         format(__class__, self._proxies_bare_minimum))

    @abstractmethod
    def _analysis_homepage(self) -> List:
        raise NotImplementedError

    def get_proxy(self) -> Union[None, dict]:
        if not self._available:
            return None
        return {
            'http': choice(self._http_proxy_storage),
            'https': choice(self._https_proxy_storage),
        }

    def _check_proxy_available(self, proxy: str, protocol: str, lock: Lock) -> NoReturn:
        if protocol == 'HTTP' and self._is_http_proxy_available(proxy):
            lock.acquire()
            self._tmp_http_proxy_storage.add(proxy)
            lock.release()
        if protocol == 'HTTPS' and self._is_https_proxy_available(proxy):
            lock.acquire()
            self._tmp_https_proxy_storage.add(proxy)
            lock.release()

    def _automatic_update_monitor(self, time_watch_interval: int = 10000) -> NoReturn:
        while True:
            time.sleep(time_watch_interval)
            if time.time() - self._update_time > self._expiration_data:
                self._confirm_proxy_availability()

    @property
    def http_proxy_storage(self):
        return self._http_proxy_storage

    @property
    def https_proxy_storage(self):
        return self._https_proxy_storage
