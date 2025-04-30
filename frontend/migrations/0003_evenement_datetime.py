from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('frontend', '0002_alter_conducteur_id_alter_evenement_id_and_more'),
    ]
    operations = [
        migrations.RemoveField(
            model_name='evenement',
            name='date',
        ),
        migrations.AddField(
            model_name='evenement',
            name='datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
