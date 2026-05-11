import pandas as pd
import os

class AssociationRecommender:
    """
    Class for recommending products based on association rules from Instacart data.
    Supports different clusters with custom rules for each segment.
    """

    def __init__(self, cluster: int):
        """
        Initialize the recommender for a specific cluster.

        Args:
            cluster (int): The cluster number (0, 1, or 2) to load rules from.
        """
        self.cluster = cluster
        self.rules_file = f"Rule/Association_Rules_Cluster_{cluster}.csv"
        self.mapping = {}  # Mapping: antecedent (str) -> list of (consequent (str), confidence (float))

        self.load_rules()

    def load_rules(self):
        """
        Load association rules from the CSV file for the specified cluster.
        Parses antecedents and consequents, creates mapping for recommendations.
        """
        if not os.path.exists(self.rules_file):
            raise FileNotFoundError(f"Rules file for cluster {self.cluster} not found: {self.rules_file}")

        df = pd.read_csv(self.rules_file)

        # Assuming columns: Rule, Antecedents, Consequents, Support, Confidence, Lift
        # Antecedents and Consequents are already strings without {}, so no need to parse further
        for _, row in df.iterrows():
            antecedent = row['Antecedents'].strip()
            consequent = row['Consequents'].strip()
            confidence = row['Confidence']

            if antecedent not in self.mapping:
                self.mapping[antecedent] = []
            self.mapping[antecedent].append((consequent, confidence))

    def get_all_products(self):
        """
        Get a sorted list of all unique products from the rules.

        Returns:
            list: Sorted list of product names.
        """
        products = set()
        for ant in self.mapping:
            products.add(ant)
        for recs in self.mapping.values():
            for cons, _ in recs:
                products.add(cons)
        return sorted(list(products))

    def get_top_products_by_support(self, top_n: int = 20):
        """
        Get top products by highest support from the rules.

        Returns:
            list: List of product names sorted by max support descending.
        """
        product_support = {}
        # Reload df to get support
        if os.path.exists(self.rules_file):
            df = pd.read_csv(self.rules_file)
            for _, row in df.iterrows():
                ant = row['Antecedents'].strip()
                cons = row['Consequents'].strip()
                support = row['Support']
                
                if ant not in product_support:
                    product_support[ant] = support
                else:
                    product_support[ant] = max(product_support[ant], support)
                
                if cons not in product_support:
                    product_support[cons] = support
                else:
                    product_support[cons] = max(product_support[cons], support)
        
        sorted_products = sorted(product_support.items(), key=lambda x: x[1], reverse=True)
        return [prod for prod, _ in sorted_products[:top_n]]

    def recommend(self, cart: list, top_n: int = 5):
        """
        Recommend products based on the current cart using association rules.

        Logic:
        - For each product in cart, find rules where it is antecedent.
        - For each consequent, calculate score as max confidence from any cart item.
        - Exclude products already in cart.
        - Return top_n recommendations sorted by score descending.

        Args:
            cart (list): List of product names in the cart.
            top_n (int): Number of top recommendations to return.

        Returns:
            list: List of tuples (product, score) for recommendations.
        """
        score = {}
        for product in cart:
            if product in self.mapping:
                for consequent, confidence in self.mapping[product]:
                    if consequent not in cart:
                        # Score is max confidence for this consequent from any cart item
                        score[consequent] = max(score.get(consequent, 0), confidence)

        # If direct recommendations are fewer than requested, add popular fallback items
        if len(score) < top_n:
            fallback = {}
            for antecedent, consequents in self.mapping.items():
                for consequent, confidence in consequents:
                    if consequent not in cart and consequent not in score:
                        fallback[consequent] = max(fallback.get(consequent, 0), confidence)

            for consequent, confidence in sorted(fallback.items(), key=lambda x: x[1], reverse=True):
                if len(score) >= top_n:
                    break
                score[consequent] = confidence

        sorted_recommendations = sorted(score.items(), key=lambda x: x[1], reverse=True)
        return sorted_recommendations[:top_n]