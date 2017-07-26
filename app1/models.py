from django.contrib.auth.models import User  # for using the User one to one model
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

class Division(models.Model):
    title = models.CharField(max_length=10, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        # if self.id is None:
        # self.slug = slugify(self.name)
        self.slug = slugify(self.title)
        super(Division, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

#changed
class Type(models.Model):
    type_name = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.type_name


class Place(models.Model):
    name = models.TextField(max_length=50, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField()
    # description field
    des = models.TextField(max_length=100, blank=False)
    division = models.ForeignKey(Division, related_name='places')

    # changing default save method to save slug field
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        # if self.id is None:
        # self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(Place, self).save(*args, **kwargs)
    def give_me_div_slug(self):
        return self.division.slug

    def __str__(self):
        return self.name

    def __int__(self):
        return self.views


# upload destination for images
def desti(instance, filename):
    return "%s/%s/%s" % (instance.page, instance.user, filename)
# upload destination for images
def user_desti(instance, filename):
    return "%s/%s" % (instance.display_name,filename)

class Story(models.Model):
    user = models.ForeignKey(User)
    story_division = models.ForeignKey(Division)
    story_page = models.ForeignKey(Place)
    type_name = models.ForeignKey(Type)
    title_name = models.CharField(max_length=100)
    budget = models.CharField(max_length=15)
    member = models.IntegerField(default=0, null=True)
    des = models.TextField(max_length=5000, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes')

    def give_me_page(self):
        return self.story_page

    def give_me_div(self):
        return self.story_page.division

    def get_absolute_url(self):
        return reverse('story_detail', args=[str(self.id)])

    def __str__(self):
        return self.title_name

    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.likes.count()

    # Shohag: testing.. :)
    @property
    def is_user_like_this(self, user_id):
        if self.likes.filter(id=user_id).exists():
            return True
        else:
            return False

    @property
    def is_user_story(self, user_id):
        if self.filter(id=user_id).exists():
            return True
        else:
            return False


class Picture(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.
    """
    user = models.ForeignKey(User)
    page = models.ForeignKey(Place, related_name='pages')
    story = models.ForeignKey(Story, related_name='stories')
    file = models.ImageField(upload_to=desti)
    slug = models.SlugField(max_length=50, blank=True)
    def __str__(self):
        return self.user.username + "->" + self.page.name

    @models.permalink
    def get_absolute_url(self):
        return 'upload-new',

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)


# user class

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    # comes up with some basic attributes(username,passward,email)
    # user = models.OneToOneField(User)
    user = models.OneToOneField(User)
    display_name = models.TextField(max_length=100, default='')
    birth_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to=user_desti,blank=True)
    GENDER_TYPE = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_TYPE,
        blank=True, null=True,
    )
    country = models.TextField(max_length=50, blank=True, null=True)

    # The additional attributes we wish to include.
    def __str__(self):
        return self.display_name

# here is the profile model

def user_post_save(sender, instance, created, **kwargs):
    """Create a user profile when a new user account is created"""
    if created == True:
        p = UserProfile()
        p.user = instance
        p.save()

post_save.connect(user_post_save, sender=User)


class Comment(models.Model):
    story = models.ForeignKey(Story, related_name='comments')
    author = models.ForeignKey(User)
    text = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
    @property
    def is_user_comment(self, user_id):
        if self.filter(id=user_id).exists():
            return True
        else:
            return False
    @property
    def approve(self):
        self.approved_comment = True
        self.save()
    def __str__(self):
        return self.text

class Question(models.Model):
    author = models.ForeignKey(User)
    question = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.question

class Answer(models.Model):
    answered_by = models.ForeignKey(User)
    answer_of = models.ForeignKey(Question, related_name='answers')
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    @property
    def is_user_answer(self, user_id):
        if self.filter(id=user_id).exists():
            return True
        else:
            return False


