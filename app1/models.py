from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User  # for using the USer one to one model

class Division(models.Model):
    title=models.CharField(max_length=10,unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField( )
    def save(self, *args, **kwargs):
            # Uncomment if you don't want the slug to change every time the name changes
            #if self.id is None:
                    #self.slug = slugify(self.name)
            self.slug = slugify(self.title)
            super(Division, self).save(*args, **kwargs)
    def __str__(self):
        return self.title

class Page(models.Model):
    name=models.CharField(max_length=10,unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField( )
    #description field
    des=models.TextField(max_length=500,blank=False)
    division=models.ForeignKey(Division)
    #changing default save method to save slug field
    def save(self, *args, **kwargs):
            # Uncomment if you don't want the slug to change every time the name changes
            #if self.id is None:
                    #self.slug = slugify(self.name)
            self.slug = slugify(self.name)
            super(Page, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class like(models.Model):
    user=models.ForeignKey(User)
    page=models.ForeignKey(Page)

#upload destination for images
def desti (instance,filename):
    return "%s/%s/%s"%(instance.page,instance.user,filename)

class Story(models.Model):
    user=models.ForeignKey(User)
    story_page=models.ForeignKey(Page)
    title_name=models.CharField(max_length=100)
    member=models.IntegerField(default=0,null=True)
    des=models.TextField(max_length=500,default='')
    def __str__(self):
        return  self.user.username +"-->"+self.title_name


class Picture(models.Model):
    """This is a small demo using just two fields. The slug field is really not
    necessary, but makes the code simpler. ImageField depends on PIL or
    pillow (where Pillow is easily installable in a virtualenv. If you have
    problems installing pillow, use a more generic FileField instead.
    """
    user=models.ForeignKey(User)
    page=models.ForeignKey(Page,related_name='pages')
    story=models.ForeignKey(Story,related_name='stories')
    file = models.ImageField(upload_to="picture")
    slug = models.SlugField(max_length=50, blank=True)
    def __str__(self):
        return  self.user.username+"->"+self.page.name
    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)



class Type(models.Model):
    type_name=models.CharField(max_length=10)
#user class


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    #comes up with some basic attributes(username,passward,email)
    user = models.OneToOneField(User)
    # The additional attributes we wish to include.
    def __str__(self):
        return self.user.username
