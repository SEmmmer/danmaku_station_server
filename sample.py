# -*- coding: utf-8 -*-

import asyncio

import blivedm
import datetime
import os


class MyBLiveClient(blivedm.BLiveClient):
    # 演示如何自定义handler
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    async def _on_receive_popularity(self, popularity: int):
        print(f'当前人气值：{popularity}')

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        the_time = str(datetime.datetime.now()).split(" ", 1)
        filename = 'danmaku_files/' + the_time[0] + '.txt'
        if danmaku.user_level > 5:
            if danmaku.msg_type == 0:
                danmaku_content = f'{danmaku.timestamp}:{danmaku.uid}:{danmaku.msg}\n'
                with open(filename, "a+") as code:
                    code.write(danmaku_content)
                    code.close()
                    print(f'{danmaku.timestamp}:{danmaku.uid}:{danmaku.msg}')


async def main():
    # 参数1是直播间ID
    # 如果SSL验证失败就把ssl设为False
    client = MyBLiveClient(21613730, ssl=True)
    future = client.start()
    try:
        await future
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
