
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20211005_2310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='cuastom_user',
            new_name='custom_user',
        ),
    ]