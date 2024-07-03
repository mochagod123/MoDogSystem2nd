from discord.ext import commands
import discord
from discord import Webhook
import os
import requests
import random
from pytube import YouTube
import json
from bs4 import BeautifulSoup
import time
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from rembg import remove
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from discord_webhook import DiscordWebhook
import re
from discord import app_commands
from googletrans import Translator
import datetime
import subprocess
import pyttsx3
import asyncio
import logging
from moviepy.editor import *
import pyshorteners
import shutil
import glob
import pickle
from ast import keyword
from googleapiclient.discovery import build
import suddendeath
import yt_dlp as youtube_dl

# 自作ライブラリ
import TextDataBase
from cogs import dogAI

intents = discord.Intents.default()
intents.members = True # メンバー管理の権限
intents.message_content = True # メッセージの内容を取得する権限

# Botをインスタンス化
bot = commands.Bot(
    command_prefix="mc!", # $コマンド名　でコマンドを実行できるようになる
    case_insensitive=True, # コマンドの大文字小文字を区別しない ($hello も $Hello も同じ!)
    intents=intents # 権限を設定
)

# データ倉庫
bot.adsurl = 'まだありません'
bot.globalchaturl = ''
bot.autoreplaywww = 'まだありません'
bot.markinguser = 'マーキングUser'
bot.ytdlcheck = 0
bot.useridgamelist = 'UserIDゲームのリスト'
bot.jp = None
bot.en = None
bot.maingchat = None

# Tokens
token = "Token"
bot.youtubeapikey = "Token"

print('<------------------>')

with open("token.txt") as f:
    token = f.read()

with open("ytapikey.txt") as f:
    bot.youtubeapikey = f.read()

# 再起動後も読み込み
with open("save/autoreplay.txt") as f:
    l_strip = [s.rstrip() for s in f.readlines()]
    bot.autoreplaywww = int(l_strip[0])
    print(f'自動返信-草を許可したか?: {bot.autoreplaywww}')

with open("save/gads.txt", encoding="utf-8") as f:
    l_strip = [s.rstrip() for s in f.readlines()]
    bot.adsurl = l_strip[0]
    print(f'グローバル宣伝: {bot.adsurl}')

with open("save/marking.txt", encoding="utf-8") as f:
    l_strip = [s.rstrip() for s in f.readlines()]
    bot.markinguser = l_strip
    print(f'危険人物リスト: {bot.markinguser}')

with open("save/useridgame.txt", encoding="utf-8") as f:
    l_strip = [s.rstrip() for s in f.readlines()]
    bot.useridgamelist = l_strip
    print(f'ユーザーIDゲーム: {bot.useridgamelist}')

with open('data/Lang/jp.json', encoding="utf-8") as f:
    bot.jp = json.load(f)

with open('data/Lang/en.json', encoding="utf-8") as f:
    bot.en = json.load(f)

print('<------------------>')
def remove_background(input_image_path, output_image_path):
    # 背景を削除
    try:
        input_image = Image.open(input_image_path)
    except IOError:
        print(f"Error: Cannot open {input_image_path}")
        return

    output_image = remove(input_image)
    output_image.save(output_image_path)

def apply_mask_to_background(masked_image_path):
    # RGBA画像を読み込み
    rgba_image = cv2.imread(masked_image_path, cv2.IMREAD_UNCHANGED)
    if rgba_image is None:
        print(f"Error: Cannot open {masked_image_path}")
        return

    # アルファチャネルをマスクとして使用
    alpha_channel = rgba_image[:, :, 3]

    # 白い背景画像を作成
    background = np.ones_like(rgba_image, dtype=np.uint8) * 255
    # マスクを適用
    background_masked = cv2.bitwise_and(background, background, mask=alpha_channel)
    return background_masked

def is_open_check(filepath: str) -> bool:
    try:
        f = open(filepath, 'a')
        f.close()
    except:
        return True
    else:
        return False

def ReadAutoReplayList(path: str):
    f = open(path, encoding="utf-8")
    ret = [s.rstrip() for s in f.readlines()]
    return ret

def WriteAutoReplayList(path: str, addname: str):
    a = open(file=path, mode='a', encoding="utf-8")
    a.write(f"{addname}\n")

def FuncUranai():
    unsei = ["大吉", "中吉", "吉", "末吉", "小吉", "凶", "大凶"]
    choice = random.choice(unsei)
    return choice

def FuncJanken():
    list=["グー","チョキ","パー"]
    choice = random.choice(list)
    return choice

def Robokasu(path: str, addname: str):
    image1 = Image.open("data/Robo/Base.png")
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 15)
    draw.text((40, 45), path, fill=(0, 0, 0), font=font)
    image1.save(f"data/Robo/{addname}.png")

class Janken(discord.ui.View):
    @discord.ui.button(label="グー")
    async def ok(self, interaction: discord.Interaction, button: discord.Button) -> None:
        unsei = ["あなたの勝ち！", "あなたの負けw\nじゃんけんやめたら？www", "あいこ"]
        choice = random.choice(unsei)
        await interaction.channel.send(choice)

    @discord.ui.button(label="チョキ")
    async def ng(self, interaction: discord.Interaction, button: discord.Button) -> None:
        unsei = ["あなたの勝ち！", "あなたの負けw\nじゃんけんやめたら？www", "あいこ"]
        choice = random.choice(unsei)
        await interaction.channel.send(choice)

    @discord.ui.button(label="パー")
    async def pa(self, interaction: discord.Interaction, button: discord.Button) -> None:
        unsei = ["あなたの勝ち！", "あなたの負けw\nじゃんけんやめたら？www", "あいこ"]
        choice = random.choice(unsei)
        await interaction.channel.send(choice)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


#URLや言葉を参照するとき..
#lines[参照したい行].rstrip()
#といれて使う。

@bot.event
async def on_ready():
    os.system('cls')
    print("--Log--")
    await bot.tree.sync()
    count = len(bot.guilds)
    await bot.change_presence(activity=discord.Game(name=f"mc!help | {count}鯖"))
    startnot = "ドッグ起動通知"
    for channel in bot.get_all_channels():
	    if channel.name == startnot:
		    await channel.send("犬が起きました")

@bot.event
async def on_member_join(member):
    if os.path.exists(f"save/Servers/{member.guild.id}"):
        if os.path.isfile(f"save/Servers/{member.guild.id}/joinrole.txt"):
            with open(f"save/Servers/{member.guild.id}/joinrole.txt", "r") as f:
                readrole = f.read()
            # 用意したIDから Role オブジェクトを取得
            role = member.guild.get_role(int(readrole))

            # 入ってきた Member に役職を付与
            await member.add_roles(role)

        if os.path.isfile(f"save/Servers/{member.guild.id}/welcome.txt"):
            with open(f"save/Servers/{member.guild.id}/welcome.txt", "r", encoding="utf-8") as f:
                readwelcome = f.read()
                if os.path.isfile(f"save/Servers/{member.guild.id}/welcha.txt"):
                    fa = open(f"save/Servers/{member.guild.id}/welcha.txt", 'r', encoding="utf-8")
                    chan = fa.read()
                    channel = bot.get_channel(int(chan))
                    fa.close()
                    await channel.send(readwelcome)

@bot.event
async def on_guild_join(guild):
    await guild.me.edit(nick=bot.jp['BotName'])
    if os.path.isfile(f"save/banserver.txt"):
        for guluds in ReadAutoReplayList(f"save/banserver.txt"):
            if (guild.id == int(guluds)):
                arashi1 = await bot.fetch_guild(int(guluds))
                time.sleep(0.5)
                startnot = "ddos攻撃対策"
                for channel in bot.get_all_channels():
                    if channel.name == startnot:
                        await channel.send(f"{guluds}からDDOS攻撃を受けたため、BANされました。")
                await arashi1.leave()

@bot.event
async def on_voice_state_update(member, before, after):
    os.system('cls')
    if os.path.isfile(f"save/mutehaku.txt"):
        if f"{after.channel.id}" in ReadAutoReplayList(f"save/mutehaku.txt"):
            if member.voice.self_mute == True:    
                time.sleep(0.5)
                await member.move_to(None)
                os.system('cls')

    if os.path.isfile(f"save/vcbanch.txt"):
        if os.path.isfile(f"save/vcbanid.txt"):
            if f"{after.channel.id}" in ReadAutoReplayList(f"save/vcbanch.txt"):
                if f"{member.id}" in ReadAutoReplayList(f"save/vcbanid.txt"):   
                    await member.move_to(None)
                    os.system('cls')

