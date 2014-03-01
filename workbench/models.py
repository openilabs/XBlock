from django.db import models

from xblock.fields import BlockScope, Scope, UserScope

BLOCK_SCOPE_NAMES = [
    (sentinel.attr_name, sentinel.attr_name)
    for sentinel in BlockScope.scopes() + [Scope.parent, Scope.children]
]

class XBlockState(models.Model):
    # Not really a block_scope... block or child/parent... :-(
    block_scope = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
        choices=BLOCK_SCOPE_NAMES
    )
    block_scope_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )
    user_id = models.CharField(
        max_length=255,
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

        record, _ = cls.objects.get_or_create(
            block_scope=block_scope_name,
            block_scope_id=key.block_scope_id,
            user_id=key.user_id,
        )
        return record


    class Meta:
        ordering = ['-id']
