from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0037_offerfile_is_sent"),
        ("documents", "0005_alter_invoice_number"),
        ("products", "0005_product_price"),
        ("Users", "0004_alter_user_avatar_alter_user_country_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="OfferFile",
                    fields=[
                        (
                            "id",
                            models.BigAutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        ("name", models.CharField(max_length=200)),
                        ("file", models.FileField(upload_to="price_files/")),
                        ("created_at", models.DateTimeField(auto_now_add=True)),
                        ("is_sent", models.BooleanField(default=False)),

                        (
                            "client",
                            models.ForeignKey(
                                blank=True,
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="offer_files",
                                to="clients.clients",
                            ),
                        ),

                        (
                            "created_by",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                to="Users.user",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "clients_offerfile",
                    },
                ),
            ],
        ),
    ]