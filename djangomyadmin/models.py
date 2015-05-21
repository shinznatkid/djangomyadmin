from django.db import models


class Tables(models.Model):
    table_catalog = models.CharField(db_column='TABLE_CATALOG', max_length=512)  # Field name made lowercase.
    table_schema = models.CharField(db_column='TABLE_SCHEMA', max_length=64, primary_key=True)  # Field name made lowercase.
    table_name = models.CharField(db_column='TABLE_NAME', max_length=64)  # Field name made lowercase.
    table_type = models.CharField(db_column='TABLE_TYPE', max_length=64)  # Field name made lowercase.
    engine = models.CharField(db_column='ENGINE', max_length=64, blank=True)  # Field name made lowercase.
    version = models.BigIntegerField(db_column='VERSION', blank=True, null=True)  # Field name made lowercase.
    row_format = models.CharField(db_column='ROW_FORMAT', max_length=10, blank=True)  # Field name made lowercase.
    table_rows = models.BigIntegerField(db_column='TABLE_ROWS', blank=True, null=True)  # Field name made lowercase.
    avg_row_length = models.BigIntegerField(db_column='AVG_ROW_LENGTH', blank=True, null=True)  # Field name made lowercase.
    data_length = models.BigIntegerField(db_column='DATA_LENGTH', blank=True, null=True)  # Field name made lowercase.
    max_data_length = models.BigIntegerField(db_column='MAX_DATA_LENGTH', blank=True, null=True)  # Field name made lowercase.
    index_length = models.BigIntegerField(db_column='INDEX_LENGTH', blank=True, null=True)  # Field name made lowercase.
    data_free = models.BigIntegerField(db_column='DATA_FREE', blank=True, null=True)  # Field name made lowercase.
    auto_increment = models.BigIntegerField(db_column='AUTO_INCREMENT', blank=True, null=True)  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME', blank=True, null=True)  # Field name made lowercase.
    update_time = models.DateTimeField(db_column='UPDATE_TIME', blank=True, null=True)  # Field name made lowercase.
    check_time = models.DateTimeField(db_column='CHECK_TIME', blank=True, null=True)  # Field name made lowercase.
    table_collation = models.CharField(db_column='TABLE_COLLATION', max_length=32, blank=True)  # Field name made lowercase.
    checksum = models.BigIntegerField(db_column='CHECKSUM', blank=True, null=True)  # Field name made lowercase.
    create_options = models.CharField(db_column='CREATE_OPTIONS', max_length=255, blank=True)  # Field name made lowercase.
    table_comment = models.CharField(db_column='TABLE_COMMENT', max_length=2048)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TABLES'

    def __str__(self):
        return self.table_name


class Columns(models.Model):
    table_catalog = models.CharField(db_column='TABLE_CATALOG', max_length=512)  # Field name made lowercase.
    table_schema = models.CharField(db_column='TABLE_SCHEMA', max_length=64, primary_key=True)  # Field name made lowercase.
    table_name = models.CharField(db_column='TABLE_NAME', max_length=64)  # Field name made lowercase.
    column_name = models.CharField(db_column='COLUMN_NAME', max_length=64)  # Field name made lowercase.
    ordinal_position = models.BigIntegerField(db_column='ORDINAL_POSITION')  # Field name made lowercase.
    column_default = models.TextField(db_column='COLUMN_DEFAULT', blank=True)  # Field name made lowercase.
    is_nullable = models.CharField(db_column='IS_NULLABLE', max_length=3)  # Field name made lowercase.
    data_type = models.CharField(db_column='DATA_TYPE', max_length=64)  # Field name made lowercase.
    character_maximum_length = models.BigIntegerField(db_column='CHARACTER_MAXIMUM_LENGTH', blank=True, null=True)  # Field name made lowercase.
    character_octet_length = models.BigIntegerField(db_column='CHARACTER_OCTET_LENGTH', blank=True, null=True)  # Field name made lowercase.
    numeric_precision = models.BigIntegerField(db_column='NUMERIC_PRECISION', blank=True, null=True)  # Field name made lowercase.
    numeric_scale = models.BigIntegerField(db_column='NUMERIC_SCALE', blank=True, null=True)  # Field name made lowercase.
    character_set_name = models.CharField(db_column='CHARACTER_SET_NAME', max_length=32, blank=True)  # Field name made lowercase.
    collation_name = models.CharField(db_column='COLLATION_NAME', max_length=32, blank=True)  # Field name made lowercase.
    column_type = models.TextField(db_column='COLUMN_TYPE')  # Field name made lowercase.
    column_key = models.CharField(db_column='COLUMN_KEY', max_length=3)  # Field name made lowercase.
    extra = models.CharField(db_column='EXTRA', max_length=27)  # Field name made lowercase.
    privileges = models.CharField(db_column='PRIVILEGES', max_length=80)  # Field name made lowercase.
    column_comment = models.CharField(db_column='COLUMN_COMMENT', max_length=1024)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COLUMNS'

    def __str__(self):
        return self.column_name


class Collations(models.Model):
    collation_name = models.CharField(db_column='COLLATION_NAME', max_length=32)
    character_set_name = models.CharField(db_column='CHARACTER_SET_NAME', max_length=32)
    collation_id = models.BigIntegerField(db_column='ID')
    is_default = models.CharField(db_column='IS_DEFAULT', max_length=3)
    is_compiled = models.CharField(db_column='IS_COMPILED', max_length=3)
    sortlen = models.BigIntegerField(db_column='SORTLEN')

    class Meta:
        managed = False
        db_table = 'COLLATIONS'            
        ordering = ['collation_name']

    def __str__(self):
        return self.collation_name