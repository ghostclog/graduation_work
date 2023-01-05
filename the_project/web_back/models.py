from django.db import models

# Create your models here.

class FindPeople(models.Model):
    post_code = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    team_name = models.ForeignKey('TeamData', models.DO_NOTHING, db_column='team_name')
    post_title = models.CharField(max_length=128)
    post_con = models.TextField()

    class Meta:
        managed = False
        db_table = 'find_people'
        unique_together = (('post_code', 'user'),)


class RegitData(models.Model):
    res_code = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserData', models.DO_NOTHING)
    team_name = models.ForeignKey('TeamData', models.DO_NOTHING, db_column='team_name')

    class Meta:
        managed = False
        db_table = 'regit_data'


class TeamData(models.Model):
    team_name = models.CharField(primary_key=True, max_length=250)
    user = models.ForeignKey('UserData', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'team_data'


class UserData(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    user_pass = models.CharField(max_length=128)
    user_name = models.CharField(max_length=50)
    user_admin = models.CharField(max_length=1, blank=True, null=True)
    login_state = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_data'


class UserTeam(models.Model):
    user = models.OneToOneField(UserData, models.DO_NOTHING, primary_key=True)
    team_name = models.ForeignKey(TeamData, models.DO_NOTHING, db_column='team_name')

    class Meta:
        managed = False
        db_table = 'user_team'
        unique_together = (('user', 'team_name'),)