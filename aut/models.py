from django.db import models

# Create your models here.

from django.db.models import F
from django.urls import reverse
from django.contrib.auth.models import User

#import der Choices damit die überall verwendbar sind
from .choices import *
from django.contrib.auth.models import User

#Ende der Imports
########################################################################################################################

#neue Klasse die den User erweitern soll

class user_erweitern(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gruppennummer = models.CharField(max_length=1, choices=GRUPPEN, null=True, blank=True)
    rolle = models.CharField(max_length=1, choices=ROLLEN, null=True, blank=True)

#Ende der organisatorischen Klassen
########################################################################################################################

class requirement(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    req_pk_requirementid = models.AutoField(primary_key=True, null=False, unique=True)
    req_fk_ersteller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    #Atrribute:
    req_name = models.CharField(max_length=100, null=True, blank=True)
    req_kommentar = models.CharField(max_length=300, null=True, blank=True)
    req_datum_erstellung = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    req_datum_aenderung = models.DateTimeField(auto_now=True, null=True, blank=True)
    req_beschreibung = models.CharField(max_length=300, null=True, blank=True)

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
    testc_fk_ersteller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    testc_fk_requirement = models.ManyToManyField(requirement, blank=True)

    #Atrribute:
    testc_name = models.CharField(max_length=128, null=True, blank=True)
    testc_kommentar = models.CharField(max_length=128, null=True, blank=True)
    testc_datum_erstellung = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    testc_datum_aenderung = models.DateTimeField(auto_now=True, null=True, blank=True)
    testc_beschreibung = models.CharField(max_length=128, null=True, blank=True)
    testc_vorbedingung = models.CharField(max_length=128, null=True, blank=True)

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
    schritt_tatsaechlichesergebnis = models.CharField(max_length=128, null=True, blank=True)
    schritt_ergebnis = models.CharField(max_length=1, choices=RUN_STATUS, default=RUN_STATUS[1], null=True, blank=False)

    #zum Kopieren der TestCase Schritte
    schritt_schritte = models.CharField(max_length=128, null=True, blank=True)
    schritt_erwartetesergebnis = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return "ID: " + str(self.schritt_pk_id)

class testrun(models.Model):
    #Private Keys, Foreign Keys and other relationships:
    testr_pk_testrunid = models.AutoField(primary_key=True, null=False, unique=True)
    testr_fk_ersteller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    testr_fk_testcaseid = models.ForeignKey('testcase', on_delete=models.SET_NULL, null=True, blank=True)

    #Atrribute:
    testr_name = models.CharField(max_length=100, null=True, blank=True)
    testr_kommentar = models.CharField(max_length=300, null=True, blank=True)
    testr_datum_erstellung = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    testr_datum_aenderung = models.DateTimeField(auto_now=True, null=True, blank=True)
    testr_beschreibung = models.CharField(max_length=128, null=True, blank=True)
    testr_testc_datum = models.DateTimeField(null=True, blank=True)

    testr_status = models.CharField(max_length=1, choices=RUN_STATUS, help_text='TestRun Ergebnis', null=True, blank=True)
    testr_dauer = models.IntegerField(null=True, blank=True)
    testr_datum_durchführung = models.DateTimeField(auto_now_add=True, null=True, blank=True)

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

    notes = models.CharField(max_length=128, null=True, blank=True)