@bot.event
async def on_message(message: discord.Message):
    # 自動返信
    if 'www' in message.content:
        if bot.autoreplaywww == 1:
            if message.author.bot:
                pass
            else:
                await message.channel.send('wwww')

    if os.path.isfile(f"save/Servers/{message.guild.id}/autoreplay.txt"):
        if message.content in ReadAutoReplayList(f"save/Servers/{message.guild.id}/autoreplay.txt"):
            if message.author.bot:
                pass
            else:
                await message.channel.send(ReadAutoReplayList(f"save/Servers/{message.guild.id}/autoreplayanswer.txt")[ReadAutoReplayList(f"save/Servers/{message.guild.id}/autoreplay.txt").index(message.content)])

    if os.path.isfile(f"save/rolepanel.txt"):
        if message.content in ReadAutoReplayList(f"save/rolepanel.txt"):
            if message.author.bot:
                pass
            elif ReadAutoReplayList(f"save/rolepanela.txt")[ReadAutoReplayList(f"save/rolepanel.txt").index(message.content)]:
                role = message.guild.get_role(int(ReadAutoReplayList(f"save/rolepanela.txt")[ReadAutoReplayList(f"save/rolepanel.txt").index(message.content)]))
                await message.author.add_roles(role)
                await message.channel.send(f"{message.author.mention}にロールを付与しました。")

    if os.path.isfile(f"save/Servers/{message.guild.id}/customcommand.txt"):
        if message.content in ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommand.txt"):
            ut = datetime.datetime.now()

            if message.author.bot:
                pass
            elif ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt")[ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommand.txt").index(message.content)] in "<time>":
                await message.channel.send(ut)
            elif ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt")[ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommand.txt").index(message.content)] in "<uranai>":
                await message.channel.send(FuncUranai())
            elif ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt")[ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommand.txt").index(message.content)] in "<dragon>":
                message.guild.voice_client.play(discord.FFmpegPCMAudio("data/Sound/DRG.mp3"))
                await message.channel.send("ドラゴンの鳴き声を再生しました。")
            elif ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt")[ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommand.txt").index(message.content)] in "<Knight>":
                message.guild.voice_client.play(discord.FFmpegPCMAudio("data/Sound/KSD.mp3"))
                await message.channel.send("騎士の走る音を再生しました。")
            else:
                await message.channel.send(ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt")[ReadAutoReplayList(f"save/Servers/{message.guild.id}/customcommand.txt").index(message.content)])

    if os.path.isfile(f"save/Servers/{message.guild.id}/automod.txt"):
        if message.author.bot:
            pass
        if message.content in ReadAutoReplayList(f"save/Servers/{message.guild.id}/automod.txt"):
            await message.channel.purge(limit=1)

    if os.path.isfile(f"save/marking.txt"):
        if message.author.bot:
            pass
        if str(message.author.id) in ReadAutoReplayList(f"save/marking.txt"):
            if os.path.isfile(f"save/Servers/{message.guild.id}/gmutenable.txt"):
                await message.channel.purge(limit=1)

    files = glob.glob("save/GChat/*.json")
    ret = [s.rstrip() for s in files]
    id = message.channel.name.replace('mcg2-', '')
    for a in ret:
        file_path = a
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        if id in file_name:
            os.system('cls')
            if message.author.bot:
                pass
            elif str(message.author.id) in ReadAutoReplayList(f"save/gchatban.txt"):
                await message.author.send("あなたは、GChatからBANされています!")
                pass
            else:
                startnot = f"{message.channel.name}"
                for channel in bot.get_all_channels():
                    if channel.name == startnot:
                        id = message.content.replace('@', '')
                        if channel == message.channel: #発言したチャンネルには送らない
                            continue
                        if message.attachments != []:
                            embed = discord.Embed(title=message.author.display_name, color=message.author.accent_color)
                            embed.add_field(name="メッセージ",value=id)
                            embed.set_image(url=message.attachments[0].url)
                            embed.set_thumbnail(url=message.author.avatar)
                            await channel.send(embed=embed)
                            await message.add_reaction('<:connect:1257669190719111271>')
                            await message.add_reaction('<:database:1257668508406382603>')
                        else:
                            embed = discord.Embed(title=message.author.display_name, color=message.author.accent_color)
                            embed.add_field(name="メッセージ",value=id)
                            embed.set_thumbnail(url=message.author.avatar)
                            await channel.send(embed=embed)
                            await message.add_reaction('<:connect:1257669190719111271>')

    if os.path.isfile(f"save/Users/{message.author.id}/afkmode.txt"):
        if message.author.bot:
            pass
        if str(message.author.id) in ReadAutoReplayList(f"save/Users/{message.author.id}/afkmode.txt"):
            os.remove(f"save/Users/{message.author.id}/afkmode.txt")
            await message.channel.send('AFKが解除されました。')

    if os.path.isfile(f"save/blockcmd.txt"):
        if not str(message.author.id) in ReadAutoReplayList(f"save/blockcmd.txt"):
            if os.path.isfile(f"save/blockch.txt"):
                if not str(message.channel.id) in ReadAutoReplayList(f"save/blockch.txt"):
                    # Mocha専用こまんど
                    if 'mcm!ddos ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        user = await bot.fetch_guild(int(r))
                        if message.author.id == 1205847533763428412:
                            await user.leave()
                            await message.channel.send(f'DDOS対策の為、{r}から脱退させました。')
                        if not message.author.id == 1205847533763428412:
                            await message.channel.send('あなたは関連者ではありません。\n関連者専用コマンドです。')

                    # プレミアム機能
                    if 'mcp!buy' in message.content:
                        await message.channel.send("~プレミアム機能~\nプレミアム機能の購入は現在受け付けておりません。")

                    if 'mcp!ads' in message.content:
                        await message.channel.send("~プレミアム機能~\nプレミアム機能の購入は現在受け付けておりません。\n予定: 宣伝をすることが出来ます!\n値段予定:300円")

                    # Bot関連
                    if 'mc!announce' in message.content:
                        await message.channel.send(f'「hbc-announce」という、テキストチャンネルを作成してください。\nそこにBotのお知らせを送信します。')

                    if 'mc!help' in message.content:
                        await message.channel.send("https://mochagod123.github.io/MoDog-BotWeb/")

                    if 'mc!donate' in message.content:
                        await message.channel.send("寄付は現在受け付けておりません。")

                    if 'mc!botads' in message.content:
                        await message.channel.send("HunterBot\nhttps://discord.com/oauth2/authorize?client_id=1242795774002073610&permissions=8&scope=bot\n自作ボット！\n掲示板機能、フレンド検索機能、音楽再生、Google検索、Amazon検索、QRコード作成などいろいろな機能があります！\n便利だから入れてね！\n前の名前は、モカBot\n管理者権限は、メッセージ削除機能などあるため、つけています。\nあと、権限設定で困らないようにするためです！\nご了承ください。", file=discord.File('data/ads.png'))

                    if 'mc!sendlog ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        print(r)

                    if 'mc!clearlog' in message.content:
                        os.system('cls')

                    if 'mc!dmtest ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        await message.author.send(r)

                    if 'mc!mentiogetntest ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        id = re.findall('<@(.*)>', r)
                        await message.channel.send(id[0])

                    if 'mc!kugiri ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        r.rsplit(' ')
                        print(r.rsplit(' '))
                        list = r.rsplit(' ')
                        print(list[0])
                        print(list[1])

                    # 音楽関連
                    if 'mc!join' in message.content:
                        if message.author.voice is None:
                            await message.channel.send("あなたはボイスチャンネルに接続していません。")
                            return
                        await message.author.voice.channel.connect()
                        await message.channel.send('参加しました。')

                    if 'mc!leave' in message.content:
                        await message.guild.voice_client.disconnect()
                        await message.channel.send('退出しました。')

                    if 'mc!play ' in message.content:
                        if message.guild.voice_client is None:
                            await message.channel.send("接続していません。")
                            return
                        # 再生中の場合は再生しない
                        if message.guild.voice_client.is_playing():
                            await message.channel.send("再生中です。")
                            return         
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.id == 1205847533763428412:
                            # youtubeから音楽をダウンロードする
                            player = await YTDLSource.from_url(r, loop=bot.loop)
                            # 再生する
                            await message.guild.voice_client.play(player)

                    if 'mc!ssplay ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if r == "Dragon":
                            message.guild.voice_client.play(discord.FFmpegPCMAudio("data/Sound/DRG.mp3"))
                        elif r == "Knight":
                            message.guild.voice_client.play(discord.FFmpegPCMAudio("data/Sound/KSD.mp3"))
                        elif r == "You":
                            message.guild.voice_client.play(discord.FFmpegPCMAudio("data/Sound/YOU.mp3"))
                        elif r == "XXHunter":
                            message.guild.voice_client.play(discord.FFmpegPCMAudio("data/Sound/MHX.mp3"))

                    if 'mc!speak ' in message.content:
                        ut = time.time()
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        engine = pyttsx3.init()
                        engine.setProperty('rate', 150)
                        engine.setProperty('volume', 3)
                        text = r
                        engine.save_to_file(text, f'{ut}.wav')
                        engine.runAndWait()
                        message.guild.voice_client.play(discord.FFmpegPCMAudio(f"{ut}.wav"))
                        await asyncio.sleep(30)
                        os.remove(f'{ut}.wav')

                    if 'mc!stop' in message.content:
                        if not message.guild.voice_client.is_playing():
                            await message.channel.send("再生していません。")
                            return
                        message.guild.voice_client.stop()
                        await message.channel.send('停止しました。')

                    # おもしろ
                    if 'mc!uranai' in message.content:
                        if os.path.isfile(f"save/Servers/{message.guild.id}/jp.txt"):
                            unsei = [bot.jp['Uranai']['Daikiti'], bot.jp['Uranai']['Chukiti'], bot.jp['Uranai']['Kiti'], bot.jp['Uranai']['Suekiti'], bot.jp['Uranai']['Kyou'], bot.jp['Uranai']['Daikyo']]
                            choice = random.choice(unsei)
                            await message.channel.send(choice)
                        elif os.path.isfile(f"save/Servers/{message.guild.id}/en.txt"):
                            unsei = [bot.en['Uranai']['Daikiti'], bot.en['Uranai']['Chukiti'], bot.en['Uranai']['Kiti'], bot.en['Uranai']['Suekiti'], bot.en['Uranai']['Kyou'], bot.en['Uranai']['Daikyo']]
                            choice = random.choice(unsei)
                            await message.channel.send(choice)

                    if 'mc!janken' in message.content:
                        await message.channel.send(view=Janken())

                    if 'mc!minesweeper' in message.content:
                        unsei = ["||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:two:||||:bomb:||||:one:||\n||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:three:||||:two:||\n||:zero:||||:one:||||:one:||||:one:||||:zero:||||:one:||||:one:||||:two:||||:bomb:||\n||:zero:||||:one:||||:bomb:||||:two:||||:one:||||:zero:||||:zero:||||:one:||||:one:||\n||:zero:||||:one:||||:three:||||:bomb:||||:two:||||:zero:||||:zero:||||:zero:||||:zero:||\n||:zero:||||:zero:||||:three:||||:bomb:||||:three:||||:zero:||||:zero:||||:zero:||||:zero:||\n||:zero:||||:zero:||||:two:||||:bomb:||||:two:||||:zero:||||:zero:||||:one:||||:one:||\n||:one:||||:one:||||:one:||||:one:||||:one:||||:zero:||||:zero:||||:two:||||:bomb:||\n||:bomb:||||:one:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:two:||||:bomb:||", "||:one:||||:bomb:||||:one:||||:zero:||||:two:||||:bomb:||||:two:||||:one:||||:bomb:||\n||:one:||||:one:||||:one:||||:zero:||||:two:||||:bomb:||||:two:||||:one:||||:one:||\n||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||||:zero:||||:zero:||\n||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||\n||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:one:||||:bomb:||||:one:||\n||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:zero:||||:two:||||:two:||||:two:||\n||:zero:||||:zero:||||:zero:||||:one:||||:one:||||:one:||||:two:||||:bomb:||||:three:||\n||:zero:||||:zero:||||:zero:||||:two:||||:bomb:||||:two:||||:two:||||:bomb:||||:bomb:||\n||:zero:||||:zero:||||:zero:||||:two:||||:bomb:||||:two:||||:one:||||:two:||||:two:||"]
                        choice = random.choice(unsei)
                        await message.channel.send(choice)

                    if 'mc!hunter' in message.content:
                        url = ""
                        response = requests.get(url)
                        jsonData = response.json()
                        embed = discord.Embed(title="ハンターさん")
                        embed.set_image(url=jsonData["message"])
                        msg = await message.channel.send(embed=embed)
                        await msg.add_reaction('<:gene:1257669020136640575>')

                    if 'mc!mhavatar ' in message.content:
                        ut = time.time()
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            image1 = Image.open("data/MonsterHunter/hunter.jpg")
                            draw = ImageDraw.Draw(image1)
                            font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 50)
                            draw.text((bot.hunteravatarfontsetting, 0), r, fill=(0, 0, 0), font=font)
                            image1.save(f"data/MonsterHunter/{ut}.png")
                            await message.channel.send(file=discord.File(f'data/MonsterHunter/{ut}.png'))
                            os.remove(f"data/MonsterHunter/{ut}.png")

                    if 'mc!shinchoku ' in message.content:
                        ut = time.time()
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            image1 = Image.open("data/Shinchoku/Base.png")
                            draw = ImageDraw.Draw(image1)
                            font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 10)
                            draw.text((45, 24), r, fill=(255, 255, 255), font=font)
                            image1.save(f"data/Shinchoku/{ut}.png")
                            await message.channel.send(file=discord.File(f'data/Shinchoku/{ut}.png'))
                            os.remove(f'data/Shinchoku/{ut}.png')

                    if 'mc!mypanel1 ' in message.content:
                        ut = time.time()
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        r.rsplit(' ')
                        list = r.rsplit(' ')
                        if message.author.guild_permissions.administrator:
                            image1 = Image.open("data/Jiko/Base.jpg")
                            draw = ImageDraw.Draw(image1)
                            font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 30)
                            draw.text((40, 195), list[0], fill=(0, 0, 0), font=font)
                            draw.text((45, 295), list[1], fill=(0, 0, 0), font=font)
                            draw.text((235, 290), list[2], fill=(0, 0, 0), font=font)
                            draw.text((520, 195), list[3], fill=(0, 0, 0), font=font)
                            draw.text((525, 400), list[4], fill=(0, 0, 0), font=font)
                            image1.save(f'data/Jiko/{ut}.png')
                            await message.channel.send(file=discord.File(f'data/Jiko/{ut}.png'))
                            os.remove(f'data/Jiko/{ut}.png')

                    if 'mc!horror ' in message.content:
                        ut = time.time()
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            image1 = Image.open("data/Horror/Base.png")
                            draw = ImageDraw.Draw(image1)
                            font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 60)
                            draw.text((670, 40), r, fill=(0, 0, 0), font=font)
                            draw.text((670, 110), r, fill=(0, 0, 0), font=font)
                            draw.text((670, 180), r, fill=(0, 0, 0), font=font)
                            draw.text((670, 250), r, fill=(0, 0, 0), font=font)
                            draw.text((670, 320), r, fill=(0, 0, 0), font=font)
                            draw.text((670, 390), r, fill=(0, 0, 0), font=font)
                            draw.text((670, 460), r, fill=(0, 0, 0), font=font)
                            draw.text((670, 530), "Your Died..", fill=(0, 0, 0), font=font)
                            image1.save(f"data/Horror/{ut}.png")
                            await message.channel.send(file=discord.File(f'data/Horror/{ut}.png'))
                            os.remove(f'data/Horror/{ut}.png')

                    if 'mc!pokemon ' in message.content:
                        ut = time.time()
                        if message.author.guild_permissions.administrator:
                            target = ' '
                            idx = message.content.find(target)
                            r = message.content[idx+1:]
                            image1 = Image.open("data/Pokemon/Base.jpeg")
                            draw = ImageDraw.Draw(image1)
                            font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 30)
                            draw.text((33, 370), r + 'が', fill=(0, 0, 0), font=font)
                            image1.save(f"data/Pokemon/{ut}.png")
                            await message.channel.send(file=discord.File(f"data/Pokemon/{ut}.png"))
                            os.remove(f"data/Pokemon/{ut}.png")

                    if 'mc!gengo ' in message.content:
                        ut = time.time()
                        if message.author.guild_permissions.administrator:
                            target = ' '
                            idx = message.content.find(target)
                            r = message.content[idx+1:]
                            image1 = Image.open("data/Gengo/Base.jpg")
                            draw = ImageDraw.Draw(image1)
                            font = ImageFont.truetype('font/GN-KillGothic-U-KanaO.ttf', 10)
                            draw.text((35, 25), r, font=font, direction='ttb')
                            image1.save(f"data/Gengo/{ut}.png")
                            await message.channel.send(file=discord.File(f"data/Gengo/{ut}.png"))
                            os.remove(f"data/Gengo/{ut}.png")

                    if 'mc!robokasu ' in message.content:
                        ut = time.time()
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            Robokasu(r, ut)
                            await message.channel.send(file=discord.File(f'data/Robo/{ut}.png'))
                            os.remove(f'data/Robo/{ut}.png')

                    if 'mc!gacha ' in message.content:
                        ut = time.time()
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            user = await bot.fetch_user(int(r))
                            image1 = Image.open("data/Gacha/Base.jpg")
                            urlData = requests.get(user.avatar).content
                            with open(f"data/Gacha/{ut}.jpg", mode='wb') as f:
                                f.write(urlData)
                            im2 = Image.open(f"data/Gacha/{ut}.jpg")
                            img_resize = im2.resize((1024, 1024))
                            image1.paste(img_resize, (340, 920))
                            font = ImageFont.truetype('font/GN-KillGothic-U-KanaO.ttf', 10)
                            image1.save(f"data/Gacha/{ut}.png")
                            await message.channel.send(file=discord.File(f"data/Gacha/{ut}.png"))
                            os.remove(f"data/Gacha/{ut}.png")
                            os.remove(f"data/Gacha/{ut}.jpg")

                    if 'mc!codemoji ' in message.content:
                        ut = time.time()
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            img = Image.new("RGB", (160, 160), color=(255, 255, 255))
                            draw = ImageDraw.Draw(img)
                            font = ImageFont.truetype('C:/Windows/Fonts/meiryob.ttc', 100)
                            draw.text((0, 0), f" {r}", 'red', font=font)
                            img.save(f"save/{ut}.png")
                            with open(f"save/{ut}.png", "rb") as img:
                                img_byte = img.read()
                                await message.guild.create_custom_emoji(name = f"emoji", image = img_byte)
                            os.remove(f"save/{ut}.png")

                    if 'mc!5000choen ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        r.rsplit(' ')
                        list = r.rsplit(' ')
                        embed = discord.Embed(title="5000兆円ほしい!")
                        embed.set_image(url=f"https://gsapi.cbrx.io/image?top={list[0]}&bottom={list[1]}")
                        msg = await message.channel.send(embed=embed)
                        await msg.add_reaction('<:gene:1257669020136640575>')

                    if 'mc!neko' in message.content:
                        url = "https://nekobot.xyz/api/image?type=neko"
                        response = requests.get(url)
                        jsonData = response.json()
                        embed = discord.Embed(title="猫耳娘")
                        embed.set_image(url=jsonData["message"])
                        msg = await message.channel.send(embed=embed)
                        await msg.add_reaction('<:gene:1257669020136640575>')

                    if 'mc!food' in message.content:
                        url = "https://nekobot.xyz/api/image?type=food"
                        response = requests.get(url)
                        jsonData = response.json()
                        embed = discord.Embed(title="食べ物")
                        embed.set_image(url=jsonData["message"])
                        msg = await message.channel.send(embed=embed)
                        await msg.add_reaction('<:gene:1257669020136640575>')

                    if 'mc!kanna' in message.content:
                        url = "https://nekobot.xyz/api/image?type=kanna"
                        response = requests.get(url)
                        jsonData = response.json()
                        embed = discord.Embed(title="カンナちゃん")
                        embed.set_image(url=jsonData["message"])
                        msg = await message.channel.send(embed=embed)
                        await msg.add_reaction('<:gene:1257669020136640575>')

                    if 'mc!dog' in message.content:
                        url = "https://dog.ceo/api/breeds/image/random"
                        response = requests.get(url)
                        jsonData = response.json()
                        embed = discord.Embed(title="犬")
                        embed.set_image(url=jsonData["message"])
                        msg = await message.channel.send(embed=embed)
                        await msg.add_reaction('<:gene:1257669020136640575>')

                    if 'mc!httpcat ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        embed = discord.Embed(title="HttpCat")
                        embed.set_image(url=f"https://http.cat/{r}")
                        msg = await message.channel.send(embed=embed)
                        await msg.add_reaction('<:gene:1257669020136640575>')

                    if 'mc!fox' in message.content:
                        url = "https://randomfox.ca/floof/"
                        response = requests.get(url)
                        jsonData = response.json()
                        embed = discord.Embed(title="きつね🦊")
                        embed.set_image(url=jsonData["image"])
                        msg = await message.channel.send(embed=embed)
                        await msg.add_reaction('<:gene:1257669020136640575>')

                    if 'mc!suddendeath ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        msg = await message.channel.send(f"```{suddendeath.suddendeathmessage(r)}```")
                        await msg.add_reaction('<:gene:1257669020136640575>')

                    if 'mc!hikakin' in message.content:
                        list = glob.glob('C:/Users/enoki/Documents/DiscordBot/mocha/data/Hikakin/*.png')
                        data = random.choice(list)
                        await message.channel.send(file=discord.File(data))

                    if 'mc!numbergame ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        answer = random.randrange(start=1, stop=100)
                        if answer == int(r):
                            await message.channel.send('正解しました!')
                        elif int(r) > answer:
                            await message.channel.send(f'あなたの予想した数は答えより大きかったです\n答え:{answer}')
                        else:
                            await message.channel.send(f'あなたの予想した数は答えより小さかったです\n答え:{answer}')

                    if 'mc!useridgame' in message.content:
                        answer = random.randrange(start=1, stop=len(bot.useridgamelist))
                        minus = answer - 1
                        await message.channel.send(f'{bot.useridgamelist[minus]}はだれでしょうか?\nこたえは、mc!answeruseridgame')

                    if 'mc!answeruseridgame ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        user = await bot.fetch_user(int(r))
                        await message.channel.send(f'正解は、{user.display_name}さんです!')

                    # 管理コマンド
                    if 'mc!delete ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            await message.channel.purge(limit=int(r)+1)
                        if not message.author.guild_permissions.administrator:
                            await message.channel.send('あなたは管理者ではありません。\nこのコマンドは管理者専用です。')

                    if 'mc!slowmode ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            await message.channel.edit(slowmode_delay=int(r))

                    if 'mc!kick' in message.content:
                        await message.channel.send(f'キックは、/kickコマンドで行ってください。')

                    if 'mc!ban' in message.content:
                        await message.channel.send(f'BANは、/banコマンドで行ってください。')

                    if 'mc!welmsg ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            if not os.path.exists(f"save/Servers/{message.guild.id}"):
                                os.mkdir(f"save/Servers/{message.guild.id}")
                            if not os.path.isfile(f"save/Servers/{message.guild.id}/welcome.txt"):
                                with open(f"save/Servers/{message.guild.id}/welcome.txt", "x", encoding="utf-8") as f:
                                    f.write(f"{r}")
                                with open(f"save/Servers/{message.guild.id}/welcha.txt", "x", encoding="utf-8") as f:
                                    f.write(f"{message.channel.id}")
                            else:
                                with open(f"save/Servers/{message.guild.id}/welcome.txt", "w", encoding="utf-8") as f:
                                    f.write(f"{r}")
                                with open(f"save/Servers/{message.guild.id}/welcha.txt", "w", encoding="utf-8") as f:
                                    f.write(f"{message.channel.id}")
                            await message.channel.send(f'ウェルカムメッセージを追加しました。')

                    if 'mc!create-channel ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        r.rsplit(' ')
                        list = r.rsplit(' ')
                        if message.author.guild_permissions.administrator:
                            for i in range(int(list[1])):
                                cha = await message.guild.create_text_channel(name=list[0])
                                if list[2] == "1":
                                    await cha.edit(nsfw=True)
                            embed = discord.Embed(title="チャンネルを作成しました。", color=0x70006e)
                            msg = await message.channel.send(embed=embed)
                            await msg.add_reaction('<:toolcreate:1258020265112375369>')

                    if 'mc!delete-channel' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.delete()
                            embed = discord.Embed(title="チャンネルを削除しました。", color=0x70006e)

                    if 'mc!pin-message ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            id = await message.channel.send(r)
                            await id.pin()

                    if 'mc!message-pin-channel ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            cha = await message.guild.create_voice_channel(name=r)

                    if 'mc!lisobadd ' in message.content:
                        if message.author.guild_permissions.administrator:
                            target = ' '
                            idx = message.content.find(target)
                            r = message.content[idx+1:]
                            WriteAutoReplayList(f"save/mutehaku.txt", r)
                            await message.channel.send(f'{r}から聞き専をブロックするようにしました。')

                    if 'mc!nick ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        await message.author.edit(nick=r)
                        await message.channel.send(f'{r}に変更が完了しました。')

                    if 'mc!gmute ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            if r == "enable":
                                if not os.path.exists(f"save/Servers/{message.guild.id}"):
                                    os.mkdir(f"save/Servers/{message.guild.id}")
                                if not os.path.isfile(f"save/Servers/{message.guild.id}/gmutenable.txt"):
                                    with open(file=f"save/Servers/{message.guild.id}/gmutenable.txt", mode="x") as f:
                                        await message.channel.send(f'GMuteを有効にしました。')
                                else:
                                    await message.channel.send(f'GMuteは現在有効になっています。')
                            elif r == "disable":
                                if os.path.isfile(f"save/Servers/{message.guild.id}/gmutenable.txt"):
                                    os.remove(f"save/Servers/{message.guild.id}/gmutenable.txt")
                                    await message.channel.send(f'GMuteを無効にしました。')
                                else:
                                    await message.channel.send(f'GMuteは現在無効になっています。')


                    if 'mc!botnick ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            await message.guild.me.edit(nick=r)
                            await message.channel.send(f'{r}に変更が完了しました。')
                        if not message.author.guild_permissions.administrator:
                            await message.channel.send('あなたは管理者ではありません。\nこのコマンドは管理者専用です。')

                    if 'mc!admincheck' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.send('あなたは管理者です。')
                        if not message.author.guild_permissions.administrator:
                            await message.channel.send('あなたは管理者ではありません。')

                    if 'mc!addautomod ' in message.content:
                        if message.author.guild_permissions.administrator:
                            target = ' '
                            idx = message.content.find(target)
                            r = message.content[idx+1:]
                            if not os.path.exists(f"save/Servers/{message.guild.id}"):
                                os.mkdir(f"save/Servers/{message.guild.id}")
                            if not os.path.isfile(f"save/Servers/{message.guild.id}/automod.txt"):
                                with open(file=f"save/Servers/{message.guild.id}/automod.txt", mode="x") as f:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/automod.txt", f"{r}")
                            else:
                                WriteAutoReplayList(f"save/Servers/{message.guild.id}/automod.txt", f"{r}")
                                await message.channel.send(f'自動管理を有効化しました。\n{r}をブロックします。')
                        if not message.author.guild_permissions.administrator:
                            await message.channel.send('管理者権限がありません..🥺')

                    if 'mc!automodlist' in message.content:
                        if message.author.guild_permissions.administrator:
                            join_servers_information = '\n'.join(f"{s}" for s in ReadAutoReplayList(f"save/Servers/{message.guild.id}/automod.txt"))
                            embed = discord.Embed(title="AutoModによって制限されている言葉", description=join_servers_information)
                            await message.author.send(embed=embed)

                    if 'mc!addautoreplay ' in message.content:
                        if message.author.guild_permissions.administrator:
                            target = ' '
                            idx = message.content.find(target)
                            r = message.content[idx+1:]
                            r.rsplit(' ')
                            print(r.rsplit(' '))
                            list = r.rsplit(' ')
                            if not os.path.exists(f"save/Servers/{message.guild.id}"):
                                os.mkdir(f"save/Servers/{message.guild.id}")
                            if not os.path.isfile(f"save/Servers/{message.guild.id}/autoreplay.txt"):
                                with open(file=f"save/Servers/{message.guild.id}/autoreplay.txt", mode="x") as f:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/autoreplay.txt", f"{list[0]}")
                            else:
                                WriteAutoReplayList(f"save/Servers/{message.guild.id}/autoreplay.txt", f"{list[0]}")

                            if not os.path.isfile(f"save/Servers/{message.guild.id}/autoreplayanswer.txt"):
                                with open(file=f"save/Servers/{message.guild.id}/autoreplayanswer.txt", mode="x") as f:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/autoreplayanswer.txt", f"{list[1]}")
                            else:
                                WriteAutoReplayList(f"save/Servers/{message.guild.id}/autoreplayanswer.txt", f"{list[1]}")
                            await message.channel.send(f'自動返信を有効化しました。\n{list[0]} -> {list[1]}')
                        if not message.author.guild_permissions.administrator:
                            await message.channel.send('管理者権限がありません..🥺')

                    if 'mc!removeautoreplay' in message.content:
                        if message.author.guild_permissions.administrator:
                            if os.path.isfile(f"save/Servers/{message.guild.id}/autoreplay.txt"):
                                os.remove(f"save/Servers/{message.guild.id}/autoreplay.txt")
                            if os.path.isfile(f"save/Servers/{message.guild.id}/autoreplayanswer.txt"):
                                os.remove(f"save/Servers/{message.guild.id}/autoreplayanswer.txt")
                            await message.channel.send('自動返信の削除が完了しました。')
                        if not message.author.guild_permissions.administrator:
                            await message.channel.send('管理者権限がありません..🥺')

                    if 'mc!autoreplaylist' in message.content:
                        if message.author.guild_permissions.administrator:
                            join_servers_information = '\n'.join(f"{s}" for s in ReadAutoReplayList(f"save/Servers/{message.guild.id}/autoreplay.txt"))
                            embed = discord.Embed(title="自動返信に反応する言葉", description=join_servers_information)
                            await message.channel.send(embed=embed)

                    if 'mc!addcmd ' in message.content:
                        if message.author.guild_permissions.administrator:
                            target = ' '
                            idx = message.content.find(target)
                            r = message.content[idx+1:]
                            r.rsplit(' ')
                            list = r.rsplit(' ')
                            if not os.path.exists(f"save/Servers/{message.guild.id}"):
                                os.mkdir(f"save/Servers/{message.guild.id}")
                            if not os.path.isfile(f"save/Servers/{message.guild.id}/customcommand.txt"):
                                with open(file=f"save/Servers/{message.guild.id}/customcommand.txt", mode="x") as f:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/customcommand.txt", f"mc!{list[0]}")
                            else:
                                WriteAutoReplayList(f"save/Servers/{message.guild.id}/customcommand.txt", f"mc!{list[0]}")

                            if not os.path.isfile(f"save/Servers/{message.guild.id}/customcommandanswer.txt"):
                                with open(file=f"save/Servers/{message.guild.id}/customcommandanswer.txt", mode="x") as f:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt", f"{list[1]}")
                            else:
                                if '<time>' in list[1]:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt", f"<time>")
                                    await message.channel.send(f'カスタムコマンドを有効化しました。\nmc!{list[0]} -> 時間表示')
                                elif '<uranai>' in list[1]:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt", f"<uranai>")
                                    await message.channel.send(f'カスタムコマンドを有効化しました。\nmc!{list[0]} -> うらない')
                                elif '<dragon>' in list[1]:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt", f"<dragon>")
                                    await message.channel.send(f'カスタムコマンドを有効化しました。\nmc!{list[0]} -> ドラゴンの鳴き声を再生')
                                elif '<knight>' in list[1]:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt", f"<Knight>")
                                    await message.channel.send(f'カスタムコマンドを有効化しました。\nmc!{list[0]} -> 騎士の走る音を再生')
                                else:
                                    WriteAutoReplayList(f"save/Servers/{message.guild.id}/customcommandanswer.txt", f"{list[1]}")
                                    await message.channel.send(f'カスタムコマンドを有効化しました。\nmc!{list[0]} -> {list[1]}')
                        if not message.author.guild_permissions.administrator:
                            await message.channel.send('管理者権限がありません..🥺')

                    if 'mc!openserver' in message.content:
                        if message.author.guild_permissions.administrator:
                            f = open('save/gserver.txt', 'a', encoding="utf-8")
                            url = await message.channel.create_invite()
                            f.write(f"{url.url} - {str(message.guild)}\n")

                    if 'mc!opsjoin' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.send(file=discord.File('save/gserver.txt'))

                    if 'mc!rolejoin ' in message.content:
                        if message.author.guild_permissions.administrator:
                            target = ' '
                            idx = message.content.find(target)
                            r = message.content[idx+1:]
                            if not os.path.exists(f"save/Servers/{message.guild.id}"):
                                os.mkdir(f"save/Servers/{message.guild.id}")
                            if not os.path.isfile(f"save/Servers/{message.guild.id}/joinrole.txt"):
                                with open(f"save/Servers/{message.guild.id}/joinrole.txt", "x") as f:
                                    f.write(f"{r}")
                            else:
                                with open(f"save/Servers/{message.guild.id}/joinrole.txt", "w") as f:
                                    f.write(f"{r}")
                            await message.channel.send(f"{r}を登録しました。")

                    if 'mc!blockcmd' in message.content:
                        if message.author.guild_permissions.administrator:
                            WriteAutoReplayList(f"save/blockch.txt", f"{message.channel.id}")
                            await message.channel.send(f"このチャンネルで、コマンドを実行できなくしました。")

                    # 便利
                    if 'mc!youtube ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            youtube = build('youtube', 'v3', developerKey=bot.youtubeapikey)
                            search_responses = youtube.search().list(
                                q=r,
                                part='snippet',
                                type='video',
                                regionCode="jp",
                                maxResults=5,# 5~50まで
                            ).execute()
                            embed = discord.Embed(title=f"Youtube検索:{r}")
                            for search_response in search_responses['items']:
                                snippetInfo = search_response['snippet']
                                # 動画タイトル
                                title = snippetInfo['title']
                                # チャンネル名
                                channeltitle = snippetInfo['channelTitle']
                                embed.add_field(name=channeltitle,value=title)
                            msg = await message.channel.send(embed=embed)
                            await msg.add_reaction('<:search:1257668829094350938>')

                    if 'mc!ping' in message.content:
                        raw_ping = bot.latency

                        ping = round(raw_ping * 1000)

                        await message.reply(f"BotのPing値は{ping}msです。")

                    if 'mc!member' in message.content:
                        guild = message.guild
                        member_count = guild.member_count
                        await message.channel.send(f'現在のメンバー数：{member_count}')

                    if 'mc!randombot' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.send(f'https://discord.com/oauth2/authorize?client_id={random.randint(100000000000000000, 999999999999999999)}&permissions=8&scope=bot')

                    if 'mc!amazon ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        await message.channel.send(f'https://www.amazon.co.jp/s?k={r}&sprefix=%2Caps%2C167&ref=nb_sb_ss_sx-trend-t-dedupe-d-phrasedoc-jp_2_0')

                    if 'mc!google ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if os.path.isfile(f"save/Servers/{message.guild.id}/googleblock.txt"):
                            if message.author.bot:
                                pass
                            if str(message.channel.id) in ReadAutoReplayList(f"save/Servers/{message.guild.id}/googleblock.txt"):
                                await message.channel.send(f'このチャンネルでは使用できません。')
                            else:
                                msg = await message.channel.send(f'https://www.google.com/search?q={r}&sclient=gws-wiz')
                                await msg.add_reaction('<:search:1257668829094350938>')
                        else:
                            msg = await message.channel.send(f'https://www.google.com/search?q={r}&sclient=gws-wiz')
                            await msg.add_reaction('<:search:1257668829094350938>')

                    if 'mc!iss' in message.content:
                        url = "http://api.open-notify.org/iss-now.json"
                        response = requests.get(url)
                        jsonData = response.json()
                        embed = discord.Embed(title="国際宇宙ステーションの位置",description=f"経度:{jsonData['iss_position']['longitude']}\n緯度:{jsonData['iss_position']['latitude']}",color=discord.Colour.red())
                        msg = await message.channel.send(embed=embed)
                        await msg.add_reaction('<:search:1257668829094350938>')

                    if 'mc!mhnow ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        response = requests.get(f"https://gamewith.jp/monsterhunternow/bbs/threads/show/{r}")
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = soup.find_all('p', {'class': 'bbs-post-body'})[0]
                        await message.channel.send(f'```{links.get_text()}```')

                    if 'mc!qrcode ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            await message.channel.send(f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={r}')

                    if 'mc!urlcheck ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        await message.channel.send(f'https://safeweb.norton.com/report?url={r}')

                    if 'mc!wayback ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        await message.channel.send(f'https://web.archive.org/web/20240000000000*/{r}')

                    if 'mc!password' in message.content:
                        url = ""
                        response = requests.get(url)
                        jsonData = response.json()
                        await message.channel.send(f'パスワード:「{jsonData["message"]}」')

                    if 'mc!weather' in message.content:
                        url = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
                        response = requests.get(url)
                        jsonData = response.json()
                        await message.channel.send(f'```天気:「{jsonData[0]['timeSeries'][0]['areas'][0]['weathers'][0]}」\n風向き:「{jsonData[0]['timeSeries'][0]['areas'][0]['winds'][0]}」```')

                    if 'mc!emoji ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            if os.path.isfile('download/temp.json'):
                                os.remove('download/temp.json')
                            urlData = requests.get("https://script.googleusercontent.com/macros/echo?user_content_key=yyynJw79mdUs05V2_6-QJyweYHdrnG6geAv-NhcUvD4mRVNXl-6QD_JvuvBJKNaqCZaK8-S6RgxwkmiCjB8C8VnPdDXyq7oFm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnEHvOcX3eoqlBPfgXPHbmykMmcSr_4zizilX3jfRTS29BGe1cEN5qBkO0hQ3xq0x8h-exTrjr98c8mXaLabeR7Db3lj62okUAQ&lib=M5QfM7uGrN-xbspezpi_enX5chaeZMmGx").content
                            with open('download/temp.json', mode='wb') as f:
                                f.write(urlData)
                            fa = open('download/temp.json')
                            jsona = json.load(fa)
                            if os.path.isfile('download/temp.png'):
                                os.remove('download/temp.png')
                            urlData = requests.get(r).content
                            with open('download/temp.png' ,mode='wb') as f:
                                f.write(urlData)
                            with open("download/temp.png", "rb") as img:
                                img_byte = img.read()
                                await message.guild.create_custom_emoji(name = jsona["message"], image = img_byte)
                        if not message.author.guild_permissions.administrator:
                            await message.channel.send('あなたは管理者ではありません。\nこのコマンドは管理者専用です。')

                    if 'mc!yahooauction ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        response = requests.get(f"https://auctions.yahoo.co.jp/search/search?auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&fr=auc_top&p={r}&x=0&y=0")
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = soup.find_all('a', {'class': 'Product__titleLink js-browseHistory-add js-rapid-override'})[0]
                        await message.channel.send(f'商品名:「{links.get_text()}」\n{links["href"]}')

                    if 'mc!botgeturl ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            await message.channel.send(f'https://discord.com/oauth2/authorize?client_id={r}&permissions=8&scope=bot')

                    if 'mc!installbot' in message.content:
                        if message.author.guild_permissions.administrator:
                            join_servers_information = '\n'.join(f"{s.name} ({s.member_count}人) ({s.owner})" for s in bot.guilds)
                            embed = discord.Embed(title="導入鯖一覧", description=join_servers_information)
                            await message.channel.send(embed=embed)

                    if 'mc!serveridlist' in message.content:
                        if message.author.guild_permissions.administrator:
                            join_servers_information = '\n'.join(f"{s.name} {s.id}" for s in bot.guilds)
                            embed = discord.Embed(title="導入鯖一覧", description=join_servers_information)
                            await message.channel.send(embed=embed)

                    if 'mc!news' in message.content:
                        response = requests.get(f"https://www.yahoo.co.jp/")
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = soup.find_all('span', {'class': 'fQMqQTGJTbIMxjQwZA2zk _1alzSpTqJzvSVUWqpx82d4'})[0]
                        linksa = soup.find_all('span', {'class': 'fQMqQTGJTbIMxjQwZA2zk _1alzSpTqJzvSVUWqpx82d4'})[1]
                        linksb = soup.find_all('span', {'class': 'fQMqQTGJTbIMxjQwZA2zk _1alzSpTqJzvSVUWqpx82d4'})[2]
                        await message.channel.send(f'```{links.get_text()}\n{linksa.get_text()}\n{linksb.get_text()}```')

                    if 'mc!translator ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        translator = Translator()
                        text_ja = r
                        text_en = translator.translate(text_ja, src='ja', dest='en').text
                        text_fr = translator.translate(text_ja, src='ja', dest='fr').text
                        await message.channel.purge(limit=1)
                        embed = discord.Embed(title=f"{r}の翻訳結果")
                        embed.add_field(name="翻訳結果(英語)",value=text_en)
                        embed.add_field(name="翻訳結果(フランス語)",value=text_fr)
                        await message.channel.send(embed=embed)

                    if 'mc!graf ' in message.content:
                        ut = time.time()
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        r.rsplit(' ')
                        list = r.rsplit(' ')
                        left = [1, 2, 3]  # グラフの横軸（X軸）
                        height = [int(list[1]), int(list[2]), int(list[3])]  # 値（Y軸）
                        plt.plot(left, height)
                        plt.suptitle(list[0])
                        plt.savefig(f"save/graf/{ut}.png")
                        plt.clf()
                        await message.channel.send(file=discord.File(f"save/graf/{ut}.png"))
                        os.remove(f"save/graf/{ut}.png")

                    if 'mc!manga ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        r.rsplit(' ')
                        response = requests.get(f"https://comic.k-manga.jp/search/word/{r}")
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = soup.find_all('h2', {'class': 'book-list--title'})[0]
                        exa = soup.find_all('span', {'class': 'book-list--author-item'})[0]
                        linksa = soup.find_all('img', {'class': 'book-list--img'})[0]
                        embed = discord.Embed(title="漫画情報")
                        embed.add_field(name="タイトル",value=links.get_text())
                        embed.add_field(name="著者",value=exa.get_text())
                        embed.set_thumbnail(url=linksa["src"])
                        await message.channel.send(embed=embed)

                    if 'mc!afk' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if not os.path.exists(f"save/Users/{message.author.id}"):
                            os.mkdir(f"save/Users/{message.author.id}")
                        with open(file=f"save/Users/{message.author.id}/afkmode.txt", mode="x") as f:
                            WriteAutoReplayList(f"save/Users/{message.author.id}/afkmode.txt", f"{message.author.id}")
                        startnot = "afk通知"
                        for channel in bot.get_all_channels():
                            if channel.name == startnot:
                                await channel.send(f"{message.author.name}がAFKになりました。\n理由:{r}")
                        await message.channel.send(f"AFKになりました。\nなにかを発言した瞬間に解除されます。")

                    if 'mc!poll ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        r.rsplit(' ')
                        list = r.rsplit(' ')
                        if message.author.guild_permissions.administrator:
                            if not os.path.exists(f"save/Servers/{message.guild.id}"):
                                os.mkdir(f"save/Servers/{message.guild.id}")
                            if not os.path.isfile(f"save/Servers/{message.guild.id}/{list[0]}.txt"):
                                with open(file=f"save/Servers/{message.guild.id}/{list[0]}.txt", mode="x") as f:
                                    print("Pollを作成しました。")
                            channel = message.channel
                            await channel.send(f'「{list[0]}」について\n{list[1]}秒以内に答えてください。')
                            await asyncio.sleep(int(list[1]))
                            await message.channel.send(f"アンケート結果: {list[0]}")
                            await message.channel.send(file=discord.File(f"save/Servers/{message.guild.id}/{list[0]}.txt"))
                            os.remove(f"save/Servers/{message.guild.id}/{list[0]}.txt")

                    if 'a# ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        r.rsplit(' ')
                        list = r.rsplit(' ')
                        if os.path.isfile(f"save/Servers/{message.guild.id}/{list[0]}.txt"):
                            WriteAutoReplayList(f"save/Servers/{message.guild.id}/{list[0]}.txt", f"{list[1]}")
                            await message.author.send(f"{list[1]}として解答しました。")
                        else:
                            await message.channel.send(f'現在、そのようなアンケートは実施されておりません。')

                    if 'mc!gcc' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.send(f'コンパイルをしています、、\nエラーの場合は、exeは出力されません。')
                            ut = time.time()
                            if not os.path.exists(f"download/{ut}"):
                                os.mkdir(f"download/{ut}")
                            urlData = requests.get(message.attachments[0].url).content
                            with open(f'download/{ut}/temp.c', mode='wb') as f:
                                f.write(urlData)
                            await asyncio.sleep(5)
                            subprocess.run(['gcc', '-o', f'download/{ut}/temp', f'download/{ut}/temp.c'])
                            await asyncio.sleep(5)
                            await message.channel.send(f'コンパイル完了!\nもっとC言語を楽しんでね!')
                            await message.channel.send(file=discord.File(f'download/{ut}/temp.exe'))
                            await asyncio.sleep(20)
                            os.remove(f'download/{ut}/temp.exe')
                            os.remove(f'download/{ut}/temp.c')
                            os.rmdir(f'download/{ut}')

                    if 'mc!meme ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        await message.channel.send(f"https://tenor.com/ja/search/{r}-gifs")

                    if 'mc!shorturl ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            s = pyshorteners.Shortener()
                            await message.channel.send(s.tinyurl.short(r))

                    if 'mc!mcskin ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        await message.channel.send(f"https://crafatar.com/renders/body/{r}")

                    if 'mc!mhwimage ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        url = f"https://mhw-db.com/weapons/{r}"
                        response = requests.get(url)
                        jsonData = response.json()
                        embed = discord.Embed(title=jsonData["name"], color=0x702f00)
                        embed.set_image(url=jsonData['assets']['image'])
                        embed.set_thumbnail(url=jsonData['assets']['icon'])
                        await message.channel.send(embed=embed)

                    if 'mc!mhrqsearch ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        response = requests.get(f"https://gamepedia.jp/mh-rise/quests?q={r}")
                        soup = BeautifulSoup(response.text, 'html.parser')
                        table = soup.find_all('table', {'class': 'mhrise-table'})
                        title = table[0].find_all("td")
                        titled = title[0].find_all("a")[0]
                        embed = discord.Embed(title=titled.get_text(), color=0x702f00)
                        embed.add_field(name="フィールド",value=title[2].get_text())
                        embed.add_field(name="報酬金",value=title[3].get_text())
                        await message.channel.send(embed=embed)

                    if 'mc!mhrmsearch ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        response = requests.get(f"https://gamepedia.jp/mh-rise/monsters?q={r}")
                        soup = BeautifulSoup(response.text, 'html.parser')
                        table = soup.find_all('table', {'class': 'mhrise-table text-s-xs'})
                        title = table[0].find_all("td")
                        titled = title[0].find_all("a")[0]
                        embed = discord.Embed(title=titled.get_text(), color=0x702f00)
                        embed.add_field(name="弱点",value=title[1].get_text())
                        await message.channel.send(embed=embed)

                    if 'mc!books ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        response = requests.get(f"https://www.google.com/search?q={r}&tbm=bks")
                        soup = BeautifulSoup(response.text, 'html.parser')
                        books = soup.find_all('div', {'class': 'BNeawe vvjwJb AP7Wnd'})[0]
                        booksa = soup.find_all('div', {'class': 'BNeawe vvjwJb AP7Wnd'})[1]
                        booksb = soup.find_all('div', {'class': 'BNeawe vvjwJb AP7Wnd'})[2]
                        embed = discord.Embed(title=f"{r}を検索しました", color=0x702f00)
                        embed.add_field(name="結果1",value=f"{books.get_text()}")
                        embed.add_field(name="結果2",value=f"{booksa.get_text()}")
                        embed.add_field(name="結果3",value=f"{booksb.get_text()}")
                        await message.channel.send(embed=embed)

                    if 'mc!forms ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        response = requests.get(r)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        title = soup.find_all('div', {"class": "F9yp7e ikZYwf LgNcQe"})[0]
                        form1 = soup.find_all('span', {'class': 'M7eMe'})
                        embed = discord.Embed(title=title.get_text(), color=0x702f00)
                        for ra in range(len(form1)):
                            form2 = soup.find_all('span', {'class': 'M7eMe'})[ra]
                            num = ra + 1
                            embed.add_field(name=f"質問{num}",value=form2.get_text())
                        await message.channel.send(embed=embed)

                    if 'mc!timer ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            await message.channel.send(f"{r}秒計測します。")
                            await asyncio.sleep(int(r))
                            await message.channel.send(f"{r}秒経ちました!")

                    if 'mc!botrans ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            if r == "jp":
                                if not os.path.exists(f"save/Servers/{message.guild.id}"):
                                    os.mkdir(f"save/Servers/{message.guild.id}")
                                if not os.path.isfile(f"save/Servers/{message.guild.id}/jp.txt"):
                                    await message.guild.me.edit(nick=bot.jp['BotName'])
                                    if os.path.isfile(f"save/Servers/{message.guild.id}/en.txt"):
                                        os.remove(f"save/Servers/{message.guild.id}/en.txt")
                                    with open(file=f"save/Servers/{message.guild.id}/jp.txt", mode="x") as f:
                                        print(f"{message.guild.name}の言語をJPにしました。")
                                        await message.channel.send(f"言語をJPにしました。")
                                else:
                                    await message.channel.send(f"もともとJPです。")
                            elif r == "en":
                                if not os.path.exists(f"save/Servers/{message.guild.id}"):
                                    os.mkdir(f"save/Servers/{message.guild.id}")
                                if not os.path.isfile(f"save/Servers/{message.guild.id}/en.txt"):
                                    await message.guild.me.edit(nick=bot.en['BotName'])
                                    if os.path.isfile(f"save/Servers/{message.guild.id}/jp.txt"):
                                        os.remove(f"save/Servers/{message.guild.id}/jp.txt")
                                    with open(file=f"save/Servers/{message.guild.id}/en.txt", mode="x") as f:
                                        print(f"{message.guild.name}の言語をENにしました。")
                                        await message.channel.send(f"I changed the language to EN.")
                                else:
                                    await message.channel.send(f"I originally chose EN as the language.")
                            else:
                                await message.channel.send(f"JPかENで指定してください。\nPlease specify in JP or EN.")

                    if 'mc!rolepanel ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        r.rsplit(' ')
                        list = r.rsplit(' ')
                        if message.author.guild_permissions.administrator:
                            role = message.guild.get_role(int(list[1]))
                            embed = discord.Embed(title=list[0])
                            embed.add_field(name="ロール",value=f"r#{role.name}-{message.guild.name}")
                            await message.channel.send(embed=embed)
                            WriteAutoReplayList(f"save/rolepanel.txt", f"r#{role.name}-{message.guild.name}")
                            WriteAutoReplayList(f"save/rolepanela.txt", str(role.id))
                            
                    if 'mc!nsfw' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.edit(nsfw=True)
                            await message.channel.send(f'NSFWチャンネル化しました。')

                    if 'mc!copy' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.clone()

                    # 交流関連
                    if 'mc!friend ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        response = requests.get(f"https://dissoku.net/ja/friend/search/result?q={r}&page=1")
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = soup.find_all('a', {'class': 'font-weight-bold text-wrap text-h6'})[0]
                        linksa = soup.find_all('div', {'class': 'v-card-text profile-card__inner_text'})[0]
                        await message.channel.send(f'```名前:「{links.get_text()}」```\n```詳細:\n{linksa.get_text()}```')

                    if 'mc!randomfriend' in message.content:
                        if message.author.guild_permissions.administrator:
                            response = requests.get("https://dissoku.net/ja/friend")
                            soup = BeautifulSoup(response.text, 'html.parser')
                            links = soup.find_all('a', {'class': 'font-weight-bold text-wrap text-h6'})[random.randint(0, 20)]
                            linksa = soup.find_all('div', {'class': 'v-card-text profile-card__inner_text'})[random.randint(0, 20)]
                            await message.channel.send(f'```名前:「{links.get_text()}」```\n```詳細:\n{linksa.get_text()}```')

                    if 'mc!autofriend ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            for i in range(int(r)):
                                time.sleep(1.0)
                                await message.channel.send('mc!randomfriend')

                    if 'mc!server ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            response = requests.get(f"https://dissoku.net/ja/search/result?q={r}&page=1")
                            soup = BeautifulSoup(response.text, 'html.parser')
                            links = soup.find_all('a', {'class': 'v-btn v-btn--slim v-theme--dark v-btn--density-default v-btn--size-default v-btn--variant-text join-btn bottom-btn__inner'})[0]
                            href = links.get('href')
                            await message.channel.send(href)

                    if 'mc!randomserver' in message.content:
                        if message.author.guild_permissions.administrator:
                            response = requests.get(f"https://dissoku.net/ja")
                            soup = BeautifulSoup(response.text, 'html.parser')
                            links = soup.find_all('a', {'class': 'v-btn v-btn--slim v-theme--dark v-btn--density-default v-btn--size-default v-btn--variant-text join-btn bottom-btn__inner'})[random.randint(0, 20)]
                            href = links.get('href')
                            await message.channel.send(href)

                    if 'mc!autoserver ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            for i in range(int(r)):
                                time.sleep(1.0)
                                await message.channel.send('mc!randomserver')

                # グローバルチャット
                    if 'mc!gcactive ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            if os.path.isfile(f'save/GChat/{r}.json'):    
                                await message.channel.edit(name=f"mcg2-{r}")
                                await message.channel.send(f"{r}に参加しました!")
                            else:
                                with open(f'save/GChat/{r}.json', mode="x", encoding="utf-8") as f:
                                    sample_dict = {r: "None"}
                                    json.dump(sample_dict, f, ensure_ascii=False)
                                    await message.channel.edit(name=f"mcg2-{r}")
                                    await message.channel.send(f"{r}を作成しました。")

                    if 'mc!mc-startnot' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.send(f"{message.guild.name}がドッグ起動通知に接続しました。")
                            await message.channel.edit(name=f"ドッグ起動通知")

                    if 'mc!mc-afknot' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.send(f"{message.guild.name}がAFK通知に接続しました。")
                            await message.channel.edit(name=f"afk通知")

                    if 'mc!mc-gmutenot' in message.content:
                        if message.author.guild_permissions.administrator:
                            await message.channel.send(f"{message.guild.name}がGMute登録通知に接続しました。")
                            await message.channel.edit(name=f"gmute登録通知")

                    if 'mc!aglist ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if message.author.guild_permissions.administrator:
                            if not r in ReadAutoReplayList(f"save/notmarkinglist.txt"):
                                with open("save/marking.txt", "a") as f:
                                    f.write(f"\n{r}")
                                user = await bot.fetch_user(int(r))
                                await message.channel.send(f"{str(user)}を登録しました")
                                globalchat = "gmute登録通知"
                                for channel in bot.get_all_channels():
                                    if channel.name == globalchat:
                                        await channel.send(f"{str(user)}を{message.author.name}が登録しました")
                            else:
                                await message.channel.send('この人物は登録できません!')
                        if not message.author.guild_permissions.administrator:
                            await message.channel.send('あなたは管理者ではありません。\nこのコマンドは管理者専用です。')

                    if 'mc!usersearch ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        if os.path.isfile(f"save/Servers/{message.guild.id}/jp.txt"):
                            unsei = [bot.jp['Uranai']['Daikiti'], bot.jp['Uranai']['Chukiti'], bot.jp['Uranai']['Kiti'], bot.jp['Uranai']['Suekiti'], bot.jp['Uranai']['Kyou'], bot.jp['Uranai']['Daikyo']]
                        elif os.path.isfile(f"save/Servers/{message.guild.id}/en.txt"):
                            unsei = [bot.en['Uranai']['Daikiti'], bot.en['Uranai']['Chukiti'], bot.en['Uranai']['Kiti'], bot.en['Uranai']['Suekiti'], bot.en['Uranai']['Kyou'], bot.en['Uranai']['Daikyo']]
                        else:
                            unsei = [bot.jp['Uranai']['Daikiti'], bot.jp['Uranai']['Chukiti'], bot.jp['Uranai']['Kiti'], bot.jp['Uranai']['Suekiti'], bot.jp['Uranai']['Kyou'], bot.jp['Uranai']['Daikyo']]
                        choice = random.choice(unsei)
                        user = await bot.fetch_user(int(r))
                        if os.path.isfile(f"save/Servers/{message.guild.id}/jp.txt"):
                            embed = discord.Embed(title=bot.jp['UserSearch']['Title'],color=user.accent_color)
                            embed.add_field(name=bot.jp['UserSearch']['Name'],value=str(user))
                            embed.add_field(name=bot.jp['UserSearch']['Nick'],value=user.display_name)
                            embed.add_field(name=bot.jp['UserSearch']['Akaunto'],value=user.created_at)
                            if r in bot.markinguser:
                                embed.add_field(name=bot.jp['UserSearch']['Mute'],value=bot.jp['YesNo']['Yes'])
                            else:
                                embed.add_field(name=bot.jp['UserSearch']['Mute'],value=bot.jp['YesNo']['No'])
                            if not r in '1095621183908618240':
                                embed.add_field(name=bot.jp['UserSearch']['Unsei'],value=choice)
                            else:
                                embed.add_field(name=bot.jp['UserSearch']['Unsei'],value="FPS 18")
                            embed.set_thumbnail(url=user.avatar)
                        elif os.path.isfile(f"save/Servers/{message.guild.id}/en.txt"):
                            embed = discord.Embed(title=bot.en['UserSearch']['Title'],color=user.accent_color)
                            embed.add_field(name=bot.en['UserSearch']['Name'],value=str(user))
                            embed.add_field(name=bot.en['UserSearch']['Nick'],value=user.display_name)
                            embed.add_field(name=bot.en['UserSearch']['Akaunto'],value=user.created_at)
                            if r in bot.markinguser:
                                embed.add_field(name=bot.en['UserSearch']['Mute'],value=bot.en['YesNo']['Yes'])
                            else:
                                embed.add_field(name=bot.en['UserSearch']['Mute'],value=bot.en['YesNo']['No'])
                            if not r in '1095621183908618240':
                                embed.add_field(name=bot.en['UserSearch']['Unsei'],value=choice)
                            else:
                                embed.add_field(name=bot.en['UserSearch']['Unsei'],value="FPS 18")
                            embed.set_thumbnail(url=user.avatar)
                        else:
                            embed = discord.Embed(title=bot.jp['UserSearch']['Title'],color=user.accent_color)
                            embed.add_field(name=bot.jp['UserSearch']['Name'],value=str(user))
                            embed.add_field(name=bot.jp['UserSearch']['Nick'],value=user.display_name)
                            embed.add_field(name=bot.jp['UserSearch']['Akaunto'],value=user.created_at)
                            if r in bot.markinguser:
                                embed.add_field(name=bot.jp['UserSearch']['Mute'],value=bot.jp['YesNo']['Yes'])
                            else:
                                embed.add_field(name=bot.jp['UserSearch']['Mute'],value=bot.jp['YesNo']['No'])
                            if not r in '1095621183908618240':
                                embed.add_field(name=bot.jp['UserSearch']['Unsei'],value=choice)
                            else:
                                embed.add_field(name=bot.jp['UserSearch']['Unsei'],value="FPS 18")
                            embed.set_thumbnail(url=user.avatar)
                        await message.channel.send(embed=embed)

                    if 'mc!serversearch ' in message.content:
                        target = ' '
                        idx = message.content.find(target)
                        r = message.content[idx+1:]
                        user = await bot.fetch_guild(int(r))
                        usera = await bot.fetch_user(user.owner_id)
                        embed = discord.Embed(title="サーバー情報", color=0x70006e)
                        embed.add_field(name="名前",value=str(user))
                        embed.add_field(name="サーバーID",value=str(user.id))
                        embed.add_field(name="管理者の名前",value=usera.name)
                        embed.add_field(name="管理者のニックネーム",value=usera.display_name)
                        embed.add_field(name="管理者のID",value=user.owner_id)
                        if user.owner_id in bot.markinguser:
                            embed.add_field(name="ミュートされてるか?",value="はい")
                        else:
                            embed.add_field(name="ミュートされてるか?",value="いいえ")
                        embed.set_thumbnail(url=user.icon)
                        await message.channel.send(embed=embed)
                        
