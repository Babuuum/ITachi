from django.contrib import admin

from .models import Achievement, AchievementType, Quest, QuestType, UserAchievement, AchievementGrade, UserQuest


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1
    fields = ('name', 'grade', 'type')


class QuestAdmin(admin.ModelAdmin):
    inlines = [AchievementInline]


admin.site.register(Quest, QuestAdmin)
admin.site.register(QuestType)
admin.site.register(Achievement)
admin.site.register(AchievementType)
admin.site.register(AchievementGrade)
admin.site.register(UserAchievement)
admin.site.register(UserQuest)
