from django.db import models

class SizeChoices(models.TextChoices):
    # Shirts
    XS = "XS", "XS"
    S = "S", "S"
    M = "M", "M"
    L = "L", "L"
    XL = "XL", "XL"
    XXL = "XXL", "XXL"

    # Shoes
    SHOES_37 = "shoes_37", "37"
    SHOES_38 = "shoes_38", "38"
    SHOES_39 = "shoes_39", "39"
    SHOES_40 = "shoes_40", "40"
    SHOES_41 = "shoes_41", "41"
    SHOES_42 = "shoes_42", "42"
    SHOES_43 = "shoes_43", "43"
    SHOES_44 = "shoes_44", "44"
    SHOES_45 = "shoes_45", "45"
    
    # Jeans
    JEANS_29 = "jeans_29", "29"
    JEANS_30 = "jeans_30", "30"
    JEANS_31 = "jeans_31", "31"
    JEANS_32 = "jeans_32", "32"
    JEANS_33 = "jeans_33", "33"
    JEANS_34 = "jeans_34", "34"
    JEANS_36 = "jeans_36", "36"
    JEANS_38 = "jeans_38", "38"
    JEANS_40 = "jeans_40", "40"
    JEANS_42 = "jeans_42", "42"

    # Monar
    MONAR_40 = "monar_40", "40/46"
    MONAR_42 = "monar_42", "42/48"
    MONAR_44 = "monar_44", "44/50"
    MONAR_46 = "monar_46", "46/52"
    MONAR_48 = "monar_48", "48/54"
    MONAR_50 = "monar_50", "50/56"
    MONAR_52 = "monar_52", "52/58"
    MONAR_54 = "monar_54", "54/60"
    
    # SUIT
    SUIT_44 = "suit_44", "44/38"
    SUIT_46 = "suit_46", "46/40"
    SUIT_48 = "suit_48", "48/42"
    SUIT_50 = "suit_50", "50/44"
    SUIT_52 = "suit_52", "52/46"
    SUIT_54 = "suit_54", "54/48"
    SUIT_56 = "suit_56", "56/50"
    SUIT_58 = "suit_58", "58/52"
    SUIT_60 = "suit_60", "60/54"
    SUIT_62 = "suit_62", "62/56"


class CategoryTypeChoices(models.TextChoices):
    DEFAULT = "default", "По умолчанию"
    SHOES = "shoes", "Обувь"
    JEANS = "jeans", "Джинсы"
    MONAR = "monar", "Монар"
    SUIT = "suit", "Костюмы"

class OrderStatusTypeChoices(models.TextChoices):
    WAITING_PAYMENT = "waiting_payment", "Ожидает оплату"
    PENDING = "pending", "В обработке"
    ON_WAY = "on_way", "В пути"
    DELIVERED = "delivered", "Доставлен"
    
class PaymentTypeChoices(models.TextChoices):
    PAYME = "payme", "Payme"
    CLICK = "click", "Click"
    UZUM = "uzum", "Uzum Bank"

class OrderTypeChoices(models.TextChoices):
    ONLINE = "online", "Онлайн-заказ"
    OFFLINE = "offline", "Офлайн-продажа"

class ColorTypeChoices(models.TextChoices):
    WHITE = "white", "Белый"
    BLACK = "black", "Черный"
    GREY = "grey", "Серый"
    BLUE = "blue", "Синий"
    NAVY = "navy", "Темно-синий"
    RED = "red", "Красный"
    GREEN = "green", "Зеленый"
    BROWN = "brown", "Коричневый"
    BEIGE = "beige", "Бежевый"
    YELLOW = "yellow", "Желтый"
    ORANGE = "orange", "Оранжевый"
    PURPLE = "purple", "Фиолетовый"
    PINK = "pink", "Розовый"
    OLIVE = "olive", "Оливковый"
    MAROON = "maroon", "Темно-красный"
