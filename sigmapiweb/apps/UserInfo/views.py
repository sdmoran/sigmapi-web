"""
Views for UserInfo app.
"""
import json

from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.defaultfilters import stringfilter, register
from django.utils.html import strip_tags
from django.core.serializers.json import DjangoJSONEncoder

from . import utils
from .forms import EditUserInfoForm
from .models import UserInfo, PledgeClass


def users(request):
    """
    Provides the collections of brothers in the house.

    Organizes them based on year and exec positions.
    TODO: Refactor
    """
    # pylint: disable=too-many-statements

    # Find out what current year is the senior year grad date.
    senior_year = utils.get_senior_year()

    # Get the execs.
    # Use try/catch to avoid crashing the site if an exec is missing.
    # The "newX" positions are for when NME needs the updated list for
    # notebooks, but permissions aren't transitioned yet
    # (last two weeks of B-term basically)
    sage = check_user_exists('Sage', 'newSage')
    second = check_user_exists('2nd Counselor', 'new2nd')
    third = check_user_exists('3rd Counselor', 'new3rd')
    fourth = check_user_exists('4th Counselor', 'new4th')
    first = check_user_exists('1st Counselor', 'new1st')
    herald = check_user_exists('Herald', 'newHerald')

    # Get the rest of the users.  Exclude pledges or any execs.
    seniors = User.objects.filter(groups__name='Brothers')
    seniors = seniors.filter(
        userinfo__graduationYear__lte=senior_year
    ).prefetch_related('userinfo').order_by("last_name")

    juniors = User.objects.filter(
        userinfo__graduationYear=(senior_year + 1)
    ).prefetch_related('userinfo').order_by("last_name")
    juniors = juniors.exclude(groups__name='Pledges')
    juniors = juniors.exclude(groups__name='Alumni')

    sophomores = User.objects.filter(
        userinfo__graduationYear=(senior_year + 2)
    ).prefetch_related('userinfo').order_by("last_name")
    sophomores = sophomores.exclude(groups__name='Pledges')
    sophomores = sophomores.exclude(groups__name='Alumni')

    freshmen = User.objects.filter(
        userinfo__graduationYear=(senior_year + 3)
    ).prefetch_related('userinfo').order_by("last_name")
    freshmen = freshmen.exclude(groups__name='Pledges')
    freshmen = freshmen.exclude(groups__name='Alumni')

    # Exclude the execs, if applicable.
    if sage is not None:
        seniors = seniors.exclude(username=sage.username)
        juniors = juniors.exclude(username=sage.username)
        sophomores = sophomores.exclude(username=sage.username)
        freshmen = freshmen.exclude(username=sage.username)
        sage.title = "Sage"

    if second is not None:
        seniors = seniors.exclude(username=second.username)
        juniors = juniors.exclude(username=second.username)
        sophomores = sophomores.exclude(username=second.username)
        freshmen = freshmen.exclude(username=second.username)
        second.title = "2nd Counselor"

    if third is not None:
        seniors = seniors.exclude(username=third.username)
        juniors = juniors.exclude(username=third.username)
        sophomores = sophomores.exclude(username=third.username)
        freshmen = freshmen.exclude(username=third.username)
        third.title = "3rd Counselor"

    if fourth is not None:
        seniors = seniors.exclude(username=fourth.username)
        juniors = juniors.exclude(username=fourth.username)
        sophomores = sophomores.exclude(username=fourth.username)
        freshmen = freshmen.exclude(username=fourth.username)
        fourth.title = "4th Counselor"

    if first is not None:
        seniors = seniors.exclude(username=first.username)
        juniors = juniors.exclude(username=first.username)
        sophomores = sophomores.exclude(username=first.username)
        freshmen = freshmen.exclude(username=first.username)
        first.title = "1st Counselor"

    if herald is not None:
        seniors = seniors.exclude(username=herald.username)
        juniors = juniors.exclude(username=herald.username)
        sophomores = sophomores.exclude(username=herald.username)
        freshmen = freshmen.exclude(username=herald.username)
        herald.title = "Herald"

    context = {
        'pages': settings.PUBLIC_PAGES,
        'current_page_name': 'Brothers',
        'brother_groups': [
            {
                'group_title': 'Executive Council',
                'brothers': [sage, second, third, fourth, first, herald],
                'count': 6
            },
            {
                'group_title': 'Seniors',
                'brothers': seniors,
                'count': len(seniors)
            },
            {
                'group_title': 'Juniors',
                'brothers': juniors,
                'count': len(juniors)
            },
            {
                'group_title': 'Sophomores',
                'brothers': sophomores,
                'count': len(sophomores)
            },
            {
                'group_title': 'Freshmen',
                'brothers': freshmen,
                'count': len(freshmen)
            }
        ]
    }

    return render(request, 'userinfo/public/brothers.html', context)


