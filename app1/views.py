from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import PageForm, storyForm, imageForm
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
    what.views = what.views + 1
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
    return render(request, 'app1/story.html',
                  {'stories': stories, 'division': division_name_slug, 'page': page_name_slug})


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


@login_required
def like_catagory(request):
    cat_id = None
    if request.method == 'GET':
        user = request.user
        cat_id = request.GET['page_id']
    likes = 0
    if cat_id:
        cat = Page.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
        else:
            return HttpResponse("No Pages found")
    return HttpResponse(likes)


@login_required
def like(request):
    if request.method == 'POST':
        user = request.user
        cat_id = None
        page = Page.objects.get(id=int(cat_id))
        if page.likes.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            page.likes.remove(user)
            message = 'You disliked this'
        else:
            # add a new like for a company
            page.likes.add(user)
            message = 'You liked this'

    ctx = {'likes_count': page.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def image_delete(request, division_name_slug, page_name_slug, story_id, value_id):
    obj = Picture.objects.get(pk=value_id)
    obj.delete()
    return redirect('image_share', division_name_slug, page_name_slug, story_id)
