# migrate reset
# https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models

#이미지 용량을 줄이려면 메타데이터를 제거하고, 적절한 크기로 리사이징 가급적 JPG포맷 사용
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class UserManager(BaseUserManager):
    def create_superuser(self, *args, **kwargs):
        return super.create_superuser(gender=self.model.GENDER_MALE, *args, **kwargs)

class User(AbstractUser):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    CHOICES_GENDER = (
        (GENDER_MALE, '남성'),
        (GENDER_FEMALE, '여성'),
    )
    img_profile = ProcessedImageField(upload_to='user',
                                processors=[ResizeToFill(600, 600)],
                                format='JPEG',
                                options={'quality':90},
                                blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)
    like_posts = models.ManyToManyField('imagebook.Post', blank=True, related_name='like_users')
    
    objects = UserManager()
    
    def __str__(self):
        return self.username


# Create your models here.
