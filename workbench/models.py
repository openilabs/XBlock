from django.db import models

from xblock.fields import BlockScope, Scope, UserScope

def shorten_scope_name(scope_name):
    prefix, rest = scope_name.split("_", 1)
    return rest

BLOCK_SCOPE_NAMES = [
    (shorten_scope_name(sentinel.attr_name), shorten_scope_name(sentinel.attr_name))
    for sentinel in BlockScope.scopes() + [Scope.parent, Scope.children]
]

class XBlockState(models.Model):
    # Not really a block_scope... block or child/parent... :-(
    scope = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
        choices=BLOCK_SCOPE_NAMES
    )
    scope_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Scope ID",
    )
    user_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="User ID",
    )
    scenario = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )
    tag = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
    )

    state = models.TextField(default="{}")

    @classmethod
    def get_for_key(cls, key):
        if key.scope in [Scope.parent, Scope.children]:
            block_scope_name = key.scope.attr_name
        else:
            block_scope_name = key.scope.block.attr_name

        block_scope_name = shorten_scope_name(block_scope_name)

        scope_id = key.block_scope_id
        scenario, tag, rest = scope_id.split(".", 2)
        record, _ = cls.objects.get_or_create(
            scope=block_scope_name,
            scope_id=key.block_scope_id,
            user_id=key.user_id,
            scenario=scenario,
            tag=tag,
        )
        return record


    class Meta:
        verbose_name = "XBlock State"
        verbose_name_plural = "XBlock State"
        ordering = ['scope_id', 'scope', 'user_id']
