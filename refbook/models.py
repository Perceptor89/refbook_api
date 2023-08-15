from django.db import models


class Refbook(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name='Код')
    name = models.CharField(max_length=300, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'


class RefbookVersion(models.Model):
    refbook = models.ForeignKey('Refbook', on_delete=models.CASCADE,
                                related_name='versions')
    version = models.CharField(max_length=50)
    active_from = models.DateTimeField(unique=True)

    def __str__(self) -> str:
        return self.version

    class Mets:
        constraints = [
            models.UniqueConstraint(
                fields=['refbook', 'version'],
                name='unique_refbook_version',
            ),
        ]


class RefbookElement(models.Model):
    refbook_version = models.ForeignKey(
        'RefbookVersion', on_delete=models.CASCADE, related_name='elements'
    )
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.code
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['refbook_version', 'code'],
                name='unique_version_element_code',
            ),
        ]
