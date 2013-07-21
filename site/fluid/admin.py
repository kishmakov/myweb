from django.contrib import admin
from fluid.models import Link, Paper, Book, Other, DataPaper
from fluid.models import Subsection, Section, Chapter

admin.site.register(Link)
admin.site.register(Paper)
admin.site.register(Book)
admin.site.register(Other)
admin.site.register(DataPaper)

admin.site.register(Subsection)
admin.site.register(Section)
admin.site.register(Chapter)