@bot.hybrid_command(name="kick", with_app_command = True, description = "メンバーをキックします。")
@commands.has_permissions(administrator = True)
async def kick(ctx: commands.Context, メンバー:discord.Member):
    await メンバー.kick()
    await ctx.reply(f"メンバーをキックしました。")
    os.system('cls')

@bot.hybrid_command(name="ban", with_app_command = True, description = "メンバーをBANします。")
@commands.has_permissions(administrator = True)
async def kick(ctx: commands.Context, メンバー:discord.Member):
    await メンバー.ban()
    await ctx.reply(f"メンバーをBANしました。")
    os.system('cls')

@bot.hybrid_command(name="vc-kick", with_app_command = True, description = "VCからキックさせます。")
@commands.has_permissions(administrator = True)
async def kick(ctx: commands.Context, メンバー:discord.Member):
    await メンバー.move_to(None)
    await ctx.reply(f"メンバーをVCからキックしました。")
    os.system('cls')

@bot.hybrid_command(name="vc-move", with_app_command = True, description = "VCから移動させます。")
@commands.has_permissions(administrator = True)
async def kick(ctx: commands.Context, メンバー:discord.Member, チャンネル:discord.VoiceChannel):
    await メンバー.move_to(チャンネル)
    await ctx.reply(f"メンバーをVCから移動させました。")
    os.system('cls')

