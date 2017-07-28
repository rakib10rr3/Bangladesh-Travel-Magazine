from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # for using the User one to one model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from itertools import chain
from .forms import PageForm, CommentForm, UserProfileForm, storyForm, imageForm, ProfileForm, QuestionForm, AnswerForm
from .models import Division, Place, Picture, Story, UserProfile, Comment, Question, Answer, Notification

try:
    from django.utils import simplejson as json
except ImportError:
    import json


def index(request):
    if request.user.is_authenticated:
        page_list = Place.objects.order_by('-views')[:3]
        recent_story = Story.objects.order_by('-created_date')[:5]
        question_list = Question.objects.order_by('-created')[:5]
        q_form = QuestionForm()
        a_form = AnswerForm()
        user_profile = UserProfile.objects.filter(user=request.user)
        user = request.user
        # storyByThisUser = stories.likes.filter(id=user.id)
        print(user.id)
        # print(storyByThisUser)
        like_list = []
        comment_list = []

        for s in recent_story:
            print(s.id)
            story_ = Story.objects.get(id=s.id)
            for s2 in story_.comments.all():
                if s2.author_id == user.id:
                    comment_list.append(s2.id)
            if story_.likes.filter(id=user.id).exists():
                like_list.append(s.id)

        print(like_list)
        print(comment_list)
        form = CommentForm()

        return render(request, 'app1/index.html',
                      {
                          'page_list': page_list,
                          'question_list': question_list,
                          'stories': recent_story,
                          'q_form': q_form,
                          'a_form': a_form,
                          'user_profile': user_profile,
                          'like_list': like_list,
                          'comment_list': comment_list,
                          'form': form
                      })
    else:
        return render(request, 'app1/index_default.html',
                      {})


def forum(request):
    if request.user.is_authenticated:
        user = request.user
        question_list = Question.objects.order_by('-created')[:5]
        q_form = QuestionForm()
        a_form = AnswerForm()
        return render(request, 'app1/forum.html',
                      {'q_form': q_form,
                       'a_form': a_form, 'question_list': question_list,
                       'user_id': user.id
                       })


