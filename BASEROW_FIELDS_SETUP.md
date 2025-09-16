# 📋 Baserow CRM Fields Setup Guide

## Current Status
- **Baserow Table**: 698
- **Current Fields**: Name (text)
- **Missing Fields**: 40 CRM/Marketing fields needed

## 🛠️ Manual Field Creation Required

Your API token can create rows but not fields. Create these CRM fields manually:

### Step-by-Step Instructions:

1. **Open Baserow**: http://localhost:8080/database/174/table/698
2. **Click the "+" button** next to existing columns to add new fields
3. **Create each field** with these exact specifications:

## 📝 Required CRM Fields (40 total):

### Personal Information
| Field Name       | Field Type    | Description                    |
|------------------|---------------|--------------------------------|
| first_name       | Text          | Contact's first name           |
| last_name        | Text          | Contact's last name            |
| full_name        | Text          | Complete full name             |
| email            | Email         | Email address                  |
| phone_numbers    | Phone number  | Phone number                   |

### Professional Information  
| Field Name          | Field Type    | Description                    |
|---------------------|---------------|--------------------------------|
| linkedin_url        | URL           | LinkedIn profile URL           |
| account_linkedin    | Text          | LinkedIn username/handle       |
| headline            | Text          | Professional headline          |
| title               | Text          | Job title/position             |
| designation         | Text          | Job designation/level          |
| about               | Long text     | Personal bio/summary           |
| skills              | Long text     | Skills and competencies        |

### Contact Location
| Field Name       | Field Type    | Description                    |
|------------------|---------------|--------------------------------|
| contact_city     | Text          | Contact's city                 |
| contact_state    | Text          | Contact's state/province       |
| contact_country  | Text          | Contact's country              |

### Organization Information
| Field Name                  | Field Type    | Description                    |
|-----------------------------|---------------|--------------------------------|
| organization_name          | Text          | Company/organization name      |
| organization_name_url      | URL           | Organization profile URL       |
| company_name_for_emails    | Text          | Email domain company           |
| website                    | URL           | Company website                |
| organization_linkedin_url  | URL           | Company LinkedIn URL           |
| facebook_url              | URL           | Company Facebook URL           |
| twitter_url               | URL           | Company Twitter URL            |

### Business Details
| Field Name          | Field Type    | Description                    |
|---------------------|---------------|--------------------------------|
| industries          | Text          | Business industries            |
| technologies        | Text          | Technologies used              |
| keywords           | Text          | Business keywords/tags         |
| employees          | Number        | Number of employees            |
| headquarters_location | Text        | HQ location                    |

### Organization Address
| Field Name                    | Field Type    | Description                    |
|-------------------------------|---------------|--------------------------------|
| organization_street_address   | Long text     | Company street address         |
| organization_city            | Text          | Company city                   |
| organization_state           | Text          | Company state/province         |
| organization_country         | Text          | Company country                |
| organization_postal_code     | Text          | Company ZIP/postal code        |
| company_phone               | Phone number  | Company main phone             |

### Additional Details
| Field Name              | Field Type    | Description                    |
|-------------------------|---------------|--------------------------------|
| job_time_period         | Text          | Employment duration            |
| founded_year           | Number        | Company founding year          |
| description            | Long text     | Job/role description           |
| full_description       | Long text     | Detailed description           |
| account_owner          | Text          | Account manager/owner          |
| cb_rank_company        | Number        | Crunchbase company rank        |
| estimated_revenue_range | Text         | Revenue range estimate         |

## ⚡ Quick Setup:

For each field:
1. Click **"+ Add Field"**
2. Enter the **Field Name** (exact spelling)
3. Select the **Field Type** 
4. Click **"Create Field"**

## 🎯 After Creating Fields:

Run this command to verify all fields are created:
```bash
python3 -c "
from baserow_integration import BaserowIntegration
integration = BaserowIntegration()
integration.authenticate('http://localhost:8080', '8qTh3TSwAHVoEQGE7C11YQsKxTpcWfoD', '698')
fields = integration.get_table_fields()
print(f'Total fields: {len(fields)}')
for name, type in fields.items():
    print(f'✓ {name} ({type})')
"
```

## ✅ Expected Result:
You should have **41 total fields** (including the existing "Name" field)

## 🎯 Field Type Reference:
- **Text**: Short text fields (names, titles, etc.)
- **Long text**: Multi-line text (descriptions, bios, etc.) 
- **Email**: Email addresses with validation
- **Phone number**: Phone numbers with formatting
- **URL**: Website URLs with validation
- **Number**: Numeric values (employee count, years, etc.)

Once all 40 CRM fields are created, your consolidated marketing data will export perfectly to Baserow! 🚀
