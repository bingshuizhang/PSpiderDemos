# _*_ coding: utf-8 _*_

"""
inst_parse.py by xianhu
"""

import re
import logging
import datetime
from ..utilities import get_url_legal


class ParserAsync(object):
    """
    class of ParserAsync, must include function parse()
    """

    def __init__(self, max_deep=0):
        """
        constructor
        """
        self._max_deep = max_deep       # default: 0, if -1, spider will not stop until all urls are fetched
        return

    async def parse(self, priority: int, url: str, keys: object, deep: int, content: object) -> (int, list, list):
        """
        parse the content of a url, must "try, except" and don't change the parameters and return
        :return (parse_result, url_list, save_list): parse_result can be -1(parse failed), 1(parse success)
        :return (parse_result, url_list, save_list): url_list is [(url, keys, priority), ...], save_list is [item(a list or tuple), ...]
        """
        logging.debug("%s start: priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, priority, keys, deep, url)

        try:
            *_, html_text = content

            parse_result, url_list = 1, []
            if (self._max_deep < 0) or (deep < self._max_deep):
                a_list = re.findall(r"<a[\w\W]+?href=\"(?P<url>[\w\W]{5,}?)\"[\w\W]*?>[\w\W]+?</a>", html_text, flags=re.IGNORECASE)
                url_list = [(_url, keys, priority + 1) for _url in [get_url_legal(href, url) for href in a_list]]

            title = re.search(r"<title>(?P<title>[\w\W]+?)</title>", html_text, flags=re.IGNORECASE)
            save_list = [(title.group("title").strip(), datetime.datetime.now()), ] if title else []
        except Exception as excep:
            parse_result, url_list, save_list = -1, [], []
            logging.error("%s error: %s, priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, excep, priority, keys, deep, url)

        logging.debug("%s end: parse_result=%s, len(url_list)=%s, len(save_list)=%s, url=%s", self.__class__.__name__, parse_result, len(url_list), len(save_list), url)
        return parse_result, url_list, save_list
