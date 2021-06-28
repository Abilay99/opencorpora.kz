# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, verbose_name = _('name'))

    class Meta:
        verbose_name = _('authorization group')
        verbose_name_plural = _('authorization groups')
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, verbose_name = _('group'))
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING, verbose_name = _('permission'))

    class Meta:
        verbose_name = _('Authorization group permission')
        verbose_name_plural = _('Authorization group permissions')
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, verbose_name = _('name'))
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, verbose_name = _('content type'))
    codename = models.CharField(max_length=100, verbose_name = _('code name'))

    class Meta:
        verbose_name = _('Authorization permission')
        verbose_name_plural = _('Authorization permissions')
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, verbose_name = _('password'))
    last_login = models.DateTimeField(blank=True, null=True, verbose_name = _('last login'))
    is_superuser = models.IntegerField(verbose_name = _('is superuser'))
    username = models.CharField(unique=True, max_length=150, verbose_name = _('username'))
    first_name = models.CharField(max_length=150, verbose_name = _('first name'))
    last_name = models.CharField(max_length=150, verbose_name = _('last name'))
    email = models.CharField(max_length=254, verbose_name = _('email address'))
    is_staff = models.IntegerField(verbose_name = _('is staff'))
    is_active = models.IntegerField(verbose_name = _('is active'))
    date_joined = models.DateTimeField(verbose_name = _('date joined'))

    class Meta:
        verbose_name = _('Authorization user')
        verbose_name_plural = _('Authorization users')
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, verbose_name = _('user'))
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING, verbose_name = _('group'))

    class Meta:
        verbose_name = _('Authorization user group')
        verbose_name_plural = _('Authorization user groups')
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, verbose_name = _('user'))
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING, verbose_name = _('permission'))

    class Meta:
        verbose_name = _('Authorization user permission')
        verbose_name_plural = _('Authorization user permissions')
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Corpora(models.Model):
    title = models.TextField(blank=True, null=True, verbose_name= _('Title'))
    text = models.TextField(verbose_name= _('Text'))
    lemmas = models.TextField(blank=True, null=True, verbose_name= _('Lemmatization'))
    morphanaliz = models.TextField(blank=True, null=True, verbose_name= _('Morphological analysis'))
    outtext = models.TextField(blank=True, null=True)
    genre = models.ForeignKey('Genres', models.DO_NOTHING, related_name = 'genre', blank=True, null=True, verbose_name = _('Genre'))
    keywords = models.TextField(blank=True, null=True, verbose_name = _('Key words'))
    annotation = models.TextField(blank=True, null=True, verbose_name= _('Annotation'))
    subject = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True, verbose_name = _('URL address'))
    class Meta:
        verbose_name_plural = _('Corpora')
        verbose_name = _('Corpora')
        managed = False
        db_table = 'corpora'
        ordering = ['-id']


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField(verbose_name = _('action time'))
    object_id = models.TextField(blank=True, null=True, verbose_name = _('object id'))
    object_repr = models.CharField(max_length=200, verbose_name = _('object representation'))
    action_flag = models.PositiveSmallIntegerField(verbose_name = _('action flag'))
    change_message = models.TextField(verbose_name = _('change message'))
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True, verbose_name = _('content type'))
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, verbose_name = _('user'))

    class Meta:
        verbose_name_plural = _('Django admin logs')
        verbose_name = _('Django admin log')
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, verbose_name = _('app label'))
    model = models.CharField(max_length=100, verbose_name = _('model'))

    class Meta:
        verbose_name_plural = _('Django content types')
        verbose_name = _('Django content type')
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, verbose_name = _('app'))
    name = models.CharField(max_length=255, verbose_name = _('name'))
    applied = models.DateTimeField(verbose_name = _('applied'))

    class Meta:
        verbose_name_plural = _('Django migrations')
        verbose_name = _('Django migration')
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, verbose_name = _('session key'))
    session_data = models.TextField(verbose_name = _('session data'))
    expire_date = models.DateTimeField(verbose_name = _('expire date'))

    class Meta:
        verbose_name_plural = _('Django sessions')
        verbose_name = _('Django session')
        managed = False
        db_table = 'django_session'


class Genres(models.Model):
    rus = models.TextField(blank=True, null=True, verbose_name= _('Russian'))
    kz = models.TextField(blank=True, null=True, verbose_name= _('Kazakh'))
    en = models.TextField(blank=True, null=True, verbose_name= _('English'))
    def __str__(self):
        return self.kz
    class Meta:
        verbose_name_plural = _('Genres')
        verbose_name = _('Genre')
        managed = False
        db_table = 'genres'
        ordering = ['kz']

