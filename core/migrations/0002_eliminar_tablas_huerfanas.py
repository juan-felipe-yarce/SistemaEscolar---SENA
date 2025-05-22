from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("DROP TABLE IF EXISTS core_docente CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS core_estudiante CASCADE;"),
        migrations.RunSQL("DROP TABLE IF EXISTS core_acudiente CASCADE;"),
    ]
