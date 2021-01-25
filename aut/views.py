import os
import time
from io import StringIO, BytesIO
from xml.dom.minidom import Document
import os
from pathlib import Path
from PIL import Image
from django import forms
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import render, redirect
import datetime
# Create your views here.

from django.http import HttpResponse, HttpResponsePermanentRedirect

from django.contrib.auth.decorators import login_required

# restrict access to logged in users with an check if he is authenticated
# see django docs
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

from .models import requirement, testcase, testrun, testcase_schritt, note, testrun_schritt, user_erweitern

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .forms import RequirementForm, TestCaseForm, TestRunForm, TestCase_Schritt_Form, TestCase_Schritt_Form2, GroupForm, \
    Note_Form, SignUpForm
from .choices import *
from django.shortcuts import render

# relative import of forms
from .forms import TestCase_Schritte_Form

# importing formset_factory
from django.forms import modelformset_factory, inlineformset_factory
from django.db.models import Avg, Max, Min

#Ende der Imports
########################################################################################################################

@login_required()
def view_dashboard(request):
    #Variable, um Fehler anzuzeigen, die man noch beheben sollte vor dem Erzeugen der PDF.
    check_for_errors = []

    #eingeloggten User und seine Gruppennummer erhalten
    #danach alle User mit derselben Gruppennummer speichern
    user = User.objects.get(username=request.user.username)
    user_gruppennummer = user.user_erweitern.gruppennummer
    all_users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')

    #Code um die Elemente der eigenen Gruppe zu bekommen
    #users ist wie all_users und wird zur Sicherheit bei allen ELementen definiert
    #Requirements
    ########################################################################################################################
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    req_for_usergroup = requirement.objects.filter(req_fk_ersteller__in=users)
    num_req = req_for_usergroup.count()

    #eigene Anzahl an Requirements
    num_req_eigene = req_for_usergroup.filter(req_fk_ersteller=request.user)
    num_req_eigene = num_req_eigene.count()

    #abgedeckte Requirements = Requiremtens mit TestCase
    lis_no_testcase = []
    lis_yes_testcase = []
    for req in req_for_usergroup:
        if req.testcase_set.all().exists():
            #wenn es mindestens 1 TestCase gibt
            lis_yes_testcase.append(req)
        else:
            #wenn es keinen TestCase gibt
            lis_no_testcase.append(req)

    num_yes_testcase = len(lis_yes_testcase)
    num_no_testcase = len(lis_no_testcase)

    if int(num_no_testcase) > 0:
        check_for_errors.append("Es gibt noch Requirements ohne TestCases!")

    #TestCases
    ########################################################################################################################
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    testc_for_usergroup = testcase.objects.filter(testc_fk_ersteller__in=users)
    num_testc = testc_for_usergroup.count()

    #eigene Anzahl an TestCases
    num_testc_eigene = testc_for_usergroup.filter(testc_fk_ersteller=request.user)
    num_testc_eigene = num_testc_eigene.count()

    #abgedeckte TestCases = TestCases mit TestRuns
    lis_no_testrun_or_no_run = [] #enthält TestCases ohne TestRun
    lis_yes_testrun_run_failed = []
    lis_yes_testrun_run_passed = []

    for testc in testc_for_usergroup:
        if testc.testrun_set.all().exists():
            #bei beiden Fällen wird der letzte Run überprüft
            if testc.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'f': #failed
                lis_yes_testrun_run_failed.append(testc)
            elif testc.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'p': #passed
                lis_yes_testrun_run_passed.append(testc)
        else: #wenn es kein TestRun gibt
            lis_no_testrun_or_no_run.append(testc)

    num_lis_no_testrun_or_no_run = len(lis_no_testrun_or_no_run)
    num_lis_yes_testrun_run_failed = len(lis_yes_testrun_run_failed)
    num_lis_yes_testrun_run_passed = len(lis_yes_testrun_run_passed)

    if int(num_lis_no_testrun_or_no_run) > 0:
        check_for_errors.append("Es gibt noch TestCases ohne TestRuns!")

    if int(num_lis_yes_testrun_run_failed) > 0:
        check_for_errors.append("Es gibt noch TestCases mit failed TestRuns!")

    #TestRuns
    ########################################################################################################################
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    testr_for_usergroup = testrun.objects.filter(testr_fk_ersteller__in=users)
    num_testr = testr_for_usergroup.count()

    #eigene Anzahl an TestRuns
    num_testr_eigene = testr_for_usergroup.filter(testr_fk_ersteller=request.user)
    num_testr_eigene = num_testr_eigene.count()

    num_lis_no_testrun = testr_for_usergroup.filter(testr_status='n')
    num_lis_failed_testrun = testr_for_usergroup.filter(testr_status='f')
    num_lis_passed_testrun = testr_for_usergroup.filter(testr_status='p')

    num_lis_no_testrun = len(num_lis_no_testrun)
    num_lis_failed_testrun = len(num_lis_failed_testrun)
    num_lis_passed_testrun = len(num_lis_passed_testrun)

    if int(num_lis_no_testrun) > 0:
        check_for_errors.append("Es gibt noch TestRuns ohne Runs!")

    #der Professor hat noch ein Form mit dem die Gruppennummer geändert werden kann
    if request.user.user_erweitern.rolle == 'p':
        #Professor Seite
        if request.method == 'POST':
            form = GroupForm(request.POST)
            if form.is_valid():
                user.user_erweitern.gruppennummer = form.cleaned_data['group_form_group']
                user.user_erweitern.save()

                return HttpResponseRedirect(reverse('aut:view_dashboard'))
        else:
            form = GroupForm(initial={'group_form_group': user.user_erweitern.gruppennummer,
                                      })
        #Context übergeben mit dem Form
        context = {
            'user_gruppennummer': user_gruppennummer,
            'all_users': all_users,

            'num_req': num_req,
            'num_req_eigene': num_req_eigene,
            'num_yes_testcase': num_yes_testcase,
            'num_no_testcase': num_no_testcase,

            'num_testc': num_testc,
            'num_testc_eigene': num_testc_eigene,
            'num_lis_no_testrun_or_no_run': num_lis_no_testrun_or_no_run,
            'num_lis_yes_testrun_run_failed': num_lis_yes_testrun_run_failed,
            'num_lis_yes_testrun_run_passed': num_lis_yes_testrun_run_passed,

            'num_testr': num_testr,
            'num_testr_eigene': num_testr_eigene,
            'num_lis_no_testrun': num_lis_no_testrun,
            'num_lis_failed_testrun': num_lis_failed_testrun,
            'num_lis_passed_testrun': num_lis_passed_testrun,

            'check_for_errors': check_for_errors,

            'form': form,
        }
        return render(request, 'aut/010_dashboard.html', context=context)

    #Context ohne Form, da der Student das nicht hat
    context = {
        'user_gruppennummer': user_gruppennummer,
        'all_users': all_users,

        'num_req': num_req,
        'num_req_eigene': num_req_eigene,
        'num_yes_testcase': num_yes_testcase,
        'num_no_testcase': num_no_testcase,

        'num_testc': num_testc,
        'num_testc_eigene': num_testc_eigene,
        'num_lis_no_testrun_or_no_run': num_lis_no_testrun_or_no_run,
        'num_lis_yes_testrun_run_failed': num_lis_yes_testrun_run_failed,
        'num_lis_yes_testrun_run_passed': num_lis_yes_testrun_run_passed,

        'num_testr': num_testr,
        'num_testr_eigene': num_testr_eigene,
        'num_lis_no_testrun': num_lis_no_testrun,
        'num_lis_failed_testrun': num_lis_failed_testrun,
        'num_lis_passed_testrun': num_lis_passed_testrun,

        'check_for_errors': check_for_errors,
    }
    return render(request, 'aut/010_dashboard.html', context=context)

