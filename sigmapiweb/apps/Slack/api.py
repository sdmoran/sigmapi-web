"""
API Endpoints for Slack Apps
"""
import json
import re

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from requests import post

from .utils import verify_sigma_poll_sig, verify_clique_sig
from .models import CliqueGroup, CliqueUser

SLACK_ID_REGEX = r"@(.*?)\|"
# TODO(Tom): Find a regex that works for single and double quote
DOUBLE_QUOTE_ARG_REGEX = r"\"(.*?)\""


def make_poll_usage_error(message, user_text):
    """
    Helper for creating the usage text response for Sigma Polls
    :param user_text: The command the user attempted to use
    """
    response = {
        "response_type": "ephemeral",
        "text": message + "\n"
                          "To create a poll, you need to format your query in the following way:\n"
                          "/sigmapoll \"Is this a poll?\" \"Yes\" \"No\"\n"
                          "This will create a poll with the question \"Is this a poll?\", and with the two possible "
                          "responses \"Yes\" and \"No\".\n"
                          "You invoked the following slash command: " + str(user_text)
    }
    return JsonResponse(response)


EMOJI_NUMS = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:']


@verify_sigma_poll_sig
def sigma_poll_create(request):
    """
    Creates a poll from a slash command POST that slack will send us
    Format: "What should we eat today?" "Apples" "Oranges"
    """

    response_url = request.POST.get('response_url')
    original_text = request.POST.get('text')

    if original_text is None or response_url is None:
        return HttpResponse('POST missing required fields', status=400)

    # Split the text on any type of quote, and make sure there are at least two options
    args = re.split('["“”]', original_text)
    if len(args) < 7 or args[0] != '' or len(args) % 2 == 0 or args[1].strip() == "" or args[2] != " ":
        return make_poll_usage_error("Error: Invalid Message Format", original_text)

    poll_question = args[1]
    poll_options = []
    poll_buttons = []
    i = 3
    while i < len(args):
        if args[i].strip() == "" or args[i + 1].strip() != "":
            return make_poll_usage_error("Error: Invalid Message Format", original_text)
        poll_options.append(args[i].strip())

        index = len(poll_buttons)
        if index >= len(EMOJI_NUMS):
            return make_poll_usage_error("Error: Too many options provided (max is 9)", original_text)
        poll_buttons.append({
            "name": str(index),
            "text": EMOJI_NUMS[index],
            "type": "button",
            "value": str(index)
        })

        # Add 2 since the next element is a space
        i += 2

    poll_buttons.append({
        "name": "delete",
        "text": "Delete Poll",
        "style": "danger",
        "type": "button",
        "value": "delete",
        "confirm": {
            "title": "Delete Poll?",
            "text": "Are you sure you want to delete the poll?",
            "ok_text": "Yes",
            "dismiss_text": "No"
        }
    })

    poll_text = "*" + poll_question + "*\n"
    option_index = 0
    while option_index < len(poll_options):
        poll_text += EMOJI_NUMS[option_index] + " " + poll_options[option_index] + "\n\n"

        option_index += 1

    response = {
        "response_type": "in_channel",
        "replace_original": True,
        "delete_original": True,
        "text": poll_text,
        "attachments": [{
            "fallback": "You are unable to complete this survey",
            "color": "#4196ca",
            "callback_id": "poll_buttons",
            "actions": poll_buttons[0:5]
        }]
    }

    if len(poll_buttons) > 5:
        response['attachments'].append({
            "fallback": "You are unable to complete this survey",
            "color": "#4196ca",
            "callback_id": "poll_buttons",
            "actions": poll_buttons[5:]
        })

    return JsonResponse(response)


def format_user(user_id):
    """
    Formats a user id so it appears as @user in the slack
    """
    return "<@" + user_id + ">"


def process_sigma_poll_action(user_id, action, response):
    """
    Applies an action to a poll
    :param user_id: The ID of the user who did this action
    :param action: The action to perform
    :param response: The response object to modify
    :return: True if the message isn't being deleted
    """
    option_value = action['value']
    if option_value == 'delete':
        response.clear()
        response['delete_original'] = True
        return False

    option_value = int(option_value)

    poll_split = response['text'].split('\n')

    option_text_index = 2 * option_value + 1
    option_users_index = option_text_index + 1

    option_text_split = list(filter(None, re.split(" ", poll_split[option_text_index])))
    option_users = list(filter(None, poll_split[option_users_index].split(', ')))

    if format_user(user_id) in option_users:
        option_users.remove(format_user(user_id))
    else:
        option_users.append(format_user(user_id))

    # Update the users list
    poll_split[option_users_index] = ', '.join(str(x) for x in option_users)

    num_votes = len(option_users)

    if re.search(r'`\d+`', option_text_split[-1]) is not None:
        poll_split[option_text_index] = ' '.join(option_text_split[:-1])
    else:
        poll_split[option_text_index] = ' '.join(option_text_split)

    if num_votes > 0:
        poll_split[option_text_index] += '    `' + str(num_votes) + "`"

    response['text'] = '\n'.join(str(x) for x in poll_split)

    return True


