from django.db import models
from apps.administration.models import (
    Faculty,
    Authenticated_User,
    Nationality,
    Specialization,
    Regulation,
    Transaction,
    Regulation_Grade,
)


class Certificate(models.Model):
    certificate_id = models.BigIntegerField(primary_key=True)
    certificate_serial = models.CharField(max_length=20)
    certificate_date = models.DateTimeField()
    certificate_status = models.CharField(max_length=2)
    # db_column="graduate" because old schema used BigIntegerField named "graduate"
    graduate = models.ForeignKey(
        "Graduate",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="graduate",
    )
    print_date = models.DateTimeField(blank=True, null=True)
    delivered = models.CharField(max_length=2, blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    certificate_notes = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ("certificate_id",)

    def __str__(self):
        return str(self.certificate_id)

    @property
    def is_delivered(self):
        return self.delivered in ("Y", "y", "1", "T", "t", "True", "true", "YES", "yes")

    @is_delivered.setter
    def is_delivered(self, value):
        self.delivered = "Y" if value else "N"

    @property
    def is_printed(self):
        return self.print_date is not None


class Faculty_Turn(models.Model):
    faculty_turn_id = models.BigIntegerField(primary_key=True)
    faculty = models.ForeignKey(
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
    # db_column="nationality" because old schema used BigIntegerField named "nationality"
    nationality = models.ForeignKey(
        Nationality,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="nationality",
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
    # db_column="specialization" because old schema used BigIntegerField named "specialization"
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="specialization",
    )
    # db_column="faculty_turn" because old schema used BigIntegerField named "faculty_turn"
    faculty_turn = models.ForeignKey(
        Faculty_Turn,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="faculty_turn",
    )
    # db_column="regulation" because old schema used BigIntegerField named "regulation"
    regulation = models.ForeignKey(
        Regulation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="regulation",
    )
    isdelete = models.CharField(max_length=2, blank=True, null=True)
    # db_column="transaction" because old schema used BigIntegerField named "transaction"
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="transaction",
    )
    lastuser = models.BigIntegerField()
    transdesciption = models.CharField(max_length=200)
    # db_column="faculty" because old schema used BigIntegerField named "faculty"
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="graduates",
        db_column="faculty",
    )
    ic_card_init = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ("graduate_id",)

    def __str__(self):
        return str(self.graduate_id)

    @property
    def is_checked(self):
        return self.ischeked in ("Y", "y", "1", "T", "t", "True", "true", "YES", "yes")

    @is_checked.setter
    def is_checked(self, value):
        self.ischeked = "Y" if value else "N"

    @property
    def is_checked2(self):
        return self.ischeked2 in ("Y", "y", "1", "T", "t", "True", "true", "YES", "yes")

    @is_checked2.setter
    def is_checked2(self, value):
        self.ischeked2 = "Y" if value else "N"

    @property
    def is_deleted(self):
        return self.isdelete in ("Y", "y", "1", "T", "t", "True", "true", "YES", "yes")

    @is_deleted.setter
    def is_deleted(self, value):
        self.isdelete = "Y" if value else "N"

    @property
    def computed_grade(self):
        """
        Compute grade from Regulation_Grade ranges.
        Score is total points → convert to percentage before matching.
        Falls back to stored grade_name_ar if available.
        """
        # 1. Return stored value if available
        if self.grade_name_ar:
            return {
                "ar": self.grade_name_ar,
                "en": self.grade_name_en,
                "letter": self.grade_letter,
            }

        # 2. Need regulation_id, score, and total_score to compute
        if not self.regulation_id or self.score is None:
            return {"ar": None, "en": None, "letter": self.grade_letter}

        try:
            # Convert total score to percentage
            if self.specialization and self.specialization.total_score:
                pct = (float(self.score) / self.specialization.total_score) * 100
            else:
                # Fallback: try raw score if no total_score available
                pct = float(self.score)

            rg = (
                Regulation_Grade.objects.filter(
                    regulation__regulation_id=self.regulation_id,
                    grade_start__lte=pct,
                    grade_end__gte=pct,
                )
                .select_related("grade")
                .first()
            )

            if rg and rg.grade:
                return {
                    "ar": rg.grade.grade_ar_name,
                    "en": rg.grade.grade_en_name,
                    "letter": self.grade_letter,
                }

        except Exception:
            pass

        return {"ar": None, "en": None, "letter": self.grade_letter}

    @property
    def computed_grade_ar(self):
        return self.computed_grade.get("ar")

    @property
    def computed_grade_en(self):
        return self.computed_grade.get("en")


class History(models.Model):
    history_id = models.DecimalField(primary_key=True, max_digits=20, decimal_places=0)
    # db_column="graduate" because old schema used BigIntegerField named "graduate"
    graduate = models.ForeignKey(
        "Graduate",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        db_column="graduate",
    )
    history_date = models.DateTimeField(blank=True, null=True)
    history_field = models.CharField(max_length=400, blank=True, null=True)
    history_old = models.CharField(max_length=400, blank=True, null=True)
    history_new = models.CharField(max_length=400, blank=True, null=True)
    history_type = models.CharField(max_length=20, blank=True, null=True)
    history_desc = models.CharField(max_length=200, blank=True, null=True)
    # db_column="authunticated_user_id" because old schema used BigIntegerField named "authunticated_user_id"
    authunticated_user_id = models.ForeignKey(
        Authenticated_User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_column="authunticated_user_id",
    )
    # db_column="faculty" because old schema used BigIntegerField named "faculty"
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, blank=True, null=True, db_column="faculty"
    )

    class Meta:
        ordering = ("history_id",)

    def __str__(self):
        return str(self.history_id)
