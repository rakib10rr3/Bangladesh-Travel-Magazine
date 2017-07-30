from django import template
from app1.models import Division, Question, Follower

register = template.Library()


@register.inclusion_tag('app1/divs.html')
def get_division_list():
    # print("Running from inclusion tag ", this_user)
    # follower_obj = Follower.objects.all()
    # print('follower obj', follower_obj)
    # follower_list = []
    # for i in follower_obj:
    #     print(i.my_id)
    #     if i.my_id == this_user:
    #         follower_list.append(i.following_id)
    #
    # print(follower_list)
    # return {'divs': follower_list}

    divs = Division.objects.all()
    return {'divs': divs}


@register.filter
def in_page(image_list, page):
    return image_list.filter(page=page)


@register.inclusion_tag('app1/partial/follow_unfollow.html')
def pass_follower_list(this_user,obj_id,div_id):
    print("Logged in user = ",this_user)
    print("Have to delete = ",obj_id)
    print("Unique div id = ",div_id)
    follower_obj = Follower.objects.all()
    #print('follower obj', follower_obj)
    follower_list = []
    for i in follower_obj:
        if i.my_id == this_user:
            follower_list.append(i.following_id)
    print(follower_list)
    return {'follower_list': follower_list,"obj_id":obj_id,"div_id":div_id}



@register.filter
def is_user_question(question_list, user_id):
    if question_list.get(id=user_id):
        return True
    else:
        return False
