from enum import Enum
from dataclasses import dataclass
from typing import Union, Tuple, List
import os


class HazardType(Enum):
    VOLCANOES    = 1
    EARTHQUAKES  = 2

    @classmethod
    def from_string(cls, string: str) -> "HazardType":
        """
        Example: HazardType.from_string("volcanoes")

        :param string: Either "volcanoes" or "earthquakes"
        :raises ValueError when `string not in ("volcanoes", "earthquakes")
        """
        upper_string = string.upper()
        if upper_string in HazardType.__members__:
            return HazardType[upper_string]
        else:
            raise ValueError("{} is not a valid hazard type".format(string))

    @classmethod
    def to_string(cls, hazard_type: "HazardType") -> str:
        """
        Converts a hazard type into a lowercase string.
        Examples: HazardType.to_string(HazardType.VOLCANOES) returns 'volcanoes'
                  HazardType.to_string(HazardType.EARTHQUAKES) returns 'earthquakes'
        """
        return hazard_type.name.lower()


class ImageType(Enum):
    GEO_BACKSCATTER       = 1
    GEO_COHERENCE         = 2
    GEO_INTERFEROGRAM     = 3
    ORTHO_BACKSCATTER     = 4
    ORTHO_COHERENCE       = 5
    ORTHO_INTERFEROGRAM   = 6


    @classmethod
    def from_string(cls, string: str) -> "ImageType":
        upper_string = string.upper()
        if upper_string in ImageType.__members__:
            return ImageType[upper_string]
        else:
            raise ValueError("{} is not a valid image type".format(string))


    @classmethod
    def to_string(cls, image_type: "ImageType") -> str:
        return image_type.name.lower()

class DatabaseSuccess(Enum):
    SUCCESS = 1
    FAILURE = 2


@dataclass
class LatLong:
    lat: float
    long: float


class Date:
    """
    Class for dates of the format YYYYMMDD

    Example:
        >>> today = Date("20190411")
        >>> print(today.date)
        20190411
        >>> print("The year is {0} in the {1}th month".format(today.date[:4], today.date[4:6]))
        The year is 2019 in the 04th month
    """

    def __init__(self, date: str):
        if self.is_valid_date(date):
            self.date = date
        else:
            raise ValueError("The date {0} is not a valid date of the form \"YYYYMMDD\"".format(date))

    def is_valid_date(possible_date: str):
        """
        Checks if date is of format "YYYYMMDD"
        """
        if len(possible_date) == 8:
            if possible_date.isdigit():
                if 1 <= int(possible_date[4:6]) <= 12:
                    if 1 <= int(possible_date[6:]) <= 31:
                        return True
        return False


@dataclass
class DateRange:
    """
    This class is used for filtering images by a range of dates.
    If `end = None`, then the date range ends on the current date
    """
    start: Date
    end: Union[Date, None]


class ImageURL():
    """
    Creates and validates a URL
    """
    def __init__(self, url: str):
        if self.is_valid_url(url):
            self.url = url
        else:
            raise ValueError("The url {0} is not a valid URL".format(url))

    # TODO: Add further validation
    def is_valid_url(url):
        valid_extensions = [".jpg", ".png", ".tiff", ".gif"]
        filename, file_extension = os.path.splitext(url)
        if filename[0] is not "/" or file_extension not in valid_extensions:
            return False
        return True


class Location:
    def __init__(self, center: LatLong, north: LatLong, south: LatLong, east: LatLong, west: LatLong):
        
        valid_lats = self.validate_latitudes(north, south)
        valid_lons = self.validate_longitudes(east, west)

        if valid_lats and valid_lons:
            self.center = center
            self.bounding_box = {}
            self.bounding_box["North"] = north
            self.bounding_box["South"] = south
            self.bounding_box["East"] = east
            self.bounding_box["West"] = west
        else:
            raise Exception()

    @classmethod
    def validate_latitudes(cls, north, south):
        return -90 < float(north) < 90 and -90 < float(south) < 90

    @classmethod
    def validate_longitudes(cls, east, west):
        return float(east) < 180 and float(west) > -180


@dataclass
class Satellite:
    satellite_id: str
    satellite_name: str
    ascending: bool        


@dataclass
class HazardInfo:
    location: Location
    last_updated: Date
    hazard_id: str
    hazard_type: HazardType
    name: str


@dataclass
class Hazard:
    hazard_id: str
    name: str
    hazard_type: HazardType
    location: Location
    last_updated: Date


@dataclass
class Image:
    hazard_id: str
    satellite_id: str
    image_type: ImageType
    image_date: Date
    raw_image_url: ImageURL
    tif_image_url: ImageURL
    compressed_image_url: ImageURL
    modified_image_url: ImageURL
    
    
@dataclass
class HazardInfoFilter:
    satellite_ids: Tuple[List[str], None]
    image_type: Tuple[List[ImageType], None]
    date_range: Union[DateRange, None]
    last_n_images: Union[int, None]
