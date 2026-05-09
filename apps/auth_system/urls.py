from django.urls import path

from .views.login import LoginView
from .views.logout import LogoutView
from .views.refresh import TokenRefreshView
from .views.twofa.backup_codes import BackupCodesView
from .views.twofa.disable import Disable2FAView
from .views.twofa.enable import Enable2FAView
from .views.twofa.setup import Setup2FAView
from .views.twofa.verify import Verify2FALoginView

app_name = "auth_system"

urlpatterns = [
    # Core auth
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # 2FA management (all require authentication)
    path("2fa/setup/", Setup2FAView.as_view(), name="2fa-setup"),
    path("2fa/enable/", Enable2FAView.as_view(), name="2fa-enable"),
    path("2fa/disable/", Disable2FAView.as_view(), name="2fa-disable"),
    # 2FA login flow (public — uses Redis session_token)
    path("2fa/verify-login/", Verify2FALoginView.as_view(), name="2fa-verify-login"),
    # Backup code management (requires authentication)
    path("2fa/backup-codes/", BackupCodesView.as_view(), name="2fa-backup-codes"),
]
