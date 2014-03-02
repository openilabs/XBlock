from django.contrib import admin
from .models import XBlockState

class XBlockStateAdmin(admin.ModelAdmin):
    list_display = (
        'block_scope_id', 'block_scope', 'user_id', 'state'
    )
    list_filter = ['block_scope', 'user_id']

    search_fields = ['user_id', 'block_scope_id', 'state']

    #def state_preview(self, obj):
    #    return obj.state[:120]

    # def scores(self, obj):
    #     return ", ".join(
    #         "{}/{}".format(score.points_earned, score.points_possible)
    #         for score in Score.objects.filter(submission=obj.id)
    #     )

admin.site.register(XBlockState, XBlockStateAdmin)
