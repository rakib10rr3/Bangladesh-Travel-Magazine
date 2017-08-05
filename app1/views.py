from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # for using the User one to one model
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from datetime import datetime, timedelta
from collections import Counter
from .forms import PageForm, CommentForm, UserProfileForm, storyForm, imageForm, ProfileForm, QuestionForm, AnswerForm
from .forms import StoryAddForm
from .models import Division, Place, Picture, Story, UserProfile, Comment, Question, Answer, Notification, Follower, \
    Click_url_track
from .models import OwnReport, ReportCounter
from .models import Division, Place, Picture, Story, UserProfile, Comment, Question, Answer, Notification, Follower
from .models import OwnReport, ReportCounter, Favourite
from django.http import JsonResponse
from .models import Type

try:
    from django.utils import simplejson as json
except ImportError:
    import json

@login_required
def trending_list_division(request, division):
    take = trending_list(request)
    new_dict = {}
    for pl, value in take.items():
        if pl.division == division:
            new_dict[pl] = value
    print("New dict = ", new_dict)
    return new_dict

@login_required
def trending_list(request):
    print("*" * 5, "Trending_list function", "*" * 5)
    story_last_n_day = Story.objects.filter(created_date__gte=datetime.now() - timedelta(days=10))
    track_last_n_day = Click_url_track.objects.filter(created__gte=datetime.now() - timedelta(days=10))

    print('story track = ', story_last_n_day)
    print('click  track = ', track_last_n_day)

    story_submit_list = []
    track_list = []
    like_dict = {}
    ans = {}
    for i in story_last_n_day:
        story_submit_list.append(i.give_me_page())
    for i in track_last_n_day:
        track_list.append(i.give_me_page())
    new_submit_list = dict(Counter(story_submit_list).most_common(7))
    print('new submit list ', new_submit_list)
    new_track_url_list = dict(Counter(track_list).most_common(7))
    print('click  track = ', new_track_url_list)
    for i in new_submit_list.keys():
        all_stories = Story.objects.filter(story_page=i)
        # print("all stories of ", i, "= ", all_stories)
        take = 0
        for j in all_stories:
            take += j.total_likes
        # print("Likes for ", i, "= ", take)
        like_dict[i] = take
        ans[i] = like_dict[i] + new_submit_list[i]
        if i in new_track_url_list.keys():
            ans[i] += new_track_url_list[i]
        print('[', i, '] = ', ans[i])

    final_list = dict(Counter(ans).most_common(7))
    print("Final list = ", final_list)
    return final_list

@login_required
def get_follow_list(request):
    follower_obj = Follower.objects.all()
    follower_list = []
    for i in follower_obj:
        if i.my_id == request.user:
            follower_list.append(i.following_id)

    return follower_list


# def entry_list(request,
#                template='app1/entry_list.html',
#                page_template='app1/entry_list_page.html'):
#     context = {
#         'stories': Story.objects.order_by('-created_date'),
#         'page_template': page_template,
#     }
#     if request.is_ajax():
#         template = page_template
#     return render(request, template, context)

@login_required
def timeline_algo(request, context):
    print("##Timeline Algorithm ##")

    following_list = get_follow_list(request)
    favourite_list = context['favourites']
    print('My Following list', following_list)
    print('My Favourite places  list', favourite_list)
    my_story = []

    for x in favourite_list:
        place = Place.objects.get(pk=x.place_id)
        obj = Story.objects.filter(story_page=place).order_by('-id')[0]
        print('His story = ', obj.give_me_page())
        if obj.id not in my_story:
            my_story.append(obj.id)

    for i in following_list:
        obj = Story.objects.filter(user=i).order_by('-id')[0]
        print('His story = ', obj)
        if obj.id not in my_story:
            my_story.append(obj.id)

    recent_story = Story.objects.order_by('-created_date')

    for i in recent_story:
        if i.id not in my_story:
            my_story.append(i.id)
    print("##Timeline Algorithm End ##")
    return_list = []
    for i in my_story:
        obj = Story.objects.get(pk=i)
        return_list.append(obj)
    return return_list