@bot.hybrid_command(name="role-add", with_app_command = True, description = "メンバーにロールを付与します。")
@commands.has_permissions(administrator = True)
async def kick(ctx: commands.Context, メンバー:discord.Member, ロール:discord.Role):
    await メンバー.add_roles(ロール)
    await ctx.reply(f"メンバーにロールを付与しました。")
    os.system('cls')

@bot.hybrid_command(name="role-remove", with_app_command = True, description = "メンバーからロールを剥奪します。")
@commands.has_permissions(administrator = True)
async def kick(ctx: commands.Context, メンバー:discord.Member, ロール:discord.Role):
    await メンバー.remove_roles(ロール)
    await ctx.reply(f"メンバーからロールを剥奪しました。")
    os.system('cls')

@bot.hybrid_command(name="uranai", with_app_command = True, description = "占いします。")
async def kick(ctx: commands.Context):
    await ctx.reply(FuncUranai())
    os.system('cls')

@bot.hybrid_command(name="vc-ban", with_app_command = True, description = "VCからBANします。")
@commands.has_permissions(administrator = True)
async def kick(ctx: commands.Context, メンバー:discord.Member, チャンネル:discord.VoiceChannel):
    WriteAutoReplayList(f"save/vcbanid.txt", str(メンバー.id))
    WriteAutoReplayList(f"save/vcbanch.txt", str(チャンネル.id))
    await ctx.reply("メンバーをボイチャからBANしました。")
    os.system('cls')

