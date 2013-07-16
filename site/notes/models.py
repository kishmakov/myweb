import HTMLParser
from django.db import models

class MPNote(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    classifier = models.CharField(db_column='Classifier', max_length=30)
    title = models.CharField(db_column='Title', max_length=100)
    author = models.CharField(db_column='Author', max_length=100)
    link = models.CharField(db_column='Link', max_length=200)
    teaser = models.TextField(db_column='Teaser')
    body = models.TextField(db_column='Body')

    def __unicode__(self):
        h = HTMLParser.HTMLParser()
        unescaped = h.unescape(self.title)
        return u'{0}: {1}'.format(self.id, unescaped)

    class Meta:
        db_table = 'mp_note'

class THNote(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    classifier = models.CharField(db_column='Classifier', max_length=30)
    title = models.CharField(db_column='Title', max_length=100)
    teaser = models.TextField(db_column='Teaser')
    body = models.TextField(db_column='Body')

    def __unicode__(self):
        h = HTMLParser.HTMLParser()
        unescaped = h.unescape(self.title)
        return u'{0}: {1}'.format(self.id, unescaped)

    class Meta:
        db_table = 'th_note'

