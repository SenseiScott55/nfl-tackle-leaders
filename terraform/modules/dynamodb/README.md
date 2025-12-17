# DynamoDB Module

This module creates a DynamoDB table for storing NFL weekly tackle and sack leaders.

## Table Design

### Primary Key Structure

- **Partition Key (PK):** `SEASON#2025`
- **Sort Key (SK):** `WEEK#01#STAT#TOTAL_TACKLES` or `WEEK#01#STAT#SACKS`

### Example Items
```json
{
  "PK": "SEASON#2025",
  "SK": "WEEK#14#STAT#TOTAL_TACKLES",
  "season": "2025",
  "week_number": 14,
  "stat_type": "TOTAL_TACKLES",
  "player_id": "4043130",
  "player_name": "Jordyn Brooks",
  "team_name": "Miami Dolphins",
  "team_abbreviation": "MIA",
  "stat_value": 155,
  "updated_at": "2025-12-16T23:00:00Z"
}
```

### Global Secondary Index

**StatTypeIndex:**
- **Hash Key:** `stat_type` (TOTAL_TACKLES or SACKS)
- **Range Key:** `week_number`
- **Purpose:** Query all weeks for a specific stat type

## Query Patterns

1. **Get both leaders for a specific week:**
```
   PK = "SEASON#2025" AND SK begins_with "WEEK#14#"
```

2. **Get all weeks for Total Tackles:**
```
   Use StatTypeIndex
   stat_type = "TOTAL_TACKLES"
```

3. **Get specific stat for specific week:**
```
   PK = "SEASON#2025" AND SK = "WEEK#14#STAT#TOTAL_TACKLES"
```

## Features

- **On-demand billing** - Pay only for what you use
- **Server-side encryption** - Data encrypted at rest
- **Point-in-time recovery** - Optional backup (disabled by default for cost)
- **Global Secondary Index** - Efficient querying by stat type
- **IAM policies** - Separate read/write policies for Lambda functions

## Usage
```hcl
module "dynamodb" {
  source = "./modules/dynamodb"

  table_name                    = "nfl_weekly_leaders"
  enable_point_in_time_recovery = false

  tags = {
    Environment = "production"
    Project     = "nfl-tackle-leaders"
  }
}
```

## Outputs

- `table_name` - DynamoDB table name
- `table_arn` - DynamoDB table ARN
- `lambda_write_policy_arn` - IAM policy ARN for write access
- `lambda_read_policy_arn` - IAM policy ARN for read access
- `gsi_name` - Global Secondary Index name

## Cost Estimate

With ~36 items per season (2 stats × 18 weeks):
- **Storage:** < $0.01/month
- **On-demand reads/writes:** < $0.25/month (4 writes/month, minimal reads)
- **Total:** < $0.50/month
```

---

## ✅ All Four Files Created!

**To add these to your project:**

1. Create the files in the exact paths shown
2. Copy the content into each file
3. Save all files

**File locations:**
```
terraform/modules/dynamodb/
├── main.tf         ✅ 
├── variables.tf    ✅
├── outputs.tf      ✅
└── README.md       ✅