@verify_sigma_poll_sig
def sigma_poll_update(request):
    """
    Updates a Sigma Poll. This will either be a vote being cast, removed, or the creator
    requesting it to be deleted
    :param request:
    :return:
    """
    body = json.loads(request.POST.get('payload'))
    user = body['user']['id']

    response = {
        "replace_original": True,
        "text": body['original_message']['text'],
        "attachments": body['original_message']['attachments']
    }

    for action in body['actions']:
        if not process_sigma_poll_action(user, action, response):
            break

    return JsonResponse(response)

############################################
### Clique integration specific functions
############################################

def make_clique_group_error(msg):
    """
    Helper to pass along error messages encountered during Clique operations
    :param msg: Error message for the integration to report
    """
    return JsonResponse({"response_type": "ephermal", "text": msg})


@verify_clique_sig
def clique_create(request):
    """
    Creates a new grouping in the database (this integration must be stored in the db to be useful)
    Arguments: /group-create "groupname" "@user1 @user2"
    """
    requesting_user_id = request.POST.get('user_id')
    args = re.findall(DOUBLE_QUOTE_ARG_REGEX, request.POST.get("text"))
    # Check to see if everything looks right
    if len(args) != 2:
        return make_clique_group_error("Error in arguments (Double quotes are required!). Usage:\n"
                                        "`/group-create \"groupName\" \"@user1 @user2\"")

    if CliqueGroup.objects.filter(name=args[0]).count() > 0:
        return make_clique_group_error("This group <{}> already exists!".format(args[0]))

    # Move on to creating the group
    raw_group_members = re.findall(SLACK_ID_REGEX, args[1])
    group_users = []
    for slack_id in raw_group_members:
        try:
            group_users.append(CliqueUser.objects.get(slack_id=slack_id))
        except CliqueUser.DoesNotExist:
            # This is the first time that we've seen this user
            # we need to add them to the db
            new_user = CliqueUser(slack_id=slack_id)
            new_user.save()
            group_users.append(new_user)

    # Case where the owner is 1) new and 2) not in the group
    try:
        CliqueUser.objects.get(slack_id=requesting_user_id)
    except CliqueUser.DoesNotExist:
        # This is the first time that we've seen this user
        # we need to add them to the db
        CliqueUser(slack_id=requesting_user_id).save()

    new_group = CliqueGroup(
        creator=CliqueUser.objects.get(slack_id=requesting_user_id),
        name=args[0]
    )
    new_group.save()
    for clique_user in group_users:
        new_group.members.add(clique_user)

    new_group.save()
    # Testing response string
    resp_string = 'Group <{0}> has been created with users:'.format(args[0])
    resp_string += ' '.join(format_user(user.slack_id) for user in new_group.members.all())
    return JsonResponse({"replace_original": True, "text": resp_string})


@verify_clique_sig
def clique_send_msg(request):
    """
    Send a message to a Clique group
    Arguments: /group-message "groupname" "message"
    """
    args = re.findall(DOUBLE_QUOTE_ARG_REGEX, request.POST.get('text'))
    # Boilerplate error checking before continuing the function
    if len(args) != 2:
        return make_clique_group_error("Error in arguments (Double quotes are required!). Usage:\n"
                                       "`/group-message \"groupName\" \"message\"")

    if CliqueGroup.objects.filter(name=args[0]).count() == 0:
        return make_clique_group_error("This group <{}> doesn't exist!".format(args[0]))

    group = CliqueGroup.objects.get(name=args[0])
    request_args = {
        "token": settings.CLIQUE_SLACK_OATH_TOKEN,
        "channel": request.POST.get('channel_id'),
        "text": ("@{}".format(args[0]) +
                 " { " + " ".join(format_user(user.slack_id) for user in group.members.all()) +
                 " }:\n" + args[1]),
        "as_user": True,
    }
    post("https://slack.com/api/chat.postMessage", data=request_args)
    # Best practice to return _something_ so we give a 200
    return HttpResponse('')


