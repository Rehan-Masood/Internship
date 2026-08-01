class FlightData:
    """Holds the structured details of a single flight offer."""

    def __init__(self, price, origin_city, origin_airport, destination_city,
                 destination_airport, out_date, return_date, stops=0):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

    @staticmethod
    def from_sky_scrapper_itinerary(itinerary):
        """Builds a FlightData object from one raw itinerary returned by the Air Scraper API.
        NOTE: if the field names below don't match what you see printed from a live call,
        share the printed raw itinerary and this parsing can be adjusted to match exactly."""
        price = itinerary["price"]["raw"]

        outbound_leg = itinerary["legs"][0]
        origin_code = outbound_leg["origin"]["displayCode"]
        destination_code = outbound_leg["destination"]["displayCode"]
        origin_city = outbound_leg["origin"].get("city", origin_code)
        destination_city = outbound_leg["destination"].get("city", destination_code)
        out_date = outbound_leg["departure"].split("T")[0]
        stops = outbound_leg.get("stopCount", 0)

        return_date = None
        if len(itinerary["legs"]) > 1:
            inbound_leg = itinerary["legs"][1]
            return_date = inbound_leg["departure"].split("T")[0]

        return FlightData(
            price=price,
            origin_city=origin_city,
            origin_airport=origin_code,
            destination_city=destination_city,
            destination_airport=destination_code,
            out_date=out_date,
            return_date=return_date,
            stops=stops,
        )