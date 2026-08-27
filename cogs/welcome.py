"""Welcome new server members."""

import random

import discord
from discord import app_commands
from discord.ext import commands


WELCOME_CHANNEL_ID = 1542382170159579218

class Welcome(commands.Cog, name="welcome"):
    """Send a randomly selected welcome message when a member joins."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @staticmethod
    def _format_message(template: str, member: discord.Member) -> str:
        """Render a welcome template using its supported placeholders."""
        return template.format(
            user=member.mention,
            server=member.guild.name,
            # Retained for compatibility with any earlier welcome templates.
            member=member.mention,
            member_name=member.display_name,
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if not WELCOME_MESSAGES:
            self.bot.logger.warning(
                "Welcome message list is empty; no welcome was sent for %s.", member
            )
            return

        channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(WELCOME_CHANNEL_ID)
            except discord.DiscordException:
                self.bot.logger.exception("Could not fetch the welcome channel.")
                return

        if not isinstance(channel, discord.abc.Messageable):
            self.bot.logger.error("Configured welcome channel cannot receive messages.")
            return

        try:
            message = self._format_message(random.choice(WELCOME_MESSAGES), member)
            if WELCOME_ASCII_IMAGES:
                message = f"{random.choice(WELCOME_ASCII_IMAGES)}\n{message}"
            await channel.send(
                message, allowed_mentions=discord.AllowedMentions(users=True)
            )
        except discord.DiscordException:
            self.bot.logger.exception("Could not send the welcome message.")

async def setup(bot: commands.Bot) -> None:
    """Load the welcome cog."""
    await bot.add_cog(Welcome(bot))








WELCOME_ASCII_IMAGES: list[str] = [
    """⡆⣿⣿⣦⠹⣳⣳⣕⢅⠈⢗⢕⢕⢕⢕⢕⢈⢆⠟⠋⠉⠁⠉⠉⠁⠈⠼⢐⢕ 
⡗⢰⣶⣶⣦⣝⢝⢕⢕⠅⡆⢕⢕⢕⢕⢕⣴⠏⣠⡶⠛⡉⡉⡛⢶⣦⡀⠐⣕ 
⡝⡄⢻⢟⣿⣿⣷⣕⣕⣅⣿⣔⣕⣵⣵⣿⣿⢠⣿⢠⣮⡈⣌⠨⠅⠹⣷⡀⢱ 
⡝⡵⠟⠈⢀⣀⣀⡀⠉⢿⣿⣿⣿⣿⣿⣿⣿⣼⣿⢈⡋⠴⢿⡟⣡⡇⣿⡇⡀ 
⡝⠁⣠⣾⠟⡉⡉⡉⠻⣦⣻⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣦⣥⣿⡇⡿⣰⢗ 
⠁⢰⣿⡏⣴⣌⠈⣌⠡⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣉⣉⣁⣄⢖⢕⢕ 
⡀⢻⣿⡇⢙⠁⠴⢿⡟⣡⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣵⣵ 
⡻⣄⣻⣿⣌⠘⢿⣷⣥⣿⠇⣿⣿⣿⣿⣿⣿⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ 
⣷⢄⠻⣿⣟⠿⠦⠍⠉⣡⣾⣿⣿⣿⣿⣿⣿⢸⣿⣦⠙⣿⣿⣿⣿⣿⣿⣿⣿ 
⡕⡑⣑⣈⣻⢗⢟⢞⢝⣻⣿⣿⣿⣿⣿⣿⣿⠸⣿⠿⠃⣿⣿⣿⣿⣿⣿⡿⠁
""",
    """⣿⡇⣿⣿⣿⠛⠁⣴⣿⡿⠿⠧⠹⠿⠘⣿⣿⣿⡇⢸⡻⣿⣿⣿⣿⣿⣿⣿