#Ende des Dashboards
########################################################################################################################

def view_requirement(request):
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    req_for_usergroup = requirement.objects.filter(req_fk_ersteller__in=users).order_by('-req_pk_requirementid')

    context = {
        'requirements': req_for_usergroup,
    }
    return render(request, 'aut/010_requirement.html', context=context)
########################################################################################################################

def edit_requirement(request, pk=None):
    #das aktuelle Requirement
    requ_instance, created = requirement.objects.get_or_create(req_pk_requirementid=pk)
    if created == True:
        requ_instance.req_fk_ersteller = request.user
        requ_instance.save()

    #Alle TestCases zum Auswählen
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    testc_for_usergroup = testcase.objects.filter(testc_fk_ersteller__in=users)

    if request.method == 'POST':
        form = RequirementForm(request.POST,tecs=testc_for_usergroup)

        if request.POST.get("delete_requirement"):
            name = "ID:" + str(requ_instance.req_pk_requirementid) + " Name: " + str(requ_instance.req_name)
            requ_instance.delete()
            return HttpResponse(name + " wurde gelöscht")

        if form.is_valid():
            requ_instance.req_kommentar = form.cleaned_data['req_form_kommentar']
            requ_instance.req_name = form.cleaned_data['req_form_name']
            requ_instance.req_beschreibung = form.cleaned_data['req_form_beschreibung']

            #Für alle TestCases das jetzige Requirement speichern als Foreign Key
            #das hier ist die andere Seite der Many-to-Many Relationship
            a = form.cleaned_data['req_form_fk_testcase']
            if a:
                for b in a:
                    b.testc_fk_requirement.add(requ_instance)
            else:
                users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
                testc_for_usergroup = testcase.objects.filter(testc_fk_ersteller__in=users)
                for b in testc_for_usergroup:
                    b.testc_fk_requirement.remove(requ_instance)


            requ_instance.save()
            return HttpResponseRedirect(reverse('aut:requirement_change', kwargs={'pk': pk}))
    else:
      form = RequirementForm(initial={'req_form_kommentar': requ_instance.req_kommentar,
                                      'req_form_name': requ_instance.req_name,
                                      'req_form_beschreibung': requ_instance.req_beschreibung,
      'req_form_fk_testcase': requ_instance.testcase_set.all(),

      }, tecs = testc_for_usergroup)

    context = {
        'form': form,
        'requ_instance': requ_instance,
    }

    return render(request, 'aut/020_requirement_anpassen.html', context)
