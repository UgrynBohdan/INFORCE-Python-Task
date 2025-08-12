from django.utils.deprecation import MiddlewareMixin

class AppVersionMiddleware(MiddlewareMixin):
    """
    Middleware зчитує Build-Version з заголовків і додає до request.
    Додатково створює прапорець request.is_legacy_client для старих версій.
    """

    def process_request(self, request):
        build_version = request.headers.get("Build-Version")
        if build_version:
            try:
                request.app_version = int(build_version)
            except ValueError:
                request.app_version = None
        else:
            request.app_version = None

        # Припустимо, що остання версія — 2 і вище
        request.is_legacy_client = bool(request.app_version and request.app_version < 2)

