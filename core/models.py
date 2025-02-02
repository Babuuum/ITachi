from django.db import models


class AchievementType(models.Model):
    """
    Kvesti: ачивки завязанные на выполнении квестов.
    Mastering: разные ачивки построенные вокруг вышеперечисленных ачивок, требующие либо уникальное действие при выполнении, либо уникальные условия.
    Grind: ачивки связанные с выполнением какого то действия... Прогресия гринд ачивок 1-common, 10-uncommon, 50-rare, 100-uniq, так же Legendary
    Joke: разные шуточные ачивки, каждая имеет грейд Unique
    """
    # it's dynamic, so we can add new types without changing the database schema
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AchievementGrade(models.Model):
    """
    Common: самый простой и типовой грейд, награда 10 очков
    Uncommon: более сложные квесты, либо более длительные, 20 очков
    Rare: самые сбалансированные ачивки, 50 очков
    Epic: не простые очивки требующие длительного выполнения, либо сложностей в реализации, 100 - 200 очков
    Legendary: реально сложные в достижении ачивки, 5000 очков
    Unique: абсолютно уникальный грейд, содержащий любую награду, абсурдные или фановые квесты.
    """
    # it's dynamic, so we can add new grades without changing the database schema
    name = models.CharField(max_length=100, unique=True)
    points = models.IntegerField()  # Награда

    def __str__(self):
        return f"{self.name} ({self.points} pts)"


class Achievement(models.Model):
    """
    Основная механника, к которой привязанно по сути все.

    Пока что, у нас нет квестов и других сущностей, поэтому все будет в ачивке, например
    name = "[<Quest Name>] <Name>"
    """
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)  # optional
    requirements = models.TextField(null=True, blank=True)  # optional
    type = models.ForeignKey(AchievementType, on_delete=models.CASCADE, related_name='achievements')
    grade = models.ForeignKey(AchievementGrade, on_delete=models.CASCADE, related_name='achievements')

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.grade}"


class UserAchievement(models.Model):
    # user's completed achievements
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    date_completed = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)  # aka proof

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'achievement'], name='unique_user_achievement')
        ]
