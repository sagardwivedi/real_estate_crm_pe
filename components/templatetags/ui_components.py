from django import template
from django.templatetags.static import static
from django.urls import reverse

register = template.Library()


@register.inclusion_tag("button.html")
def ui_button(text="Click me", color="primary", size="md"):
    color_classes = {
        "primary": "bg-primary-600 dark:bg-primary-500 text-white hover:bg-primary-700 dark:hover:bg-primary-600",
        "white": "bg-white dark:bg-gray-800 text-primary-600 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-700",
        "gray": "border-2 border-white/20 text-primary-50 dark:text-gray-300 hover:border-white/40",
    }
    size_classes = {
        "sm": "px-4 py-2 text-sm",
        "md": "px-6 py-2.5 text-base",
        "lg": "px-8 py-4 text-lg",
    }

    return {
        "text": text,
        "color_class": color_classes.get(color, color_classes["primary"]),
        "size_class": size_classes.get(size, size_classes["md"]),
    }


@register.inclusion_tag("link.html")
def ui_link(
    text="Click me",
    href="#",
    target="_self",
    rel="noopener noreferrer",
    color="primary",
    size="md",
    url_name=None,
    is_button=False,
):
    """
    A Django template tag to render a link that can optionally be styled as a button.

    Args:
        text (str): The link text.
        href (str): The URL the link points to. Defaults to '#'.
        target (str): The target for the link (e.g., '_self', '_blank').
        rel (str): The rel attribute for the link.
        color (str): The color style for the link/button.
        size (str): The size of the button if is_button=True.
        url_name (str): If provided, resolves the URL using Django's reverse lookup.
        is_button (bool): Whether the link should be styled as a button.

    Returns:
        dict: A context dictionary with attributes to render the link.
    """

    # Resolve URL if `url_name` is provided
    if url_name:
        href = reverse(url_name)

    # Define color and size classes for button styling
    color_classes = {
        "primary": "bg-primary-600 dark:bg-primary-500 text-white hover:bg-primary-700 dark:hover:bg-primary-600",
        "white": "bg-white dark:bg-gray-800 text-primary-600 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-700",
        "gray": "border-2 border-white/20 text-primary-50 dark:text-gray-300 hover:border-white/40",
    }

    size_classes = {
        "sm": "px-4 py-2 text-sm",
        "md": "px-6 py-2.5 text-base",
        "lg": "px-8 py-4 text-lg",
    }

    # Default button classes
    button_class = (
        color_classes.get(color, color_classes["primary"])
        + " "
        + size_classes.get(size, size_classes["md"])
    )

    # Prepare the link attributes
    link_attributes = {
        "href": href,
        "target": target,
        "rel": rel,
        "class": color_classes.get(color, color_classes["primary"]),
    }

    # If the link should be styled as a button
    if is_button:
        link_attributes["class"] = (
            f"{button_class} inline-block rounded-lg font-medium text-center no-underline"
        )

    return {
        "text": text,
        "link_attributes": link_attributes,
        "is_button": is_button,
    }


@register.inclusion_tag("card.html")
def ui_card(title, content, icon=None):
    if icon:
        icon = static(icon)  # Convert to full static URL
    return {"title": title, "content": content, "icon": icon}


@register.inclusion_tag("alert.html")
def ui_alert(message="This is an alert!", type="info"):
    type_classes = {
        "info": "bg-blue-100 text-blue-800 border-blue-500",
        "warning": "bg-yellow-100 text-yellow-800 border-yellow-500",
        "error": "bg-red-100 text-red-800 border-red-500",
        "success": "bg-green-100 text-green-800 border-green-500",
    }
    alert_class = type_classes.get(type, "bg-gray-100 text-gray-800 border-gray-500")
    return {"message": message, "alert_class": alert_class}
