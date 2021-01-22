from django import template
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from ..models import testrun

register = template.Library()

#{{ testcase|passed_runs }}
@register.filter(name='passed_runs')
def passed_runs(testcase):

    liste = []
    result = ""

    for testr in testrun.objects.filter(testr_fk_testcaseid=testcase):
        if testr.testr_status == 'p':
            print("Testrun" + str(testr))
            liste.append(testr)
            result = 'erfolgreicher testrun zu case'

    return result


@register.filter(name='passed_runs_2')
def passed_runs_2(testcase):
    result = ""
    if testcase.testrun_set.all().exists():
        if testcase.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'n':
            result = '<p style="color: blue;">X</p>'
        if testcase.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'f':
            result = '<p style="color: red;">X</p>'
        if testcase.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'p':
            result = '<p style="color: green;">X</p>'
    return mark_safe(result)

@register.filter(name='color_tc')
def color_tc(testcase):
    result = 'style="color: #FFC72C;"'
    if testcase.testc_fk_requirement.all().exists():
        result = ""

    return mark_safe(result)

@register.filter(name='color_req')
def color_req(requirement):
    result = 'style="color: red;"'
    if requirement.testcase_set.all().exists():
        result = 'style="color: green;"'

    return mark_safe(result)

@register.filter(name='color_req_run')
def color_req(requirement):
    testrun_list = []
    result = 'style="color: green;"'
    if requirement.testcase_set.all().exists():
        for req in requirement.testcase_set.all():

            if req.testrun_set.all().exists():
                #das Append ist nur dafür da um überhaupt zu gucken ob es TestRuns gibt
                testrun_list.append(req.testrun_set.all().latest('testr_datum_aenderung'))

                if req.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'f':
                    result = 'style="color: red;"'
                elif req.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'n':
                    result = 'style="color: red;"'

    else: #Wenn es keine TestCases gibt
        result = 'style="color: red;"'
    if testrun_list == []:#Wenn es keine TestRuns gibt für ein ganzes Requirement
        result = 'style="color: red;"'

    return mark_safe(result)


@register.filter(name='requirement_color')
def requirement_color(requirement):
    result = ' style=" background: linear-gradient(to right, white 0%, white 80%, #FF0000 100%);"'
    if requirement.testcase_set.all().exists():
        result = ' style=" background: linear-gradient(to right, white 0%, white 80%, #00ff00 100%);"'
    return mark_safe(result)

#müssen noch getestet werden
@register.filter(name='testcase_color')
def testcase_color(testcase):
    result = ' style=" background: linear-gradient(to right, white 0%, white 80%, #FF0000 100%);"'
    if testcase.testrun_set.all().exists() and testcase.testc_fk_requirement.exists():
        if testcase.testrun_set.all().latest('testr_datum_aenderung').testr_status == 'p':
            result = ' style=" background: linear-gradient(to right, white 0%, white 80%, #00ff00 100%);"'
    return mark_safe(result)

@register.filter(name='testrun_color')
def testrun_color(testrun):
    result = ' style=" background: linear-gradient(to right, white 0%, white 80%, #FF0000 100%);"'
    if testrun.testr_fk_testcaseid and testrun.testr_status == 'p':
        result = ' style=" background: linear-gradient(to right, white 0%, white 80%, #00ff00 100%);"'
    if testrun.testr_fk_testcaseid and testrun.testr_status == 'n':
        result = ' style=" background: linear-gradient(to right, white 0%, white 80%, #0000ff 100%);"'

    #wenn der TestRun durchgefallen ist wird er orange markiert
    if testrun.testr_fk_testcaseid and testrun.testr_status == 'f':
        result = ' style=" background: linear-gradient(to right, white 0%, white 80%, orange 100%);"'

    return mark_safe(result)


#Timer
@register.filter(name='testrun_time')
def testrun_time(testrun, time):
    testrun.testr_dauer = time


#Rote Markierung
@register.filter(name='rote_markierung')
def rote_markierung(element):
    if int(element) > 0:
        return mark_safe('style="background: orange;"')

@register.filter(name='zip')
def zip_lists(a, b):
    print(b)
    return zip(a, b)