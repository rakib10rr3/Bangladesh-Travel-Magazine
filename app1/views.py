from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # for using the User one to one model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import PageForm, CommentForm,storyForm, imageForm
from .models import Division, Page, Picture, Story

try:
    from django.utils import simplejson as json
except ImportError:
    import json


# this acquires all the pages and sends it to index html with 'page_list' dictionary

def index(request):
    page_list = Page.objects.order_by('-views')[:5]

    return render(request, 'app1/index.html', {'page_list': page_list})


def division_detail(request, division_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        division = Division.objects.get(slug=division_name_slug)
        context_dict['division_name'] = division.title
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(division=division).order_by('-views')
        # Adds our results list to the template context under name pages.
        context_dict['page_list'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['division'] = division
        context_dict['division_name_slug'] = division_name_slug

    except Division.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    # Go render the response and return it to the client.
    return render(request, 'app1/division_detail.html', context_dict)


def track_url(request, page_name):
    what = Page.objects.get(slug=page_name)
    what.views += 1
    what.save()
    return


@login_required
def add_page(request, division_name_slug):
    try:
        cat = Division.objects.get(slug=division_name_slug)
    except Division.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.division = cat
            bet.save()
            # probably better to use a redirect here.
            return division_detail(request, division_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, 'division': cat, 'division_name_slug': division_name_slug}
    return render(request, 'app1/add_page.html', context_dict)


@login_required
def story(request, division_name_slug, page_name_slug):
    try:
        stories = Story.objects.filter(story_page__slug=page_name_slug)
        track_url(request, page_name_slug)

    except Story.DoesNotExist:
        stories = None
    user = request.user
    # storyByThisUser = stories.likes.filter(id=user.id)
    print(user.id)
    # print(storyByThisUser)
    like_list = []


    for s in stories:
        print(s.id)
        story = Story.objects.get(id=s.id)
        if story.likes.filter(id=user.id).exists():
            like_list.append(s.id)

    print(like_list)
    form=CommentForm()
    return render(request, 'app1/story.html',
                  {
                      'stories': stories,
                      'division': division_name_slug,
                      'page': page_name_slug,
                      'like_list': like_list,
                      'form':form
                  })






@login_required
def story_share(request, division_name_slug, page_name_slug):
    page_name = page_name_slug.title()
    page = Page.objects.get(name=page_name)

    if request.method == 'POST':
        form = storyForm(request.POST, request.FILES)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.user = request.user
            bet.story_page = page
            bet.save()
            context_dict = {'division': division_name_slug, 'page': page_name_slug, 'story_obj': bet}
            # return  redirect('image_share',context_dict)
            # return render(request, 'app1/image_upload.html', context_dict)
            return image_redirect(request, context_dict)
        else:
            print(form.errors)
    else:
        form = storyForm()
    context_dict = {'form': form}
    return render(request, 'app1/story_share.html', context_dict)


@login_required
def view_profile(request, user_name):
    # user = request.user

    the_user = User.objects.filter(username=user_name)
    print(the_user)

    return render(request, 'app1/profile.html',
                  {
                      'the_user': the_user[0]
                  })


@login_required
def image_redirect(request, context_dict):
    division = context_dict['division']

    page = context_dict['page']

    story_obj = context_dict['story_obj']
    story_obj_id = story_obj.id

    return redirect('image_share', division, page, story_obj_id)


@login_required
def image_share(request, division_name_slug, page_name_slug, story_id):
    page_name = page_name_slug.title()
    page = Page.objects.get(name=page_name)
    story_save = Story.objects.get(id=story_id)
    print(story_save)
    if request.method == 'POST':
        form = imageForm(request.POST, request.FILES)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.user = request.user
            bet.page = page
            bet.story = story_save
            bet.save()
            context_dict = {'division': division_name_slug, 'page': page_name_slug, 'story_obj': bet}
            # return  redirect('image_share',context_dict)
            # return render(request, 'app1/image_upload.html', context_dict)
            return redirect('image_share', division_name_slug, page_name_slug, story_id)
        else:
            print(form.errors)
    else:
        form = imageForm()
    context_dict = {'form': form, 'story_obj': story_save, 'division': division_name_slug, 'page': page_name_slug}
    return render(request, 'app1/image_upload.html', context_dict)




@login_required()
def like(request):
    story_id = request.GET.get('obj_id', None)
    story = Story.objects.get(id=story_id)
    print(story)
    user = request.user
    print(user.username)

    isLiked = True

    if story.likes.filter(id=user.id).exists():
        story.likes.remove(user)
        isLiked = False
    else:
        story.likes.add(user)
    totalLikes = story.total_likes

    # return HttpResponse(likees)

    jsonData = {
        'isLiked': isLiked,
        'totalLikes': totalLikes,
    }
    return HttpResponse(json.dumps(jsonData), content_type='application/json')

def image_delete(request, division_name_slug, page_name_slug, story_id, value_id):
    obj = Picture.objects.get(pk=value_id)
    obj.delete()
    return redirect('image_share', division_name_slug, page_name_slug, story_id)
@login_required()
def add_comment_to_story(request, division_name_slug, page_name_slug,story_id):
    story=Story.objects.get(id=story_id)
    if request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.story=story
            comment.save()
            print("all done")
            return redirect('story',division_name_slug, page_name_slug)
    else:
        form=CommentForm()
        print("took the form and called html")
    return render(request,'app1/comment_add.html',{'form': form } )