@verify_clique_sig
def clique_add_users(request):
    """
    Add a user to an existing group
    Arguments: /group-add-users "groupname" "@user1 @user2"
    """
    args = re.findall(DOUBLE_QUOTE_ARG_REGEX, request.POST.get('text'))
    # Boilerplate error checking before continuing the function
    if len(args) != 2:
        return make_clique_group_error("Error in arguments (Double quotes are required!). Usage:\n"
                                       "`/group-add-users \"groupName\" \"@user1 @user2\"")

    if CliqueGroup.objects.filter(name=args[0]).count() == 0:
        return make_clique_group_error("This group <{}> doesn't exist!".format(args[0]))

    group = CliqueGroup.objects.get(name=args[0])
    raw_group_members = re.findall(SLACK_ID_REGEX, args[1])
    new_group_users = []
    for slack_id in raw_group_members:
        try:
            new_group_users.append(CliqueUser.objects.get(slack_id=slack_id))
        except CliqueUser.DoesNotExist:
            # This is the first time that we've seen this user
            # we need to add them to the db
            new_user = CliqueUser(slack_id=slack_id)
            new_user.save()
            new_group_users.append(new_user)

    for clique_user in new_group_users:
        group.members.add(clique_user)

    group.save()

    response = {
        "response_type": "ephemeral",
        "text": ("Added " +
                 " ".join(format_user(user.slack_id) for user in new_group_users) +
                 "to <{}>.\n".format(args[0]) +
                 "Group now contains:\n{" +
                 ", ".join(format_user(user.slack_id) for user in group.members.all()).strip(',') +
                 " }"),
    }
    return JsonResponse(response)


@verify_clique_sig
def clique_remove_users(request):
    """
    Remove a user from an existing group
    Arguments: /group-remove-users "groupname "@user1 @user2"
    """
    args = re.findall(DOUBLE_QUOTE_ARG_REGEX, request.POST.get('text'))
    # Boilerplate error checking before continuing the function
    if len(args) != 2:
        return make_clique_group_error("Error in arguments (Double quotes are required!). Usage:\n"
                                       "`/group-remove-users \"groupName\" \"@user1 @user2\"")

    if CliqueGroup.objects.filter(name=args[0]).count() == 0:
        return make_clique_group_error("This group <{}> doesn't exist!".format(args[0]))

    group = CliqueGroup.objects.get(name=args[0])
    raw_group_members = re.findall(SLACK_ID_REGEX, args[1])
    users_to_remove = []
    for slack_id in raw_group_members:
        try:
            users_to_remove.append(CliqueUser.objects.get(slack_id=slack_id))
        except CliqueUser.DoesNotExist:
            # We don't care that this fails,
            # we are removing people anyway
            pass

    for clique_user in users_to_remove:
        group.members.remove(clique_user)

    group.save()

    response = {
        "response_type": "ephemeral",
        "text": ("<{}> now contains:\n".format(args[0]) +  "{" +
                 ", ".join(format_user(user.slack_id) for user in group.members.all()).strip(',') +
                 " }"),
    }
    return JsonResponse(response)


@verify_clique_sig
def clique_delete(request):
    """
    Delete an existing group
    Arguments: /group-delete "groupname"
    """
    args = re.findall(DOUBLE_QUOTE_ARG_REGEX, request.POST.get('text'))
    # Boilerplate error checking before continuing the function
    if len(args) != 1:
        return make_clique_group_error("Error in arguments (Double quotes are required!). Usage:\n"
                                       "`/group-delete \"groupName\"")

    if CliqueGroup.objects.filter(name=args[0]).count() == 0:
        return make_clique_group_error("This group <{}> doesn't exist!".format(args[0]))

    group = CliqueGroup.objects.get(name=args[0])

    group.delete()

    response = {
        "response_type": "ephemeral",
        "text": "<{}> was deleted.".format(args[0])
    }
    return JsonResponse(response)


@verify_clique_sig
def clique_list(request):
    """
    List all members of all groups, if group is specified only list members of that group
    Arguments: /group-list ["groupname"]
    """

    args = re.findall(DOUBLE_QUOTE_ARG_REGEX, request.POST.get('text'))
    # Boilerplate error checking before continuing the function
    if len(args) > 1:
        return make_clique_group_error("Error in arguments (Double quotes are required!). Usage:\n"
                                       "`/group-list (optional: \"groupName\")")

    # Split into two helper functions to handle the different control flows
    if len(args) == 1:
        if CliqueGroup.objects.filter(name=args[0]).count() == 0:
            return make_clique_group_error("This group <{}> doesn't exist!".format(args[0]))
        return describe_clique(args[0])
    else:
        return describe_all_cliques()


def describe_clique(group_name):
    """
    Helper to list members of a specific CliqueGroup
    :param group_name: Regex matched group name that we KNOW exists
    """
    group = CliqueGroup.objects.get(name=group_name)

    response = {
        "response_type": "ephemeral",
        "text": ("Members of group <{}>:\n".format(group.name) + "{" +
                 ", ".join(format_user(user.slack_id) for user in group.members.all()).strip(',') +
                 "}")
    }
    return JsonResponse(response)


def describe_all_cliques():
    """
    Iterate through all CliqueGroup objects and list their members
    """
    final_string = ""
    for group in CliqueGroup.objects.all():
        final_string += (
            "Members of group <{}>:\n".format(group.name) + "{" +
            ", ".join(format_user(user.slack_id) for user in group.members.all()).strip(',') +
            "}"
        )
        final_string += "\n"

    response = {
        "response_type": "ephemeral",
        "text": final_string,
    }
    return JsonResponse(response)
