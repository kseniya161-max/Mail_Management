from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0037_offerfile_is_sent"),
        ("documents", "0006_move_offerfile_to_documents"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(
                    name="OfferFile",
                ),
            ],
        ),
    ]