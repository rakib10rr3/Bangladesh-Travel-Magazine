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
    #likes = models.ManyToManyField(User, related_name='likes')
    #images=models.ImageField(upload_to=desti, null=False ,blank=False)
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
    return "%s/%s/%s"%(instance.page,instance.user,filename) #EITAI KAJ BAKI ASE

class image(models.Model):
    user=models.ForeignKey(User)
    page=models.ForeignKey(Page)
    images=models.ImageField(upload_to=desti, null=False ,blank=False)



#user class

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    #comes up with some basic attributes(username,passward,email)
    user = models.OneToOneField(User)
    # The additional attributes we wish to include.
    def __str__(self):
        return self.username