#Ende der Requirements
########################################################################################################################

def view_testcase(request):
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    testc_for_usergroup = testcase.objects.filter(testc_fk_ersteller__in=users).order_by('-testc_pk_testcaseid')

    context = {
        'testcases': testc_for_usergroup,
    }
    return render(request, 'aut/010_testcase.html', context=context)
########################################################################################################################

def edit_testcase(request, pk=None):
    testc_instance, created = testcase.objects.get_or_create(testc_pk_testcaseid=pk)
    if created == True:
        testc_instance.testc_fk_ersteller = request.user
        testc_instance.save()

    #oder einfach testcase instance
    tc = testcase.objects.get(testc_pk_testcaseid=testc_instance.testc_pk_testcaseid)

    TestCase_Schritt_FormSet = inlineformset_factory(testcase, testcase_schritt,
                                                     fields=('schritt_schritte', 'schritt_erwartetesergebnis'),
                                                     can_delete=True, extra=1)


    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    req_for_usergroup = requirement.objects.filter(req_fk_ersteller__in=users)

    #Die TestCases sollen die zugehörigen TestRuns anzeigen können
    #alle TestRuns außer die, die noch nicht liefen
    testruns = testc_instance.testrun_set.exclude(testr_status='n')

    if request.method == 'POST':
        if request.POST.get("delete_testcase"):
            name = "ID:" + str(testc_instance.testc_pk_testcaseid) + " Name: " + str(testc_instance.testc_name)
            testc_instance.delete()
            return HttpResponse(name + " wurde gelöscht")

        form = TestCaseForm(request.POST, reqs=req_for_usergroup)
        schritt_form = TestCase_Schritt_Form(request.POST) #das kann weg
        formset = TestCase_Schritt_FormSet(request.POST, instance=tc)

        if formset.is_valid():
            formset.save()


        if form.is_valid():
            testc_instance.testc_vorbedingung = form.cleaned_data['testc_form_vorbedingung']
            testc_instance.testc_kommentar = form.cleaned_data['testc_form_kommentar']
            testc_instance.testc_name = form.cleaned_data['testc_form_name']
            testc_instance.testc_beschreibung = form.cleaned_data['testc_form_beschreibung']
            testc_instance.testc_fk_requirement.set(form.cleaned_data['testc_form_fk_requirement'])

            testc_instance.testc_fk_ersteller = request.user

            testc_instance.save()

        return HttpResponseRedirect(reverse('aut:testcase_change', kwargs={'pk': testc_instance.testc_pk_testcaseid}))
    else:

        formset = TestCase_Schritt_FormSet(instance=tc)
        schritt_form = TestCase_Schritt_Form()
        form = TestCaseForm(initial={'testc_form_name': testc_instance.testc_name,
                                      'testc_form_beschreibung': testc_instance.testc_beschreibung,
                                      'testc_form_kommentar': testc_instance.testc_kommentar,
                                      'testc_form_vorbedingung': testc_instance.testc_vorbedingung,
                                      'testc_form_fk_requirement': requirement.objects.filter(testcase=testc_instance),

                                     }, reqs=req_for_usergroup)

    schritte_instance = testcase_schritt.objects.filter(schritt_fk_testcase=testc_instance)
    context = {
        'form': form,
        'schritt_form': schritt_form,
        'testc_instance': testc_instance,
        'schritte_instance': schritte_instance,
        'testruns': testruns,
        'formset': formset
    }

    return render(request, 'aut/020_testcase_anpassen.html', context)
