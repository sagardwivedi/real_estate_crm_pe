from django.contrib.auth.models import Group, Permission
from django_typer.management import TyperCommand


class Command(TyperCommand):
    help = "Creates and updates user roles with proper permissions"

    ROLES_PERMISSIONS: dict[str, list[str]] = {
        "Company Admin": [
            "view_customuser",
            "add_customuser",
            "change_customuser",
            "delete_customuser",
            "view_property",
            "add_property",
            "change_property",
            "delete_property",
            "view_transaction",
            "add_transaction",
            "change_transaction",
            "delete_transaction",
        ],
        "Sales Manager": [
            "view_property",
            "change_property",
            "view_transaction",
            "add_transaction",
            "change_transaction",
        ],
        "Agent": [
            "view_property",
            "change_property",
            "view_transaction",
            "add_transaction",
            "change_transaction",
        ],
    }

    def handle(self) -> None:
        """Main function to create/update groups and assign permissions."""
        self.stdout.write(self.style.NOTICE("🚀 Starting role creation/update..."))

        for role, permissions in self.ROLES_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=role)
            missing_permissions: set[str] = self.assign_permissions(group, permissions)

            action: str = "✅ Created" if created else "🔄 Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} group: {role}"))

            if missing_permissions:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️ Missing permissions: {', '.join(missing_permissions)}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("🎉 All roles updated successfully!"))

    def assign_permissions(self, group: Group, permissions: list[str]) -> set[str]:
        """
        Assigns the specified permissions to a group and returns any missing ones.

        Args:
            group (Group): The Django Group object to assign permissions to.
            permissions (List[str]): A list of permission codenames.

        Returns:
            Set[str]: A set of missing permission codenames.
        """
        permission_objs = Permission.objects.filter(codename__in=permissions)
        found_codenames: set[str] = set(
            permission_objs.values_list("codename", flat=True)
        )

        # Find missing permissions
        missing_permissions: set[str] = set(permissions) - found_codenames
        group.permissions.set(permission_objs)
        group.save()

        return missing_permissions
