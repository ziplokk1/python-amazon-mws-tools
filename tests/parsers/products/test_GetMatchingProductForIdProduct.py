from unittest import TestCase
from unittest import TestSuite
from unittest import main
from unittest import makeSuite

from mwstools.parsers.products import GetMatchingProductForIdProduct


class TestGetMatchingProductForIdProduct(TestCase):

    body = """
    <Product xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"
                  xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
        <Identifiers>
            <MarketplaceASIN>
                <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                <ASIN>B007P5RN9Y</ASIN>
            </MarketplaceASIN>
        </Identifiers>
        <AttributeSets>
            <ns2:ItemAttributes xml:lang="en-US">
                <ns2:Binding>Misc.</ns2:Binding>
                <ns2:Brand>Darice</ns2:Brand>
                <ns2:Color>Black</ns2:Color>
                <ns2:Department>womens</ns2:Department>
                <ns2:Feature>The largest space has 11 Inch of hanging clearance and the three smaller spaces
                    each have a hanging clearance of 2-1/2 Inch
                </ns2:Feature>
                <ns2:Feature>Overall dimensions are 12x3-1/2x14 Inch</ns2:Feature>
                <ns2:Feature>The entire piece is black painted metal</ns2:Feature>
                <ns2:ItemDimensions>
                    <ns2:Height Units="inches">13.00</ns2:Height>
                    <ns2:Length Units="inches">14.00</ns2:Length>
                    <ns2:Width Units="inches">3.65</ns2:Width>
                    <ns2:Weight Units="pounds">1.39</ns2:Weight>
                </ns2:ItemDimensions>
                <ns2:Label>Darice</ns2:Label>
                <ns2:ListPrice>
                    <ns2:Amount>24.99</ns2:Amount>
                    <ns2:CurrencyCode>USD</ns2:CurrencyCode>
                </ns2:ListPrice>
                <ns2:Manufacturer>Darice</ns2:Manufacturer>
                <ns2:ManufacturerMinimumAge Units="months">120.00</ns2:ManufacturerMinimumAge>
                <ns2:MaterialType>not-applicable</ns2:MaterialType>
                <ns2:MetalType>base</ns2:MetalType>
                <ns2:Model>2025-418</ns2:Model>
                <ns2:NumberOfItems>1</ns2:NumberOfItems>
                <ns2:PackageDimensions>
                    <ns2:Height Units="inches">3.60</ns2:Height>
                    <ns2:Length Units="inches">16.00</ns2:Length>
                    <ns2:Width Units="inches">12.40</ns2:Width>
                    <ns2:Weight Units="pounds">1.40</ns2:Weight>
                </ns2:PackageDimensions>
                <ns2:PackageQuantity>1</ns2:PackageQuantity>
                <ns2:PartNumber>2025-418</ns2:PartNumber>
                <ns2:ProductGroup>Art and Craft Supply</ns2:ProductGroup>
                <ns2:ProductTypeName>HOME</ns2:ProductTypeName>
                <ns2:Publisher>Darice</ns2:Publisher>
                <ns2:SmallImage>
                    <ns2:URL>http://ecx.images-amazon.com/images/I/51%2Bc1vQkVXL._SL75_.jpg</ns2:URL>
                    <ns2:Height Units="pixels">75</ns2:Height>
                    <ns2:Width Units="pixels">64</ns2:Width>
                </ns2:SmallImage>
                <ns2:Studio>Darice</ns2:Studio>
                <ns2:Title>Darice Metal Jewelry Display Shelf, Black</ns2:Title>
            </ns2:ItemAttributes>
        </AttributeSets>
        <Relationships/>
        <SalesRankings>
            <SalesRank>
                <ProductCategoryId>art_and_craft_supply_display_on_website</ProductCategoryId>
                <Rank>361960</Rank>
            </SalesRank>
            <SalesRank>
                <ProductCategoryId>16350341</ProductCategoryId>
                <Rank>1510</Rank>
            </SalesRank>
        </SalesRankings>
    </Product>
    """

    def setUp(self):
        self.parser = GetMatchingProductForIdProduct.load(self.body)

    def test_asin(self):
        self.assertEqual(self.parser.asin, 'B007P5RN9Y')


__all__ = [
    TestGetMatchingProductForIdProduct
]


def suite():
    s = TestSuite()
    for a in __all__:
        s.addTest(makeSuite(a))
    return s


if __name__ == '__main__':
    main(defaultTest='suite')
