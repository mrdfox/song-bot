# This Repo was not fully owned by me. Some codes are scraped from respected DEVOLEPERS whom where mine friends. 
# check Readme.md For More. 

import logging
logger = logging.getLogger(__name__)
import os, re, time, math, json, string, random, traceback, wget, asyncio, datetime, aiofiles, aiofiles.os, requests, youtube_dl, lyricsgenius
from config import Config
from random import choice 
from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch
from database import Database
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid


Bot = Client(
    "Song Downloader Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

db = Database()

START_TEXT = """Hᴀɪ {}, 
Aᴍ ᴀ YᴏᴜTᴜʙᴇ Dᴏᴡɴʟᴏᴀᴅᴇʀ Bᴏᴛ I Cᴀɴ Dᴏᴡɴʟᴏᴀᴅ Sᴏɴɢs,Vɪᴅᴇᴏs & Lʏʀɪᴄs Fʀᴏᴍ YᴏᴜTᴜʙᴇ ᴀɴᴅ ʟʏʀɪᴄs ᴀɴᴅ  Wᴏᴜʟᴅ ᴜᴘʟᴏᴀᴅ ɪɴᴛᴏ Tᴇʟᴇɢʀᴀᴍ.\n\n
Usᴇ /help Cᴏᴍᴍᴀɴᴅs Fᴏʀ Mᴏʀᴇ.\n\nBʏ <a href="https://t.me/VAMPIRE_KING_NO_1">Tᴇʀʀᴏʀ Mɪᴄᴋᴇʏ</a>
"""

CMDS_TEXT = """
`Hᴇʀᴇ Iᴛ ɪs Tʜᴇ Lɪsᴛ ᴏғ Cᴏᴍᴍᴀᴍᴅs ᴀɴᴅ Iᴛs ᴜsᴀɢᴇ`

- /song - Tʜɪs Cᴏᴍᴍᴀɴᴅ ɪs Fᴏʀ Dᴏᴡɴʟᴏᴀᴅɪɴɢ Sᴏɴɢs  
- /lyrics - Tʜɪs Cᴏᴍᴍᴀɴᴅ ɪs Fᴏʀ Sᴄʀᴀᴘᴘɪɴɢ Lʏʀɪᴄs ᴏғ ᴀ Sᴏɴɢ  
- /video - Tʜɪs Cᴏᴍᴍᴀɴᴅ ɪs Fᴏʀ Dᴏᴡɴʟᴏᴀᴅɪɴɢ Vɪᴅᴇᴏs  
- Aʟsᴏ Yᴏᴜ Cᴀɴ sᴇᴀʀᴄʜ ᴠɪᴅᴇᴏs ᴠɪᴀ ɪɴʟɪɴᴇ Mᴏᴅᴇ ᴏɴ Bᴏᴛ 

`Exᴍᴘʟᴇs Fᴏʀ Bᴏᴛʜ Tʜᴏsᴇ Cᴏᴍᴍᴀɴᴅs`

- /song [Sᴏɴɢ Nᴀᴍᴇ] Oʀ [Yᴏᴜᴛᴜʙᴇ Lɪɴᴋ]  
  [/song Alone]   
- /lyrics [Sᴏɴɢ Nᴀᴍᴇ]   
  [/lyrics Alone] 
- /video [Sᴏɴɢ Nᴀᴍᴇ] Oʀ [Yᴏᴜᴛᴜʙᴇ Lɪɴᴋ]
  [/video Alone] 
"""

ABOUT_TEXT = """
╔════❰ Aʙᴏᴜᴛ ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣ 
║┣⪼ Mʏ Nᴀᴍᴇ - <a href="http://t.me/BlackCatMSRobot">Bʟᴀᴄᴋ Cᴀᴛ</a>
║┣⪼ Cʀᴇᴀᴛᴏʀ - <a href=https://t.me/VAMPIRE_KING_NO_1>ƬЄƦƦƠƦ MƖƇƘЄƳ</a>
║┣⪼ Lɪʙʀᴀʀʏ - <a href="https://docs.pyrogram.org/"> Pʏʀᴏɢʀᴀᴍ </a>
║┣⪼ Lᴀɴɢᴜᴀɢᴇ - Pʏᴛʜᴏɴ 3 
║┣⪼ Sᴜᴘᴘᴏʀᴛ - <a href="https://t.me/STMbOTsUPPORTgROUP">Mᴇᴘʜɪsᴛᴏ Bᴏᴛ Sᴜᴘᴘᴏʀᴛ</a>
║┣⪼ ⲂⲞⲦ Sᴇʀᴠᴇʀ - Hᴇʀᴏᴋᴜ
║┣⪼ Sᴏᴜʀᴄᴇ -  [Cʟɪᴄᴋ Hᴇʀᴇ](https://t.me/NOKIERUNNOIPPKITTUM)
║╰━━━━━━━━━━━━━━━➣ ╚══════════════════❍⊱❁۪۪
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url=f"https://telegram.me/{Config.SUPPORT}"), 
        InlineKeyboardButton(text="Sᴇᴀʀᴄʜ", switch_inline_query_current_chat="")
        ],[
        InlineKeyboardButton('Hᴇʟᴘ & Usᴀɢᴇ', callback_data ='cmds') 
        ],[
        InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close')
        ]]
    )
CMDS_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Hᴏᴍᴇ', callback_data='home'),
        InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Hᴏᴍᴇ', callback_data='home'),
        InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close')
        ]]
    )

@Bot.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "cmds":
        await update.message.edit_text(
            text=CMDS_TEXT,
            reply_markup=CMDS_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

        
@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)  

    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
	reply_markup=START_BUTTONS
    )

@Bot.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT,
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )

broadcast_ids = {}

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ\n"
    except UserIsBlocked:
        return 400, f"{user_id} : ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : ᴜsᴇʀ ɪᴅ ɪɴᴠᴀʟɪᴅ\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))



@Bot.on_message(filters.command(['song']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('`🎧Fɪɴᴅɪɴɢ Yᴏᴜʀ Sᴏɴɢ....PLᴢ Wᴀɪᴛ🎸`')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 7000:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"[Bʟᴀᴄᴋ Cᴀᴛ Mᴜsɪᴄ]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**Fᴏᴜɴᴅ Nᴏᴛʜɪɴɢ. Pʟᴢ Tʀʏ Aɴᴏᴛʜᴇʀ Sᴏɴɢ Oʀ Usᴇ Cᴏʀʀᴇᴄᴛ Sᴘᴇʟʟɪɴɢ**')
            return
    except Exception as e:
        m.edit(
            "**Eɴᴛᴇʀ Sᴏɴɢ Nᴀᴍᴇ Wɪᴛʜ Cᴏᴍᴍᴀɴᴅ**❗\nFᴏʀ Exᴀᴍᴘʟᴇ: `/song Alone marshmellow`"
        )
        print(str(e))
        return
    m.edit("`🎸Uᴘʟᴏᴀᴅɪɴɢ.....💞Pʟᴢ Wᴀɪᴛ`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎸 <b>𝐓𝐢𝐭𝐥𝐞:</b> <a href="{link}">{title}</a>\n🎙️ <b>𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧:</b> <code>{duration}</code>\n🎧 <b>𝐕𝐢𝐞𝐰𝐬:</b> <code>{views}</code>\n🎷 <b>𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐛𝐲:</b> {message.from_user.mention()}'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('**An Error Occured. Please Report This To** @STMbOTsUPPORTgROUP !!')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
	

@Bot.on_inline_query()
async def inline(client: Client, query: InlineQuery):
    answers = []
    search_query = query.query.lower().strip().rstrip()

    if search_query == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text="Sᴇᴀʀᴄʜ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ ʜᴇʀᴇ...🔎",
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        search = VideosSearch(search_query, limit=50)

        for result in search.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=result["title"],
                    description="{}, {} views.".format(
                        result["duration"],
                        result["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "https://www.youtube.com/watch?v={}".format(
                            result["id"]
                        )
                    ),
                    thumb_url=result["thumbnails"][0]["url"]
                )
            )

        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Eʀʀᴏʀ: Sᴇᴀʀᴄʜ ᴛɪᴍᴇᴅ ᴏᴜᴛ",
                switch_pm_parameter="",
            )
        
@Bot.on_message(filters.private & filters.command("broadcast") & filters.reply)
async def broadcast_(c, m):
    print("Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ......")
    if m.from_user.id not in Config.OWNER_ID:
        await c.delete_messages(
            chat_id=m.chat.id,
            message_ids=m.message_id,
            revoke=True
        )
        return
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    
    out = await m.reply_text(
        text = f"Bʀᴏᴀᴅᴄᴀsᴛ ɪɴɪᴛɪᴀᴛᴇᴅ! Yᴏᴜ ᴡɪʟʟ ʙᴇ ɴᴏᴛɪғɪᴇᴅ ᴡɪᴛʜ ʟᴏɢ ғɪʟᴇ ᴡʜᴇɴ ᴀʟʟ ᴛʜᴇ ᴜsᴇʀs ᴀʀᴇ ɴᴏᴛɪғɪᴇᴅ"
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    
    broadcast_ids[broadcast_id] = dict(
        total = total_users,
        current = done,
        failed = failed,
        success = success
    )
    
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            
            sts, msg = await send_msg(
                user_id = int(user['id']),
                message = broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            
            if sts == 200:
                success += 1
            else:
                failed += 1
            
            if sts == 400:
                await db.delete_user(user['id'])
            
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current = done,
                        failed = failed,
                        success = success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    
    await asyncio.sleep(3)
    
    await out.delete()
    
    if failed == 0:
        await m.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    
    await aiofiles.os.remove('broadcast.txt')

@Bot.on_message(filters.command("lyrics"))
async def lrsearch(_, message: Message):  
    m = await message.reply_text("Searching Lyrics")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("Lʏʀɪᴄs ɴᴏᴛ ғᴏᴜɴᴅ..🙃😔")
    xxx = f"""
**Lʏʀɪᴄs Sᴇᴀʀᴄʜ Pᴏᴡᴇʀᴇᴅ Bʏ Bʟᴀᴄᴋ Cᴀᴛ Mᴜsɪᴄ Bᴏᴛ**
**Sᴇᴀʀᴄʜᴇᴅ Sᴏɴɢ -** __{query}__
**Fᴏᴜɴᴅ Lʏʀɪᴄs Fᴏʀ -** __{S.title}__
**Aʀᴛɪsᴛ -** {S.artist}
**__Lʏʀɪᴄs:__**
{S.lyrics}"""
    await m.edit(xxx)

@Bot.on_message(filters.command(["vsong", "video"]))
async def ytmusic(client, message: Message):
    global is_downloading
    if is_downloading:
        await message.reply_text(
            "Aɴᴏᴛʜᴇʀ ᴅᴏᴡɴʟᴏᴀᴅ ɪs ɪɴ ᴘʀᴏɢʀᴇss, ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ sᴏᴍᴇᴛɪᴍᴇ"
        )
        return

    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"`Fɪɴᴅɪɴɢ {urlissed} Fʀᴏᴍ Yᴏᴜᴛᴜʙᴇ Sᴇʀᴠᴇʀs. Pʟᴇᴀsᴇ Wᴀɪᴛ.\n\nUᴘʟᴏᴀᴅɪɴɢ Sʟᴏᴡᴇᴅ ᴅᴏᴡɴ Dᴜᴇ ᴛᴏ Hᴇᴀᴠʏ Tʀᴀғғɪᴄ.!`"
    )
    if not urlissed:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        is_downloading = True
        with youtube_dl.YoutubeDL(opts) as ytdl:
            infoo = ytdl.extract_info(url, False)
            duration = round(infoo["duration"] / 60)

            if duration > DURATION_LIMIT:
                await pablo.edit(
                    f"❌ Vɪᴅᴇᴏs ʟᴏɴɢᴇʀ ᴛʜᴀɴ{DURATION_LIMIT} ᴍɪɴᴜᴛᴇ(s) ᴀʀᴇɴ'ᴛ ᴀʟʟᴏᴡᴇᴅ, ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴠɪᴅᴇᴏ ɪs {duration} ᴍɪɴᴜᴛᴇ(s)"
                )
                is_downloading = False
                return
            ytdl_data = ytdl.extract_info(url, download=True)

    except Exception:
        # await pablo.edit(event, f"**Failed To Download** \n**Error :** `{str(e)}`")
        is_downloading = False
        return

    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"**Vɪᴅᴇᴏ Tɪᴛʟᴇ ➠** `{thum}` \n**Rᴇᴏ̨ᴜᴇsᴛᴇᴅ Sᴏɴɢ :** `{urlissed}` \n**Sᴏᴜʀᴄᴇ :** `{thums}` \n**Lɪɴᴋ :** `{mo}`"
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"`Uᴘʟᴏᴀᴅɪɴɢ {urlissed} Sᴏɴɢ Fʀᴏᴍ YᴏᴜTᴜʙᴇ Mᴜsɪᴄ!`",
            file_stark,
        ),
    )
    await pablo.delete()
    is_downloading = False
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)

Bot.run()