@bot.hybrid_command(name="timeout", with_app_command = True, description = "メンバーをタイムアウトします。")
@commands.has_permissions(administrator = True)
async def timeout(ctx: commands.Context, メンバー:discord.Member, 何分:int):
    await メンバー.timeout(datetime.timedelta(minutes=何分))
    await ctx.reply("メンバーをタイムアウトしました。")
    os.system('cls')

@bot.hybrid_command(name="timeout-remove", with_app_command = True, description = "メンバーのタイムアウトを解除します。")
@commands.has_permissions(administrator = True)
async def timeout(ctx: commands.Context, メンバー:discord.Member):
    await メンバー.timeout(None)
    await ctx.reply("メンバーのタイムアウトを解除しました。")
    os.system('cls')

@bot.hybrid_command(name="nick-copy", with_app_command = True, description = "ニックネームをコピーします。")
@commands.has_permissions(administrator = True)
async def copynick(ctx: commands.Context, コピー元:discord.Member, コピー先:discord.Member):
    await コピー先.edit(nick=コピー元.display_name)
    await ctx.reply("ニックネームをコピーしました。")
    os.system('cls')

@bot.hybrid_command(name="nick-exchange", with_app_command = True, description = "ニックネームを交換します。")
@commands.has_permissions(administrator = True)
async def copynick(ctx: commands.Context, ユーザー１:discord.Member, ユーザー２:discord.Member):
    await ユーザー１.edit(nick=ユーザー２.display_name)
    await ユーザー２.edit(nick=ユーザー１.display_name)
    await ctx.reply("ニックネームを交換しました。")
    os.system('cls')

@bot.hybrid_command(name="nick", with_app_command = True, description = "ニックネームを編集します。")
@commands.has_permissions(administrator = True)
async def copynick(ctx: commands.Context, ユーザー:discord.Member, 新しいニックネーム:str):
    await ユーザー.edit(nick=新しいニックネーム)
    await ctx.reply(f"ニックネームを{新しいニックネーム}に変更しました。")
    os.system('cls')

@bot.hybrid_command(name="nick-remove", with_app_command = True, description = "ニックネームを剥奪します。")
@commands.has_permissions(administrator = True)
async def copynick(ctx: commands.Context, ユーザー:discord.Member):
    await ユーザー.edit(nick=None)
    await ctx.reply(f"ニックネームを除去しました。")
    os.system('cls')

bot.run(token)