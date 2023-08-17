from django.db import models
from django.utils import timezone


class RefbookVersion(models.Model):
    refbook = models.ForeignKey(
        'Refbook', on_delete=models.CASCADE, related_name='versions',
        verbose_name='Справочник')
    version = models.CharField(max_length=50, verbose_name='Версия')
    active_from = models.DateField(verbose_name='Действует с')

    def __str__(self) -> str:
        return '{}-{}'.format(self.refbook,
                              self.version)

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        constraints = [
            models.UniqueConstraint(
                fields=['refbook', 'version'],
                name='unique_refbook_version',
            ),
            models.UniqueConstraint(
                fields=['refbook', 'active_from'],
                name='unique_refbook_active_from',
            )
        ]


class Refbook(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name='Код')
    name = models.CharField(max_length=300, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self) -> str:
        return self.code

    class Meta:
        ordering = ['id']
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def current_version(self) -> RefbookVersion | None:
        now = timezone.now().date()
        return self.versions.all()\
            .filter(active_from__lte=now)\
            .order_by('-active_from')\
            .first()


class RefbookElement(models.Model):
    refbook_version = models.ForeignKey(
        'RefbookVersion', on_delete=models.CASCADE, related_name='elements',
        verbose_name='Версия справочника',
    )
    code = models.CharField(max_length=100, verbose_name='Код')
    value = models.CharField(max_length=300, verbose_name='Название')

    class Meta:
        ordering = ['id']
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'
        constraints = [
            models.UniqueConstraint(
                fields=['refbook_version', 'code'],
                name='unique_version_element_code',
            ),
        ]

    def __str__(self) -> str:
        return self.code
