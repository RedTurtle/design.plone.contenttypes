# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.testing import z2
from redturtle.volto.testing import RedturtleVoltoLayer
from redturtle.volto.testing import RedturtleVoltoRestApiLayer
from zope.configuration import xmlconfig

import collective.address
import collective.taxonomy

# import collective.folderishtypes
import collective.venue
import collective.volto.blocksfield
import collective.volto.cookieconsent
import collective.z3cform.datagridfield
import design.plone.contenttypes
import eea.api.taxonomy
import kitconcept.seo
import plone.app.caching
import plone.formwidget.geolocation
import redturtle.bandi
import redturtle.volto


class DesignPloneContenttypesLayer(RedturtleVoltoLayer):
    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=collective.venue)
        self.loadZCML(package=collective.volto.blocksfield)
        self.loadZCML(package=design.plone.contenttypes, context=configurationContext)
        self.loadZCML(package=plone.formwidget.geolocation)
        self.loadZCML(name="overrides.zcml", package=design.plone.contenttypes)
        xmlconfig.file(
            "configure.zcml",
            design.plone.contenttypes,
            context=configurationContext,
        )
        self.loadZCML(package=redturtle.bandi)
        self.loadZCML(package=kitconcept.seo)
        self.loadZCML(package=eea.api.taxonomy)
        self.loadZCML(package=collective.taxonomy)
        self.loadZCML(package=collective.z3cform.datagridfield)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
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


class DesignPloneContenttypesRestApiLayer(RedturtleVoltoRestApiLayer):
    def setUpZope(self, app, configurationContext):
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=collective.venue)
        self.loadZCML(package=collective.volto.blocksfield)
        self.loadZCML(package=design.plone.contenttypes, context=configurationContext)
        self.loadZCML(package=plone.formwidget.geolocation)
        self.loadZCML(package=eea.api.taxonomy)
        self.loadZCML(package=collective.taxonomy)
        self.loadZCML(package=collective.z3cform.datagridfield)
        xmlconfig.file(
            "configure.zcml",
            design.plone.contenttypes,
            context=configurationContext,
        )
        self.loadZCML(package=redturtle.bandi)
        self.loadZCML(package=kitconcept.seo)

        self.loadZCML(name="overrides.zcml", package=design.plone.contenttypes)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
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
