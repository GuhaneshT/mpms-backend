import unittest

from core.rbac import AppRole, Permission, build_user_context, has_permission, resolve_role


class RBACTests(unittest.TestCase):
    def test_app_metadata_role_takes_precedence(self):
        role, source = resolve_role(
            {
                "role": "authenticated",
                "app_metadata": {"rbac_role": "service_manager", "role": "viewer"},
                "user_metadata": {"role": "admin"},
            }
        )

        self.assertEqual(role, AppRole.SERVICE_MANAGER)
        self.assertEqual(source, "app_metadata.rbac_role")

    def test_reserved_supabase_role_falls_back_to_viewer(self):
        user = build_user_context(
            {
                "sub": "user-1",
                "email": "viewer@example.com",
                "role": "authenticated",
                "app_metadata": {},
                "user_metadata": {},
            }
        )

        self.assertEqual(user["role"], AppRole.VIEWER.value)
        self.assertTrue(has_permission(user, Permission.DASHBOARD_READ))
        self.assertFalse(has_permission(user, Permission.CUSTOMERS_WRITE))

    def test_custom_permissions_extend_role_defaults(self):
        user = build_user_context(
            {
                "sub": "user-2",
                "email": "tech@example.com",
                "app_metadata": {"role": "service_engineer"},
                "user_metadata": {"permissions": ["customers:read"]},
            }
        )

        self.assertEqual(user["role"], AppRole.SERVICE_ENGINEER.value)
        self.assertTrue(has_permission(user, Permission.SERVICE_CALLS_RESOLVE))
        self.assertTrue(has_permission(user, Permission.CUSTOMERS_READ))


if __name__ == "__main__":
    unittest.main()
