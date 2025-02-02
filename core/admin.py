from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import AchievementType, AchievementGrade, Achievement, UserAchievement


class UserAchievementInline(admin.TabularInline):
    def has_proof(self, obj) -> bool:
        return bool(obj.description)

    has_proof.short_description = "Has Proof"
    has_proof.boolean = True

    model = UserAchievement
    extra = 0  # Do not add empty forms
    fields = ("achievement", "date_completed", "has_proof")
    readonly_fields = ("achievement", "date_completed", "has_proof")


class UserAdmin(DefaultUserAdmin):
    inlines = [UserAchievementInline]

    def total_score(self, obj):
        return sum(ua.achievement.grade.points for ua in obj.achievements.all())

    total_score.short_description = "Total Score"

    def total_achievements(self, obj):
        return obj.achievements.count()

    total_achievements.short_description = "Total Achievements"

    readonly_fields = ("total_score", "total_achievements")
    fieldsets = (
        (None, {"fields": ("username", "password")}),  # from DefaultUserAdmin.fieldsets
        ("Achievements", {"fields": ("total_score", "total_achievements")}),
    )
    list_display = ("username", "total_score", "total_achievements")
    list_filter = ()
    search_fields = ("username", "first_name", "last_name", "email")
    filter_horizontal = ()


# Unregister default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(AchievementType)
class AchievementTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(AchievementGrade)
class AchievementGradeAdmin(admin.ModelAdmin):
    list_display = ("name", "points")


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "grade")


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    def has_proof(self, obj) -> bool:
        return bool(obj.description)

    has_proof.short_description = "Has Proof"
    has_proof.boolean = True

    search_fields = (
        "user__username",
        "achievement__name",
        "achievement__description",
        "achievement__type__name",
        "achievement__grade__name",
    )
    list_display = ("user", "achievement", "date_completed", "has_proof")