@login_required
def division_detail(request, division_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.

    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        division = Division.objects.get(slug=division_name_slug)
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.

        pages = Place.objects.filter(division=division).order_by('-views')
        stories = Story.objects.filter(story_division=division).order_by('-created_date')[:5]
        user = request.user
        # storyByThisUser = stories.likes.filter(id=user.id)
        print(user.id)
        # print(storyByThisUser)
        like_list = []
        comment_list = []

        for s in stories:
            print(s.id)
            story_ = Story.objects.get(id=s.id)
            for s2 in story_.comments.all():
                if s2.author_id == user.id:
                    comment_list.append(s2.id)
            if story_.likes.filter(id=user.id).exists():
                like_list.append(s.id)

        print(like_list)
        print(comment_list)
        form = CommentForm()
        # Adds our results list to the template context under name pages.
        context_dict['stories'] = stories
        context_dict['page_list'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['division'] = division
        context_dict['like_list'] = like_list
        context_dict['comment_list'] = comment_list
        context_dict['form'] = form
    except Division.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    # Go render the response and return it to the client.
    return render(request, 'app1/division_detail.html', context_dict)


@login_required
def track_url(request, page_id):
    what = Place.objects.get(id=page_id)
    what.views += 1
    what.save()
    return


@login_required
def add_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            bet = form.save(commit=True)
            div = bet.division.slug
            print(div)
            # probably better to use a redirect here.
            return division_detail(request, div)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, }
    return render(request, 'app1/add_page.html', context_dict)


# @login_required
# def view_profile(request, user_name):
#     if request.method == 'POST':
#         print(request.POST)
#         if not UserProfile.objects.filter(user=request.user).exists():
#             form = ProfileForm(request.POST)
#             if form.is_valid():
#                 bet = form.save(commit=False)
#                 bet.user = request.user
#                 bet.save()
#             else:
#                 print(form.errors)
#         else:
#             result_ = UserProfile.objects.filter(user=request.user).update(
#                 display_name=request.POST['display_name'],
#                 birth_date=request.POST['birth_date'],
#                 gender=request.POST['gender'],
#                 country=request.POST['country']
#             )
#             result_.save()
#             print('Result: ' + str(result_))
#
#     # =====================================================
#
#     the_user = User.objects.filter(username=user_name)
#
#     user_info = {
#         'display_name': '',
#         'gender': '',
#         'birth_date': '',
#         'country': '',
#     }
#
#     if UserProfile.objects.filter(user=the_user).exists():
#         user_pro_info = UserProfile.objects.filter(user=the_user).values()
#         print(user_pro_info[0])
#         # Just style one.. -_-
#         user_info['display_name'] = user_pro_info[0]['display_name']
#         # Just style two.. -_-
#         user_info['gender'] = user_pro_info[0].get('gender')
#         user_info['birth_date'] = user_pro_info[0].get('birth_date').strftime('%Y-%m-%d') if not user_pro_info[0].get(
#             'birth_date') is None else user_pro_info[
#             0].get('birth_date')
#         user_info['country'] = user_pro_info[0].get('country')
#
#     print(the_user)
#     tour_list = Story.objects.filter(user=the_user)
#     print(tour_list)
#     return render(request, 'app1/profile.html',
#                   {
#                       'the_user': the_user[0],
#                       'user_info': user_info,
#                       'tour_list': tour_list,
#
#                  })
@login_required
def view_profile(request, user_name):
    # if request.method == 'POST':
    #     print(request.POST)
    #     if not UserProfile.objects.filter(user=request.user).exists():
    #         form = ProfileForm(request.POST)
    #         if form.is_valid():
    #             bet = form.save(commit=False)
    #             bet.user = request.user
    #             bet.save()
    #         else:
    #             print(form.errors)
    #     else:
    #         result_ = UserProfile.objects.filter(user=request.user).update(
    #             display_name=request.POST['display_name'],
    #             birth_date=request.POST['birth_date'],
    #             gender=request.POST['gender'],
    #             country=request.POST['country']
    #         )
    #         result_.save()
    #         print('Result: ' + str(result_))
    #
    # # =====================================================

    the_user = User.objects.filter(username=user_name)

    # user_info = {
    #     'display_name': '',
    #     'gender': '',
    #     'birth_date': '',
    #     'country': '',
    # }

    # if UserProfile.objects.filter(user=the_user).exists():
    #     user_pro_info = UserProfile.objects.filter(user=the_user).values()
    #     print(user_pro_info[0])
    #     # Just style one.. -_-
    #     user_info['display_name'] = user_pro_info[0]['display_name']
    #     # Just style two.. -_-
    #     user_info['gender'] = user_pro_info[0].get('gender')
    #     user_info['birth_date'] = user_pro_info[0].get('birth_date').strftime('%Y-%m-%d') if not user_pro_info[0].get(
    #         'birth_date') is None else user_pro_info[
    #         0].get('birth_date')
    #     user_info['country'] = user_pro_info[0].get('country')

    print(the_user[0])
    tour_list = Story.objects.filter(user=the_user)
    print(tour_list)

    return render(request, 'app1/profile.html',
                  {
                      'the_user': the_user[0],
                      # 'user_info': user_info,
                      'tour_list': tour_list,
                  })


@login_required
# changed
def update_userprofile(request, user_id):
    the_user = User.objects.get(id=user_id)

    print(the_user.username)
    user_profile = UserProfile.objects.get(user_id=the_user)
    print(user_profile)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.save()
            return redirect('user_profile', the_user.username)
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'app1/profile_edit.html', {'form': form, 'the_user': the_user})


@login_required
def image_redirect(request, context_dict):
    division = context_dict['division']
    page = context_dict['page']
    story_obj = context_dict['story_obj']
    story_obj_id = story_obj.id
    return redirect('image_share', division, page, story_obj_id)


@login_required
def image_share(request, story_id):
    print('Image Share Running')
    # page_ob = context_dict['story_page']
    # page_id = page_ob.id
    # page = Place.objects.get(id=page_id)

    story = Story.objects.get(id=story_id)

    page = story.give_me_page()
    print(page)
    print(story)
    if request.method == 'POST':
        form = imageForm(request.POST, request.FILES)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.user = request.user
            bet.page = page
            bet.story = story
            bet.save()
            context_dict2 = {'story_id': story_id}
            # return  redirect('image_share',context_dict)
            # return render(request, 'app1/image_upload.html', context_dict)
            return redirect('image_share', story_id)
        else:
            print(form.errors)
    else:
        form = imageForm()
    context_dict2 = {'form': form, 'story_obj': story, 'page': page}
    return render(request, 'app1/image_upload.html', context_dict2)


def image_share_jquery(request, story_id):
    story = Story.objects.get(id=story_id)
    page = story.give_me_page()
    if request.method == "POST":
        files = request.FILES.getlist('myfiles')
        for number, a_file in enumerate(files):
            instance = Picture(
                user=request.user,
                page=page,
                story=story,
                file=a_file
            )
            instance.save()
        request.session['number_of_files'] = number + 1
        return redirect('image_share', story_id)
    else:
        return render(request, 'app1/add_attachment.html', {})


