from django.conf import settings
from django.db import models
#이미지 용량을 줄이려면 메타데이터를 제거하고, 적절한 크기로 리사이징 가급적 JPG포맷 사용
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import re

def photo_path(instance, filename):
    from time import gmtime, strftime
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return '{}/{}/{}.{}'.format(strftime('post/%Y/%m/%d/'), instance.author.username, pid, extension)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    #photo = models.ImageField(upload_to='post')
    photo = ProcessedImageField(upload_to=photo_path,
                                processors=[ResizeToFill(600, 600)],
                                format='JPEG',
                                options={'quality':90})
    content = models.CharField(max_length=140, help_text="최대 140자 입력 가능")
    
    
    def __str__(self):
        #return 'Post (PK: {self.pk}, Author: {self.author.username})'
        return 'Post (PK: %s, Author: %s)' % (self.pk, self.author.username)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(max_length=40)

    def __str__(self):
        #return 'Comment (PK: {self.pk}, Author: {self.author.username})'
        return 'Comment (PK: %s, Author: %s)' % (self.pk, self.author.username)