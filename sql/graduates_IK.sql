CREATE VIEW GRADUATE_ID_IK
AS SELECT
        graduate_id,
        ( CASE
            WHEN turn_year > 2016 THEN lpad(graduate_data_all.faculty_id, 2, 0)
                                       || turn_year
                                       || substr(graduate_id_card, - 4)
                                       || lpad(substr(graduate_id * score, 1, 4), 4, 0)
            ELSE TO_CHAR(graduate_id_card)
        END ) AS "IK",
        turn_year,
        transaction.transaction_date
    FROM
        graduate_data_all,
        transaction
    WHERE
        graduate_data_all.transaction_id = transaction.transaction_id
        AND graduate_data_all.isdelete = 'N'
        AND graduate_data_all.ischeked = 'Y'
        AND graduate_data_all.ischeked2 = 'Y'
    ORDER BY
        graduate_id;