def image_share_jquery2(request, story_id):
    story = Story.objects.get(id=story_id)
    page = story.give_me_page()
    files = request.FILES.getlist('myfiles')
    for number, a_file in enumerate(files):
        instance = Picture(
            user=request.user,
            page=page,
            story=story,
            file=a_file
        )
        instance.save()
    request.session['number_of_files'] = number + 1


@login_required
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

        delete_notify_story_new_like(story_id, story.user.id, user.id)
    else:
        story.likes.add(user)

        add_notify_story_new_like(story_id, story.user.id, user.id)

    totalLikes = story.total_likes

    jsonData = {
        'isLiked': isLiked,
        'totalLikes': totalLikes,
    }
    return HttpResponse(json.dumps(jsonData), content_type='application/json')


@login_required
def image_delete(request, story_id, value_id):
    obj = Picture.objects.get(pk=value_id)
    obj.delete()
    story = Story.objects.get(id=story_id)
    page = story.give_me_page()
    context_dict = {'story_id': story_id, 'page': page}
    return redirect('image_share', story_id)


@login_required
def add_comment(request):
    if request.method == 'POST':
        user = request.user
        text = request.POST['text']
        story_id = request.POST['story_id']
        story = Story.objects.get(id=story_id)
        print(story)
        c = Comment.objects.create(
            text=text,
            story=story,
            author=user
        )

        add_notify_story_new_comment(story.user.id, c.id, user.id)

        return HttpResponse('')


@login_required
def comment_delete(request):
    if request.method == 'POST':
        user = request.user
        comment_id = request.POST['comment_id']
        print(comment_id)
        comment = Comment.objects.get(id=comment_id)
        print(comment)
        comment.delete()

        story_id = comment.story_id
        story = Story.objects.get(id=story_id)
        delete_notify_story_new_comment(story.user.id, comment_id, user.id)

        return HttpResponse('')


def answer_delete(request):
    if request.method == 'POST':
        user = request.user
        answer_id = request.POST['answer_id']
        print(answer_id)
        answer = Answer.objects.get(id=answer_id)
        print(answer)
        answer.delete()
        return HttpResponse('')


@login_required
def story_share(request):
    """
    Add new Story
    """
    if request.method == 'POST':
        form = storyForm(request.POST, request.FILES)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.user = request.user
            bet.save()
            print(bet)
            print(bet.story_page)

            context_dict = {'story_id': bet.id, 'page': bet.story_page}
            # return  redirect('image_share',context_dict)
            # return render(request, 'app1/image_upload.html', context_dict)
            # return redirect('image_share', bet.id)
            # return redirect('image_share_jquery', bet.id)
            image_share_jquery2(request, bet.id)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = storyForm()

    context_dict = {'form': form}
    return render(request, 'app1/story_share.html', context_dict)


@login_required
def story(request, division_name_slug, page_id):
    try:
        stories = Story.objects.filter(story_page__id=page_id)
        track_url(request, page_id)
    except Story.DoesNotExist:
        stories = None

    user = request.user
    # storyByThisUser = stories.likes.filter(id=user.id)
    print(user.id)
    # print(storyByThisUser)
    like_list = []
    comment_list = []

    for s in stories:
        print(s.id)
        story_ = Story.objects.get(id=s.id)
        for s2 in story_.comments.all():
            if s2.author_id == user.id:
                comment_list.append(s2.id)
        if story_.likes.filter(id=user.id).exists():
            like_list.append(s.id)

    print(like_list)
    print(comment_list)
    form = CommentForm()
    return render(request, 'app1/story.html',
                  {
                      'stories': stories,
                      'division': division_name_slug,
                      'page': Place.objects.get(id=page_id),
                      'like_list': like_list,
                      'comment_list': comment_list,
                      'form': form
                  })


@login_required
def story_detail(request, story_id):
    story = Story.objects.get(pk=story_id)
    user = request.user
    comment_list = []
    for s2 in story.comments.all():
        if s2.author_id == user.id:
            comment_list.append(s2.id)

    like_list = []
    if story.likes.filter(id=user.id).exists():
        like_list.append(story.id)
    return render(request, 'app1/Story_view.html', {'obj': story, 'like_list': like_list, 'comment_list': comment_list})


