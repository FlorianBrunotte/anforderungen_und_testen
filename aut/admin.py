from django.contrib import admin

# Register your models here.
from .models import requirement, testcase, testrun, testcase_schritt, testrun_schritt, user_erweitern, note, projekt

admin.site.register(requirement)
admin.site.register(testrun)
admin.site.register(testcase)
admin.site.register(testcase_schritt)
admin.site.register(testrun_schritt)
admin.site.register(user_erweitern)
admin.site.register(note)
admin.site.register(projekt)

#Test für die Gruppennummer
from .models import user_erweitern
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class GruppeInline(admin.StackedInline):
    model = user_erweitern

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (GruppeInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)








#Die beiden Arten sind gleich in ihrer Funktion
#define the admin class
#class ProfessorAdmin(admin.ModelAdmin):
#    list_display = ('Professorennummer', 'Name', 'Passwort')
#    #für mehr Attribute anzeigen

#admin.site.register(professor, ProfessorAdmin)

#@admin.register(projekt)
#class ProjektAdmin(admin.ModelAdmin):
#    pass


#@admin.register(student)
#class StudentAdmin(admin.ModelAdmin):
#    list_display = ('Matrikelnummer', 'Name', 'Passwort', 'Gruppennummer_FK', 'display_project')


#class RequirementInline(admin.StackedInline):
#    model = requirement

#mal gucken mit Datum
#@admin.register(Element)
#class ElementAdmin(admin.ModelAdmin):
 #   list_display = ('Name', 'ElementID', 'Kommentar', 'Datum_Erstellung', 'Datum_Aenderung', 'ProjektID_FK', 'Matrikelnummer_FK')
#    list_filter = ('ProjektID_FK', 'Matrikelnummer_FK')
 #  fieldsets = (
  #      (None, {
#
#            'fields': ('Name', 'Kommentar' )
#        }),
 #       ('Foreign Kesy:', {
#            'fields': ('ProjektID_FK', 'Matrikelnummer_FK')
#        }),
#    )
#    inlines = [RequirementInline]
