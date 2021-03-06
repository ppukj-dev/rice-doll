from datetime import datetime, timedelta
import re
import requests
import io

LOCAL_OFFSET_HOUR = 7
TIME_FORMAT = "%d-%m-%Y %H.%M"


def get_local_timestamp(ts):
    if ts is None:
        local_time_now = datetime.now() + timedelta(hours=LOCAL_OFFSET_HOUR)
        return local_time_now.strftime(TIME_FORMAT)

    local_ts = ts + timedelta(hours=LOCAL_OFFSET_HOUR)
    return local_ts.strftime(TIME_FORMAT)


def millis():
    return timedelta(milliseconds=1)


def sub_discord_markdown(str, conf):
    str = re.sub(r'```([^```]*)```', fr'{conf["codeblock"][0]}\1{conf["codeblock"][1]}', str)
    str = re.sub(r'\*\*([^\*\*]*)\*\*', fr'{conf["bold"][0]}\1{conf["bold"][1]}', str)
    str = re.sub(r'__([^__]*)__', fr'{conf["underline"][0]}\1{conf["underline"][1]}', str)
    str = re.sub(r'\*([^\*]*)\*', fr'{conf["italic"][0]}\1{conf["italic"][1]}', str)
    str = re.sub(r'_([^_]*)_', fr'{conf["italic"][0]}\1{conf["italic"][1]}', str)
    str = re.sub(r'~~([^~~]*)~~', fr'{conf["strike"][0]}\1{conf["strike"][1]}', str)
    str = re.sub(r'`([^`]*)`', fr'{conf["onelinecode"][0]}\1{conf["onelinecode"][1]}', str)
    str = re.sub(r'^> (.*)', fr'{conf["quoteblock"]}\1', str)  # for the first quote block
    str = re.sub(r'\n> (.*)', fr'\n{conf["quoteblock"]}\1', str)  # for any quote block afte
    return str


def strip_markdown_txt(str):
    config = dict({
        'bold': ('', ''),
        'codeblock': ('', ''),
        'italic': ('', ''),
        'onelinecode': ('', ''),
        'quoteblock': '',
        'strike': ('', ''),
        'underline': ('', ''),
    })
    str = re.sub(r'<:(.*):\d+>', r':\1:', str)
    str = re.sub(r'~~([^~~]*)~~', lambda match: fr'{striken(match.group(1))}', str)
    return sub_discord_markdown(str, config)


def map_mention(s, mentions):
    mention_dict = dict()

    for m in mentions:
        mention_dict[str(m.id)] = m.display_name

    return re.sub(r'<@.*(\d+)>', lambda match: fr'@{mention_dict[match.group(1)]}', s)


def striken(text):
    return ''.join(t+chr(822) for t in text)


async def get_avatar(transcript: str):
    avatars = re.findall(r'"https:.*\/avatars\/.*"', transcript)
    # make it unique
    avatars = list(set(avatars))

    file = []
    for a in avatars:
        a = a.strip('"')
        file.append(
            {
                'avatar_before': a.split('?')[0],
                'filename': a.split('/')[-1].split('?')[0],
                'image': io.BytesIO(requests.get(a, stream=True).content),
                'avatar_string': a
            }
        )
    return file


def message_link2id(link_string: str = None) -> str:
    '''
    Function for converting message link to id.
    Return message_id if the message is a message_list, otherwise just pass it.
    '''
    if link_string is None:
        return link_string
    if link_string.isnumeric():
        return link_string
    if link_string.split('/')[-1].isnumeric:
        return link_string.split('/')[-1]
    raise NameError("Input is not Message ID or Message Link")