@login_required
def story_delete(request, story_id):
    story = Story.objects.get(id=story_id)
    story.delete()
    return redirect('user_profile', request.user.username)


@login_required
def save_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.author = request.user
            bet.save()
            # probably better to use a redirect here.
        else:
            print(form.errors)

    return redirect('forum')


@login_required
def save_answer(request, q_id):
    question = Question.objects.get(id=q_id)
    print(question)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.answered_by = request.user
            ans.answer_of = question
            ans.save()
            # probably better to use a redirect here.

            add_notify_question_new_comment(question.author_id, ans.id, ans.answered_by_id)

        else:
            print(form.errors)
    return redirect('forum')


@login_required
def story_edit(request, story_id):
    story = Story.objects.get(id=story_id)
    if request.method == "POST":
        form = storyForm(request.POST, instance=story)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.user = request.user
            bet.save()
            return redirect('story_detail', bet.id)
    else:
        form = storyForm(instance=story)
    return render(request, 'app1/story_edit.html', {'form': form})

    # custom change list creating -_-


@login_required
def search(request):
    if request.method == "POST":
        txt = request.POST.get("place")
        print(txt)
        if txt == '':
            return redirect('index')
        place = Place.objects.filter(name__contains=txt)
        return render(request, 'app1/search_result.html',
                      {
                          'place': place,
                          'query': txt
                      })


@login_required
def search_ques(request):
    if request.method == "POST":
        txt = request.POST.get("ques")
        print(txt)
        if txt == '':
            return redirect('forum')
        question_list = Question.objects.filter(question__contains=txt)
        q_form = QuestionForm()
        a_form = AnswerForm()
        return render(request, 'app1/forum.html',
                      {'q_form': q_form,
                       'a_form': a_form,
                       'question_list': question_list})

        # custom change


def notifications(request):
    user = request.user
    n = Notification.objects.filter(recipient_id=user.id).order_by('-date_created')
    unread_count = n.filter(unread=True).count()

    # Complete: change to all read!
    set_unread = set()
    for item in n:
        if item.unread:
            set_unread.add(item.id)

    n.update(unread=False)

    # TODO: Limit notifications view number and make it infinite list type (more button)
    # TODO: update link in html file for question notifications

    return render(request, 'app1/notifications.html',
                  {
                      'notifications': n,
                      'unread_list': set_unread,
                      'unread_count': unread_count,
                  })


def about(request):
    return render(request, 'app1/about.html',
                  {})


'''
==================================================
    Utility Functions for Notification
==================================================
'''

'''
    For Story Comment
    =================
        notify_from :   'story_cmnt'
        ref_type    :   'comment'
        ref_value   :   int(comment_id)
        
    For Like
    ========
        notify_from :   'story_like'
        ref_type    :   'story'
        ref_value   :   int(story_id)
        
    For Question Comment
    ====================
        notify_from :   'q_a'
        ref_type    :   'answer'
        ref_value   :   int(answer_id)
'''


def add_notification(recipient, sender, notify_from, ref_type, ref_value):
    n = Notification(recipient_id=recipient, sender_id=sender, notify_from=notify_from,
                     ref_type=ref_type, ref_value=ref_value)
    n.save()


def delete_notification(recipient, sender, notify_from, ref_type, ref_value):
    n = Notification.objects.filter(recipient_id=recipient, sender_id=sender, notify_from=notify_from,
                                    ref_type=ref_type, ref_value=ref_value)
    n.delete()


'''
Notification for comment in a Story
'''


def add_notify_story_new_comment(story_author_id, comment_id, commentator_id):
    if story_author_id != commentator_id:
        add_notification(story_author_id, commentator_id, "story_cmnt", "comment", comment_id)


def delete_notify_story_new_comment(story_author_id, comment_id, commentator_id):
    if story_author_id != commentator_id:
        delete_notification(story_author_id, commentator_id, "story_cmnt", "comment", comment_id)

'''
Notification for like in a Story
'''


def add_notify_story_new_like(story_id, story_author_id, liker_id):
    if story_author_id != liker_id:
        add_notification(story_author_id, liker_id, "story_like", "story", story_id)


def delete_notify_story_new_like(story_id, story_author_id, liker_id):
    if story_author_id != liker_id:
        delete_notification(story_author_id, liker_id, "story_like", "story", story_id)


'''
Notification for comment in a Question (Not Final)
'''


def add_notify_question_new_comment(question_author_id, answer_id, answer_giver_id):
    if question_author_id != answer_giver_id:
        add_notification(question_author_id, answer_giver_id, "q_a", "answer", answer_id)