#Ende der TestCases
########################################################################################################################

def view_testrun(request):
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    testr_for_usergroup = testrun.objects.filter(testr_fk_ersteller__in=users).order_by('-testr_pk_testrunid')

    context = {
        'testruns': testr_for_usergroup,
    }
    return render(request, 'aut/010_testrun.html', context=context)
########################################################################################################################

def edit_testrun(request, pk=None):
    testr_instance, created = testrun.objects.get_or_create(testr_pk_testrunid=pk)
    if created == True:
        testr_instance.testr_fk_ersteller = request.user
        testr_instance.testr_status = 'n'
        testr_instance.save()

    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    testc_for_usergroup = testcase.objects.filter(testc_fk_ersteller__in=users)
    req_for_usergroup = requirement.objects.filter(req_fk_ersteller__in=users)
    testc_with_requirement = testc_for_usergroup.filter(testc_fk_requirement__in=req_for_usergroup).distinct()
    print(testc_with_requirement)

    if request.method == 'POST':
        form = TestRunForm(request.POST,tecs=testc_with_requirement)

        if request.POST.get("delete_testrun"):
            name = "ID:" + str(testr_instance.testr_pk_testrunid) + " Name: " + str(testr_instance.testr_name)
            testr_instance.delete()
            return HttpResponse(name + " wurde gelöscht")

        if form.is_valid():
            testr_instance.testr_name = form.cleaned_data['testr_form_name']
            testr_instance.testr_kommentar = form.cleaned_data['testr_form_kommentar']
            testr_instance.testr_beschreibung = form.cleaned_data['testr_form_beschreibung']

            testr_instance.testr_fk_testcaseid = form.cleaned_data['testr_form_fk_testcase']
            testr_instance.testr_fk_ersteller = request.user
            testr_instance.save()

            if request.POST.get("save_and_testrun"):
                link = reverse('aut:testrun_run', kwargs={'pk': pk})
                html = "<script>window.top.location.href = '" + link + "' </script>"
                return HttpResponse(html)

            return HttpResponseRedirect(reverse('aut:testrun_change', kwargs={'pk': pk}))
    else:
      form = TestRunForm(initial={'testr_form_name': testr_instance.testr_name,
                                      'testr_form_kommentar': testr_instance.testr_kommentar,
                                      'testr_form_beschreibung': testr_instance.testr_beschreibung,
                                      'testr_form_status': testr_instance.testr_status,
                                    'testr_form_fk_testcase':testr_instance.testr_fk_testcaseid

                                      },tecs=testc_with_requirement)


    testc_schritte = testcase_schritt.objects.filter(schritt_fk_testcase=testr_instance.testr_fk_testcaseid)
    testr_schritte = testrun_schritt.objects.filter(schritt_fk_testrun=testr_instance).order_by('schritt_pk_id')
    for schritt in testr_schritte:
        print(schritt.schritt_schritte)

    context = {
        'form': form,
        'testr_instance': testr_instance,
        'testc_schritte':testc_schritte,
        'testr_schritte':testr_schritte

    }

    return render(request, 'aut/020_testrun_anpassen.html', context)
