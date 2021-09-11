from .. import loader, utils
from telethon import functions, types
from asyncio import sleep
msgs = [f"{i} - 7 = {i-7}" for i in range(1000, 0, -7)]


def register(cb):
    cb(axMod())


class axMod(loader.Module):
    strings = {'name': 'O_O'}

    async def client_ready(self, client, db):
        self.client = client

    async def deadinsidecmd(self, message):
        '''1000-7'''
        for word in msgs:
            await message.edit(word)
            await sleep(0.5)
        await message.delete()
