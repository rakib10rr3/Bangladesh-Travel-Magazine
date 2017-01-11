from django.db import models
from django.template.defaultfilters import slugify

class Division(models.Model):
    title=models.CharField(max_length=10,unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField( )
    def save(self, *args, **kwargs):
            # Uncomment if you don't want the slug to change every time the name changes
            #if self.id is None:
                    #self.slug = slugify(self.name)
            self.slug = slugify(self.name)
            super(Division, self).save(*args, **kwargs)
    def __str__(self):
        return self.title


def desti (instance,filename):
    return "%s/%s"%(instance.id,filename) #EITAI KAJ BAKI ASE

class Page(models.Model):
    name=models.CharField(max_length=10,unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField( )
    likes = models.IntegerField(default=0)
    images=models.ImageField(upload_to=desti, null=True ,blank=True)
    division=models.ForeignKey(Division)
    def save(self, *args, **kwargs):
            # Uncomment if you don't want the slug to change every time the name changes
            #if self.id is None:
                    #self.slug = slugify(self.name)
            self.slug = slugify(self.name)
            super(Page, self).save(*args, **kwargs)
    def __str__(self):
        return self.name