########################################################################################################################

def testrun_run(request, pk):
    testr_instance = get_object_or_404(testrun, testr_pk_testrunid=pk)
    if testr_instance.testr_status != 'n':
        return HttpResponse(str(testr_instance) + " wurde bereits durchgeführt")

    testc_schritte = testcase_schritt.objects.filter(schritt_fk_testcase=testr_instance.testr_fk_testcaseid)


    zeilen = testc_schritte.count()
    TestRun_Schritt_FormSet = inlineformset_factory(testrun, testrun_schritt,fields=('schritt_tatsaechlichesergebnis', 'schritt_ergebnis'),can_delete=False, widgets={'schritt_ergebnis': forms.RadioSelect(choices=RUN_STATUS)}, extra=zeilen)



    #Zeit speichern bei Abgabe
    if request.method == 'POST':
        formset = TestRun_Schritt_FormSet(request.POST, instance=testr_instance)

        if formset.is_valid():
            formset.save()
            list_mit_Ergebnissen = []
            for form in formset:
                if form.cleaned_data:
                    dran = form.cleaned_data['schritt_ergebnis']
                else:
                    dran = 'f'

                list_mit_Ergebnissen.append(dran)
                form.save()
            formset.save()
            # Generator
            if all(item == list_mit_Ergebnissen[0] == 'p' for item in list_mit_Ergebnissen):
                testr_instance.testr_status = 'p'
            else:
                testr_instance.testr_status = 'f'

        if request.POST.get("TIME"):
            testr_instance.testr_dauer = int(request.POST.get("TIME"))
            testr_instance.save()

        testc = testcase.objects.get(testc_pk_testcaseid=testr_instance.testr_fk_testcaseid.testc_pk_testcaseid)
        testr_instance.testr_testc_datum = testc.testc_datum_aenderung
        testr_instance.save()

        # hier die Zuordnung der Schritte?
        testr_schritte = testrun_schritt.objects.filter(schritt_fk_testrun=testr_instance)
        testc_schritte = testc_schritte.order_by('schritt_pk_id')

        aktueller_testc = testc_schritte.first()

        #next Operator für Arme von Reddit
        for schritt in testr_schritte:
            schritt.schritt_schritte = aktueller_testc.schritt_schritte
            schritt.schritt_erwartetesergebnis = aktueller_testc.schritt_erwartetesergebnis

            schritt.schritt_fk_testcase_schritt = aktueller_testc
            schritt.save()
            aktueller_testc = testc_schritte.filter(schritt_pk_id__gt=aktueller_testc.schritt_pk_id).order_by(        'schritt_pk_id').first()

        #pass
        #testr_schritte = testrun_schritt.objects.filter(schritt_fk_testrun=testr_instance)
        #for schritt in testc_schritte:
        #    schritt.schritt_schritte = testcase schritt.get(foreign kes vom testr schritt) . die Sache
        #    schritt.schritt_fk_testcase_schritt
        #    noch die Zuordnung vob den Teytschritten zuerienander
        #
        #testr_schritte.schritt_schritte = testc_schritte.schritt_schritte
        #testr_schritte.schritt_erwartetesergebnis = testc_schritte.schritt_erwartetesergebnis
        #testr_schritte.save()
        #print(testr_schritte)
        #pass



        return HttpResponseRedirect(reverse('aut:view_testrun'))
        #return HttpResponseRedirect(reverse('aut:testrun_change', kwargs={'pk': pk}))


    else:
        formset = TestRun_Schritt_FormSet(instance=testr_instance, )

        if testr_instance.testrun_schritt_set.exists:
            testr_schritte = testrun_schritt.objects.filter(schritt_fk_testrun=testr_instance)
            print(testr_schritte)
            liste_mit_dictios = []
            for schritt in testr_schritte:
                dictio = {}
                dictio['schritt_tatsaechlichesergebnis'] = schritt.schritt_tatsaechlichesergebnis
                dictio['schritt_ergebnis'] = schritt.schritt_ergebnis
                liste_mit_dictios.append(dictio)

            print(liste_mit_dictios)

        formset.initial = liste_mit_dictios

    context = {
        'testr_instance': testr_instance,
        'testc_schritte': testc_schritte,
        'formset': formset

    }

    return render(request, 'aut/020_testrun_run.html', context)
