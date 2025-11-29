from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        if not username:
            raise ValueError('Имя пользователя обязательно')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, username, password, **extra_fields)

class Genres(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name

class Account(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    email = models.EmailField(unique=True, max_length=100)
    username = models.CharField(unique=True, max_length=50)
    avatar = models.BinaryField(null=True, blank=True)
    count_game = models.IntegerField(default=0)
    count_winner = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    favorite_genre = models.ForeignKey(Genres, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Обязательные поля для кастомной модели пользователя
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    captain = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Team_Account(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team_account'

    def __str__(self):
        return f"{self.account.username} - {self.team.name}"