import discord
import pycountry
from datetime import datetime, timedelta
import re


def kwargs_to_dict(**kwargs):
    return kwargs


def transform_string(input_string):
    # 使用正则表达式匹配目标格式中的文本
    match = re.search(r'\[SM] (.*?) successfully added to both the whitelist file and the current whitelist',
                      input_string)

    if match:
        # 获取匹配到的文本
        steam_id = match.group(1)
        # 构建新的字符串
        output_string = f'✅已成功将 {steam_id} 添加到白名单'
        return output_string
    else:
        return "❌添加失败"


def record_format_time(time_str):
    # 将时间字符串解析为 datetime 对象
    dt = datetime.fromisoformat(time_str)

    offset = timedelta(hours=8)
    dt += offset

    # 格式化时间为指定格式
    formatted_time = dt.strftime("%Y年%-m月%-d日 %H:%M")

    return formatted_time


def get_country_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2 if country else None
    except Exception as e:
        print(f"获取国家代码失败 {e}")
        return None


def format_string_to_datetime(date_string):
    """
    Converts a string in the format "YYYY年MM月DD日 - HH:MM:SS" to a datetime object.

    :param date_string: A string representing the date and time in the specified format.
    :return: A datetime object.
    """
    # Define the format string based on the input format
    format_str = '%Y年%m月%d日 - %H:%M:%S'
    # Use datetime.strptime to convert the string to a datetime object
    datetime_obj = datetime.strptime(date_string, format_str)
    return datetime_obj


async def get_or_create_message(channel, title, description):
    async for message in channel.history(limit=1):
        # If there's an existing message, use that message
        return message

    # If no existing message, send a new one
    embed = discord.Embed(title=title, description=description)
    return await channel.send(embed=embed)


def seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds


def percentage_bar(percentage, bar_length=20, fill_char="■", empty_char="□", show_percentage=True, show_brackets=False):
    progress = int(bar_length * percentage)

    if show_brackets:
        bar = "[" + fill_char * progress + empty_char * (bar_length - progress) + "]"
    else:
        bar = fill_char * progress + empty_char * (bar_length - progress)
    if show_percentage:
        return f"{bar} {percentage * 100:.2f}%"
    else:
        return bar


def seconds_to_dhms(seconds):
    # Calculate days, hours, minutes, and remaining seconds
    days, seconds = divmod(seconds, 86400)  # 1 day = 24 * 60 * 60 seconds
    hours, seconds = divmod(seconds, 3600)   # 1 hour = 60 * 60 seconds
    minutes, seconds = divmod(seconds, 60)   # 1 minute = 60 seconds
    return days, hours, minutes, seconds


def add_commas(number):
    # Convert the number to a string
    num_str = str(number)

    # Initialize an empty result string
    result = ""

    # Calculate the length of the string
    length = len(num_str)

    # Iterate through the characters in reverse order
    for i, char in enumerate(reversed(num_str)):
        # Append the character to the result string
        result = char + result

        # Add a comma every three digits, except for the last group
        if i % 3 == 2 and i != length - 1:
            result = ',' + result

    return result


def formate_record_time(data_str):

    date_format = "%Y-%m-%dT%H:%M:%S"

    # Parse the datetime string into a datetime object
    return datetime.strptime(data_str, date_format)


def format_seconds_to_time(total_seconds):
    # Calculate hours, minutes, seconds, and milliseconds
    hours = int(total_seconds // 3600)
    remaining_seconds = total_seconds % 3600
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)

    # Format the result with leading zeros for minutes if more than 1 hour
    formatted_time = ""
    if hours > 0:
        formatted_time += f"{hours}时"
        formatted_time += f"{minutes:02d}分{seconds:02d}秒{milliseconds:03d}"
    else:
        formatted_time += f"{minutes}分{seconds:02d}秒{milliseconds:03d}"

    return formatted_time


def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours >= 10:
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    elif hours >= 1:
        return "{}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    else:
        return "{:02}:{:02}".format(int(minutes), int(seconds))


if __name__ == "__main__":

    pass