#Ende der TestRuns
########################################################################################################################

def view_statistik(request):
    #TestCase Coverage: Requriements mit TestCase / alle Requirements
    #Für die Gruppe die Requirements
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    req_for_usergroup = requirement.objects.filter(req_fk_ersteller__in=users)

    int_req_with_testcase = 0
    for req in req_for_usergroup:
        if req.testcase_set.all().exists():
            int_req_with_testcase += 1
    num_req = req_for_usergroup.count()
    if num_req != 0:
        TestCase_Coverage = int_req_with_testcase/num_req * 100 #Für Prozent
    elif num_req == 0:
        TestCase_Coverage = 0

    #TestRun Coverage: Requirement mit erfolgreichem TestRun / alle Requirements
    #Für die Gruppe die Requirements
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    req_for_usergroup = requirement.objects.filter(req_fk_ersteller__in=users)

    int_req_with_testrun = 0
    for req in req_for_usergroup:
        all_passed = True
        if req.testcase_set.all().exists(): #pro Req die TestCases TEST
            for testc in req.testcase_set.all(): #pro Req die TestCases
                if testc.testrun_set.all().exists():
                    if testc.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'f' or testc.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'n':
                        all_passed = False
        else:
            all_passed = False

        if all_passed == True:
            int_req_with_testrun += 1

    num_req = req_for_usergroup.count()
    if num_req != 0:
        TestRun_Coverage = int_req_with_testrun/num_req * 100 #Für Prozent
    elif num_req == 0:
        TestRun_Coverage = 0

    #Alle ELemente für eine Gruppe an Studenten
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')
    req_for_usergroup = requirement.objects.filter(req_fk_ersteller__in=users)
    testc_for_usergroup = testcase.objects.filter(testc_fk_ersteller__in=users)
    testr_for_usergroup = testrun.objects.filter(testr_fk_ersteller__in=users)

    #Projektstatisitk über Studenten der gleichen Gruppe:
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')

    #Zeiten der Testruns:
    min_testrun = testrun.objects.all().aggregate(Min('testr_dauer'))
    max_testrun = testrun.objects.all().aggregate(Max('testr_dauer'))
    durchschnitt_testrun = testrun.objects.all().aggregate(Avg('testr_dauer'))

    #Usergruppe:
    usergruppe = request.user.user_erweitern.gruppennummer


    context = {
        'all_requirements': req_for_usergroup,
        'all_testcases': testc_for_usergroup,
        'all_testruns': testr_for_usergroup,
        'TestCase_Coverage': TestCase_Coverage,
        'TestRun_Coverage': TestRun_Coverage,
        'users': users,
        'min_testrun': min_testrun,
        'max_testrun': max_testrun,
        'durchschnitt_testrun': durchschnitt_testrun,
        'usergruppe': usergruppe
    }

    return render(request, 'aut/010_statistik.html', context)


