def reduce_to_22(n: int) -> int:
    """
    Reduces a number to the range [1, 22].
    If the number is greater than 22, its digits are summed.
    Example: 23 -> 2 + 3 = 5.
    If the result is still > 22, it repeats (though rare for sums of 3 single digits).
    """
    if n <= 22:
        return n
    while n > 22:
        n = sum(int(digit) for digit in str(n))
    return n

class MatrixService:
    @staticmethod
    def calculate_matrix(birth_date):
        """
        Calculates the complete Matrix of Destiny (Ladini Matrix).
        
        Args:
            birth_date (datetime.date): The user's birth date.
            
        Returns:
            dict: A dictionary containing all nodes of the matrix.
        """
        day = birth_date.day
        month = birth_date.month
        year = birth_date.year
        
        # 1. Main Points (Personal Square)
        # A: Left (Personality, Society)
        a = reduce_to_22(day)
        # B: Top (Connection to Divine, Talents)
        b = reduce_to_22(month)
        # C: Right (Material, Money)
        year_sum = sum(int(d) for d in str(year))
        c = reduce_to_22(year_sum)
        # D: Bottom (Karmic Tail, Past lives)
        d = reduce_to_22(a + b + c)
        # E: Center (Comfort Zone)
        e = reduce_to_22(a + b + c + d)
        
        # 2. Clan Points (Diagonal Square)
        # F: Top-Left (Father's lineage)
        f = reduce_to_22(a + b)
        # G: Top-Right (Mother's lineage)
        g = reduce_to_22(b + c)
        # H: Bottom-Right (Mother's lineage)
        h = reduce_to_22(c + d)
        # I: Bottom-Left (Father's lineage)
        i = reduce_to_22(d + a)
        
        # 3. Internal Nodes (Inner circle)
        j = reduce_to_22(a + e)
        k = reduce_to_22(b + e)
        l = reduce_to_22(c + e)
        m = reduce_to_22(d + e)
        
        # 4. Karmic Tail Line (D, N, M)
        n = reduce_to_22(d + m)
        
        # 5. Relationship and Money Channels
        # R: Central point of the relation/money bridge
        r = reduce_to_22(l + m)
        # R1: Love Point (between center and relation-center)
        # Actually R1 is often closer to M (karmic line side)
        r1 = reduce_to_22(r + m)
        # R2: Money Point (between relation-center and C)
        r2 = reduce_to_22(r + l)
        
        # 6. Destinies
        # Personal (to 40y)
        sky = reduce_to_22(b + d)
        earth = reduce_to_22(a + c)
        destiny_personal = reduce_to_22(sky + earth)
        
        # Social (40-60y)
        male = reduce_to_22(f + h)
        female = reduce_to_22(g + i)
        destiny_social = reduce_to_22(male + female)
        
        # Spiritual (General)
        destiny_spiritual = reduce_to_22(destiny_personal + destiny_social)
        
        # 7. Yearly Cycle Preparation (Every 1.25 years)
        # Nodes for every 10 years
        # 0: A, 10: F, 20: B, 30: G, 40: C, 50: H, 60: D, 70: I, 80: A
        years = {
            0: a, 10: f, 20: b, 30: g, 40: c, 50: h, 60: d, 70: i
        }
        
        # Fill in 5-year intervals
        years[5] = reduce_to_22(years[0] + years[10])
        years[15] = reduce_to_22(years[10] + years[20])
        years[25] = reduce_to_22(years[20] + years[30])
        years[35] = reduce_to_22(years[30] + years[40])
        years[45] = reduce_to_22(years[40] + years[50])
        years[55] = reduce_to_22(years[50] + years[60])
        years[65] = reduce_to_22(years[60] + years[70])
        years[75] = reduce_to_22(years[70] + years[0]) # Wrap around
        
        return {
            "main": {"A": a, "B": b, "C": c, "D": d, "E": e},
            "clan": {"F": f, "G": g, "H": h, "I": i},
            "inner": {"J": j, "K": k, "L": l, "M": m},
            "karmic_tail": [d, n, m],
            "channels": {
                "love": r1,
                "money": r2,
                "bridge": r
            },
            "destiny": {
                "personal": destiny_personal,
                "social": destiny_social,
                "spiritual": destiny_spiritual
            },
            "yearly_cycle": years
        }

if __name__ == "__main__":
    # Test with a date: March 15, 1994
    from datetime import date
    test_date = date(1994, 3, 15)
    res = MatrixService.calculate_matrix(test_date)
    print(res)
