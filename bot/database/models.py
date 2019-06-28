from tortoise.models import Model
from tortoise import fields

class GuildSettings(Model):
    guild_id = fields.BigIntField()
    prefix = fields.TextField()

    def __str__(self):
        return self.name
