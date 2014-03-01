from django.contrib import admin
from .models import XBlockState

class XBlockStateAdmin(admin.ModelAdmin):
    list_display = (
        'block_scope_id', 'block_scope', 'user_id', 'state_preview'
    )
    list_filter = ['block_scope']

    search_fields = ['user_id', 'block_scope_id']

    def state_preview(self, obj):
        return obj.state[:100]

    # def scores(self, obj):
    #     return ", ".join(
    #         "{}/{}".format(score.points_earned, score.points_possible)
    #         for score in Score.objects.filter(submission=obj.id)
    #     )

admin.site.register(XBlockState, XBlockStateAdmin)
