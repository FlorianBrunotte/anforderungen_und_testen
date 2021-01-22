# Generated by Django 3.1.2 on 2021-01-22 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='professor',
            fields=[
                ('prof_pk_professorennummer', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('prof_name', models.CharField(help_text='Name des Professors', max_length=128, null=True)),
                ('prof_passwort', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='projekt',
            fields=[
                ('pro_pk_projektid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('pro_name', models.CharField(max_length=128, null=True)),
                ('pro_fk_professorennummer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aut.professor')),
            ],
        ),
        migrations.CreateModel(
            name='requirement',
            fields=[
                ('req_pk_requirementid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('req_name', models.CharField(max_length=128, null=True)),
                ('req_kommentar', models.CharField(max_length=128, null=True)),
                ('req_datum_erstellung', models.DateTimeField(auto_now_add=True)),
                ('req_datum_aenderung', models.DateTimeField(auto_now=True)),
                ('req_beschreibung', models.CharField(max_length=128, null=True)),
                ('req_kategorie', models.CharField(blank=True, choices=[('1', 'Kategorie 1'), ('2', 'Kategorie 2')], help_text='Kategorie des Requirements', max_length=1)),
                ('req_fk_ersteller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('req_fk_projektid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aut.projekt')),
            ],
            options={
                'ordering': ['req_pk_requirementid'],
            },
        ),
        migrations.CreateModel(
            name='testcase',
            fields=[
                ('testc_pk_testcaseid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('testc_name', models.CharField(max_length=128, null=True)),
                ('testc_kommentar', models.CharField(max_length=128, null=True)),
                ('testc_datum_erstellung', models.DateTimeField(auto_now_add=True)),
                ('testc_datum_aenderung', models.DateTimeField(auto_now=True)),
                ('testc_beschreibung', models.CharField(max_length=128, null=True)),
                ('testc_vorbedingung', models.CharField(max_length=128, null=True)),
                ('testc_fk_ersteller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('testc_fk_projektid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aut.projekt')),
                ('testc_fk_requirement', models.ManyToManyField(blank=True, to='aut.requirement')),
            ],
            options={
                'ordering': ['testc_pk_testcaseid'],
            },
        ),
        migrations.CreateModel(
            name='testcase_schritt',
            fields=[
                ('schritt_pk_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('schritt_schritte', models.CharField(blank=True, max_length=128, null=True)),
                ('schritt_erwartetesergebnis', models.CharField(blank=True, max_length=128, null=True)),
                ('schritt_fk_testcase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aut.testcase')),
            ],
        ),
        migrations.CreateModel(
            name='testrun',
            fields=[
                ('testr_pk_testrunid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('testr_name', models.CharField(max_length=128, null=True)),
                ('testr_kommentar', models.CharField(max_length=128, null=True)),
                ('testr_datum_erstellung', models.DateTimeField(auto_now_add=True)),
                ('testr_datum_aenderung', models.DateTimeField(auto_now=True)),
                ('testr_beschreibung', models.CharField(max_length=128, null=True)),
                ('testr_testc_datum', models.DateTimeField(blank=True, null=True)),
                ('testr_status', models.CharField(blank=True, choices=[('p', 'pass'), ('f', 'fail')], help_text='TestRun Ergebnis', max_length=1)),
                ('testr_dauer', models.CharField(blank=True, max_length=100, null=True)),
                ('testr_datum_durchführung', models.DateTimeField(auto_now_add=True)),
                ('testr_fk_ersteller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('testr_fk_projektid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aut.projekt')),
                ('testr_fk_testcaseid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aut.testcase')),
            ],
            options={
                'ordering': ['testr_pk_testrunid'],
            },
        ),
        migrations.CreateModel(
            name='user_erweitern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gruppennummer', models.CharField(blank=True, choices=[('1', 'Gruppe 1'), ('2', 'Gruppe 2'), ('3', 'Gruppe 3'), ('4', 'Gruppe 4'), ('5', 'Gruppe 5'), ('6', 'Gruppe 6'), ('7', 'Gruppe 7'), ('8', 'Gruppe 8'), ('9', 'Gruppe 9')], max_length=1)),
                ('rolle', models.CharField(blank=True, choices=[('s', 'Student'), ('p', 'Professor')], max_length=1)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='testrun_schritt',
            fields=[
                ('schritt_pk_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('schritt_schritte', models.CharField(blank=True, max_length=128, null=True)),
                ('schritt_erwartetesergebnis', models.CharField(blank=True, max_length=128, null=True)),
                ('schritt_tatsaechlichesergebnis', models.CharField(blank=True, max_length=128, null=True)),
                ('schritt_ergebnis', models.CharField(choices=[('p', 'pass'), ('f', 'fail')], max_length=1)),
                ('schritt_fk_testcase_schritt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aut.testcase_schritt')),
                ('schritt_fk_testrun', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aut.testrun')),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('stud_pk_matrikelnummer', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('stud_name', models.CharField(max_length=128, null=True)),
                ('stud_passwort', models.CharField(max_length=128, null=True)),
                ('stud_fk_gruppennummer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aut.projekt')),
            ],
        ),
        migrations.CreateModel(
            name='note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(max_length=128, null=True)),
                ('note_fk_ersteller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
