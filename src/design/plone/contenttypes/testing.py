# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PloneRestApiDXLayer
from plone.testing import z2

import collective.address
import collective.dexteritytextindexer
import collective.folderishtypes
import collective.venue
import collective.volto.cookieconsent
import design.plone.contenttypes
import plone.formwidget.geolocation
import plone.restapi
import redturtle.volto
import redturtle.bandi
from zope.configuration import xmlconfig


class DesignPloneContenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.dexteritytextindexer)
        self.loadZCML(package=collective.folderishtypes)
        self.loadZCML(package=collective.venue)
        self.loadZCML(package=collective.volto.cookieconsent)
        self.loadZCML(
            package=design.plone.contenttypes, context=configurationContext
        )
        self.loadZCML(package=plone.formwidget.geolocation)
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=redturtle.volto)
        self.loadZCML(name="overrides.zcml", package=design.plone.contenttypes)
        xmlconfig.file(
            "configure.zcml",
            design.plone.contenttypes,
            context=configurationContext,
        )
        self.loadZCML(package=redturtle.bandi)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "design.plone.contenttypes:default")


DESIGN_PLONE_CONTENTTYPES_FIXTURE = DesignPloneContenttypesLayer()


DESIGN_PLONE_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_CONTENTTYPES_FIXTURE,),
    name="DesignPloneContenttypesLayer:IntegrationTesting",
)


DESIGN_PLONE_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_CONTENTTYPES_FIXTURE,),
    name="DesignPloneContenttypesLayer:FunctionalTesting",
)


class DesignPloneContenttypesRestApiLayer(PloneRestApiDXLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(DesignPloneContenttypesRestApiLayer, self).setUpZope(
            app, configurationContext
        )

        self.loadZCML(package=collective.dexteritytextindexer)
        self.loadZCML(package=collective.folderishtypes)
        self.loadZCML(package=collective.venue)
        self.loadZCML(package=collective.volto.cookieconsent)
        self.loadZCML(package=design.plone.contenttypes)
        self.loadZCML(name="overrides.zcml", package=design.plone.contenttypes)
        self.loadZCML(package=plone.formwidget.geolocation)
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=redturtle.volto)
        self.loadZCML(package=redturtle.bandi)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "design.plone.contenttypes:default")


DESIGN_PLONE_CONTENTTYPES_API_FIXTURE = DesignPloneContenttypesRestApiLayer()
DESIGN_PLONE_CONTENTTYPES_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_CONTENTTYPES_API_FIXTURE,),
    name="DesignPloneContenttypesRestApiLayer:Integration",
)

DESIGN_PLONE_CONTENTTYPES_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_CONTENTTYPES_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="DesignPloneContenttypesRestApiLayer:Functional",
)
