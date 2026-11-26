"""Security headers added to every response."""

from starlette.middleware.base import BaseHTTPMiddleware

# The site loads GSAP and DOMPurify from cdnjs/jsdelivr and fonts from Google.
# Article images may be any https URL, so img-src stays broad.
SITE_CSP = "; ".join(
    [
        "default-src 'self'",
        "script-src 'self' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com",
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com",
        "img-src 'self' https: data:",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ]
)

# Swagger UI and ReDoc ship an inline bootstrap script, so they get a looser policy.
DOCS_PATHS = ("/docs", "/redoc")
DOCS_CSP = "; ".join(
    [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net",
        "img-src 'self' https: data:",
        "connect-src 'self'",
        "frame-ancestors 'none'",
    ]
)

STATIC_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Cross-Origin-Opener-Policy": "same-origin",
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, hsts: bool = False):
        super().__init__(app)
        self.hsts = hsts

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        for name, value in STATIC_HEADERS.items():
            response.headers.setdefault(name, value)
        csp = DOCS_CSP if request.url.path.startswith(DOCS_PATHS) else SITE_CSP
        response.headers.setdefault("Content-Security-Policy", csp)
        if self.hsts:
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        return response