def req_desc(request):
    return render(request, 'aut/040_req_desc.html')
def testc_desc(request):
    return render(request, 'aut/040_testc_desc.html')
def testr_desc(request):
    return render(request, 'aut/040_testr_desc.html')

#Für die TestCases die Schritte
def formset_view(request, id):
    tc = testcase.objects.get(testc_pk_testcaseid=id)

    # creating a formset
    TestCase_Schritt_FormSet = inlineformset_factory(testcase, testcase_schritt, fields=('schritt_schritte', 'schritt_erwartetesergebnis'), can_delete=True, extra=1)

    if request.method == 'POST':
        formset = TestCase_Schritt_FormSet(request.POST, instance=tc)
        if formset.is_valid():
            formset.save()
            return redirect('aut:schritte', id=tc.testc_pk_testcaseid)

    formset = TestCase_Schritt_FormSet(instance=tc)
    return render(request, "aut/home.html", {'formset': formset})

#Für die TestRuns die Schritte
def formset_view_run(request, id):
    tc = testcase.objects.get(testc_pk_testcaseid=id)

    # creating a formset
    TestCase_Schritt_FormSet = inlineformset_factory(testcase, testrun_schritt, fields=('schritt_tatsaechlichesergebnis', 'schritt_ergebnis'), can_delete=False, extra=0)

    if request.method == 'POST':
        formset = TestCase_Schritt_FormSet(request.POST, instance=tc)
        if formset.is_valid():
            formset.save()
            return redirect('aut:schritte_run', id=tc.testc_pk_testcaseid)

    formset = TestCase_Schritt_FormSet(instance=tc)
    return render(request, "aut/schritte_run.html", {'formset': formset})


