from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
import hgvs.location
import hgvs.posedit

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Patient(models.Model):
    first_name = models.CharField(max_length=100) 
    last_name  = models.CharField(max_length=100)
    identifier = models.CharField(max_length=30, unique=True) 

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)


class User(AbstractUser):
    username     = models.CharField(max_length=100, default="None")
    email        = models.EmailField(_('email address'), unique=True)
    is_doctor    = models.BooleanField('student status', default=False)
    is_biologist = models.BooleanField('teacher status', default=True)
    patients     = models.ManyToManyField(Patient)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def full_name(self):
        return self.first_name + ' ' + self.last_name

class Variation(models.Model):
    OPERATION_CHOICES = (
        ('ins', 'Insertion'),
        ('del', 'Deletion'),
        ('insdel', 'Insertion-Deletion'),
        ('delins', 'Deletion-Insertion'),
        ('sub', 'Substitution'),
        ('dup', 'Duplication'),
    )
    author    = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    seq_id    = models.CharField(max_length=30)
    start     = models.IntegerField(null=True)
    end       = models.IntegerField(null=True)
    ref       = models.CharField(max_length=1000)
    alt       = models.CharField(max_length=1000)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    comment   = models.TextField(null=True)
    patient   = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    source    = models.CharField(max_length=30, default='Unknown')
    hgvs      = models.CharField(max_length=200, null=True)
    url       = models.CharField(max_length=255, null=True)

    @staticmethod
    def from_hgvs(variation, source):
        """
        Parses a string that describes a change in hgvs format and returns Variation object
        """
        hgvs_variation = hgvs.parse_hgvs_variant(variation)
        return self.from_hgvs_obj(hgvs_variation, source)

    @staticmethod
    def from_hgvs_obj(hgvs_variation, source):
        """
        Maps a hgvs.SequenceVariant to a Variation object
        """
        pos = hgvs_variation.posedit.pos
        start, end = pos.start, pos.end
        acc_id = hgvs_variation.ac
        edit = hgvs_variation.posedit.edit
        ref, alt = edit.ref, edit.alt

        change = str(edit)
        if '>' in change:
            operation = 'sub'
        elif 'delins' in change:
            operation = 'delins'
        elif 'insdel' in change:
            operation = 'insdel'
        elif 'ins' in change:
            operation = 'ins'
        elif 'dup' in change:
            operation = 'dup'
        else:
            operation = 'unknown'

        return Variation(
            seq_id=acc_id,
            start=start,
            end=end,
            ref=ref,
            alt=alt,
            operation=operation,
            source=source
        )
