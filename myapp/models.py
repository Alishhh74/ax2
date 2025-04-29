from django.db import models
class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    is_for_rent = models.BooleanField(default=False)

    def __str__(self):
        return self.title

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

class Owner(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефон должен быть в формате: '+999999999'"
    )
    
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name="Телефон"
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    passport = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Паспортные данные"
    )
    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"
        ordering = ['last_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('commercial', 'Коммерческая')
    ]

    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name="Владелец"
    )
    title = models.CharField(max_length=100, verbose_name="Название")
    address = models.TextField(verbose_name="Адрес")
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES,
        verbose_name="Тип недвижимости"
    )
    area = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Площадь (м²)"
    )
    rooms = models.PositiveIntegerField(verbose_name="Количество комнат")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена аренды"
    )
    is_available = models.BooleanField(default=True, verbose_name="Доступна")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Объект недвижимости"
        verbose_name_plural = "Объекты недвижимости"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_property_type_display()})"


class Tenant(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        max_length=17,
        verbose_name="Телефон"
    )
    email = models.EmailField(unique=True, verbose_name="Email")
    passport = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Паспортные данные"
    )
    income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Доход"
    )
    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Арендатор"
        verbose_name_plural = "Арендаторы"
        ordering = ['last_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Contract(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('completed', 'Завершен'),
        ('terminated', 'Расторгнут')
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name="Объект недвижимости"
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name="Арендатор"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    monthly_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Арендная плата"
    )
    deposit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Залог"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Договор аренды"
        verbose_name_plural = "Договоры аренды"
        ordering = ['-start_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name="check_contract_dates"
            )
        ]

    def __str__(self):
        return f"Договор №{self.id} ({self.property})"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('transfer', 'Перевод')
    ]

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Договор"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма"
    )
    payment_date = models.DateField(verbose_name="Дата платежа")
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name="Способ оплаты"
    )
    period_start = models.DateField(verbose_name="Начало периода")
    period_end = models.DateField(verbose_name="Конец периода")
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтвержден")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ['-payment_date']
        constraints = [
            models.CheckConstraint(
                check=models.Q(period_end__gt=models.F('period_start')),
                name="check_payment_period"
            )
        ]

    def __str__(self):
        return f"Платеж {self.amount} от {self.payment_date}"

