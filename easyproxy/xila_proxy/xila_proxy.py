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
from typing import List
import requests
from bs4 import BeautifulSoup
from aitool import singleton
from ..web_page_proxy import WebPageProxy
import logging
import os
from .__init__ import XiLaPath


@singleton
class XiLaProxy(WebPageProxy):
    def __init__(self):
        super().__init__(record_file_path=os.path.join(XiLaPath, 'record.json'))

    def _analysis_homepage(self) -> List:
        for page_index in range(1, 10):
            results = []
            try:
                homepage = 'http://www.xiladaili.com/gaoni/{}/'.format(page_index)
                html = requests.get(url=homepage).text
                soup = BeautifulSoup(html, 'lxml')
                trs = soup.select_one('.fl-table').select_one('tbody').select('tr')
                results = [[tr.select('td')[0].text, set(tr.select('td')[1].text.replace('代理', '').split(','))] for tr in trs]
            except Exception as e:
                print(e)
                logging.error(e)
            print('{} candidate proxies collected from {}'.format(len(results), homepage))
            logging.info('{} candidate proxies collected from {}'.format(len(results), homepage))
            yield results
