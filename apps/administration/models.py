from django.db import models


class authorize_user(models.Model):
    authorize_user_id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    motherboard_id = models.BigIntegerField()
    isfirstlog = models.CharField(max_length=20)
    browser = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ("authorize_user_id",)

    def __str__(self):
        return str(self.authorize_user_id)


class authenticated_user(models.Model):
    authunticated_user_id = models.BigIntegerField(primary_key=True)
    authorize_user_id = models.BigIntegerField()
    faculty_id = models.BigIntegerField()
    isadd = models.CharField(max_length=2)
    isedit = models.CharField(max_length=2)
    isdelete = models.CharField(max_length=2)
    isprint = models.CharField(max_length=2)
    iscommit = models.CharField(max_length=2)
    isview = models.CharField(max_length=2)

    class Meta:
        ordering = ("authunticated_user_id",)

    def __str__(self):
        return str(self.authunticated_user_id)


class certificate_counter(models.Model):
    certificate_counter_id = models.BigIntegerField(primary_key=True)
    graduate_id = models.BigIntegerField()
    certificate_count = models.BigIntegerField()
    certificate_date = models.DateTimeField()
    certificate_user = models.BigIntegerField()
    certificate_type = models.CharField(max_length=20)

    class Meta:
        ordering = ("certificate_counter_id",)

    def __str__(self):
        return str(self.certificate_counter_id)


class data(models.Model):
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


class degree(models.Model):
    degree_id = models.BigIntegerField(primary_key=True)
    degree_ar_name = models.CharField(max_length=200)
    degree_en_name = models.CharField(max_length=200)
    faculty_id = models.BigIntegerField()

    class Meta:
        ordering = ("degree_id",)

    def __str__(self):
        return str(self.degree_id)


class faculty(models.Model):
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


class history(models.Model):
    history_id = models.DecimalField(primary_key=True, max_digits=20, decimal_places=0)
    table_id = models.BigIntegerField()
    row_id = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True)
    history_date = models.DateTimeField(blank=True, null=True)
    history_field = models.CharField(max_length=400, blank=True, null=True)
    history_old = models.CharField(max_length=400, blank=True, null=True)
    history_new = models.CharField(max_length=400, blank=True, null=True)
    history_type = models.CharField(max_length=20, blank=True, null=True)
    history_desc = models.CharField(max_length=200, blank=True, null=True)
    authunticated_user_id = models.BigIntegerField(blank=True, null=True)
    faculty_id = models.BigIntegerField()

    class Meta:
        ordering = ("history_id",)

    def __str__(self):
        return str(self.history_id)


class motherboard(models.Model):
    motherboard_id = models.BigIntegerField(primary_key=True)
    motherboard_serial = models.CharField(max_length=100)
    motherboard_computer = models.CharField(max_length=20)

    class Meta:
        ordering = ("motherboard_id",)

    def __str__(self):
        return str(self.motherboard_id)


class nationality(models.Model):
    nationality_id = models.BigIntegerField(primary_key=True)
    nationality_ar_name = models.CharField(max_length=200)
    nationality_en_name = models.CharField(max_length=200)

    class Meta:
        ordering = ("nationality_id",)

    def __str__(self):
        return str(self.nationality_id)


class section(models.Model):
    section_id = models.BigIntegerField(primary_key=True)
    section_ar_namr = models.CharField(max_length=400)
    section_en_name = models.CharField(max_length=400, blank=True, null=True)
    faculty_id = models.BigIntegerField()

    class Meta:
        ordering = ("section_id",)

    def __str__(self):
        return str(self.section_id)


class specialization(models.Model):
    specialization_id = models.BigIntegerField(primary_key=True)
    specialization_ar_name = models.CharField(max_length=400)
    specialization_en_name = models.CharField(max_length=400)
    section_id = models.BigIntegerField()
    total_score = models.IntegerField(blank=True, null=True)
    ishours = models.CharField(max_length=2, blank=True, null=True)
    gawda_no = models.IntegerField(blank=True, null=True)
    gawda_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("specialization_id",)

    def __str__(self):
        return str(self.specialization_id)


class transaction(models.Model):
    transaction_id = models.BigIntegerField(primary_key=True)
    transaction_date = models.DateTimeField()
    user_id = models.BigIntegerField()
    transaction_descripsion = models.CharField(max_length=100)
    faculty_id = models.BigIntegerField()

    class Meta:
        ordering = ("transaction_id",)

    def __str__(self):
        return str(self.transaction_id)


class upload_error(models.Model):
    error_id = models.BigIntegerField(primary_key=True)
    faculty_id = models.BigIntegerField(
        blank=True,
        null=True,
    )
    user_id = models.BigIntegerField(
        blank=True,
        null=True,
    )
    graduate_id_card = models.CharField(max_length=20, blank=True, null=True)
    error_desc = models.CharField(max_length=100, blank=True, null=True)
    error_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("error_id",)

    def __str__(self):
        return str(self.error_id)


class users_profile(models.Model):
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

    user_id = models.BigIntegerField(primary_key=True)
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


class grade(models.Model):
    grade_id = models.BigIntegerField(primary_key=True)
    grade_ar_name = models.CharField(max_length=40)
    grade_en_name = models.CharField(max_length=40)

    class Meta:
        ordering = ("grade_id",)

    def __str__(self):
        return str(self.grade_id)


class regulation(models.Model):
    regulation_id = models.BigIntegerField(primary_key=True)
    regulation_ar_name = models.CharField(max_length=200)
    degree_id = models.BigIntegerField()

    class Meta:
        ordering = ("regulation_id",)

    def __str__(self):
        return str(self.regulation_id)


class regulation_grade(models.Model):
    regulation_grade_id = models.BigIntegerField(primary_key=True)
    regulation_id = models.BigIntegerField()
    grade_id = models.BigIntegerField()
    grade_start = models.SmallIntegerField()
    grade_end = models.SmallIntegerField()

    class Meta:
        ordering = ("regulation_grade_id",)

    def __str__(self):
        return str(self.regulation_grade_id)
