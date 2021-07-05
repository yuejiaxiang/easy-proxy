# -*- coding: UTF-8 -*-
# Copyright©2020 xiangyuejia@qq.com All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This module contains some base classes which can assist developer to
implement spider functions faster and clearer.
"""
from typing import Union
import requests
from abc import ABCMeta, abstractmethod
from .header import header
import logging


class ProxyBase(metaclass=ABCMeta):
    """
    The interface Class of proxy.
    """
    @abstractmethod
    def get_proxy(self) -> Union[None, dict]:
        raise NotImplementedError

    @classmethod
    def _is_http_proxy_available(cls, proxy: str) -> bool:
        proxies = {'http': proxy}
        test_url = 'http://ip.tool.chinaz.com/'
        try:
            logging.debug('url: {}, proxies: {}')
            requests.get(url=test_url, proxies=proxies, headers=header, timeout=5).text
        except Exception as e:
            logging.debug('{} unavailable, {}'.format(proxy, e))
            return False
        logging.info('{} available for http'.format(proxy))
        return True

    @classmethod
    def _is_https_proxy_available(cls, proxy: str) -> bool:
        proxies = {'https': r'https://' + proxy}
        test_url = 'https://blog.csdn.net/luoyangIT'
        try:
            logging.debug('url: {}, proxies: {}')
            requests.get(url=test_url, headers=header, proxies=proxies, timeout=5).text
        except Exception as e:
            logging.debug('{} unavailable, {}'.format(proxy, e))
            return False
        logging.info('{} available for https'.format(proxy))
        return True

    @classmethod
    def _is_proxy_available(cls, proxy: str, protocol: str) -> bool:
        if protocol == 'HTTP' and cls._is_http_proxy_available(proxy):
            return True
        if protocol == 'HTTPS' and cls._is_https_proxy_available(proxy):
            return True
        return False
