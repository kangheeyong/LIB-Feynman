import cmd
import asyncio
import websockets

from fire import Fire

from Feynman.etc.util import get_logger


class templete_cmd(cmd.Cmd):
    def __init__(self):
        self.logger = get_logger()

    async def _main(self):
        uri = "ws://localhost:8765/123"
        while True:
            name = input("What's your name? ")
            async with websockets.connect(uri) as websocket:
                await websocket.send(name)
                print('> {}'.format(name))
                greeting = await websocket.recv()
                print('< {}'.format(greeting))

    def run(self):
        asyncio.run(self._main())


if __name__ == '__main__':
    Fire(templete_cmd)
