from django.db import models


class Article(models.Model):
    article_no = models.IntegerField()
    article_newspaper = models.CharField(max_length=200)

    article_title = models.CharField(max_length=1000)
    article_link = models.URLField()
    article_image = models.URLField()

    def __str__(self):
        return self.article_title

    def is_from_delfi(self):
        if self.article_newspaper == 'delfi':
            return True
        else:
            return False



class Article_Information(models.Model):
    article_no = models.ForeignKey(Article, null = False, related_name='a_no', on_delete = models.CASCADE)
    article_newspaper = models.ForeignKey(Article, null = False, related_name='a_newspaper', on_delete = models.CASCADE)

    article_publish_date = models.DateField()
    article_publish_time = models.TimeField()
    article_modify_date = models.DateField()
    article_modify_time = models.TimeField()
    article_author = models.CharField(max_length=200)
    article_category = models.CharField(max_length=200)
    article_flex = models.CharField(max_length=200)

    def __str__(self):
        return self.article_author





