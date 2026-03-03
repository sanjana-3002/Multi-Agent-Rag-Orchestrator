"""
Day 4: Metadata Filtering
Search within specific subsets (Q4 only, Facebook only, etc.)
COST: $0 (local filtering)
"""

from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

class MetadataFilter:
    """
    Build Qdrant filters for metadata
    
    Use cases:
    - "Only Q4 campaigns"
    - "Only Facebook ads"
    - "Campaigns from 2024"
    """
    
    @staticmethod
    def by_quarter(quarter):
        """
        Filter by quarter
        
        Example:
            filter = MetadataFilter.by_quarter("Q4")
        """
        return Filter(
            must=[
                FieldCondition(
                    key="metadata.quarter",
                    match=MatchValue(value=quarter)
                )
            ]
        )
    
    @staticmethod
    def by_year(year):
        """Filter by year"""
        return Filter(
            must=[
                FieldCondition(
                    key="metadata.year",
                    match=MatchValue(value=year)
                )
            ]
        )
    
    @staticmethod
    def by_platform(platform):
        """Filter by platform (Facebook, Instagram, etc.)"""
        return Filter(
            must=[
                FieldCondition(
                    key="metadata.platform",
                    match=MatchValue(value=platform)
                )
            ]
        )
    
    @staticmethod
    def by_campaign_type(campaign_type):
        """Filter by campaign type (social, email, search)"""
        return Filter(
            must=[
                FieldCondition(
                    key="metadata.campaign_type",
                    match=MatchValue(value=campaign_type)
                )
            ]
        )
    
    @staticmethod
    def combine_filters(quarter=None, year=None, platform=None, campaign_type=None):
        """
        Combine multiple filters with AND logic
        
        Example:
            filter = MetadataFilter.combine_filters(
                quarter="Q4",
                year=2024,
                platform="Facebook"
            )
            # Returns only Q4 2024 Facebook campaigns
        """
        
        conditions = []
        
        if quarter:
            conditions.append(
                FieldCondition(
                    key="metadata.quarter",
                    match=MatchValue(value=quarter)
                )
            )
        
        if year:
            conditions.append(
                FieldCondition(
                    key="metadata.year",
                    match=MatchValue(value=year)
                )
            )
        
        if platform:
            conditions.append(
                FieldCondition(
                    key="metadata.platform",
                    match=MatchValue(value=platform)
                )
            )
        
        if campaign_type:
            conditions.append(
                FieldCondition(
                    key="metadata.campaign_type",
                    match=MatchValue(value=campaign_type)
                )
            )
        
        if not conditions:
            return None
        
        return Filter(must=conditions)


if __name__ == "__main__":
    print("="*60)
    print("METADATA FILTER EXAMPLES")
    print("="*60)
    
    # Example 1: Q4 only
    filter_q4 = MetadataFilter.by_quarter("Q4")
    print("\nFilter 1: Q4 campaigns only")
    print(filter_q4)
    
    # Example 2: 2024 Facebook
    filter_combined = MetadataFilter.combine_filters(
        year=2024,
        platform="Facebook"
    )
    print("\nFilter 2: 2024 Facebook campaigns")
    print(filter_combined)
    
    # Example 3: Q4 2024 social media
    filter_specific = MetadataFilter.combine_filters(
        quarter="Q4",
        year=2024,
        campaign_type="social"
    )
    print("\nFilter 3: Q4 2024 social media campaigns")
    print(filter_specific)