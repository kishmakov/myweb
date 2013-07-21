import HTMLParser
from django.db import models

# link representation

class CommonLink(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    title = models.CharField(db_column='Title', max_length=200)
    link = models.CharField(db_column='Link', max_length=200)
    description = models.TextField(db_column='Description')

    def __unicode__(self):
        h = HTMLParser.HTMLParser()
        title = h.unescape(self.title)
        return u'{0}: {1}'.format(self.id, title)

    class Meta:
        abstract = True

class CommonPaper(CommonLink):
    authors = models.CharField(db_column='Authors', max_length=200)
    year = models.CharField(db_column='Year', max_length=10)
    journal = models.CharField(db_column='Journal', max_length=200)
    doi = models.CharField(db_column='DOI', max_length=100)

    def __unicode__(self):
        h = HTMLParser.HTMLParser()
        title = h.unescape(self.title)
        authors = h.unescape(self.authors)
        return u'{0}: {1} -- {2}'.format(self.id, authors, title)

    class Meta:
        abstract = True

class Link(CommonLink):
    class Meta:
        db_table = 'link'

class Paper(CommonPaper):
    class Meta:
        db_table = 'paper'

class Book(CommonLink):
    authors = models.CharField(db_column='Authors', max_length=200)
    year = models.CharField(db_column='Year', max_length=10)
    publisher = models.CharField(db_column='Publisher', max_length=200)
    isbn = models.CharField(db_column='ISBN', max_length=100)

    class Meta:
        db_table = 'book'

class Other(CommonLink):
    authors = models.CharField(db_column='Authors', max_length=200)
    source = models.CharField(db_column='Source', max_length=200)

    class Meta:
        db_table = 'other'

class DataPaper(CommonPaper):
    class Meta:
        db_table = 'data_paper'

# texts representation

class CommonNode(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    title = models.CharField(db_column='Title', max_length=200)
    subnodes = models.TextField(db_column='Subnodes')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.id, self.title)

    class Meta:
        abstract = True


class Subsection(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    title = models.CharField(db_column='Title', max_length=200)
    text = models.TextField(db_column='Text')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.id, self.title)

    class Meta:
        db_table = 'subsection'

class Section(CommonNode):
    class Meta:
        db_table = 'section'

class Chapter(CommonNode):
    references = models.TextField(db_column='References')
    class Meta:
        db_table = 'chapter'
