from django.db import models

# Create your models here.

from django.db.models import F
from django.urls import reverse
from django.contrib.auth.models import User

#import der Choices damit die überall verwendbar sind
from .choices import *

#Ende der Imports
########################################################################################################################

class professor(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    prof_pk_professorennummer = models.AutoField(primary_key=True, null=False, unique=True)

    #Atrribute:
    prof_name = models.CharField(max_length=128, null=True, help_text='Name des Professors')
    prof_passwort = models.CharField(max_length=128, null=True)

    #Funktionen
    def __str__(self):
        ret = str(" Name: ") + str(self.prof_name) + str(" ID: ") + str(self.prof_pk_professorennummer)
        return ret

class projekt(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    pro_pk_projektid = models.AutoField(primary_key=True, null=False, unique=True)
    pro_fk_professorennummer = models.ForeignKey('professor', on_delete=models.SET_NULL, null=True, blank=True)

    #Atrribute:
    pro_name = models.CharField(max_length=128, null=True)

    #Funktionen
    def __str__(self):
        return self.pro_name


class student(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    stud_pk_matrikelnummer = models.AutoField(primary_key=True, null=False, unique=True)
    stud_fk_gruppennummer = models.ForeignKey('projekt', on_delete=models.SET_NULL, null=True, blank=True)

    #Atrribute:
    stud_name = models.CharField(max_length=128, null=True)
    stud_passwort = models.CharField(max_length=128, null=True)

    #Funktionen:
    def __str__(self):
        return self.Name

    def display_project(self):
        return (projekt.objects.get(student__stud_fk_gruppennummer=self.stud_fk_gruppennummer))
    display_project.short_description = 'ProjektName'

###
#neue Klasse die den User erweitern soll
###
from django.contrib.auth.models import User

class user_erweitern(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gruppennummer = models.CharField(max_length=1, choices=GRUPPEN, blank=True)
    rolle = models.CharField(max_length=1, choices=ROLLEN, blank=True)

#Ende der organisatorischen Klassen
########################################################################################################################

class requirement(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    req_pk_requirementid = models.AutoField(primary_key=True, null=False, unique=True)
    req_fk_projektid = models.ForeignKey('projekt', on_delete=models.SET_NULL, null=True, blank=True)
    req_fk_ersteller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    #Atrribute:
    req_name = models.CharField(max_length=128, null=True)
    req_kommentar = models.CharField(max_length=128, null=True)
    req_datum_erstellung = models.DateTimeField(auto_now_add=True)
    req_datum_aenderung = models.DateTimeField(auto_now=True)
    req_beschreibung = models.CharField(max_length=128, null=True)

    req_kategorie = models.CharField(max_length=1, choices=KATEGORIEN, blank=True, help_text='Kategorie des Requirements')

    #Funktionen:
    def __str__(self):
        return "r_" + str(self.req_pk_requirementid) + ": " + str(self.req_name)

    def get_id(self):
        return "r_" + str(self.req_pk_requirementid)

    def get_absolute_url(self):
        return reverse('aut:requirement_change', args=[str(self.req_pk_requirementid)])

    #Metaoptionen
    class Meta:
        ordering = ["req_pk_requirementid"]

class testcase(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    testc_pk_testcaseid = models.AutoField(primary_key=True, null=False, unique=True)
    testc_fk_projektid = models.ForeignKey('projekt', on_delete=models.SET_NULL, null=True, blank=True)
    testc_fk_ersteller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    testc_fk_requirement = models.ManyToManyField(requirement, blank=True)

    #Atrribute:
    testc_name = models.CharField(max_length=128, null=True)
    testc_kommentar = models.CharField(max_length=128, null=True)
    testc_datum_erstellung = models.DateTimeField(auto_now_add=True)
    testc_datum_aenderung = models.DateTimeField(auto_now=True)
    testc_beschreibung = models.CharField(max_length=128, null=True)

    testc_vorbedingung = models.CharField(max_length=128, null=True)

    #Funktionen:
    def __str__(self):
        return "tc_" + str(self.testc_pk_testcaseid) + ": " + str(self.testc_name)

    def get_id(self):
        return "tc_" + str(self.testc_pk_testcaseid)

    def get_absolute_url(self):
        return reverse('aut:testcase_change', args=[str(self.testc_pk_testcaseid)])

    #Metaoptionen
    class Meta:
        ordering = ["testc_pk_testcaseid"]

class testcase_schritt(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    schritt_pk_id = models.AutoField(primary_key=True, null=False, unique=True)
    schritt_fk_testcase = models.ForeignKey('testcase', on_delete=models.SET_NULL, null=True, blank=True)

    #Atrribute:
    schritt_schritte = models.CharField(max_length=128, null=True, blank=True)
    schritt_erwartetesergebnis = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return "ID: " + str(self.schritt_pk_id) + "Schritt: " + str(self.schritt_schritte)

class testrun_schritt(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    schritt_pk_id = models.AutoField(primary_key=True, null=False, unique=True)
    schritt_fk_testrun = models.ForeignKey('testrun', on_delete=models.SET_NULL, null=True, blank=True)
    schritt_fk_testcase_schritt = models.ForeignKey('testcase_schritt', on_delete=models.SET_NULL, null=True, blank=True)

    #Atrribute:
    #zum Kopieren der TestCase Schritte
    schritt_schritte = models.CharField(max_length=128, null=True, blank=True)
    schritt_erwartetesergebnis = models.CharField(max_length=128, null=True, blank=True)

    schritt_tatsaechlichesergebnis = models.CharField(max_length=128, null=True, blank=True)
    schritt_ergebnis = models.CharField(max_length=1, choices=RUN_STATUS, default=RUN_STATUS[0])

    def __str__(self):
        return "ID: " + str(self.schritt_pk_id)

class testrun(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    testr_pk_testrunid = models.AutoField(primary_key=True, null=False, unique=True)
    testr_fk_projektid = models.ForeignKey('projekt', on_delete=models.SET_NULL, null=True, blank=True)
    testr_fk_ersteller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    testr_fk_testcaseid = models.ForeignKey('testcase', on_delete=models.SET_NULL, null=True, blank=True)

    #Atrribute:
    testr_name = models.CharField(max_length=128, null=True)
    testr_kommentar = models.CharField(max_length=128, null=True)
    testr_datum_erstellung = models.DateTimeField(auto_now_add=True)
    testr_datum_aenderung = models.DateTimeField(auto_now=True)
    testr_beschreibung = models.CharField(max_length=128, null=True)
    testr_testc_datum = models.DateTimeField(blank=True, null=True)

    testr_status = models.CharField(max_length=1, choices=RUN_STATUS, blank=True, help_text='TestRun Ergebnis')
    testr_dauer = models.CharField(null=True, blank=True, max_length=100)
    testr_datum_durchführung = models.DateTimeField(auto_now_add=True) # Wird beim Erstellen geschrieben, macht Sinn da man danach nicht mehr verändert

    #Funktionen:
    def __str__(self):
        return "tr_" + str(self.testr_pk_testrunid) + ": " + str(self.testr_name)

    def get_id(self):
        return "tr_" + str(self.testr_pk_testrunid)

    def get_absolute_url(self):
        return reverse('aut:testrun_change', args=[str(self.testr_pk_testrunid)])

    def get_run_absolute_url(self):
        return reverse('aut:testrun_run', args=[str(self.testr_pk_testrunid)])

    #Metaoptionen
    class Meta:
        ordering = ["testr_pk_testrunid"]

#Ende der Elemente-Klassen
########################################################################################################################

class note(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    note_fk_ersteller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    notes = models.CharField(max_length=128, null=True)