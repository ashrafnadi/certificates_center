from django.db import models
from apps.administration.models import Faculty, Authenticated_User


class Certificate(models.Model):
    certificate_id = models.BigIntegerField(primary_key=True)
    certificate_serial = models.CharField(max_length=20)
    certificate_date = models.DateTimeField()
    certificate_status = models.CharField(max_length=2)
    graduate_id = models.BigIntegerField(blank=True, null=True)
    print_date = models.DateTimeField(blank=True, null=True)
    delivered = models.CharField(max_length=2, blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    certificate_notes = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ("certificate_id",)

    def __str__(self):
        return str(self.certificate_id)


class Faculty_Turn(models.Model):
    faculty_turn_id = models.BigIntegerField(primary_key=True)
    faculty_id = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, blank=True, null=True
    )
    turn_ar_name = models.CharField(max_length=30)
    turn_en_name = models.CharField(max_length=30)
    turn_cad_date = models.DateTimeField()
    turn_uad_date = models.DateTimeField()
    turn_year = models.CharField(max_length=20)
    turn_cad_no = models.CharField(max_length=20, blank=True, null=True)
    turn_uad_no = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ("faculty_turn_id",)

    def __str__(self):
        return str(self.faculty_turn_id)


class Graduate(models.Model):
    graduate_id = models.BigIntegerField(primary_key=True)
    graduate_id_card = models.DecimalField(max_digits=20, decimal_places=0)
    graduate_ar_name = models.CharField(max_length=400)
    graduate_en_name = models.CharField(max_length=400)
    graduate_ar_pob = models.CharField(max_length=100)
    graduate_en_pob = models.CharField(max_length=100)
    graduate_dob = models.DateTimeField()
    nationality = models.ForeignKey(
        "administration.Nationality", on_delete=models.CASCADE, blank=True, null=True
    )
    graduate_gendar = models.SmallIntegerField()
    graduate_notes = models.CharField(max_length=200, blank=True, null=True)
    score = models.DecimalField(max_digits=9, decimal_places=3)
    project_data_ar = models.CharField(max_length=200, blank=True, null=True)
    project_data_en = models.CharField(max_length=200, blank=True, null=True)
    honor = models.SmallIntegerField()
    grade_name_ar = models.CharField(max_length=50, blank=True, null=True)
    grade_letter = models.CharField(max_length=20, blank=True, null=True)
    grade_name_en = models.CharField(max_length=50, blank=True, null=True)
    ischeked = models.CharField(max_length=2)
    ischeked2 = models.CharField(max_length=20)
    specialization = models.ForeignKey(
        "administration.Specialization", on_delete=models.CASCADE, blank=True, null=True
    )
    faculty_turn = models.ForeignKey(
        "Faculty_Turn", on_delete=models.CASCADE, blank=True, null=True
    )
    regulation = models.ForeignKey(
        "administration.Regulation", on_delete=models.CASCADE, blank=True, null=True
    )
    isdelete = models.CharField(max_length=2, blank=True, null=True)
    transaction = models.ForeignKey(
        "administration.Transaction", on_delete=models.CASCADE, blank=True, null=True
    )
    lastuser = models.BigIntegerField()
    transdesciption = models.CharField(max_length=200)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, blank=True, null=True
    )
    ic_card_init = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ("graduate_id",)

    def __str__(self):
        return str(self.graduate_id)


class History(models.Model):
    history_id = models.DecimalField(primary_key=True, max_digits=20, decimal_places=0)
    row_id = models.ForeignKey(
        Graduate, on_delete=models.CASCADE, blank=True, null=True
    )
    history_date = models.DateTimeField(blank=True, null=True)
    history_field = models.CharField(max_length=400, blank=True, null=True)
    history_old = models.CharField(max_length=400, blank=True, null=True)
    history_new = models.CharField(max_length=400, blank=True, null=True)
    history_type = models.CharField(max_length=20, blank=True, null=True)
    history_desc = models.CharField(max_length=200, blank=True, null=True)
    authunticated_user_id = models.ForeignKey(
        Authenticated_User, on_delete=models.CASCADE, blank=True, null=True
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ("history_id",)

    def __str__(self):
        return str(self.history_id)
