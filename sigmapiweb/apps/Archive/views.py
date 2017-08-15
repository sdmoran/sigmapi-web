from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.utils.html import strip_tags
from django.template.defaultfilters import slugify
from datetime import datetime
from django_downloadview import sendfile
from .models import Guide, GuideForm, HouseRules, HouseRulesForm, Bylaws, BylawsForm


@login_required
def index(request):
    """
        View for the index page of the archives.
    """

    if request.user.has_perm('Archive.access_guide'):
        return redirect(guides)
    elif request.user.has_perm('Archive.access_bylaws'):
        return redirect(bylaws)
    elif request.user.has_perm('Archive.access_houserules'):
        return redirect(rules)
    else:
        return redirect('pub-permission_denied')

@permission_required('Archive.access_bylaws', login_url='pub-permission_denied')
def bylaws(request):
    """
        View for all bylaws.
    """

    if request.method == 'POST':

        if request.user.has_perm('Archive.add_bylaws'):

            form = BylawsForm(request.POST, request.FILES)

            if form.is_valid():
                bylaw = form.save(commit=False)
                bylaw.date = datetime.now()
                bylaw.save()
        else:
            redirect('pub-permission_denied')

    bylaws = Bylaws.objects.all()

    if bylaws:
        latest = bylaws.latest('date')
    else:
        latest = None

    form = BylawsForm()

    context = {
        'latest': latest,
        'bylaws': bylaws,
        'form': form
    }

    return render(request, 'archive/bylaws.html', context)


@permission_required('Archive.access_bylaws', login_url='pub-permission_denied')
def download_bylaw(request, bylaw):
    """
        View for downloading bylaws
    """

    bylawObject = Bylaws.objects.get(pk=bylaw)
    return sendfile(request, bylawObject.filepath.path, attachment=True, attachment_filename="Bylaws " + str(bylawObject.date) + ".pdf")


@permission_required('Archive.delete_bylaws', login_url='pub-permission_denied')
def delete_bylaw(request):
    """
        Deletes the bylaws with the given primary key.
    """

    if request.method == 'POST':
        bylaw_id = strip_tags(request.POST['post_id'])

        post = Bylaws.objects.get(pk=bylaw_id)

        post.filepath.delete() # Delete actual file
        post.delete()
    return redirect('archive-bylaws')


@permission_required('Archive.access_houserules', login_url='pub-permission_denied')
def rules(request):
    """
        View for all house rules
    """
    form = HouseRulesForm()

    # If its a POST, we're trying to update the rules.
    if request.method == 'POST':
        # Check permissions before going forward
        if request.user.has_perm('Archive.add_houserules'):
            form = HouseRulesForm(request.POST, request.FILES)

            if form.is_valid():
                rule = form.save(commit=False)
                rule.date = datetime.now()
                rule.save()
        else:
            redirect('pub-permission_denied')

    rules = HouseRules.objects.all()
    if rules:
        latest = rules.latest('date')
    else:
        latest = None

    context = {
        'latest': latest,
        'rules': rules,
        'form': form
        }

    return render(request, 'archive/rules.html', context)


@permission_required('Archive.access_houserules', login_url='pub-permission_denied')
def download_rules(request, rules):
    """
        View for downloading rules
    """

    houseRuleObject = HouseRules.objects.get(pk=rules)

    return sendfile(request, houseRuleObject.filepath.path, attachment=True, attachment_filename="House Rules " + str(houseRuleObject.date) + ".pdf")


@permission_required('Archive.delete_houserules', login_url='pub-permission_denied')
def delete_rules(request):
    """
        Deletes the rules with the given primary key.
    """

    if request.method == 'POST':
        rules_id = strip_tags(request.POST['post_id'])

        post = HouseRules.objects.get(pk=rules_id)

        post.filepath.delete() # Delete actual file

        post.delete()
    return redirect('archive-rules')

@permission_required('Archive.access_guide', login_url='pub-permission_denied')
def guides(request):
    """
        View for all guides
    """

    form = GuideForm()

    # If its a POST we're trying to create a guide.
    if request.method == 'POST':
        # Check if user has permission to do so first.
        if request.user.has_perm('Archive.add_guide'):
            form = GuideForm(request.POST, request.FILES)

            if form.is_valid():
                guide = form.save(commit=False)
                guide.path = slugify(guide.name)[:14]
                guide.datePosted = datetime.now()
                guide.save()
                form = GuideForm()
        else:
            redirect('pub-permission_denied')

    guides = Guide.objects.all()
    context = {
        'guides': guides,
        'form': form,
        }

    return render(request, 'archive/guides.html', context)


@permission_required('Archive.access_guide', login_url='pub-permission_denied')
def download_guides(request, guides):
    """
        View for downloading guides
    """

    guideObject = Guide.objects.get(pk=guides)

    return sendfile(request, guideObject.filepath.path, attachment=True, attachment_filename=guideObject.name + ".pdf")


@permission_required('Archive.delete_guide', login_url='pub-permission_denied')
def delete_guide(request):
    """
        Deletes the guide with the given primary key.
    """

    if request.method == 'POST':
        guide_id = strip_tags(request.POST['post_id'])

        post = Guide.objects.get(pk=guide_id)

        post.filepath.delete() # Delete actual file

        post.delete()
    return redirect('archive-guides')
