from json import load,dump
from data.data_edit import dating
class Noficate:
    def __init__(self,bot,creator):

        self.ADMIN=[creator]
        self.bot=bot
        
    async def strike(self,dp):
        for _id in self.ADMIN:
            await self.bot.send_message(int(_id),'<b>Startup complete</b>')


    async def off_strike(self,dp):
        for _id in self.ADMIN:
            await self.bot.send_message(int(_id),'<b>Bot off</b>')
