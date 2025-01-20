from django.db import models


class QuestType(models.Model):
    """
    Main: главный квест, открывающие основную часть игры.
    Сюжетные: квесты завязанные на получение Навыков, Проф, Инструментов.
    Побочные: типовые квесты, задачи на leetcode, hackerrank, простые проекты например: написание калькулятора, боссы, данжы, Разработка.
        Боссы: это реальный "боевой проект", требующий выполнение условий (в виде, ряда побочных заказов) и открывающийся за валюту, очки за прохождение x2
        Данжи: квесты подразумевающие совместное прохождение, требующие затраты огромного количества валюты для открытия, очки за прохождение x5
        Разработка: квесты по улучшению непосредственно проекта ITachi, можно брать напрямую из to do листа, очки за прохождение x3
    доп:
        *побочные квесты можно разбить на дополнительные типы...
        *так же можно включить заказы фриланса.
        *проекты для открытия боссов, будут так или иначе связанны с тем что потребуется на боссе.

    IMHO: я бы отказался от подтипов квестов (у побочных), а сделал бы подтипы просто типами
    """
    # it's dynamic, so we can add new types without changing the database schema
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Quest(models.Model):
    """
    Квесты бывают 3 видов: main, сюжетный, побочный.
    Каждый этап квеста и сам квест привязан к определенной ачивке.
    Каждый Квест имеет: Описание, А так же дублирует: Название, Требования, Шаги выполненияm, Награды привязанные к ачивке.

    IMHO: я бы не связывал квесты напрямую с ачивками, а вынес бы квесты в отдельную таблицу, а ачивки привязывать к квестам (как я и сделал).
    То есть, квест != ачивка. Квест == список ачивок, которые нужно выполнить для получения награды.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.ForeignKey(QuestType, on_delete=models.CASCADE, related_name='quests')
    points = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.type})"


class AchievementType(models.Model):
    """
    Kvesti: ачивки завязанные на выполнении квестов.
    Mastering: разные ачивки построенные вокруг вышеперечисленных ачивок, требующие либо уникальное действие при выполнении, либо уникальные условия.
    Grind: ачивки связанные с выполнением какого то действия... Прогресия гринд ачивок 1-common, 10-uncommon, 50-rare, 100-uniq, так же Legendary
    Joke: разные шуточные ачивки, каждая имеет грейд Unique
        Дополнительно: Grind, Matering ачивки, строяться вокруг разных областей это могут быть квесты и профы или что то с этим не связанное, существующие в it
                       Структура выглядит примерно так Блок ачивок[ачивки]
    """
    # it's dynamic, so we can add new types without changing the database schema
    name = models.CharField(max_length=100)

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
    name = models.CharField(max_length=100)
    points = models.IntegerField()  # Награда

    def __str__(self):
        return f"{self.name} ({self.points})"


class Achievement(models.Model):
    """
    Основная механника, к которой привязанно по сути все:
    Каждая Ачивка имеет: Название, Требования, Шаги выполненияm, Награды.

    IMHO: не совсем понимаю разницу между Требования и Шаги выполнения -- это одно и то же?
    Плюс я так понял, награды привязаны к грейдам, а не к самим ачивкам.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.ForeignKey(AchievementType, on_delete=models.CASCADE, related_name='achievements')
    grade = models.ForeignKey(AchievementGrade, on_delete=models.CASCADE, related_name='achievements')
    # quest это необязательное поле, поэтому null=True (и blank=True для админки)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='achievements', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.grade}"


class UserAchievement(models.Model):
    # user's completed achievements
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    date_completed = models.DateTimeField(auto_now_add=True)


class UserQuest(models.Model):
    # user's completed quests
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='quests')
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='user_quests')
    date_completed = models.DateTimeField(auto_now_add=True)
