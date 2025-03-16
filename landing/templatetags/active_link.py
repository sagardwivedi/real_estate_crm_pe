import hashlib
import json

from django import template
from django.conf import settings
from django.core.cache import cache
from django.urls import NoReverseMatch, reverse
from django.utils.encoding import escape_uri_path

register = template.Library()


def generate_safe_cache_key(viewname, args, kwargs):
    """Generate a safe and unique cache key using an MD5 hash."""
    key_data = {"viewname": viewname, "args": args, "kwargs": kwargs}
    key_string = json.dumps(key_data, sort_keys=True, default=str)
    return f"reverse_url_{hashlib.md5(key_string.encode()).hexdigest()}"


@register.simple_tag(takes_context=True)
def active_link(
    context,
    viewnames,
    css_class=None,
    css_inactive_class=None,
    strict=None,
    *args,
    **kwargs,
):
    """
    Determines if a link should be marked as active based on the current request URL.

    Args:
        context: The template context.
        viewnames: Pipe-separated string of view names to check.
        css_class: CSS class to apply when active (default: 'active').
        css_inactive_class: CSS class to apply when inactive (default: '').
        strict: If True, requires an exact match; otherwise, checks prefix.
        *args: Positional arguments for URL reversal.
        **kwargs: Keyword arguments for URL reversal.

    Returns:
        The appropriate CSS class based on URL matching.
    """
    # Default settings
    css_class = css_class or getattr(settings, "ACTIVE_LINK_CSS_CLASS", "active")
    css_inactive_class = css_inactive_class or getattr(
        settings, "ACTIVE_LINK_CSS_INACTIVE_CLASS", ""
    )
    strict = (
        strict if strict is not None else getattr(settings, "ACTIVE_LINK_STRICT", False)
    )

    # Get request object
    request = context.get("request")
    if not request:
        return css_inactive_class
    request_path = escape_uri_path(request.path)

    # Extract resolver kwargs
    resolver_kwargs = getattr(request.resolver_match, "kwargs", {}).copy()
    merged_kwargs = {**resolver_kwargs, **kwargs}

    # Check each viewname
    for viewname in map(str.strip, viewnames.split("||")):
        cache_key = generate_safe_cache_key(viewname, args, merged_kwargs)
        path = cache.get(cache_key)

        if path is None:
            try:
                path = reverse(viewname, args=args, kwargs=merged_kwargs)
                cache.set(cache_key, path, timeout=300)  # Cache for 5 minutes
            except NoReverseMatch:
                continue  # Skip invalid view names

        # Determine if the link should be active
        if (strict and request_path == path) or (
            not strict and request_path.startswith(path)
        ):
            return css_class

    return css_inactive_class
