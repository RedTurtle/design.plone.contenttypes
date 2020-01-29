# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import design.plone.contenttypes


class KuteContenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=design.plone.contenttypes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'design.plone.contenttypes:default')


KUTE_CONTENTTYPES_FIXTURE = KuteContenttypesLayer()


KUTE_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(KUTE_CONTENTTYPES_FIXTURE,),
    name='KuteContenttypesLayer:IntegrationTesting',
)


KUTE_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(KUTE_CONTENTTYPES_FIXTURE,),
    name='KuteContenttypesLayer:FunctionalTesting',
)


KUTE_CONTENTTYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        KUTE_CONTENTTYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='KuteContenttypesLayer:AcceptanceTesting',
)
