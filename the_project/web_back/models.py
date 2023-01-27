from django.db import models

# Create your models here.

class CommentData(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_cont = models.CharField(max_length=1024)
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    post = models.ForeignKey('PostData', models.DO_NOTHING)
    comment_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comment_data'



class ChatData(models.Model):
    chat_id = models.AutoField(primary_key=True)
    user_chat = models.CharField(max_length=100)
    team_name = models.ForeignKey('TeamData', models.DO_NOTHING, db_column='team_name')
    user_name = models.CharField(max_length=50)
    chat_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_data'



class PostData(models.Model):
    post_id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=45)
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    contents_data = models.TextField()
    post_time = models.DateTimeField()
    team_name = models.ForeignKey('TeamData', models.DO_NOTHING, db_column='team_name', blank=True, null=True)
    num_of_open = models.IntegerField()
    num_of_recommend = models.IntegerField()
    post_title = models.CharField(max_length=1024, blank=True, null=True)
    post_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_data'


class TeamApplyLog(models.Model):
    apply_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    team_name = models.ForeignKey('TeamData', models.DO_NOTHING, db_column='team_name')

    class Meta:
        managed = False
        db_table = 'team_apply_log'


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
    pr_key = models.AutoField(primary_key=True)
    team_name = models.ForeignKey(TeamData, models.DO_NOTHING, db_column='team_name')
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    is_admin = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'team_user_data'


class TeamPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=50)
    post_contents = models.TextField()
    post_time = models.DateTimeField()
    team_name = models.ForeignKey(TeamData, models.DO_NOTHING, db_column='team_name')
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    post_type = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_post'


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



class profile_photo(models.Model):
    user_photo = models.ImageField(upload_to="media/profile")
    user_id = models.CharField(max_length=50)



class WebBackProfilePhoto(models.Model):
    user_photo = models.CharField(max_length=100)
    user = models.OneToOneField(UserData, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'web_back_profile_photo'