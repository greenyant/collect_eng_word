from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Word(models.Model):
    text = models.CharField(max_length=50)
    basic_form = models.ForeignKey('self', null = True)
    
    def __str__(self):
        return self.text
    
    
class WordDetail(models.Model):
    word = models.ForeignKey(Word)
    detail = models.TextField()
    src = models.CharField(max_length=15)
    order = models.PositiveIntegerField(null = True)
    
    def __str__(self):
        return self.word.text + ' - ' + str(self.order) + '- '+ self.src