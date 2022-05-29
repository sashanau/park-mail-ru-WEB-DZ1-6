from django.db import models
from django.contrib.auth.models import User


class AnswerManager(models.Manager):
    def get_answer(self, questions):
        return self.filter(question=questions).order_by('-added_on')

    def get_answer_for_id(self, id):
        return self.get(pk=id)


class QuestionManager(models.Manager):
    def get_for_name(self, name):
        return self.filter(title__name__iexact=name).order_by('-rating_num')

    def new_questions(self):
        return self.order_by('-added_on')

    def hot_questions(self):
        return self.order_by('-rating_num')

    def get_tag(self, tag_name):
        return self.filter(tags__name__iexact=tag_name).order_by('-rating_num')

    def get_questions(self, number):
        return self.filter(pk=number)[0]

    def get_count(self):
        return self.count()


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True, upload_to='static/img/', default='static/img/Avatar.jpg')
    register_date = models.DateField(null=False, blank=True, auto_now_add=True)
    user = models.OneToOneField(User, related_name='userprofile', primary_key=True, null=False,
                                on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=256)
    context = models.CharField(max_length=256)
    rating_num = models.IntegerField(default=0)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField('Tag')
    added_on = models.DateTimeField(blank=True, auto_now_add=True)
    answer = models.IntegerField(default=0)

    manager = QuestionManager()

    def __str__(self):
        return self.title


class Likes(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Profile, null=False, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.id_user


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Answer(models.Model):
    context = models.CharField(max_length=256)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=' ')
    rating_num = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    added_on = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question, related_name='answers',
                                 on_delete=models.DO_NOTHING)

    manager = AnswerManager()

    def __str__(self):
        return self.context
