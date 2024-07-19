from django.contrib import admin

# from .models import Register, DanceForms, Tutorials
from .models import *

# Register your models here.
admin.site.register(Register)
admin.site.register(DanceForms)
admin.site.register(Tutorials)
admin.site.register(Subscription)
admin.site.register(Payment)
admin.site.register(Card_Details)
admin.site.register(PaymentDetails)
admin.site.register(TutorialProgress)

# to view the details in table form
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'start_date')


admin.site.register(PaymentAmount, PaymentAdmin)
