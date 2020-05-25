# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.folderishtypes
import design.plone.contenttypes
import collective.venue
import plone.formwidget.geolocation
import plone.restapi


class DesignPloneContenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.folderishtypes)
        self.loadZCML(package=collective.venue)
        self.loadZCML(package=plone.formwidget.geolocation)
        self.loadZCML(package=design.plone.contenttypes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'design.plone.contenttypes:default')


DESIGN_PLONE_CONTENTTYPES_FIXTURE = DesignPloneContenttypesLayer()


DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_CONTENTTYPES_FIXTURE,),
    name='DesignPloneContenttypesLayer:IntegrationTesting',
)


DESIGN_PLONE_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_CONTENTTYPES_FIXTURE,),
    name='DesignPloneContenttypesLayer:FunctionalTesting',
)


DESIGN_PLONE_CONTENTTYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        DESIGN_PLONE_CONTENTTYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='DesignPloneContenttypesLayer:AcceptanceTesting',
)
