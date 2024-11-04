from plone.restapi.blocks_linkintegrity import SlateBlockLinksRetriever
from plone.restapi.interfaces import IBlockFieldLinkIntegrityRetriever
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from plone.dexterity.interfaces import IDexterityContent


@adapter(IDexterityContent, IBrowserRequest)
@implementer(IBlockFieldLinkIntegrityRetriever)
class SimpleCardBlockLinksRetriever(SlateBlockLinksRetriever):
    order = 200
    block_type = "testo_riquadro_semplice"
    field = "simple_card_content"


# <!-- make some block indexable -->
#   <adapter
#       factory=".indexers.AccordionBlockSearchableText"
#       name="accordion"
#       />
#   <adapter
#       factory=".indexers.AlertBlockSearchableText"
#       name="alert"
#       />
#   <adapter
#       factory=".indexers.SimpleCardBlockSearchableText"
#       name="testo_riquadro_semplice"
#       />
#   <adapter
#       factory=".indexers.CardWithImageBlockSearchableText"
#       name="testo_riquadro_immagine"
#       />
#   <adapter
#       factory=".indexers.CalloutBlockSearchableText"
#       name="callout_block"
#       />
#   <adapter
#       factory=".indexers.HeroBlockSearchableText"
#       name="hero"
#       />
#   <adapter
#       factory=".indexers.CTABlockSearchableText"
#       name="cta_block"
#       />
#   <adapter
#       factory=".indexers.GridBlockSearchableText"
#       name="gridBlock"
#       />
#   <adapter
#       factory=".indexers.SlateTableBlockSearchableText"
#       name="slateTable"
#       />
#   <adapter
#       factory=".indexers.ContactsBlockSearchableText"
#       name="contacts"
#       />
#   <adapter
#       factory=".indexers.IconBlockSearchableText"
#       name="iconBlocks"
#       />
#   <adapter
#       factory=".indexers.NumbersBlockSearchableText"
#       name="numbersBlock"
#       />
#   <adapter
#       factory=".indexers.RemoteCounterBlockSearchableText"
#       name="remote-counter"
#       />
#   <adapter
#       factory=".indexers.CountDownBlockSearchableText"
#       name="count_down"
#       />