#NotePad als Spielerei
def form_note(request):
    #get über den foreign key vom usre, wenn der schon eins hat dann ok, wenn nciht machent
    note_instance, created = note.objects.get_or_create(note_fk_ersteller=request.user)

    if request.method == 'POST':
        form = Note_Form(request.POST)

        if form.is_valid():
            note_instance.notes = form.cleaned_data['note_form']
            note_instance.save()
            return HttpResponseRedirect(reverse('aut:notepad'))
    else:
      form = Note_Form(initial={'note_form': note_instance.notes,})

    context = {
        'form': form,
        'note_instance': note_instance
    }

    return render(request, 'aut/030_special_notepad_inner.html', context)


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def TestDocument(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Times-Roman", 12)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    users = User.objects.filter(user_erweitern__gruppennummer=request.user.user_erweitern.gruppennummer).filter(user_erweitern__rolle='s')

    text = p.beginText(1 * cm, 29* cm)
    text.setFont("Times-Roman", 12)
    text.textLine("Gruppe: " + str(request.user.user_erweitern.gruppennummer))
    text.textLine("Gruppenmitglieder")

    for user in users:
        text.textLine(str(user))

    p.drawText(text)
    # ###################################
    # 3) Draw a line
    p.line(0* cm, 25 * cm, 30*cm, 25 * cm)



    # ###################################
    # 5) Draw a image


    #cwd = os.getcwd()  # Get the current working directory (cwd)
    #im = Image.open(Path(cwd + '/anforderungenundtesten/aut/logo.png' ))
    #p.drawInlineImage(im, 14 * cm, 25.5* cm)

    text = p.beginText(1*cm, 24*cm)
    text.setFont("Times-Roman", 12)
    text.textLine("Requirements:")
    p.drawText(text)



    text = p.beginText(1 * cm, 23 * cm)
    text.setFont("Times-Roman", 12)
    i = 0 #nur 4 Elemente auf 1 Seite
    req_for_usergroup = requirement.objects.filter(req_fk_ersteller__in=users)
    for req in req_for_usergroup:

        text.textLine(str(req))
        text.textLine("Ersteller: " + str(req.req_fk_ersteller))
        text.textLine("Erstelldatum: " + str(req.req_datum_erstellung))
        text.textLine("Änderungsdatum: " + str(req.req_datum_aenderung))
        text.textLine("Beschreibung: " + str(req.req_beschreibung))
        text.textLine("Kommentar: " + str(req.req_kommentar))
        text.textLine("Kategorie: " + str(req.req_kategorie))
        text.textLine("")
        i = i + 1
        if i > 3:
            p.drawText(text)
            p.showPage() #neue Seite
            text = p.beginText(1 * cm, 23 * cm)
            text.setFont("Times-Roman", 12)
            i = 0
    p.drawText(text)
    p.showPage()

    text = p.beginText(1*cm, 24*cm)
    text.setFont("Times-Roman", 12)
    text.textLine("TestCases:")
    p.drawText(text)

    text = p.beginText(1 * cm, 23 * cm)
    text.setFont("Times-Roman", 12)
    i = 0  # nur 4 Elemente auf 1 Seite
    testc_for_usergroup = testcase.objects.filter(testc_fk_ersteller__in=users)
    for testc in testc_for_usergroup:

        text.textLine(str(testc))
        text.textLine("Ersteller: " + str(testc.testc_fk_ersteller))
        text.textLine("Erstelldatum: " + str(testc.testc_datum_erstellung))
        text.textLine("Änderungsdatum: " + str(testc.testc_datum_aenderung))
        text.textLine("Beschreibung: " + str(testc.testc_beschreibung))
        text.textLine("Kommentar: " + str(testc.testc_kommentar))
        text.textLine("")
        i = i + 1
        if i > 3:
            p.drawText(text)
            p.showPage()  # neue Seite
            text = p.beginText(1 * cm, 23 * cm)
            text.setFont("Times-Roman", 12)
            i = 0
    p.drawText(text)
    p.showPage()


    text = p.beginText(1 * cm, 24 * cm)
    text.setFont("Times-Roman", 12)
    text.textLine("TestRuns:")
    p.drawText(text)

    text = p.beginText(1 * cm, 23 * cm)
    text.setFont("Times-Roman", 12)
    i = 0  # nur 4 Elemente auf 1 Seite
    testr_for_usergroup = testrun.objects.filter(testr_fk_ersteller__in=users)
    for testr in testr_for_usergroup:

        text.textLine(str(testc))
        text.textLine("Ersteller: " + str(testr.testr_fk_ersteller))
        text.textLine("Erstelldatum: " + str(testr.testr_datum_erstellung))
        text.textLine("Änderungsdatum: " + str(testr.testr_datum_aenderung))
        text.textLine("Beschreibung: " + str(testr.testr_beschreibung))
        text.textLine("Kommentar: " + str(testr.testr_kommentar))
        text.textLine("")
        i = i + 1
        if i > 3:
            p.drawText(text)
            p.showPage()  # neue Seite
            text = p.beginText(1 * cm, 23 * cm)
            text.setFont("Times-Roman", 12)
            i = 0
    p.drawText(text)


    # Close the PDF object cleanly, and we're done.
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    return response


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user_instance_erweitern, created = user_erweitern.objects.get_or_create(user=user)
            user_instance_erweitern.gruppennummer = form.data.get('gruppennummer')
            user_instance_erweitern.rolle = 's'
            user_instance_erweitern.save()
            login(request, user)
            return HttpResponseRedirect(reverse('aut:view_dashboard'))


    else:
        form = SignUpForm()
    return render(request, 'aut/signup.html', {'form': form})



def easteregg(request):
    return redirect('https://www.youtube.com/watch?v=DLzxrzFCyOs&ab_channel=AllKindsOfStuff')