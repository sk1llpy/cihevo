INSTALLED_APPS = [
    # Admin-panel
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",

    # Base apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Installed apps
    'django_countries',
    'cities_light',

    # Local Apps
    "apps.general.apps.GeneralConfig",
    "apps.users.apps.UsersConfig",
    "apps.shop.apps.ShopConfig",
    "apps.orders.apps.OrdersConfig",
    "apps.marketing.apps.MarketingConfig",
    "apps.sales.apps.SalesConfig",
    "apps.accounting.apps.AccountingConfig",
]
