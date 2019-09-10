# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from design.plone.contenttypes.testing import DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that design.plone.contenttypes is properly installed."""

    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if design.plone.contenttypes is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'design.plone.contenttypes'))

    def test_browserlayer(self):
        """Test that IDesignPloneContenttypesLayer is registered."""
        from design.plone.contenttypes.interfaces import (
            IDesignPloneContenttypesLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IDesignPloneContenttypesLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['design.plone.contenttypes'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if design.plone.contenttypes is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'design.plone.contenttypes'))

    def test_browserlayer_removed(self):
        """Test that IDesignPloneContenttypesLayer is removed."""
        from design.plone.contenttypes.interfaces import \
            IDesignPloneContenttypesLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IDesignPloneContenttypesLayer,
            utils.registered_layers())
