from discord.ext import commands
import discord
from discord import Activity, ActivityType
from discord.commands import slash_command, message_command, command
from discord.ui import View

import asyncio
import logging
import yt_dlp as ytdl

import random
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

AUTHORIZED_GUILDS = eval(str(os.getenv("AUTHORIZED_GUILDS"))).values()

YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "m4a/bestaudio/best",
    "audio-quality": "128K",
    "quiet": True,
    "extract_flat": "in_playlist",
    "no_playlist": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "m4a"
    }]
}

FFMPEG_BEFORE_OPTS = \
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 20'


async def audio_playing(ctx):
    """Check if audio is currently playing."""
    client = ctx.guild.voice_client

    return True if client and client.channel and client.source else False


async def in_voice_channel(ctx):
    """Check if the user is in the same voice channel as the bot."""
    voice = ctx.user.voice
    bot_voice = ctx.guild.voice_client

    return True if voice and bot_voice and voice.channel and \
        bot_voice.channel and voice.channel == bot_voice.channel else False


class Video:
    """Represents a video from YouTube."""

    def __init__(self, url_or_search, requested_by):
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            video = ydl.extract_info(url_or_search, download=False)
            self.stream_url = video["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.duration = video["duration"]
            self.thumbnail = video["thumbnail"] if "thumbnail" in video \
                else None
            self.requested_by = requested_by

    def get_embed(self):
        """Return an embed with the video information."""
        embed = discord.Embed(title=self.title,
                              description="",
                              url=self.video_url)
        embed.set_footer(text=f"Ajouté par {self.requested_by.name}",
                         icon_url=self.requested_by.avatar)

        embed.set_thumbnail(url=self.thumbnail) if self.thumbnail else embed
        return embed


class MusicInteraction(View):
    """Base class for music interactions."""

    def __init__(self, music_player, url):
        super().__init__(timeout=None)
        self.player = music_player
        self.playing = True
        self.video_url = url
        self.errorMessage = "Tu dois être dans le même " + \
            "salon vocal que le bot pour ça"

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.grey)
    async def pause_button_callback(self, button, interaction):
        client = interaction.guild.voice_client
        if interaction.user.voice:
            if interaction.user.voice.channel.id == client.channel.id:
                if self.playing:
                    button.label = "Play"
                    button.style = discord.ButtonStyle.primary
                else:
                    button.label = "Pause"
                    button.style = discord.ButtonStyle.grey
                self.playing = not self.playing
                await interaction.response.edit_message(view=self)
                self.player._pause_audio(interaction.guild.voice_client)
            else:
                await interaction.response.send_message(self.errorMessage,
                                                        ephemeral=True)
        else:
            await interaction.response.send_message(self.errorMessage,
                                                    ephemeral=True)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.grey)
    async def skip_button_callback(self, button, interaction):
        client = interaction.guild.voice_client
        if interaction.user.voice:
            if interaction.user.voice.channel.id == client.channel.id:
                await self.player._skip(interaction)
            else:
                await interaction.response.send_message(self.errorMessage,
                                                        ephemeral=True)
        else:
            await interaction.response.send_message(self.errorMessage,
                                                    ephemeral=True)

    @discord.ui.button(label="Loop", style=discord.ButtonStyle.grey)
    async def loop_button_callback(self, button, interaction):
        client = interaction.guild.voice_client
        if interaction.user.voice:
            if interaction.user.voice.channel.id == client.channel.id:
                if await self.player._loop(interaction):
                    if await self.player.get_loop_status(interaction):
                        button.style = discord.ButtonStyle.success
                    else:
                        button.style = discord.ButtonStyle.grey
                    await interaction.response.edit_message(view=self)
                else:
                    await interaction.response.send_message(
                        "Il n'y a pas de musique en cours.")
            else:
                await interaction.response.send_message(self.errorMessage,
                                                        ephemeral=True)
        else:
            await interaction.response.send_message(self.errorMessage,
                                                    ephemeral=True)

    @discord.ui.button(label="Shuffle", style=discord.ButtonStyle.secondary)
    async def shuffle_button_callback(self, button, interaction):
        client = interaction.guild.voice_client
        if interaction.user.voice:
            if interaction.user.voice.channel.id == client.channel.id:
                state = self.player.get_state(interaction.guild)
                if len(state.playlist) > 2:
                    await self.player._shuffle_playlist(state)
                    await interaction.response.send_message("Shuffled!",
                                                            ephemeral=True)
                else:
                    await interaction.response.send_message(
                        "La playlist doit être plus remplie !", ephemeral=True)
            else:
                await interaction.response.send_message(
                    self.errorMessage, ephemeral=True)
        else:
            await interaction.response.send_message(
                self.errorMessage, ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
    async def stop_button_callback(self, button, interaction):
        client = interaction.guild.voice_client
        if interaction.user.voice:
            if interaction.user.voice.channel.id == client.channel.id:
                await self.player._stop(interaction, client)
            else:
                await interaction.response.send_message(self.errorMessage,
                                                        ephemeral=True)
        else:
            await interaction.response.send_message(self.errorMessage,
                                                    ephemeral=True)


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.states = {}

    def get_state(self, guild):
        """Get the GuildState for a guild, \
           or create one if it does not exist."""
        if guild.id in self.states:
            return self.states[guild.id]
        else:
            self.states[guild.id] = GuildState()
            return self.states[guild.id]

    async def _stop(self, interaction, client):
        """Leave the voice channel and clear the playlist."""
        state = self.get_state(interaction.guild)
        await client.disconnect()
        state.playlist = []
        state.now_playing = None
        asyncio.run_coroutine_threadsafe(
            self.bot.change_presence(activity=None), self.bot.loop)

    def _pause_audio(self, client):
        client.resume() if client.is_paused() else client.pause()

    async def _skip(self, interaction):
        interaction.guild.voice_client.stop()

    async def _shuffle_playlist(self, state):
        playlist_copy = state.playlist[1:]
        random.shuffle(playlist_copy)
        playlist_copy.insert(0, state.playlist[0])
        state.playlist = playlist_copy

    def _play_song(self, ctx, client, state,
                   song, seek_option=FFMPEG_BEFORE_OPTS):
        state.now_playing = song
        _activity = Activity(name=f"{song.title}",
                             type=getattr(ActivityType, "listening",
                                          ActivityType.playing))
        asyncio.run_coroutine_threadsafe(
            self.bot.change_presence(activity=_activity), self.bot.loop)
        channel = client.channel
        source = discord.FFmpegOpusAudio(song.stream_url,
                                         before_options=seek_option)
        print(f"Je lance {song.title}")

        def after_playing(err):
            if state.seek_asked:
                state.seek_asked = False
                state.playlist.pop(1)

            elif state.loop_flag and (len(channel.members) > 1):
                next_song = state.now_playing
                self._play_song(ctx, client, state, next_song)

            elif (len(state.playlist) > 1) and (len(channel.members) > 1):
                state.playlist.pop(0)
                next_song = Video(state.playlist[0][0], state.playlist[0][2])
                if state.player_message is not None:
                    asyncio.run_coroutine_threadsafe(
                        state.player_message.edit(view=None), self.bot.loop)
                self._play_song(ctx, client, state, next_song)
                asyncio.run_coroutine_threadsafe(
                    self.send_player(next_song, state), self.bot.loop)

            else:
                while len(state.playlist) >= 1:
                    state.playlist.pop(0)
                asyncio.run_coroutine_threadsafe(
                    state.player_message.edit(view=None), self.bot.loop)
                state.now_playing = None
                asyncio.run_coroutine_threadsafe(client.disconnect(),
                                                 self.bot.loop)
                asyncio.run_coroutine_threadsafe(
                    self.bot.change_presence(activity=None), self.bot.loop)

        client.play(source, after=after_playing)

    async def _loop(self, interaction):
        if await audio_playing(interaction):
            state = self.get_state(interaction.guild)
            state.loop_flag = not state.loop_flag
            return True
        else:
            return False

    async def get_loop_status(self, interaction):
        state = self.get_state(interaction.guild)
        return state.loop_flag

    @message_command(name="Afficher la queue", guild_ids=AUTHORIZED_GUILDS)
    async def queue(self, interaction, message):
        """Send the current queue."""
        state = self.get_state(interaction.guild)
        await interaction.response.send_message(self._queue_text(state)[:2000],
                                                ephemeral=True)

    def _queue_text(self, state):
        """Create the text for the current queue."""
        queue = state.playlist
        if len(queue) > 0 or state.now_playing is not None:
            message = ['**Queue :**']
            message += [
                f'  [P] **{state.playlist[0][1]}** \
                        (Ajoutée par **{str(state.playlist[0][2])[:-5]}**)'
            ]
            # add songs individually
            for i in range(len(state.playlist) - 1):
                message += [
                    f"  [{i+1}] **{state.playlist[i+1][1]}** " +
                    "(Ajoutée par ** " +
                    f"{str(state.playlist[i+1][2])[:-5]}**)"
                ]
            return "\n".join(message)
        else:
            return "La file est vide !"

    @slash_command(guild_ids=AUTHORIZED_GUILDS)
    @commands.guild_only()
    async def play(self, ctx, *, url):
        """Play a song from youtube from a url or \
            search query. can be a playlist."""

        client = ctx.guild.voice_client
        state = self.get_state(ctx.guild)

        await ctx.defer()

        if client and client.channel:
            if ctx.author.voice:
                if ctx.author.voice.channel.id == client.channel.id:

                    try:
                        videoList = []
                        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
                            video = ydl.extract_info(url, download=False)
                            if "_type" in video and \
                               video["_type"] == "playlist":
                                for i in range(len(video["entries"])):
                                    videoList.append([
                                        video["entries"][i]["url"],
                                        video["entries"][i]["title"],
                                        ctx.author
                                    ])
                            else:
                                videoList.append(
                                    [url, video["title"], ctx.author])

                    except ytdl.DownloadError as e:
                        logging.warn(f"Error downloading video: {e}")
                        await state.webhook.send(
                            "Une erreur est survenue pendant le \
                                téléchargement de la musique.",
                            ephemeral=True)
                        return

                    for video in videoList:
                        state.playlist.append([video[0], video[1], video[2]])

                    await ctx.followup.send(content="Musique(s) ajoutée(s)")

                else:
                    await ctx.response.send_message(
                        "Le bot est déjà dans un autre channel",
                        ephemeral=True)
            else:
                await ctx.response.send_message(
                    "Le bot est déjà dans un autre channel", ephemeral=True)

        else:
            if ctx.author.voice is not None and \
               ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel
                try:
                    videoList = []
                    with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
                        video = ydl.extract_info(url, download=False)
                        if "_type" in video and video["_type"] == "playlist":
                            for i in range(len(video["entries"])):
                                videoList.append([
                                    video["entries"][i]["url"],
                                    video["entries"][i]["title"], ctx.author
                                ])
                        else:
                            videoList.append([url, video["title"], ctx.author])

                except ytdl.DownloadError:
                    await state.webhook.send(
                        "Une erreur est survenue pendant le téléchargement \
                            de la musique.",
                        ephemeral=True)
                    return

                print("Je me connecte au vocal")

                client = await channel.connect()
                state.loop_flag = False  # reset loop flag

                for video in videoList:
                    state.playlist.append([video[0], video[1], video[2]])

                await ctx.followup.send(content="Musique(s) ajoutée(s)")

                if ctx.author.voice is not None and \
                   ctx.author.voice.channel is not None:
                    currentSong = Video(state.playlist[0][0],
                                        state.playlist[0][2])

                    await self.get_webhook(ctx, state)

                    await self.send_player(currentSong, state)

                    self._play_song(ctx, client, state, currentSong)

            else:
                await ctx.response.send_message(
                    "Tu dois être dans un salon vocal pour faire ça.",
                    ephemeral=True)

    async def get_webhook(self, ctx, state):
        """Get the webhook for the bot, or create one if it doesn't exist."""

        bot_name = ctx.guild.me.display_name

        guild_webhooks = await ctx.guild.webhooks()
        count = 0
        for webhook in guild_webhooks:
            webhook.user
            if webhook.user == ctx.guild.me:
                count += 1

        if count == 0:
            state.webhook = await ctx.channel.create_webhook(name=bot_name)
        elif count == 1:
            for webhook in guild_webhooks:
                if webhook.user == ctx.guild.me:
                    state.webhook = webhook
        else:
            count = 0
            for webhook in guild_webhooks:
                if webhook.user == ctx.guild.me:
                    if count == 0:
                        count += 1
                        state.webhook = webhook
                    else:
                        await webhook.delete()

        state.webhook_pp = str(ctx.guild.me.display_avatar.url)

    async def send_player(self, currentSong, state):
        embed = currentSong.get_embed()
        embed.add_field(name="Duration",
                        value=f"{currentSong.duration} seconds",
                        inline=True)
        state.player_message = \
            await state.webhook.send(
                embed=embed,
                view=MusicInteraction(self, currentSong.video_url),
                avatar_url=state.webhook_pp,
                wait=True)

    @command(name='seek')
    async def seek(self, ctx, new_pos: int):
        """Seek to a specified duration in the current song."""
        client = ctx.guild.voice_client

        if client and client.channel:
            if ctx.author.voice:
                if ctx.author.voice.channel.id == client.channel.id:
                    if await audio_playing(ctx):
                        state = self.get_state(ctx.guild)
                        current_song = state.now_playing
                        if current_song:
                            if 0 <= new_pos <= current_song.duration:
                                # Modifier le délai de départ pour avancer
                                state.seek_asked = True
                                options = f"{FFMPEG_BEFORE_OPTS} -ss {new_pos}"
                                state.playlist.insert(
                                    1, [
                                        current_song.video_url,
                                        current_song.title,
                                        current_song.requested_by.name])
                                client.stop()
                                self._play_song(ctx, client,
                                                state,
                                                current_song, options)
                                await ctx.response.send_message(
                                    "Seeked !", ephemeral=True)
                            else:
                                await ctx.response.send_message(
                                    "La position demandée est invalide.",
                                    ephemeral=True)
                    else:
                        await ctx.response.send_message(
                            "Aucune musique en cours de lecture.",
                            ephemeral=True)
                else:
                    await ctx.response.send_message(
                        "Vous devez être dans le même canal vocal que le bot.",
                        ephemeral=True)
            else:
                await ctx.response.send_message(
                    "Vous devez être dans un canal vocal pour"
                    "utiliser cette commande.",
                    ephemeral=True)
        else:
            await ctx.response.send_message(
                "Le bot n'est pas connecté à un canal vocal.", ephemeral=True)


def setup(bot):
    bot.add_cog(Music(bot))


class GuildState:
    """Contains the state of a guild."""

    def __init__(self):
        self.playlist = []
        self.now_playing = None
        self.webhook = None
        self.player_message = None
        self.loop_flag = False
        self.webhook_pp = None
        self.seek_asked = False