def index(request, template='app1/index.html', page_template='app1/entry_list_page.html'):
    if request.user.is_authenticated:
        this_user = request.user
        # page_list = Place.objects.order_by('-views')[:3]
        context = trending_list(request)
        page_list = context
        print(type(page_list))

        favourite_list = Favourite.objects.filter(user=request.user)
        print("Favourite list = ", favourite_list)
        recent_story = timeline_algo(request, {'favourites': favourite_list})

        question_list = Question.objects.order_by('-created')[:5]
        q_form = QuestionForm()
        a_form = AnswerForm()
        user_profile = UserProfile.objects.filter(user=request.user)
        user = request.user
        report_list = OwnReport.objects.filter(u_id=request.user.id)
        # storyByThisUser = stories.likes.filter(id=user.id)
        print("user id= ", user.id)
        # print(storyByThisUser)
        like_list = []
        comment_list = []
        report_me = []
        follower_list = get_follow_list(request)

        # S29
        for u in report_list:
            if u.u_id == request.user.id:
                report_me.append(u.story_id)
        final_report = []
        for s in recent_story:
            if s.report >= 5:
                final_report.append(s.id)
        print(report_me)
        # EndS29
        for s in recent_story:
            # print(s.id)
            story_ = Story.objects.get(id=s.id)
            for s2 in story_.comments.all():
                if s2.author_id == user.id:
                    comment_list.append(s2.id)
            if story_.likes.filter(id=user.id).exists():
                like_list.append(s.id)

        # print("like list= ", like_list)
        # print("comment list= ", comment_list)
        form = CommentForm()

        fav_list = []
        for x in favourite_list:
            fav_list.append(x.place_id)
        print("fav list: ", favourite_list)
        context = {
            'page_list': page_list,
            'question_list': question_list,
            'stories': recent_story,
            'q_form': q_form,
            'a_form': a_form,
            'user_profile': user_profile,
            'like_list': like_list,
            'comment_list': comment_list,
            'form': form,
            'page_template': page_template,
            'report_list': report_me,
            'final_report': final_report,
            'divisions': Division.objects.all(),
            'types': Type.objects.all(),
            'favourites': fav_list,
        }
        if request.is_ajax():
            template = page_template
            # trending_list(request)
        return render(request, template, context)

    else:
        return render(request, 'app1/index_default.html',
                      {})

@login_required
def forum(request):
    if request.user.is_authenticated:
        user = request.user
        question_list = Question.objects.order_by('-created')[:10]
        q_form = QuestionForm()
        a_form = AnswerForm()
        return render(request, 'app1/forum.html',
                      {'q_form': q_form,
                       'a_form': a_form, 'question_list': question_list,
                       'user_id': user.id,
                       'divisions': Division.objects.all(),
                       'types': Type.objects.all(),
                       })


