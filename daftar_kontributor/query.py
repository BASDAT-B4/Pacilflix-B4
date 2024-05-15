class ContributorManager:
    def get_all_contributors():
        return f"""
        SELECT * FROM contributors
        """
    
    def filter_by_penulis_skenario():
        return f"""
        SELECT c.*
        FROM contributors c
        JOIN penulis_skenario ps ON c.contributor_id = ps.contributor_id
        """
    
    def filter_by_pemain():
        return f"""
        SELECT c.*
        FROM contributors c
        JOIN pemain p ON c.contributor_id = p.contributor_id
        """
    
    def filter_by_sutradara():
        return f"""
        SELECT c.*
        FROM contributors c
        JOIN sutradara s ON c.contributor_id = s.contributor_id
        """