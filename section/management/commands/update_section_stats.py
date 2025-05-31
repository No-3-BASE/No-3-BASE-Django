from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from article.models import Article, Comment, Like
from board.models import Section
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Command(BaseCommand):
    help = '計算每個板塊昨天的文章數與熱度'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        yesterday_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_end = yesterday_start + timedelta(days=1)

        #清空昨天欄位
        for section in Section.objects.all():
            section.totalHot += section.yesterdayHot
            section.totalPosts += section.yesterdayPosts
            section.yesterdayHot = 0
            section.yesterdayPosts = 0
            section.save()

        #統計文章數
        articles = Article.objects.filter(publishAt__gte=yesterday_start, publishAt__lt=yesterday_end, status='published')

        for section in Section.objects.all():
            section_articles = articles.filter(section=section)
            article_count = section_articles.count()
            section.yesterdayPosts = article_count

            #統計留言數
            comment_count = Comment.objects.filter(article__in=section_articles, createAt__gte=yesterday_start, createAt__lt=yesterday_end).count()

            #統計按讚數
            article_type = ContentType.objects.get_for_model(Article)
            comment_type = ContentType.objects.get_for_model(Comment)
            like_count = Like.objects.filter(
                createAt__gte=yesterday_start,
                createAt__lt=yesterday_end
            ).filter(
                (models.Q(contentType=article_type) & models.Q(objectId__in=section_articles.values_list('id', flat=True))) |
                (models.Q(contentType=comment_type) & models.Q(objectId__in=Comment.objects.filter(article__in=section_articles).values_list('id', flat=True)))
            ).count()

            hot = article_count * 10 + comment_count * 5 + like_count * 3
            section.yesterdayHot = hot
            section.save()

        self.stdout.write("昨日統計更新完成！")