⢹⡇⣿⣿⣿⠄⣞⣯⣷⣾⣿⣿⣧⡹⡆⡀⠉⢹⡌⠐⢿⣿⣿⣿⡞⣿⣿⣿
⣾⡇⣿⣿⡇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣄⢻⣦⡀⠁⢸⡌⠻⣿⣿⣿⡽⣿⣿
⡇⣿⠹⣿⡇⡟⠛⣉⠁⠉⠉⠻⡿⣿⣿⣿⣿⣿⣦⣄⡉⠂⠈⠙⢿⣿⣝⣿
⠤⢿⡄⠹⣧⣷⣸⡇⠄⠄⠲⢰⣌⣾⣿⣿⣿⣿⣿⣿⣶⣤⣤⡀⠄⠈⠻⢮
⠄⢸⣧⠄⢘⢻⣿⡇⢀⣀⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠄⢀
⠄⠈⣿⡆⢸⣿⣿⣿⣬⣭⣴⣿⣿⣿⣿⣿⣿⣿⣯⠝⠛⠛⠙⢿⡿⠃⠄⢸
⠄⠄⢿⣿⡀⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡾⠁⢠⡇⢀
⠄⠄⢸⣿⡇⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣫⣻⡟⢀⠄⣿⣷⣾
⠄⠄⢸⣿⡇⠄⠈⠙⠿⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⡿⢠⠊⢀⡇⣿⣿
⠒⠤⠄⣿⡇⢀⡲⠄⠄⠈⠙⠻⢿⣿⣿⠿⠿⠟⠛⠋⠁⣰⠇⠄⢸⣿⣿⣿
""",
    """⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣆⠻⡫⣢⠿⣿⣿⣿⣿⣿⣿⣿⣷⣜⢻⣿
⣿⣿⡏⣿⣿⣨⣝⠿⣿⣿⣿⣿⣿⢕⠸⣛⣩⣥⣄⣩⢝⣛⡿⠿⣿⣿⣆⢝
⣿⣿⢡⣸⣿⣏⣿⣿⣶⣯⣙⠫⢺⣿⣷⡈⣿⣿⣿⣿⡿⠿⢿⣟⣒⣋⣙⠊
⣿⡏⡿⣛⣍⢿⣮⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⢱⣾⣿⣿⣿⣝⡮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⣋⣻⣿⣿⣿⣿
⢿⢸⣿⣿⣿⣿⣿⣿⣷⣽⣿⣿⣿⣿⣿⣿⣿⡕⣡⣴⣶⣿⣿⣿⡟⣿⣿⣿
⣦⡸⣿⣿⣿⣿⣿⣿⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿
⢛⠷⡹⣿⠋⣉⣠⣤⣶⣶⣿⣿⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣷⢹⣿⣿
⣷⡝⣿⡞⣿⣿⣿⣿⣿⣿⣿⣿⡟⠋⠁⣠⣤⣤⣦⣽⣿⣿⣿⡿⠋⠘⣿⣿
⣿⣿⡹⣿⡼⣿⣿⣿⣿⣿⣿⣿⣧⡰⣿⣿⣿⣿⣿⣹⡿⠟⠉⡀⠄⠄⢿⣿
⣿⣿⣿⣽⣿⣼⣛⠿⠿⣿⣿⣿⣿⣿⣯⣿⠿⢟⣻⡽⢚⣤⡞⠄⠄⠄⢸⣿
""",
]



"""Two hundred cringey anime-style Discord welcome lines and puns.

