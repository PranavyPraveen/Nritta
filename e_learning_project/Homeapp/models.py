from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Register(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    # to create a dropdown option for gender
    roles = (('none', 'None'), ('other', 'Other'), ('male', 'Male'), ('female', 'Female'))
    gender = models.CharField(max_length=20, choices=roles, default='none', help_text='Enter your gender')

    def __str__(self):
        return self.user.first_name


class DanceForms(models.Model):
    name = models.CharField(max_length=30)
    img = models.ImageField(upload_to="images")
    description = models.TextField()
    outcomes = models.TextField(null=True)
    duration = models.PositiveIntegerField()
    fees = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tutorials(models.Model):
    dance_forms = models.ForeignKey(DanceForms, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()
    cover_img = models.ImageField(upload_to='cover image', null=True)
    vdo = models.FileField(upload_to='Tutorial_vdos')

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dance = models.ManyToManyField(DanceForms)
    date = models.DateField(auto_now_add=True)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    df = models.ManyToManyField(DanceForms)
    amount = models.FloatField()


Month_choices = (
    ('Choose Month', 'Choose Month'),
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August9', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
)

Year_choices = (
    ('Choose Year', 'Choose Year'),
    ('2023', '2023'),
    ('2024', '2024'),
    ('2025', '2025'),
    ('2026', '2026'),
    ('2027', '2027'),
)


class Card_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_no = models.CharField(max_length=16)
    Exp_month = models.CharField(max_length=20, choices=Month_choices)
    Exp_year = models.CharField(max_length=20, choices=Year_choices, default="")

    def __str__(self):
        return self.user.username


class PaymentAmount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)


class PaymentDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(DanceForms)
    start_date = models.DateField(auto_now_add=True)
    amount = models.ManyToManyField(PaymentAmount)

    def __str__(self):
        return self.user.username


class TutorialProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(DanceForms, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorials, on_delete=models.CASCADE)
    end_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'user is - {self.user.username}- dance-form is - {self.course.name} - {self.tutorial.name}'
