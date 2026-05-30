"""Logistics problem definitions shared across application modules."""

FREIGHT_PROBLEM = """You need to ship 500 kg of electronics from Shenzhen, China to Berlin, Germany.

Option A (Air Freight): $2.50/kg, 3 days transit, $0.50/kg insurance
Option B (Sea Freight): $0.40/kg, 35 days transit, $0.15/kg insurance
Option C (Rail Freight): $0.90/kg, 18 days transit, $0.25/kg insurance

The electronics lose 2% of their value per week in transit due to
depreciation. Total cargo value is $200,000.

Which option has the lowest TOTAL cost including depreciation?"""

WAREHOUSE_PROBLEM = """You are expanding your logistics network in Southeast Asia.
You need one new warehouse to serve: Bangkok, Ho Chi Minh City,
Manila, and Jakarta.

Constraints:
- Each warehouse costs $12,000/month to operate
- Shipping cost per pallet: $0.50 per km
- You ship ~150 pallets/month TOTAL to these 4 cities
- The % of volume per city: Bangkok 30%, HCMC 25%, Manila 20%, Jakarta 25%

Candidate warehouse locations and distances (km) to each city:
Location A (Singapore): BKK=1420, HCMC=1090, MNL=2400, JKT=890
Location B (Kuala Lumpur): BKK=1180, HCMC=1050, MNL=2500, JKT=1170
Location C (Bangkok): BKK=50, HCMC=1050, MNL=2200, JKT=2300

Where should you place the warehouse to minimize total monthly cost?"""

INVENTORY_PROBLEM = """You manage 3 warehouses (North, Central, South) stocking the same SKU.
Current inventory and daily demand:

Warehouse  | Current Stock | Daily Demand | Reorder Cost | Holding Cost/unit/day
North      | 240 units     | 30/day       | $150         | $0.40
Central    | 90 units      | 25/day       | $150         | $0.35
South      | 450 units     | 20/day       | $150         | $0.50

Lead time from supplier: 7 days for all. A stockout costs $12/unit.
You have a budget of $3,000 for this replenishment cycle.
How much should you send to EACH warehouse to minimize total costs?"""
