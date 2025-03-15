from django import template
from django.conf import settings
from django.core.cache import cache
from django.urls import NoReverseMatch, reverse
from django.utils.encoding import escape_uri_path

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(
    context,
    viewnames,
    css_class=None,
    css_inactive_class="",
    strict=None,
    *args,
    **kwargs,
):
    """
    Template tag to determine if a link is active based on the current URL.

    Args:
        context: Template context.
        viewnames: A string of view names separated by '||' to check against.
        css_class: CSS class to apply if the link is active.
        css_inactive_class: CSS class to apply if the link is inactive.
        strict: If True, performs an exact match; otherwise, performs a prefix match.
        *args: Positional arguments for URL reversal.
        **kwargs: Keyword arguments for URL reversal.

    Returns:
        The active or inactive CSS class based on the current URL.
    """
    # Default settings
    css_class = css_class or getattr(settings, "ACTIVE_LINK_CSS_CLASS", "active")
    css_inactive_class = css_inactive_class or getattr(
        settings, "ACTIVE_LINK_CSS_INACTIVE_CLASS", ""
    )
    strict = (
        strict if strict is not None else getattr(settings, "ACTIVE_LINK_STRICT", False)
    )

    # Get the request object from the context
    request = context.get("request")
    if request is None:
        return css_inactive_class  # No request object, return inactive class

    # Get resolver kwargs from the request
    resolver_kwargs = {}
    if hasattr(request, "resolver_match") and hasattr(request.resolver_match, "kwargs"):
        resolver_kwargs = request.resolver_match.kwargs.copy()

    # Merge resolver kwargs with provided kwargs
    merged_kwargs = {**resolver_kwargs, **kwargs}

    # Escape the request path for comparison
    request_path = escape_uri_path(request.path)

    # Check each viewname for a match
    views = viewnames.split("||")
    for viewname in views:
        viewname = viewname.strip()

        # Generate a cache key for the reversed URL
        cache_key = f"reverse_url_{viewname}_{args}_{tuple(merged_kwargs.items())}"
        path = cache.get(cache_key)

        if path is None:
            try:
                # Reverse the URL and cache it
                path = reverse(viewname, args=args, kwargs=merged_kwargs)
                cache.set(cache_key, path, timeout=300)  # Cache for 5 minutes
            except NoReverseMatch:
                continue  # Skip this view if it doesn't resolve

        # Check if the request path matches the reversed URL
        if strict:
            active = request_path == path
        else:
            active = request_path.startswith(path) or path.startswith(request_path)

        if active:
            return css_class  # Return the active class if a match is found

    return css_inactive_class  # Return the inactive class if no match is found
