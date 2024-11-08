from django.db import models

#from board.models import Post  #보드 앱 추가 필요

class Address(models.Model):
    full_address = models.CharField(max_length=255,default="입력되지 않음")

    def __str__(self):
        return self.full_address
    
    
