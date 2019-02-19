"""Parallel file download test """

import os
import sys
import time
import aiohttp
import asyncio
import async_timeout
import requests
from lxml import html
from functools import wraps
from collections import defaultdict
from threading import Thread, Lock


def timeit(func):
    """
    Decorator for printing execution time of the function
    Unfortunately well-known timeit module/function cannot measure the execution time
    of a function with arguments
    """

    @wraps(func)
    def timer_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print('\nfunction {} took {}s'.format(
            func.__name__, round(time.time() - start_time, 3)))
        return result
    return timer_func


@timeit
def get_tarballs_list(size):
    """
    Returns list of absolute path links to the source tarballs from python.org
    :param size:  amount of links
    :return: list of link strings
    """

    response = requests.get('https://www.python.org/downloads/source/')
    if response.status_code != 200:
        raise Exception('Unexpected response {}'.format(response))

    doc = html.fromstring(response.text)
    return [x.attrib['href'] for x in doc.xpath('.//a[text()="Gzipped source tarball"]')][:size]


def print_progress(prog_dict):
    """
    Prints download progress for every file
    :param prog_dict: dict in {file_name: file_size, ...} format
    """

    msg = ', '.join(['{:>20}: {:<8}'.format(file_name, round(file_size / 1048576, 3))
                     for file_name, file_size in prog_dict.items()])
    sys.stdout.write('\rDownloaded (MiB): {}'.format(msg))
    sys.stdout.flush()


@timeit
def aiohttp_download(urls, chunk_size):
    """
    Downloads files from urls using aiohttp, asyncio
    :param urls: list of URL strings
    :param chunk_size:  chunk size for writing data
    """

    async def aiohttp_download(session, url):
        print('start downloading using aiohttp from {}'.format(url))
        with async_timeout.timeout(200):
            async with session.get(url) as response:
                file_name = os.path.basename(url)
                with open(file_name, 'wb') as f_handle:
                    while True:
                        chunk = await response.content.read(chunk_size)
                        if not chunk:
                            break

                        f_handle.write(chunk)

                        prog_dict[file_name] += len(chunk)
                        print_progress(prog_dict)

    async def main(loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            await asyncio.gather(*[aiohttp_download(session, url) for url in urls])

    prog_dict = defaultdict(float)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))


@timeit
def threading_download(urls, chunk_size):
    """
    Downloads files from urls using threading
    :param urls: list of URL strings
    :param chunk_size:  chunk size for writing data
    """

    print_lock = Lock()

    def downloader(session, url):
        print('start downloading using threading from {}'.format(url))
        file_name = os.path.basename(url)

        with requests.get(url, stream=True) as response:
            with open(file_name, 'wb') as f_handle:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if not chunk:
                        break
                    f_handle.write(chunk)

                    with print_lock:
                        prog_dict[file_name] += len(chunk)
                        print_progress(prog_dict)

    prog_dict = defaultdict(float)
    session = requests.Session()

    threads = []
    for url in urls:
        thread = Thread(target=downloader, args=(session, url))
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]


if __name__ == '__main__':
    urls = get_tarballs_list(10)
    chunk_size = 16384

    print('\n== Start perf test of downloading using aiohttp, asyncio ==\n')
    aiohttp_download(urls, chunk_size)

    print('\n== Start perf test of downloading using threading ==\n')
    threading_download(urls, chunk_size)
