"""Commands for posting messages without revealing the sender publicly."""

import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


AUDIT_LOG_CHANNEL_ENV_VAR = "ANONYMOUS_AUDIT_LOG_CHANNEL_ID"

# Reloading this cog should pick up configuration added to .env without a bot restart.
load_dotenv()

class Anonymous(commands.Cog, name="anonymous"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="say",
        description="Send a message anonymously in this channel.",
    )
    @app_commands.describe(message="The message to send anonymously.")
    async def say(self, interaction: discord.Interaction, message: str) -> None:
        """Post ``message`` publicly while recording its author in the audit log."""
        if interaction.guild is None or interaction.channel is None:
            await interaction.response.send_message(
                "This command can only be used in a server channel.", ephemeral=True
            )
            return

        try:
            audit_log_channel_id = int(os.environ[AUDIT_LOG_CHANNEL_ENV_VAR])
        except (KeyError, ValueError):
            await interaction.response.send_message(
                "Error Sending Message: Error 1",
                ephemeral=True,
            )
            return

        allowed_mentions = discord.AllowedMentions.none()
        anonymous_message = await interaction.channel.send(
            message, allowed_mentions=allowed_mentions
        )

        log_channel = self.bot.get_channel(audit_log_channel_id)
        if log_channel is None:
            try:
                log_channel = await self.bot.fetch_channel(audit_log_channel_id)
            except discord.DiscordException:
                await anonymous_message.delete()
                await interaction.response.send_message(
                    "Error Sending Message: Error 2",
                    ephemeral=True,
                )
                return

        audit_embed = discord.Embed(
            title="Anonymous message sent",
            description=(
                f"Sent by {interaction.user.mention} (`{interaction.user.id}`) "
                f"in {interaction.channel.mention}."
            ),
            color=0xBEBEFE,
        )
        audit_embed.add_field(
            name="Message",
            value=message[:1021] + "..." if len(message) > 1024 else message,
            inline=False,
        )
        audit_embed.add_field(name="Message link", value=anonymous_message.jump_url)

        try:
            await log_channel.send(embed=audit_embed, allowed_mentions=allowed_mentions)
        except discord.DiscordException:
            await anonymous_message.delete()
            await interaction.response.send_message(
                "Error Sending Message: Error 3",
                ephemeral=True,
            )
            return

        await interaction.response.send_message("Message sent.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Anonymous(bot))
