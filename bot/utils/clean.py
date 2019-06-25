from discord.utils import escape_mentions, escape_markdown

async def clean_escape(input):
    return(escape_markdown(text=escape_mentions(input)))
