#
# PR 130502: Executes Localization for the whole project
#
import os
#from django_common.tzinfo import Local
project_root = os.path.dirname(os.path.realpath(__file__))
print "i18n: makemessage -l de for all directories that have locale"
dirs = os.listdir(project_root)
for app in dirs:
    app_path = os.path.join(project_root, app)
    locale_path = os.path.join(app_path, "locale")
    if(os.path.exists(locale_path)): #modify this condition for exclusion of specific folders
        print "Localizing... " + locale_path
        os.chdir(app_path)
        os.system("django-admin.py makemessages -l de")
        os.system("gedit " + locale_path + "/de/LC_MESSAGES/django.po")
        os.system("django-admin.py compilemessages")
    else:
        print "Not localized: " + locale_path