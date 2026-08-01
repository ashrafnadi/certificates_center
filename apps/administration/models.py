from django.db import models
from django.contrib.auth.models import User


class Authenticated_User(models.Model):
    authunticated_user_id = models.BigIntegerField(primary_key=True)
    authorize_user_id = models.ForeignKey(
        "Users_Profile", on_delete=models.CASCADE, blank=True, null=True
    )
    faculty_id = models.ForeignKey(
        "Faculty", on_delete=models.CASCADE, blank=True, null=True
    )
    isadd = models.BooleanField(default=False)
    isedit = models.BooleanField(default=False)
    isdelete = models.BooleanField(default=False)
    isprint = models.BooleanField(default=False)
    iscommit = models.BooleanField(default=False)
    isview = models.BooleanField(default=False)

    class Meta:
        ordering = ("authunticated_user_id",)

    def __str__(self):
        return str(self.authunticated_user_id)


class System_Settings(models.Model):
    data_id = models.SmallIntegerField(primary_key=True)
    admin_name = models.CharField(max_length=100)
    super_name = models.CharField(max_length=200)
    url = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100)
    admin_en = models.CharField(max_length=100)
    super_en = models.CharField(max_length=100)

    class Meta:
        ordering = ("data_id",)

    def __str__(self):
        return str(self.data_id)


class Degree(models.Model):
    degree_id = models.BigIntegerField(primary_key=True)
    degree_ar_name = models.CharField(max_length=200)
    degree_en_name = models.CharField(max_length=200)
    faculty_id = models.ForeignKey(
        "Faculty", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ("degree_id",)

    def __str__(self):
        return str(self.degree_id)


class Faculty(models.Model):
    faculty_id = models.BigIntegerField(primary_key=True)
    faculty_ar_name = models.CharField(max_length=200)
    faculty_en_name = models.CharField(max_length=200)
    faculty_email = models.CharField(max_length=100, blank=True, null=True)
    faculty_ar_dean = models.CharField(max_length=200)
    faculty_en_dean = models.CharField(max_length=200)
    faculty_gawda_no = models.IntegerField(blank=True, null=True)
    faculty_gawda_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("faculty_id",)

    def __str__(self):
        return str(self.faculty_ar_name)


class Nationality(models.Model):
    nationality_id = models.BigIntegerField(primary_key=True)
    nationality_ar_name = models.CharField(max_length=200)
    nationality_en_name = models.CharField(max_length=200)

    class Meta:
        ordering = ("nationality_id",)

    def __str__(self):
        return str(self.nationality_id)


class Section(models.Model):
    section_id = models.BigIntegerField(primary_key=True)
    section_ar_namr = models.CharField(max_length=400)
    section_en_name = models.CharField(max_length=400, blank=True, null=True)
    faculty_id = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ("section_id",)

    def __str__(self):
        return str(self.section_id)


class Specialization(models.Model):
    specialization_id = models.BigIntegerField(primary_key=True)
    specialization_ar_name = models.CharField(max_length=400)
    specialization_en_name = models.CharField(max_length=400)
    section_id = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True
    )
    total_score = models.IntegerField(blank=True, null=True)
    ishours = models.CharField(max_length=2, blank=True, null=True)
    gawda_no = models.IntegerField(blank=True, null=True)
    gawda_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("specialization_id",)

    def __str__(self):
        return str(self.specialization_id)


class Transaction(models.Model):
    transaction_id = models.BigIntegerField(primary_key=True)
    transaction_date = models.DateTimeField()
    user = models.ForeignKey(
        "Users_Profile", on_delete=models.CASCADE, blank=True, null=True
    )
    transaction_descripsion = models.CharField(max_length=100)
    faculty = models.ForeignKey(
        "Faculty", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ("transaction_id",)

    def __str__(self):
        return str(self.transaction_id)


class Upload_Error(models.Model):
    error_id = models.BigIntegerField(primary_key=True)
    faculty_id = models.ForeignKey(
        "Faculty", on_delete=models.CASCADE, blank=True, null=True
    )
    user_id = models.ForeignKey(
        "Users_Profile", on_delete=models.CASCADE, blank=True, null=True
    )
    graduate_id_card = models.CharField(max_length=20, blank=True, null=True)
    error_desc = models.CharField(max_length=100, blank=True, null=True)
    error_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("error_id",)

    def __str__(self):
        return str(self.error_id)


class Users_Profile(models.Model):
    ROLE_SUPERVISOR = "supervisor"
    ROLE_DIRECTOR = "director"
    ROLE_AUDITOR = "auditor"
    ROLE_EMPLOYEE = "employee"

    ROLE_CHOICES = (
        (ROLE_SUPERVISOR, "مشرف"),
        (ROLE_DIRECTOR, "مدير"),
        (ROLE_AUDITOR, "مدقق"),
        (ROLE_EMPLOYEE, "موظف"),
    )

    id = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    user_name = models.CharField(max_length=60)
    user_short_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=130)
    user_email = models.CharField(max_length=40)
    user_status = models.CharField(max_length=4)
    user_notes = models.CharField(max_length=200, blank=True, null=True)
    isadmin = models.CharField(max_length=4, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_EMPLOYEE,
        verbose_name="الدور الوظيفي",
    )

    class Meta:
        ordering = ("user_id",)

    def __str__(self):
        return str(self.user_id)

    @property
    def is_faculty_required(self):
        """المدقق والموظف ملزمين باختيار الكلية، ما لم يكن المستخدم admin"""
        if self.isadmin not in (None, "", "0", "no", "false", "No", "False"):
            return False
        return self.role in (self.ROLE_AUDITOR, self.ROLE_EMPLOYEE)


class Grade(models.Model):
    grade_id = models.BigIntegerField(primary_key=True)
    grade_ar_name = models.CharField(max_length=40)
    grade_en_name = models.CharField(max_length=40)

    class Meta:
        ordering = ("grade_id",)

    def __str__(self):
        return str(self.grade_id)


class Regulation(models.Model):
    regulation_id = models.BigIntegerField(primary_key=True)
    regulation_ar_name = models.CharField(max_length=200)
    degree_id = models.BigIntegerField()

    class Meta:
        ordering = ("regulation_id",)

    def __str__(self):
        return str(self.regulation_id)


class Regulation_Grade(models.Model):
    regulation_grade_id = models.BigIntegerField(primary_key=True)
    regulation_id = models.BigIntegerField()
    grade_id = models.BigIntegerField()
    grade_start = models.SmallIntegerField()
    grade_end = models.SmallIntegerField()

    class Meta:
        ordering = ("regulation_grade_id",)

    def __str__(self):
        return str(self.regulation_grade_id)
