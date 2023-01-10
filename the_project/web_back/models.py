from django.db import models

# Create your models here.

class CommentData(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    comment_cont = models.CharField(max_length=1024)
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    post = models.ForeignKey('PostData', models.DO_NOTHING)
    comment_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comment_data'


class PostData(models.Model):
    post_id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=45)
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    contents_data = models.TextField(blank=True, null=True)
    post_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_data'


class TeamData(models.Model):
    team_name = models.CharField(primary_key=True, max_length=250)
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    introduction = models.CharField(max_length=1024, blank=True, null=True)
    team_make_time = models.DateTimeField()
    team_category = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'team_data'


class TeamUserData(models.Model):
    user = models.OneToOneField('UserData', models.DO_NOTHING, primary_key=True)
    tema_name = models.ForeignKey(TeamData, models.DO_NOTHING, db_column='tema_name')
    is_admin = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'team_user_data'
        unique_together = (('user', 'tema_name'),)


class UserData(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    user_pass = models.CharField(max_length=128)
    user_name = models.CharField(max_length=50)
    user_admin = models.CharField(max_length=1, blank=True, null=True)
    login_state = models.CharField(max_length=1, blank=True, null=True)
    user_email = models.CharField(max_length=512)
    user_comment = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_data'