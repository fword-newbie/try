from django.contrib import admin

from register.models import People, alc, badge, bloodduck, bloodsugar, caremessage, default, diet, drug_useds, friendlist, invite_code, record, requestlist, setting, weight

# Register your models here.
admin.site.register(People)
admin.site.register(bloodduck)
admin.site.register(weight)
admin.site.register(bloodsugar)
admin.site.register(default)
admin.site.register(diet)
admin.site.register(caremessage)
admin.site.register(alc)
admin.site.register(setting)
admin.site.register(badge)
admin.site.register(drug_useds)
admin.site.register(invite_code)
admin.site.register(friendlist)
admin.site.register(record)
admin.site.register(requestlist)
