from sqlalchemy import Column, Date, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# landing
class LandingSearchResultsScraped(Base):
    __tablename__ = "search_results_scraped"
    __table_args__ = {"schema": "landing"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    process_date = Column(String)
    process_file = Column(String)
    search_option_category = Column(String)
    search_option_sort = Column(String)
    product_id = Column(String)
    product_name = Column(Text)
    product_brand = Column(String)
    product_search_image = Column(Text)
    product_gender = Column(String)
    product_primary_colour = Column(String)
    product_category = Column(String)
    product_year = Column(Integer)
    product_season = Column(String)
    product_catalog_date = Column(Date)
    product_mrp = Column(Float)
    product_price = Column(Float)
    product_discount = Column(Float)
    product_rating = Column(Float)
    product_rating_count = Column(Integer)


# stage
class StageSearchResultsScraped(Base):
    __tablename__ = "search_results_scraped"
    __table_args__ = {"schema": "stage"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    process_date = Column(String)
    search_option_category = Column(String)
    search_option_sort = Column(String)
    product_id = Column(String)
    product_name = Column(Text)
    product_brand = Column(String)
    product_search_image = Column(Text)
    product_gender = Column(String)
    product_primary_colour = Column(String)
    product_category = Column(String)
    product_year = Column(Integer)
    product_season = Column(String)
    product_catalog_date = Column(Date)
    product_mrp = Column(Float)
    product_price = Column(Float)
    product_discount = Column(Float)
    product_rating = Column(Float)
    product_rating_count = Column(Integer)


# curated
class CuratedDimProduct(Base):
    __tablename__ = "dim_product"
    __table_args__ = {"schema": "curated"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, primary_key=True, index=True)
    product_name = Column(Text)
    product_brand = Column(String)
    product_search_image = Column(Text)
    product_gender = Column(String)
    product_primary_colour = Column(String)
    product_category = Column(String)
    product_year = Column(String)
    product_season = Column(String)
    product_catalog_date = Column(Date)
    created_date = Column(Date)


class CuratedFctProduct(Base):
    __tablename__ = "fct_product"
    __table_args__ = {"schema": "curated"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    process_date = Column(String, index=True)
    search_option_category = Column(String)
    search_option_sort = Column(String)
    product_id = Column(String)
    product_mrp = Column(Float)
    product_price = Column(Float)
    product_discount = Column(Float)
    product_rating = Column(Float)
    product_rating_count = Column(Integer)