def family_tree(request):
    """
    Builds the family tree based on user accounts
    """
    user_accounts = User.objects\
        .filter(groups__name__in=['Brothers', 'Alumni'])\
        .exclude(first_name__contains='Admin')\
        .prefetch_related('userinfo')

    root_node = {
        'name': "Sigma Pi Gamma Iota",
        'children': []
    }

    user_dict = dict()

    for user in user_accounts:
        new_brother = {
            'name': user.first_name + " " + user.last_name,
            'id': user.id,
            'children': []
        }
        try:
            new_brother['big_brother'] = user.userinfo.bigBrother.id
        except UserInfo.DoesNotExist:
            new_brother['big_brother'] = -1

        user_dict[user.id] = new_brother

    # Expand the dict into a tree structure
    for user in user_dict.items():
        if user['big_brother'] in user_dict:
            user_dict[user['big_brother']]['children'].append(user)
        else:
            root_node['children'].append(user)

    big_list = json.dumps(root_node, cls=DjangoJSONEncoder)

    context = {
        'users': big_list,
        'pages': settings.PUBLIC_PAGES,
        'current_page_name': 'Brothers',
    }
    return render(request, 'userinfo/public/family-tree.html', context)


def find_big(tree, big_id, little):
    """
    Find the big (user) that corresponds to the given little.
    """
    for node in tree:
        if node['id'] == big_id:
            node['children'].append(little)
            return True
        if not node['children'] and find_big(node['children'], big_id, little):
            return True
    return False


def check_user_exists(name, new_name):
    """
    Helper function to check if the EC role is assigned within the system.
    """
    user = None

    try:
        user = User.objects.get(groups__name=new_name)
    except User.DoesNotExist:
        try:
            user = User.objects.get(groups__name=name)
        except User.DoesNotExist:
            user = None

    return user


@permission_required('UserInfo.manage_users', login_url='secure-index')
def add_users(request):
    """
    Provides a view for adding a user.
    """
    context = {
        'message': []
    }

    if request.method == 'POST':
        add_type = request.POST['type']

        if add_type == "SINGLE":
            to_add = strip_tags(request.POST['username'])
            first_name = strip_tags(request.POST['firstname'])
            last_name = strip_tags(request.POST['lastname'])
            major = strip_tags(request.POST['major'])
            year = strip_tags(request.POST['class'])

            try:
                utils.create_user(
                    to_add, first_name, last_name, major, year
                )
            except utils.CreateUserError as err:
                context['message'].append(
                    'Error adding ' + to_add + ': ' + str(err)
                )
            else:
                context['message'].append(
                    'User ' + to_add + ' successfully added.'
                )
    return render(request, 'userinfo/secure/add.html', context)


@permission_required('UserInfo.manage_users', login_url='secure-index')
def manage_users(request):
    """
    Provides a view to manage all of the users in the system.
    """

    all_users = User.objects.all().order_by('last_name')

    context = {
        'all_users': all_users
    }

    return render(request, 'userinfo/secure/manage.html', context)


@permission_required('UserInfo.manage_users', login_url='secure-index')
def reset_password(_request, user):
    """
    Resets a single user's password.
    """
    # TODO: This should be changed over to being a POST request in the future.
    requested_user = User.objects.get(username__exact=user)
    utils.reset_password(requested_user)
    return redirect('userinfo-manage_users')


@login_required
def edit_user(request, user):
    """
    Provides a view to edit a single user.
    """
    requested_user = User.objects.get(username__exact=user)
    if (not requested_user == request.user) and not request.user.is_staff:
        return redirect('pub-permission_denied')
    message = ""
    if request.method == 'POST':
        try:
            form = EditUserInfoForm(
                request.POST,
                instance=requested_user.userinfo
            )
            if form.is_valid():
                form.save()
                message = 'Profile successfully updated'
        except UserInfo.DoesNotExist:
            new_userinfo, _created = UserInfo.objects.get_or_create(
                user=requested_user,
                pledgeClass=PledgeClass.objects.get(
                    id=request.POST['pledgeClass']
                ),
                phoneNumber=request.POST['phoneNumber'],
                major=request.POST['major'],
                hometown=request.POST['hometown'],
                activities=request.POST['activities'],
                interests=request.POST['interests'],
                favoriteMemory=request.POST['favoriteMemory']
            )
            form = EditUserInfoForm(request.POST, new_userinfo)
            message = 'Profile successfully updated'
    else:
        try:
            form = EditUserInfoForm(instance=requested_user.userinfo)
        except UserInfo.DoesNotExist:
            form = EditUserInfoForm()

    context = {
        'requested_user': requested_user,
        'form': form,
        'error': form.errors
    }
    if message:
        context['message'] = [message]

    return render(request, 'userinfo/secure/edit.html', context)


@login_required
def change_password(request):
    """
    Provides a view where a user can change their change_password.
    """
    context = {
        'message': []
    }
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            context['message'].append('Password successfully changed.')
        else:
            context['message'].append(
                'Error changing password. ' +
                'Check that your passwords match and that your old password ' +
                'is correct.'
            )
    context['form'] = PasswordChangeForm(user=request.user)
    return render(request, 'userinfo/secure/reset_password.html', context)


@register.filter
@stringfilter
def profile_image(rel_path):
    """
    Returns profile image path given a relative path.
    """
    return (
        '/content/' + rel_path
        if rel_path
        else '/static/img/user-placeholder.png'
    )
