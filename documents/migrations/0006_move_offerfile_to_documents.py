from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0037_offerfile_is_sent"),
        ("documents", "0005_alter_invoice_number"),
        ("products", "0005_product_price"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE clients_offerfile
                        RENAME TO documents_offerfile;
                    """,
                    reverse_sql="""
                        ALTER TABLE documents_offerfile
                        RENAME TO clients_offerfile;
                    """,
                ),
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE clients_offerfile_products
                        RENAME TO documents_offerfile_products;
                    """,
                    reverse_sql="""
                        ALTER TABLE documents_offerfile_products
                        RENAME TO clients_offerfile_products;
                    """,
                ),
            ],
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
                        (
                            "name",
                            models.CharField(
                                max_length=200,
                                verbose_name="Название файла",
                            ),
                        ),
                        (
                            "file",
                            models.FileField(
                                upload_to="price_files/",
                                verbose_name="Файл",
                            ),
                        ),
                        (
                            "created_at",
                            models.DateTimeField(
                                auto_now_add=True,
                                verbose_name="Дата создания",
                            ),
                        ),
                        (
                            "is_sent",
                            models.BooleanField(
                                default=False,
                                verbose_name="Отправлено",
                            ),
                        ),
                        (
                            "client",
                            models.ForeignKey(
                                blank=True,
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="offer_files",
                                to="clients.clients",
                                verbose_name="Клиент",
                            ),
                        ),
                        (
                            "created_by",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                to=settings.AUTH_USER_MODEL,
                                verbose_name="Создатель файла",
                            ),
                        ),
                        (
                            "products",
                            models.ManyToManyField(
                                to="products.product",
                                verbose_name="Выбранные продукты",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "documents_offerfile",
                        "verbose_name": "Сгенерированный файл",
                        "verbose_name_plural": "Сгенерированные файлы",
                    },
                ),
            ],
        ),
    ]