The collection mixes 50 short, 100 medium, and 50 long messages.
Use message.format(user=mention, server=guild_name) to replace placeholders.
"""

WELCOME_MESSAGES: list[str] = [
    # Short anime lines and puns (1-50)
    "W-welcome, {user}... baka!",
    "Senpai noticed {user}! ✨",
    "Nani?! {user} joined!",
    "Kawaii newcomer detected: {user}!",
    "{user} entered the filler arc.",
    "Welcome, protagonist-kun!",
    "Plot twist: {user} appeared!",
    "Sugoi! Welcome, {user}!",
    "Ara ara, {user} has arrived.",
    "{user} unlocked the welcome arc!",
    "Welcome to {server}, senpai!",
    "Our nakama gained {user}!",
    "{user} activated protagonist mode.",
    "Welcome, you adorable baka.",
    "A chibi hero approaches: {user}!",
    "{user} joined with maximum kawaii.",
    "The opening theme starts now, {user}.",
    "Welcome, {user}-chan! 🌸",
    "Senpai finally joined: {user}!",
    "{user} entered the wrong isekai.",
    "Welcome, chosen one... probably.",
    "Your power level is cringe, {user}.",
    "{user} spawned with plot armor.",
    "The tsundere arc welcomes {user}.",
    "Notice us, {user}-senpai!",
    "{user} joined the anime club!",
    "Welcome, magical bestie! ✨",
    "Main character detected: {user}.",
    "{user} arrived right on cue.",
    "Welcome to the beach episode!",
    "New rival unlocked: {user}!",
    "The squad adopted {user}.",
    "Welcome, ramen-tic hero! 🍜",
    "{user} is soy awesome! 🍱",
    "Miso happy you joined, {user}!",
    "You're one in a melon, {user}!",
    "Welcome, mochi-valued friend!",
    "Udon know how welcome you are!",
    "{user} brought the boba energy.",
    "Tempura-rily speechless—welcome, {user}!",
    "Rice to meet you, {user}!",
    "Soba glad you're here!",
    "Welcome, my cup of sencha!",
    "You're shrimply amazing, {user}!",
    "Welcome to the cringe arc, {user}!",
    "Your waifu Wi-Fi connected successfully.",
    "The subtitles say: welcome, {user}!",
    "{user} just skipped the intro.",
    "Welcome, future final-boss bestie!",
    "Episode one begins with {user}.",

    # Medium anime lines and puns (51-150)
    "A mysterious transfer student just entered the server, {user}! Try not to reveal your hidden powers before introductions.",
    "Welcome to {server}, {user}! Try not to reveal your hidden powers before introductions; a mysterious transfer student just entered the server.",
    "The opening theme is playing at full volume, {user}! Your main-character arc officially begins right now.",
    "Welcome to {server}, {user}! Your main-character arc officially begins right now; the opening theme is playing at full volume.",
    "Our tsundere welcome committee says it is not happy to see you, {user}! It just prepared confetti for completely unrelated reasons.",
    "Welcome to {server}, {user}! It just prepared confetti for completely unrelated reasons; our tsundere welcome committee says it is not happy to see you.",
    "A suspiciously sparkly portal opened in the welcome channel, {user}! Apparently destiny delivered our newest hero.",
    "Welcome to {server}, {user}! Apparently destiny delivered our newest hero; a suspiciously sparkly portal opened in the welcome channel.",
    "The council of senpais has reviewed your application, {user}! You have been approved for maximum notice-me energy.",
    "Welcome to {server}, {user}! You have been approved for maximum notice-me energy; the council of senpais has reviewed your application.",
    "Your friendship power level is already climbing, {user}! One introduction could unlock the legendary nakama bonus.",
    "Welcome to {server}, {user}! One introduction could unlock the legendary nakama bonus; your friendship power level is already climbing.",
    "Truck-kun missed the exit and dropped you here instead, {user}! Welcome to your strangely wholesome new isekai.",
    "Welcome to {server}, {user}! Welcome to your strangely wholesome new isekai; truck-kun missed the exit and dropped you here instead.",
    "The server soundtrack suddenly became emotional, {user}! The writers clearly planned a dramatic entrance for you.",
    "Welcome to {server}, {user}! The writers clearly planned a dramatic entrance for you; the server soundtrack suddenly became emotional.",
    "A wild protagonist has appeared in {server}, {user}! Please select friendship instead of fighting.",
    "Welcome to {server}, {user}! Please select friendship instead of fighting; a wild protagonist has appeared in {server}.",
    "The magical-girl transformation sequence has begun, {user}! Your first special ability is making the server more fabulous.",
    "Welcome to {server}, {user}! Your first special ability is making the server more fabulous; the magical-girl transformation sequence has begun.",
    "Your plot armor has been successfully equipped, {user}! You may now explore every channel without fear of character development.",
    "Welcome to {server}, {user}! You may now explore every channel without fear of character development; your plot armor has been successfully equipped.",
    "The beach episode started earlier than expected, {user}! Grab a coconut and pretend this is essential to the plot.",
    "Welcome to {server}, {user}! Grab a coconut and pretend this is essential to the plot; the beach episode started earlier than expected.",
    "Our resident rival sensed a powerful new presence, {user}! Please challenge them to a friendship montage immediately.",
    "Welcome to {server}, {user}! Please challenge them to a friendship montage immediately; our resident rival sensed a powerful new presence.",
    "The subtitles translated your entrance as extremely cool, {user}! The dub just screamed welcome for no reason.",
    "Welcome to {server}, {user}! The dub just screamed welcome for no reason; the subtitles translated your entrance as extremely cool.",
    "A chibi version of the welcome committee is running toward you, {user}! Prepare for tiny hugs and enormous enthusiasm.",
    "Welcome to {server}, {user}! Prepare for tiny hugs and enormous enthusiasm; a chibi version of the welcome committee is running toward you.",
    "Your secret anime backstory has been detected, {user}! Save the tragic flashback until at least episode three.",
    "Welcome to {server}, {user}! Save the tragic flashback until at least episode three; your secret anime backstory has been detected.",
    "The filler arc has finally become interesting, {user}! Your arrival may have rescued the entire season.",
    "Welcome to {server}, {user}! Your arrival may have rescued the entire season; the filler arc has finally become interesting.",
    "A ramen bowl foretold the coming of a new member, {user}! The prophecy was oddly specific about your username.",
    "Welcome to {server}, {user}! The prophecy was oddly specific about your username; a ramen bowl foretold the coming of a new member.",
    "The mecha hangar has assigned you a suspiciously shiny robot, {user}! Please read the rules before launching it indoors.",
    "Welcome to {server}, {user}! Please read the rules before launching it indoors; the mecha hangar has assigned you a suspiciously shiny robot.",
    "Your dramatic cape is fluttering without any visible wind, {user}! The laws of anime physics clearly welcome you.",
    "Welcome to {server}, {user}! The laws of anime physics clearly welcome you; your dramatic cape is fluttering without any visible wind.",
    "The student council president approved your transfer, {user}! Attendance is optional but friendship is mandatory.",
    "Welcome to {server}, {user}! Attendance is optional but friendship is mandatory; the student council president approved your transfer.",
    "A thousand cherry blossoms appeared when you joined, {user}! The animation budget may never recover from your entrance.",
    "Welcome to {server}, {user}! The animation budget may never recover from your entrance; a thousand cherry blossoms appeared when you joined.",
    "Your inner demon requested server access, {user}! We approved it as long as it follows the community guidelines.",
    "Welcome to {server}, {user}! We approved it as long as it follows the community guidelines; your inner demon requested server access.",
    "The tournament bracket gained one mysterious competitor, {user}! Everyone is pretending not to be intimidated by your aura.",
    "Welcome to {server}, {user}! Everyone is pretending not to be intimidated by your aura; the tournament bracket gained one mysterious competitor.",
    "A tiny mascot declared you the chosen one, {user}! Nobody understands the quest but the merchandise looks adorable.",
    "Welcome to {server}, {user}! Nobody understands the quest but the merchandise looks adorable; a tiny mascot declared you the chosen one.",
    "Your first friendship flag has been triggered, {user}! Say hello before the writers turn this into a slow-burn arc.",
    "Welcome to {server}, {user}! Say hello before the writers turn this into a slow-burn arc; your first friendship flag has been triggered.",
    "The villain monologue stopped the moment you arrived, {user}! Even evil respects a properly dramatic welcome.",
    "Welcome to {server}, {user}! Even evil respects a properly dramatic welcome; the villain monologue stopped the moment you arrived.",
    "A glowing notification appeared above the server, {user}! It says your social quest has officially begun.",
    "Welcome to {server}, {user}! It says your social quest has officially begun; a glowing notification appeared above the server.",
    "The anime café saved its coziest booth for you, {user}! Tea, cake, and unnecessary blushing are included.",
    "Welcome to {server}, {user}! Tea, cake, and unnecessary blushing are included; the anime café saved its coziest booth for you.",
    "Your aura is giving rare limited-edition character, {user}! The community is already rolling for your friendship banner.",
    "Welcome to {server}, {user}! The community is already rolling for your friendship banner; your aura is giving rare limited-edition character.",
    "The opening narration called you a normal new member, {user}! So naturally we assume you possess forbidden powers.",
    "Welcome to {server}, {user}! So naturally we assume you possess forbidden powers; the opening narration called you a normal new member.",
    "A ninja delivered your welcome message three episodes late, {user}! Please blame the flashback arc and accept our apology.",
    "Welcome to {server}, {user}! Please blame the flashback arc and accept our apology; a ninja delivered your welcome message three episodes late.",
    "The spirit of friendship sensed your arrival, {user}! Prepare for a motivational speech that lasts six episodes.",
    "Welcome to {server}, {user}! Prepare for a motivational speech that lasts six episodes; the spirit of friendship sensed your arrival.",
    "Your character design has too many belts to be ordinary, {user}! The server suspects you are important to the plot.",
    "Welcome to {server}, {user}! The server suspects you are important to the plot; your character design has too many belts to be ordinary.",
    "The moon is unusually large behind you tonight, {user}! This can only mean your dramatic arc is about to begin.",
    "Welcome to {server}, {user}! This can only mean your dramatic arc is about to begin; the moon is unusually large behind you tonight.",
    "A magical contract appeared beside your username, {user}! Read the tiny print before agreeing to save the server.",
    "Welcome to {server}, {user}! Read the tiny print before agreeing to save the server; a magical contract appeared beside your username.",
    "The cooking club prepared a legendary welcome feast, {user}! Every dish contains at least one terrible anime pun.",
    "Welcome to {server}, {user}! Every dish contains at least one terrible anime pun; the cooking club prepared a legendary welcome feast.",
    "Your entrance caused three reaction shots and a commercial break, {user}! That is how we know you are important.",
    "Welcome to {server}, {user}! That is how we know you are important; your entrance caused three reaction shots and a commercial break.",
    "A soft piano theme started when you clicked join, {user}! The emotional character development begins after introductions.",
    "Welcome to {server}, {user}! The emotional character development begins after introductions; a soft piano theme started when you clicked join.",
    "The guild receptionist stamped your adventurer card, {user}! Your rank is currently adorable novice with hidden potential.",
    "Welcome to {server}, {user}! Your rank is currently adorable novice with hidden potential; the guild receptionist stamped your adventurer card.",
    "Your server uniform arrived with a cape and cat ears, {user}! The dress code is apparently determined by fan service.",
    "Welcome to {server}, {user}! The dress code is apparently determined by fan service; your server uniform arrived with a cape and cat ears.",
    "A dramatic gust scattered paperwork across the hallway, {user}! Congratulations on your classic transfer-student entrance.",
    "Welcome to {server}, {user}! Congratulations on your classic transfer-student entrance; a dramatic gust scattered paperwork across the hallway.",
    "The final boss paused the apocalypse to greet you, {user}! Even world-ending threats have basic server manners.",
    "Welcome to {server}, {user}! Even world-ending threats have basic server manners; the final boss paused the apocalypse to greet you.",
    "A sleepy dragon added you to its treasure hoard, {user}! Apparently new friends are more valuable than gold.",
    "Welcome to {server}, {user}! Apparently new friends are more valuable than gold; a sleepy dragon added you to its treasure hoard.",
    "Your welcome speech has been dubbed into seventeen languages, {user}! Every version somehow sounds more dramatic.",
    "Welcome to {server}, {user}! Every version somehow sounds more dramatic; your welcome speech has been dubbed into seventeen languages.",
    "The prophecy named a hero with suspiciously good Discord taste, {user}! The evidence points directly to you.",
    "Welcome to {server}, {user}! The evidence points directly to you; the prophecy named a hero with suspiciously good discord taste.",
    "A tiny fox spirit followed you through the server gates, {user}! It has already claimed half your snacks.",
    "Welcome to {server}, {user}! It has already claimed half your snacks; a tiny fox spirit followed you through the server gates.",
    "Your social stats received an unexpected anime buff, {user}! Joining conversations now grants double friendship experience.",
    "Welcome to {server}, {user}! Joining conversations now grants double friendship experience; your social stats received an unexpected anime buff.",
    "The romance subplot accidentally targeted the welcome bot, {user}! Please ignore the blushing notification and proceed normally.",
    "Welcome to {server}, {user}! Please ignore the blushing notification and proceed normally; the romance subplot accidentally targeted the welcome bot.",
    "The ending credits can wait a little longer, {user}! Your story in {server} is only getting started.",
    "Welcome to {server}, {user}! Your story in {server} is only getting started; the ending credits can wait a little longer.",

    # Long anime lines and puns (151-200)
    "W-welcome to {server}, {user}—not that we were waiting for you or anything! The welcome committee only rehearsed this speech twelve times, decorated the channel with cherry blossoms, and prepared a dramatic soundtrack because it was bored. Check the rules, choose your roles, and introduce yourself before anyone notices us blushing.",
    "W-welcome to {server}, {user}—not that we were waiting for you or anything! Check the rules, choose your roles, and introduce yourself before anyone notices us blushing. The welcome committee only rehearsed this speech twelve times, decorated the channel with cherry blossoms, and prepared a dramatic soundtrack because it was bored.",
    "A blinding portal has deposited you in the strange new world of {server}, {user}. Your legendary starter abilities include reading pinned messages, reacting to announcements, and gaining friendship points by joining conversations. May your isekai adventure be wholesome, your plot armor remain strong, and Truck-kun stay very far away.",
    "A blinding portal has deposited you in the strange new world of {server}, {user}. May your isekai adventure be wholesome, your plot armor remain strong, and Truck-kun stay very far away. Your legendary starter abilities include reading pinned messages, reacting to announcements, and gaining friendship points by joining conversations.",
    "Senpai has finally noticed our server, and somehow that senpai is you, {user}. The entire cast is performing synchronized reaction shots while the opening theme swells dramatically in the background. Please explore the channels and say hello before the animation budget runs out.",
    "Senpai has finally noticed our server, and somehow that senpai is you, {user}. Please explore the channels and say hello before the animation budget runs out. The entire cast is performing synchronized reaction shots while the opening theme swells dramatically in the background.",
    "The ancient prophecy spoke of a chosen newcomer named {user}. It claimed this hero would enter {server}, collect powerful roles, form an unstoppable nakama, and defeat the terrible final boss known as awkward silence. Your quest begins with an introduction, brave protagonist.",
    "The ancient prophecy spoke of a chosen newcomer named {user}. Your quest begins with an introduction, brave protagonist. It claimed this hero would enter {server}, collect powerful roles, form an unstoppable nakama, and defeat the terrible final boss known as awkward silence.",
    "Nani?! A new challenger has appeared in {server}, and their name is {user}! Your aura is mysterious, your backstory is probably tragic, and your hair somehow moves even though there is no wind indoors. Join the party, meet your rivals, and prepare for a friendship tournament arc.",
    "Nani?! A new challenger has appeared in {server}, and their name is {user}! Join the party, meet your rivals, and prepare for a friendship tournament arc. Your aura is mysterious, your backstory is probably tragic, and your hair somehow moves even though there is no wind indoors.",
    "The magical welcome sequence has activated for {user}! Sparkles are flying, ribbons are spinning, and a tiny talking mascot is explaining rules that definitely should have been mentioned before the transformation contract. Choose your roles carefully and use your newfound power of friendship responsibly.",
    "The magical welcome sequence has activated for {user}! Choose your roles carefully and use your newfound power of friendship responsibly. Sparkles are flying, ribbons are spinning, and a tiny talking mascot is explaining rules that definitely should have been mentioned before the transformation contract.",
    "Welcome, {user}, to the coziest anime café in the Discord multiverse. Your table includes warm tea, fresh mochi, soft background music, and at least three side characters quietly wondering whether you are secretly the protagonist. Settle in, meet the regulars, and enjoy your wholesome slice-of-life arc.",
    "Welcome, {user}, to the coziest anime café in the Discord multiverse. Settle in, meet the regulars, and enjoy your wholesome slice-of-life arc. Your table includes warm tea, fresh mochi, soft background music, and at least three side characters quietly wondering whether you are secretly the protagonist.",
    "Player {user} has unlocked the ultra-rare server known as {server}. This limited banner features friendly guildmates, chaotic side quests, collectible roles, and a suspiciously generous friendship drop rate. Spend your social energy wisely, because the pity system guarantees a new bestie eventually.",
    "Player {user} has unlocked the ultra-rare server known as {server}. Spend your social energy wisely, because the pity system guarantees a new bestie eventually. This limited banner features friendly guildmates, chaotic side quests, collectible roles, and a suspiciously generous friendship drop rate.",
    "A transfer student named {user} just opened the classroom door three minutes late. Every character has turned toward you, the curtains are moving dramatically, and someone by the window has already decided you are their destined rival. Pick a seat, introduce yourself, and try not to reveal your forbidden technique before lunch.",
    "A transfer student named {user} just opened the classroom door three minutes late. Pick a seat, introduce yourself, and try not to reveal your forbidden technique before lunch. Every character has turned toward you, the curtains are moving dramatically, and someone by the window has already decided you are their destined rival.",
    "The mecha bay has registered a new pilot: {user}. Your machine is powered by courage, questionable engineering, loud motivational speeches, and the combined friendship energy of everyone in {server}. Read the operating rules before launch, then prepare to pierce the awkwardness of meeting new people.",
    "The mecha bay has registered a new pilot: {user}. Read the operating rules before launch, then prepare to pierce the awkwardness of meeting new people. Your machine is powered by courage, questionable engineering, loud motivational speeches, and the combined friendship energy of everyone in {server}.",
    "Ara ara, it seems {user} has wandered into {server}. Do not worry about the ominous music, the glowing eyes in the background, or the suspiciously calm upperclassman offering you tea. Everything is probably fine, so choose your roles and make yourself comfortable.",
    "Ara ara, it seems {user} has wandered into {server}. Everything is probably fine, so choose your roles and make yourself comfortable. Do not worry about the ominous music, the glowing eyes in the background, or the suspiciously calm upperclassman offering you tea.",
    "The server's ramen oracle predicted your arrival, {user}. According to the noodles, you possess rare flavor, powerful broth energy, and the ability to make every conversation miso much better. Udon know how excited we are, so grab a bowl and join the community.",
    "The server's ramen oracle predicted your arrival, {user}. Udon know how excited we are, so grab a bowl and join the community. According to the noodles, you possess rare flavor, powerful broth energy, and the ability to make every conversation miso much better.",
    "A tiny chibi welcome squad is charging toward you, {user}. Their legs are moving impossibly fast, their eyes contain approximately ninety percent of the animation budget, and they are carrying a banner twice their size. Accept the cuteness, explore {server}, and prepare for extremely wholesome chaos.",
    "A tiny chibi welcome squad is charging toward you, {user}. Accept the cuteness, explore {server}, and prepare for extremely wholesome chaos. Their legs are moving impossibly fast, their eyes contain approximately ninety percent of the animation budget, and they are carrying a banner twice their size.",
    "The villain was halfway through a forty-minute monologue when {user} joined {server}. Even the final boss stopped, adjusted their cape, and admitted that welcoming a new member is more important than explaining the entire evil plan. Use this rare intermission to introduce yourself and assemble your heroic party.",
    "The villain was halfway through a forty-minute monologue when {user} joined {server}. Use this rare intermission to introduce yourself and assemble your heroic party. Even the final boss stopped, adjusted their cape, and admitted that welcoming a new member is more important than explaining the entire evil plan.",
    "A shower of cherry blossoms announced your entrance, {user}. Nobody knows where the petals came from because we are indoors, but anime physics has clearly decided that your arrival deserves maximum romantic drama. Enjoy the scenery, meet the cast, and please ignore the server blushing in the corner.",
    "A shower of cherry blossoms announced your entrance, {user}. Enjoy the scenery, meet the cast, and please ignore the server blushing in the corner. Nobody knows where the petals came from because we are indoors, but anime physics has clearly decided that your arrival deserves maximum romantic drama.",
    "Your hidden power awakened the moment you joined {server}, {user}. The screen shook, the narrator gasped, and three elders whispered that such powerful community energy had not been seen for a thousand years. Train by reading the rules, then unleash your ultimate technique: saying hello.",
    "Your hidden power awakened the moment you joined {server}, {user}. Train by reading the rules, then unleash your ultimate technique: saying hello. The screen shook, the narrator gasped, and three elders whispered that such powerful community energy had not been seen for a thousand years.",
    "Welcome, {user}; your beach-episode invitation was approved. The plot has been temporarily suspended for snacks, volleyball, suspiciously elaborate swimsuits, and character development disguised as a relaxing day off. Grab a drink, meet everyone, and pretend this episode is absolutely essential.",
    "Welcome, {user}; your beach-episode invitation was approved. Grab a drink, meet everyone, and pretend this episode is absolutely essential. The plot has been temporarily suspended for snacks, volleyball, suspiciously elaborate swimsuits, and character development disguised as a relaxing day off.",
    "The guild receptionist looked at {user}'s paperwork and immediately fainted. Apparently your stats include legendary friendliness, mythical meme potential, and an unexplained skill called Main Character Entrance at maximum level. Collect your roles, greet your new party, and begin adventuring through {server}.",
    "The guild receptionist looked at {user}'s paperwork and immediately fainted. Collect your roles, greet your new party, and begin adventuring through {server}. Apparently your stats include legendary friendliness, mythical meme potential, and an unexplained skill called Main Character Entrance at maximum level.",
    "A mysterious fox spirit guided you to {server}, {user}. It promised ancient wisdom, magical protection, and unlimited friendship, but it has already stolen your snacks and denied everything with an adorable expression. Follow it into the channels and see what kind of story awaits.",
    "A mysterious fox spirit guided you to {server}, {user}. Follow it into the channels and see what kind of story awaits. It promised ancient wisdom, magical protection, and unlimited friendship, but it has already stolen your snacks and denied everything with an adorable expression.",
    "The opening theme for episode one starts the moment {user} enters {server}. There are fast cuts of future friends, shadowy villains, dramatic sunsets, and one confusing scene that will not make sense until season three. Join the cast now and help us make this arc worth watching.",
    "The opening theme for episode one starts the moment {user} enters {server}. Join the cast now and help us make this arc worth watching. There are fast cuts of future friends, shadowy villains, dramatic sunsets, and one confusing scene that will not make sense until season three.",
    "The student council held an emergency meeting about your arrival, {user}. After hours of dramatic debate, unnecessary paperwork, and one emotionally charged flashback, they unanimously approved your membership in {server}. Review the rules, select your roles, and enjoy your suspiciously prestigious welcome.",
    "The student council held an emergency meeting about your arrival, {user}. Review the rules, select your roles, and enjoy your suspiciously prestigious welcome. After hours of dramatic debate, unnecessary paperwork, and one emotionally charged flashback, they unanimously approved your membership in {server}.",
    "Your arrival caused the server narrator to whisper, 'Everything changed that day.' Nobody knows what changed, but {user} now has plot armor, a mysterious pendant, and several strangers willing to risk everything after one conversation. Welcome to {server}; please use this narrative importance responsibly.",
    "Your arrival caused the server narrator to whisper, 'Everything changed that day.' Welcome to {server}; please use this narrative importance responsibly. Nobody knows what changed, but {user} now has plot armor, a mysterious pendant, and several strangers willing to risk everything after one conversation.",
    "Mochi have we waited for this moment, {user}! {server} is soy excited to meet you that the kitchen prepared ramen-tic noodles, tempura-rary decorations, and enough boba to fuel an entire training montage. Rice to meet you—now grab a snack and join the pun-filled party.",
    "Mochi have we waited for this moment, {user}! Rice to meet you—now grab a snack and join the pun-filled party. {server} is soy excited to meet you that the kitchen prepared ramen-tic noodles, tempura-rary decorations, and enough boba to fuel an entire training montage.",
    "A cosmic anime beacon detected your legendary vibes, {user}. Your starship has docked at {server}, where the crew communicates through dramatic holograms, emotional speeches, and occasional episodes with surprisingly low animation quality. Report to introductions and prepare for the friendship frontier.",
    "A cosmic anime beacon detected your legendary vibes, {user}. Report to introductions and prepare for the friendship frontier. Your starship has docked at {server}, where the crew communicates through dramatic holograms, emotional speeches, and occasional episodes with surprisingly low animation quality.",
    "Congratulations, {user}; you have reached the final episode of being a stranger. The credits tried to roll, but {server} demanded another season filled with new conversations, ridiculous adventures, running jokes, and wholesome character growth. Press play on your next arc by choosing a role and saying hello.",
    "Congratulations, {user}; you have reached the final episode of being a stranger. Press play on your next arc by choosing a role and saying hello. The credits tried to roll, but {server} demanded another season filled with new conversations, ridiculous adventures, running jokes, and wholesome character growth.",
]
