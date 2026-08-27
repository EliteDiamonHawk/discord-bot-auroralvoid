"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.5.0
"""

import os

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv


OWNER_COMMAND_LOG_CHANNEL_ENV_VAR = "OWNER_COMMAND_LOG_CHANNEL_ID"

# Reloading this cog should pick up configuration added to .env without a bot restart.
load_dotenv()


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @staticmethod
    def _format_response(embed: discord.Embed) -> str:
        """Convert an ephemeral embed into a compact audit-log message."""
        response_parts = [part for part in (embed.title, embed.description) if part]
        response_parts.extend(
            f"{field.name}: {field.value}" for field in embed.fields
        )
        response = "\n".join(response_parts) or "No response message."
        return response[:1021] + "..." if len(response) > 1024 else response

    async def _send_ephemeral_response(
        self, context: Context, embed: discord.Embed
    ) -> None:
        """Send an ephemeral response and retain its text for the audit log."""
        await context.send(embed=embed, ephemeral=True)
        context.owner_command_response = self._format_response(embed)

    async def cog_after_invoke(self, context: Context) -> None:
        """Record successful owner commands without changing their response behavior."""
        if getattr(context, "owner_command_audit_logged", False):
            return
        context.owner_command_audit_logged = True

        try:
            log_channel_id = int(os.environ[OWNER_COMMAND_LOG_CHANNEL_ENV_VAR])
        except (KeyError, ValueError):
            self.bot.logger.warning(
                "%s is not configured; owner command was not logged.",
                OWNER_COMMAND_LOG_CHANNEL_ENV_VAR,
            )
            return

        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel is None:
            try:
                log_channel = await self.bot.fetch_channel(log_channel_id)
            except discord.DiscordException:
                self.bot.logger.warning(
                    "Unable to access the owner command log channel (%s).", log_channel_id
                )
                return

        if not isinstance(log_channel, discord.abc.Messageable):
            self.bot.logger.warning(
                "Owner command log channel (%s) cannot receive messages.", log_channel_id
            )
            return

        command_name = context.command.qualified_name if context.command else "unknown"
        location = context.guild.name if context.guild else "Direct messages"
        audit_embed = discord.Embed(
            title="Owner command executed",
            description=f"`/{command_name}`",
            color=0xBEBEFE,
        )
        audit_embed.add_field(
            name="Executed by",
            value=f"{context.author.mention} (`{context.author.id}`)",
            inline=False,
        )
        audit_embed.add_field(name="Location", value=location, inline=False)
        audit_embed.add_field(
            name="Response",
            value=getattr(context, "owner_command_response", "No response message."),
            inline=False,
        )

        try:
            await log_channel.send(
                embed=audit_embed, allowed_mentions=discord.AllowedMentions.none()
            )
        except discord.DiscordException:
            self.bot.logger.warning(
                "Unable to send an owner command audit entry to channel %s.",
                log_channel_id,
            )

    @commands.hybrid_command(
        name="sync-cmds",
        description="Synchronizes slash commands in this server.",
    )
    @commands.is_owner()
    async def sync_cmds(self, context: Context) -> None:
        """
        Synchronizes slash commands in the current server.

        :param context: The command context.
        """

        if context.guild is None:
            embed = discord.Embed(
                description="This command can only be used in a server.", color=0xE02B2B
            )
            await self._send_ephemeral_response(context, embed)
            return

        # Register an interaction response before making the API call. Command syncs
        # can take longer than Discord's three-second interaction response deadline.
        if context.interaction is not None:
            await context.defer(ephemeral=True)

        try:
            context.bot.tree.copy_global_to(guild=context.guild)
            synced_commands = await context.bot.tree.sync(guild=context.guild)
        except (app_commands.CommandLimitReached, discord.HTTPException) as error:
            self.bot.logger.exception(
                "Failed to synchronize application commands to guild %s.",
                context.guild.id,
            )
            embed = discord.Embed(
                title="Command synchronization failed",
                description=(
                    "Discord rejected the command update. Check the bot logs for "
                    f"details. (`{type(error).__name__}`)"
                ),
                color=0xE02B2B,
            )
            await self._send_ephemeral_response(context, embed)
            return

        embed = discord.Embed(
            description=f"Synchronized {len(synced_commands)} slash command(s) in this server.",
            color=0xBEBEFE,
        )
        await self._send_ephemeral_response(context, embed)

    @commands.hybrid_command(
        name="load",
        description="Load a cog",
    )
    @app_commands.describe(cog="The name of the cog to load")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        The bot will load the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to load.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not load the `{cog}` cog.", color=0xE02B2B
            )
            await self._send_ephemeral_response(context, embed)
            return
        embed = discord.Embed(
            description=f"Successfully loaded the `{cog}` cog.", color=0xBEBEFE
        )
        await self._send_ephemeral_response(context, embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        The bot will unload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to unload.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not unload the `{cog}` cog.", color=0xE02B2B
            )
            await self._send_ephemeral_response(context, embed)
            return
        embed = discord.Embed(
            description=f"Successfully unloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await self._send_ephemeral_response(context, embed)

    @commands.hybrid_command(
        name="reload",
        description="Reloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        The bot will reload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to reload.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not reload the `{cog}` cog.", color=0xE02B2B
            )
            await self._send_ephemeral_response(context, embed)
            return
        embed = discord.Embed(
            description=f"Successfully reloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await self._send_ephemeral_response(context, embed)

    @commands.hybrid_command(
        name="reload-all",
        description="Reload all currently loaded cogs.",
    )
    @commands.is_owner()
    async def reload_all(self, context: Context) -> None:
        """Reload every loaded cog and report any cogs that could not be reloaded."""
        cog_extensions = sorted(
            extension
            for extension in self.bot.extensions
            if extension.startswith("cogs.")
        )
        reloaded = []
        failed = []

        for extension in cog_extensions:
            try:
                await self.bot.reload_extension(extension)
            except commands.ExtensionError as error:
                failed.append(f"`{extension.removeprefix('cogs.')}`: {error}")
            else:
                reloaded.append(f"`{extension.removeprefix('cogs.')}`")

        embed = discord.Embed(
            title="Cog reload complete",
            description=(
                f"Reloaded: {', '.join(reloaded) if reloaded else 'none'}"
            ),
            color=0xBEBEFE if not failed else 0xE02B2B,
        )
        if failed:
            embed.add_field(
                name="Failed",
                value="\n".join(failed)[:1024],
                inline=False,
            )
        await self._send_ephemeral_response(context, embed)

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(description="Shutting down. Bye! :wave:", color=0xBEBEFE)
        await self._send_ephemeral_response(context, embed)
        await self.cog_after_invoke(context)
        await self.bot.close()

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        embed = discord.Embed(description=message, color=0xBEBEFE)
        await self._send_ephemeral_response(context, embed)


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