@login_required
def division_detail(request, division_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.

    context_dict = {}
    try:
        division = Division.objects.get(slug=division_name_slug)
        pages = trending_list_division(request, division)
        print('pages', pages)
        stories = Story.objects.filter(story_division=division).order_by('-created_date')[:5]
        user = request.user
        # storyByThisUser = stories.likes.filter(id=user.id)
        print(user.id)
        # print(storyByThisUser)
        like_list = []
        comment_list = []
        report_me = []
        report_list = OwnReport.objects.filter(u_id=request.user.id)
        for u in report_list:
            if u.u_id == request.user.id:
                report_me.append(u.story_id)
        final_report = []
        for s in stories:
            if s.report >= 5:
                final_report.append(s.id)
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
        context_dict['report_list'] = report_me
        context_dict['final_report'] = final_report
    except Division.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    # Go render the response and return it to the client.
    return render(request, 'app1/division_detail.html', context_dict)


@login_required
def track_url(request, page_id):
    place = Place.objects.get(id=page_id)
    obj = Click_url_track.objects.create(by=request.user, page_name=place)
    print("Click url is working ", obj)

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
    try:
        the_user = User.objects.filter(username=user_name)
    except User.DoesNotExist:
        the_user = None
        return render(request, 'app1/profile.html',
                      {
                          'the_user': the_user
                      })
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

    tour_list = []
    tour_list = Story.objects.filter(user=the_user)
    question_list = []
    question_list = Question.objects.filter(author_id=the_user)
    print("question", question_list)
    print("Tour_list", tour_list)
    follower_obj = Follower.objects.all()
    following = []
    follower = []
    favourite_list = Favourite.objects.filter(user=request.user)
    for i in follower_obj:
        if i.my_id == request.user:
            following.append(i.following)
        if i.following_id == request.user.id:
            follower.append(i.my_id)
    print("Following = ", following)
    print("Follower = ", follower)
    return render(request, 'app1/profile.html',
                  {
                      'the_user': the_user,
                      # 'user_info': user_info,
                      'tour_list': tour_list,
                      'question_list': question_list,
                      'following': following,
                      'follower': follower,
                      'favourite_list': favourite_list,
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

@login_required
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

@login_required
def image_share_jquery2(request, story_id):
    story = Story.objects.get(id=story_id)
    page = story.give_me_page()
    files = request.FILES.getlist('myfiles')
    print("Files = ", files)
    if (not files):
        return

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

@login_required
def comment_edit(request):
    if request.method == 'POST':
        user = request.user
        comment_id = request.POST['comment_id']
        new_comment = request.POST['new_comment']

        print(new_comment)
        comment = Comment.objects.get(id=comment_id)
        comment.text = new_comment
        print(comment)
        comment.save()
        return HttpResponse('')


@login_required
def answer_delete(request):
    if request.method == 'POST':
        user = request.user
        answer_id = request.POST['answer_id']
        print(answer_id)
        answer = Answer.objects.get(id=answer_id)
        print(answer)

        the_question = Question.objects.get(id=answer.answer_of_id)

        # question_author_id, answer_id, answer_giver_id
        delete_notify_question_new_comment(the_question.author_id, answer.id, answer.answered_by_id)

        answer.delete()

        return HttpResponse('')


@login_required
def reported_story(request):
    report_list = []
    stories = Story.objects.all()
    for s in stories:
        if s.report >= 5:
            report_list.append(s.id)
    return render(
        request, 'app1/Reported_stories.html', {
            'stories': stories,
            'report_list': report_list,
        }
    )


@login_required
def Own_report(request):  # s29
    if request.method == 'POST':
        user = request.user
        story_id = request.POST['story_id']
        print(story_id)
        print("khele")
        print(user.id)
        # c = OwnReport.objects.create(
        #    u_id=user.id,
        #    story_id=story_id
        # )
        report = Story.objects.filter(id=story_id)
        for s in report:
            print(s.report)
            s.report += 1
            s.save()
            print("after", s.report)
            print("check", s.id, "->", story_id)
        c = OwnReport()
        c.u_id = user.id
        c.story_id = story_id
        c.save()
        if ReportCounter.objects.filter(story_id=story_id):
            x = ReportCounter.objects.get(story_id=story_id)
            x.report_count += 1
            x.save()
        else:
            obj = ReportCounter()
            obj.story_id = story_id
            obj.report_count = int(1)
            obj.save()
        return render(request, 'app1/index.html')


@login_required
def answer_edit(request):
    if request.method == 'POST':
        user = request.user
        answer_id = request.POST['ans_id']
        new_ans = request.POST['new_ans']

        print(answer_id)
        answer = Answer.objects.get(id=answer_id)
        answer.text = new_ans
        print(answer)
        answer.save()
        return HttpResponse('')


@login_required
def question_edit(request):
    if request.method == 'POST':
        user = request.user
        question_id = request.POST['ques_id']
        new_ques = request.POST['new_ques']

        print(question_id)
        question = Question.objects.get(id=question_id)
        question.question = new_ques
        print(question)
        question.save()
        return HttpResponse('')


@login_required
def ajax_get_place_names(request):
    # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#icontains

    print(request.GET.get("query"))

    if request.method == 'GET':
        given_place_name = request.GET.get("query")
        given_division_name = int(request.GET.get("division"))

        if request.is_ajax():
            result = Place.objects.filter(name__icontains=given_place_name,
                                          division_id=given_division_name)

            data = [x.name for x in result]

            print(data)

            return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def ajax_add_story(request):
    if request.method == 'POST':

        print(request.POST)

        form = StoryAddForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            form_obj.save()

            # 1. Add the Place to db
            # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#get-or-create
            obj_place, created = Place.objects.get_or_create(
                name=request.POST.get("place_name"),
                division_id=int(request.POST.get("story_division")),
            )

            # 2. update the form data to add place id
            new_story_id = form_obj.id

            obj_story = Story.objects.get(pk=new_story_id)
            obj_story.story_page_id = obj_place.id
            obj_story.save()

            # 3. Then upload images; Bcoz image model need place id -_-
            add_story_images(request, form_obj.id)

            if request.is_ajax():
                data = {
                    'success': True,
                }
                return JsonResponse(data)
            else:
                return HttpResponse("Error!")
        else:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
            else:
                return HttpResponse("Error!")


@login_required
def ajax_notify_followers(request):
    if request.method == 'POST':
        if request.is_ajax():

            story_id = request.POST.get("story_id")

            followers = Follower.objects.filter(following=request.user)

            # add_notify_story_share_to_followers(follower_id, story_id, suggestion_giver_id)
            for follower in followers:
                add_notify_story_share_to_followers(follower.my_id_id, story_id, request.user.id)

            data = {
                'success': True,
            }

            return JsonResponse(data)


def add_story_images(request, story_id):
    """
    Add story images to server.
    Used in:
        - ajax_add_story()
    """

    obj_story = Story.objects.get(id=story_id)
    page = obj_story.give_me_page()
    files = request.FILES.getlist('img_files')

    print("Files = ", files)

    if not files:
        return

    for number, a_file in enumerate(files):
        instance = Picture(
            user=request.user,
            page=page,
            story=obj_story,
            file=a_file
        )
        instance.save()
        # request.session['number_of_files'] = number + 1


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
    report_me = []
    report_list = OwnReport.objects.filter(u_id=request.user.id)
    for u in report_list:
        if u.u_id == request.user.id:
            report_me.append(u.story_id)
    like_list = []
    if story.likes.filter(id=user.id).exists():
        like_list.append(story.id)
    return render(request, 'app1/Story_view.html', {'obj': story, 'like_list': like_list, 'comment_list': comment_list,
                                                    'report_list': report_me})


@login_required
def story_delete(request, story_id):
    story = Story.objects.get(id=story_id)
    story.delete()
    return redirect('user_profile', request.user.username)


@login_required
def save_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        print("Division", request.POST['story_division'], "khela", request.POST['place_name'])
        print("khele", request.FILES)
        print("Form", form)
        now_place = request.POST['place_name']
        div_id = request.POST['story_division']
        if form.is_valid():
            obj_place, created = Place.objects.get_or_create(
                name=request.POST.get("place_name"),
                division_id=int(request.POST.get("story_division")),
            )
            print(obj_place.id, "->", obj_place)
            bet = form.save(commit=False)
            bet.author = request.user
            bet.place = obj_place
            bet.save()
            # probably better to use a redirect here.
        else:
            print(form.errors)
    return redirect('forum')


@login_required
def save_answer(request):
    print("save answer is running ")

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        ques_id = request.POST['ques_id']
        print("question id = ", ques_id)
        question = Question.objects.get(id=ques_id)
        print(question)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.answered_by = request.user
            ans.answer_of = question
            b = ans.save()
            print(b)
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
def ques_detail(request, ques_id):
    try:
        ques = Question.objects.get(pk=ques_id)
    except Question.DoesNotExist:
        ques = None
    return render(request, 'app1/ques_view.html', {
        'ques': ques,
    })


@login_required
def search(request):
    if request.method == "POST":
        txt = request.POST.get("place")
        print(txt)
        if txt == '':
            return redirect('index')
        place = Place.objects.filter(name__contains=txt)
        question_list = Question.objects.filter(question__contains=txt)
        return render(request, 'app1/search_result.html',
                      {
                          'place': place,
                          'query': txt,
                          'question_list': question_list
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
        return render(request, 'app1/search_ques.html',
                      {
                          'query': txt,
                          'question_list': question_list})

        # custom change

@login_required
def save_favourite(request):
    print(request.user, "->", request.POST['story_place'])
    str = request.POST['story_place']

    print(str)

    sf = Favourite()
    sf.user = request.user
    sf.place = Place.objects.get(id=str)
    sf.save()
    return HttpResponse("")


def clear_favourite(request):
    str = request.POST['story_place']
    sf = Favourite.objects.get(user=request.user, place=Place.objects.get(name=str))
    print("unfav->", sf)
    sf.delete()
    return redirect('index')


def delete_ques(request, ques_id):
    ques = Question.objects.get(pk=ques_id)
    ques.delete()
    return redirect('forum')

@login_required
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
        
    For Story Share to Followers
    ============================
        notify_from :   'story_share'
        ref_type    :   'story'
        ref_value   :   int(story_id)
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
Notification for comment in a Question
'''


def add_notify_question_new_comment(question_author_id, answer_id, answer_giver_id):
    if question_author_id != answer_giver_id:
        add_notification(question_author_id, answer_giver_id, "q_a", "answer", answer_id)


def delete_notify_question_new_comment(question_author_id, answer_id, answer_giver_id):
    if question_author_id != answer_giver_id:
        delete_notification(question_author_id, answer_giver_id, "q_a", "answer", answer_id)


'''
Notification for Story Share to Followers
'''


def add_notify_story_share_to_followers(follower_id, story_id, suggestion_giver_id):
    if follower_id != suggestion_giver_id:
        add_notification(follower_id, suggestion_giver_id, "story_share", "story", story_id)


'''
==================================================
    View about Follow
==================================================
'''


def update_follow_list(request):
    if request.is_ajax():
        print("i am in update follow and ajax")
        text = request.GET['text']
        print(text)
        if text == "Follow":
            follower_obj = Follower.objects.all()
            follower_list = []
            for i in follower_obj:
                if i.my_id == request.user:
                    follower_list.append(i.following_id)
        else:
            follower_obj = Follower.objects.all()
            follower_list = []
            for i in follower_obj:
                if i.my_id == request.user:
                    follower_list.append(i.following_id)
        template = 'app1/partial/follow_unfollow.html'
        return render(request, template, {'follower_list': follower_list})

@login_required
def follow_unfollow(request):
    result = "null"
    text = ""
    if request.method == "POST":
        text = request.POST['button_text']
        action_id = request.POST['action_id']
        print("Command text=", text)
        print("with the id =", action_id)
        print(type(text))
        if text == "Unfollow":
            print("True")
        if text == "Unfollow":
            print("if is running,text= ", text)
            delete = Follower.objects.get(following_id=action_id).delete()
            result = "Deleted"
            print("Deleted", delete)

        elif text == "Follow":
            print("Else is running,text= ", text)
            result = "Added"
            if not Follower.objects.filter(following_id=action_id).exists():
                instance = Follower(following_id=action_id, my_id=request.user)
                value = instance.save()
                print("Added ", action_id)

        jsonData = {
            'result': result
        }
        return HttpResponse(json.dumps(jsonData), content_type='application/json')


def autocomplete(request):
    if request.is_ajax():
        queryset = Place.objects.filter(name__startswith=request.GET.get('search', None))
        list = []
        for i in queryset:
            list.append(i.name)
        data = {
            'list': list,
        }
        return JsonResponse(data)

@login_required
def picture_details(request, story_id):
    picture = Picture.objects.filter(story_id=story_id)
    return render(request, 'app1/images.html', {'picture': picture})
