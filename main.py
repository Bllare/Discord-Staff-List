"""
Discord : @bllare
Github : Bllare
"""
import discord
from discord.ext import commands
import asyncio
from json import load
from time import sleep


class StaffList():
    def __init__(self):
        self.config = load(open("config.json","r"))
        self.Settings = self.config["Settings"]
        self.Roles = self.config["Roles"]

    def SetupBot(self):
        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix='!', intents=intents)

        self.SendMessage()
        self.OnReady()

        self.bot.run(self.Settings["Token"])
            
    def OnReady(self):
        if self.Settings["MessageID"] == 1:return
        @self.bot.event
        async def on_ready():
            print("Bot Is Ready!") 
            # Get Staff List
            guild = self.bot.get_guild(self.Settings["GuildID"])
            channel = self.bot.get_channel(self.Settings["ChannelID"])
            message = await channel.fetch_message(self.Settings["MessageID"])

            RoleID_Warn1 = guild.get_role(self.Settings["RoldeID_Warn1"])
            RoleID_Warn2 = guild.get_role(self.Settings["RoldeID_Warn2"])
            RoleID_Warn3 = guild.get_role(self.Settings["RoldeID_Warn3"])

            while True:
                self.List = {}
                for Role in self.Roles:
                    role = guild.get_role(self.Roles[Role]["RoleID"])
                    members = role.members
                    if Role not in self.List:
                        self.List[Role] = set()
                    for member in members:
                        self.List[Role].add(member.id)

                # Make Message
                Text = ""
                for Role in self.List:
                    Text += f"# {Role}\n"
                    for MemberID in self.List[Role]:
                        warn = 0
                        user = guild.get_member(MemberID)
                        if RoleID_Warn1 in user.roles:
                            warn = 1
                        if RoleID_Warn2 in user.roles:
                            warn = 2
                        if RoleID_Warn3 in user.roles:
                            warn = 3
                            
                        Text += f"<@{MemberID}> **Warnings {warn}/3** \n"

                embed = discord.Embed(title="Staff List", description=f"{Text}", color=0x00ff00)
                
                await message.edit(content="",embed=embed)
                sleep(5)

    def SendMessage(self):
        @self.bot.command()
        @commands.has_permissions(administrator=True)
        async def SendMessage(ctx):
        # Send Message
            await ctx.send("Copy Message ID")
        # permission fail
        @SendMessage.error
        async def SendMessage_error(ctx, error):
            return
            message = await ctx.send("You dont have administrator permission")
            await asyncio.sleep(5) 
            await message.delete()

                                
                


if __name__ == "__main__":
    discordBot = StaffList()
    discordBot.SetupBot()