"""
Views for UserInfo app.
"""
import json

from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import stringfilter, register
from django.utils.html import strip_tags
from django.db.models import Q

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
    gradstudents = User.objects.filter(groups__name='Brothers')
    gradstudents = gradstudents.filter(
        userinfo__graduationYear__lte=senior_year,
        groups__name="Brothers"
    ).prefetch_related('userinfo').order_by("last_name")

    seniors = User.objects.filter(groups__name='Brothers')
    seniors = seniors.filter(
        userinfo__graduationYear=senior_year,
        groups__name="Brothers"
    ).prefetch_related('userinfo').order_by("last_name")

    juniors = User.objects.filter(
        userinfo__graduationYear=(senior_year + 1),
        groups__name="Brothers"
    ).prefetch_related('userinfo').order_by("last_name")
    juniors = juniors.exclude(groups__name='Pledges')
    juniors = juniors.exclude(groups__name='Alumni')

    sophomores = User.objects.filter(
        userinfo__graduationYear=(senior_year + 2),
        groups__name="Brothers"
    ).prefetch_related('userinfo').order_by("last_name")
    sophomores = sophomores.exclude(groups__name='Pledges')
    sophomores = sophomores.exclude(groups__name='Alumni')

    freshmen = User.objects.filter(
        userinfo__graduationYear=(senior_year + 3),
        groups__name="Brothers"
    ).prefetch_related('userinfo').order_by("last_name")
    freshmen = freshmen.exclude(groups__name='Pledges')
    freshmen = freshmen.exclude(groups__name='Alumni')

    sweethearts = User.objects.filter(
        userinfo__graduationYear__gte=senior_year,
        groups__name='Sweethearts'
    ).prefetch_related('userinfo').order_by("last_name")
    sweethearts = sweethearts.exclude(groups__name='Pledges')
    sweethearts = sweethearts.exclude(groups__name='Alumni')

    exec_board = [
        (sage, "Sage"),
        (second, "2nd Counselor"),
        (third, "3rd Counselor"),
        (fourth, "4th Counselor"),
        (first, "1st Counselor"),
        (herald, "Herald"),
    ]

    # Exclude exec members from their class group
    for exec_brother in exec_board:
        user = exec_brother[0]
        if user is not None:
            gradstudents = gradstudents.exclude(username=user.username)
            seniors = seniors.exclude(username=user.username)
            juniors = juniors.exclude(username=user.username)
            sophomores = sophomores.exclude(username=user.username)
            freshmen = freshmen.exclude(username=user.username)
            user.title = exec_brother[1]

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
                'group_title': 'Graduate Students',
                'brothers': gradstudents,
                'count': len(gradstudents)
            },
            {
                'group_title': 'Seniors CHECK',
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
            },
            {
                'group_title': 'Sweethearts',
                'brothers': sweethearts,
                'count': len(sweethearts)
            }
        ]
    }

    return render(request, 'userinfo/public/brothers.html', context)


def family_tree_dashboard(request):
    """
    View for the family tree landing page
    """

    user_accounts = User.objects \
        .filter(groups__name__in=['Brothers', 'Alumni']) \
        .filter(Q(userinfo__isnull=True) | Q(userinfo__bigBrother__isnull=True))\
        .exclude(first_name__contains='Admin') \
        .prefetch_related('userinfo')\
        .all()

    options = ['All'] + [(u.first_name + " " + u.last_name) for u in user_accounts]

    context = {
        'options': options
    }
    return render(request, 'userinfo/public/family-tree-dashboard.html', context)


def family_tree(request):
    """
    View for the family tree page
    """

    context = {
        'pages': settings.PUBLIC_PAGES,
        'current_page_name': 'Brothers',
    }
    return render(request, 'userinfo/public/family-tree.html', context)


def get_tree_json(request):
    """
    API endpoint for getting the list of
    :param request:
    :return:
    """
    user_accounts = User.objects \
        .filter(groups__name__in=['Brothers', 'Alumni']) \
        .exclude(first_name__contains='Admin') \
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
        except (UserInfo.DoesNotExist, AttributeError):
            new_brother['big_brother'] = -1

        user_dict[user.id] = new_brother

    # Expand the dict into a tree structure
    for user in user_dict.values():
        if user['big_brother'] in user_dict:
            user_dict[user['big_brother']]['children'].append(user)
        else:
            root_node['children'].append(user)

    # big_list = json.dumps(root_node)

    return JsonResponse({
        'tree': root_node
    })


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
