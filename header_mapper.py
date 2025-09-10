from fuzzywuzzy import fuzz
import re
from typing import Dict, List, Tuple

class HeaderMapper:
    def __init__(self):
        # Exact 39 headers required for marketing/advertising company
        self.required_headers = [
            "first_name", "last_name", "full_name", "email", "phone_numbers", 
            "linkedin_url", "account_linkedin", "headline", "title", "designation", 
            "about", "skills", "contact_city", "contact_state", "contact_country", 
            "organization_name", "organization_name_url", "company_name_for_emails", 
            "website", "organization_linkedin_url", "facebook_url", "twitter_url", 
            "industries", "technologies", "keywords", "employees", "headquarters_location", 
            "organization_street_address", "organization_city", "organization_state", 
            "organization_country", "organization_postal_code", "company_phone", 
            "job_time_period", "founded_year", "description", "full_description", 
            "account_owner", "cb_rank_company", "estimated_revenue_range"
        ]
        
        # Comprehensive mapping patterns for all possible header variations
        self.header_mapping_patterns = {
            # Name fields - extensive variations
            'first_name': [
                'first_name', 'firstname', 'fname', 'f_name', 'first', 'given_name', 'forename', 'fore_name',
                'name', 'candidate_first_name', 'customer_first_name', 'contact_first_name', 'employee_first_name',
                'f. name', 'f.', 'fn', 'person_name', 'member_first_name', 'client_first_name', 'student_first_name',
                'lead_first_name', 'prospect_first_name', 'user_first_name', 'applicant_first_name', 'donor_first_name',
                'visitor_first_name', 'subscriber_first_name', 'participant_first_name', 'attendee_first_name',
                'given', 'christian_name', 'personal_name'
            ],
            
            'last_name': [
                'last_name', 'lastname', 'lname', 'l_name', 'last', 'surname', 'family_name', 'sur_name',
                'candidate_last_name', 'customer_last_name', 'contact_last_name', 'employee_last_name',
                'l. name', 'l.', 'ln', 'member_last_name', 'client_last_name', 'student_last_name',
                'lead_last_name', 'prospect_last_name', 'user_last_name', 'applicant_last_name', 'donor_last_name',
                'visitor_last_name', 'subscriber_last_name', 'participant_last_name', 'attendee_last_name',
                'family', 'paternal_name'
            ],
            
            'full_name': [
                'full_name', 'fullname', 'name', 'complete_name', 'person_name', 'contact_name', 'full name',
                'candidate_name', 'customer_name', 'client_name', 'employee_name', 'member_name', 'student_name',
                'lead_name', 'prospect_name', 'user_name', 'applicant_name', 'donor_name', 'visitor_name',
                'subscriber_name', 'participant_name', 'attendee_name', 'display_name', 'preferred_name',
                'legal_name', 'official_name', 'registered_name', 'person', 'individual', 'contact'
            ],
            
            # Contact fields - comprehensive variations
            'email': [
                'email', 'email_address', 'e_mail', 'e-mail', 'mail', 'contact_email', 'email_id', 'e_mail_address',
                'primary_email', 'business_email', 'work_email', 'personal_email', 'main_email', 'email1',
                'candidate_email', 'customer_email', 'client_email', 'employee_email', 'member_email',
                'lead_email', 'prospect_email', 'user_email', 'applicant_email', 'subscriber_email',
                'contact_email_address', 'electronic_mail', 'mail_id', 'email_addr', 'em', 'mailto'
            ],
            
            'phone_numbers': [
                'phone_numbers', 'phone', 'phone_number', 'telephone', 'tel', 'mobile', 'cell', 'contact_number',
                'phone_no', 'tel_no', 'mobile_number', 'cell_phone', 'cellular', 'phone1', 'primary_phone',
                'business_phone', 'work_phone', 'office_phone', 'home_phone', 'personal_phone', 'main_phone',
                'candidate_phone', 'customer_phone', 'client_phone', 'employee_phone', 'member_phone',
                'lead_phone', 'prospect_phone', 'user_phone', 'applicant_phone', 'contact_phone',
                'telephone_number', 'mobile_no', 'cell_no', 'ph', 'phone #', 'tel #', 'contact #'
            ],
            
            # Professional fields - extensive variations
            'linkedin_url': [
                'linkedin_url', 'linkedin', 'linkedin_profile', 'li_url', 'linkedin_link', 'linkedin_page',
                'linkedIn', 'linked_in', 'linkedin_profile_url', 'linkedin_account', 'li_profile',
                'linkedin_handle', 'linkedin_username', 'professional_profile', 'linkedin_id',
                'linkedin.com', 'in/', 'linkedin_address', 'social_linkedin', 'li_link'
            ],
            
            'account_linkedin': [
                'account_linkedin', 'linkedin_account', 'li_account', 'linkedin_username', 'linkedin_handle',
                'linkedin_id', 'professional_account', 'business_linkedin', 'work_linkedin'
            ],
            
            'headline': [
                'headline', 'professional_headline', 'tagline', 'summary_line', 'bio_headline', 'profile_headline',
                'job_headline', 'career_headline', 'professional_summary', 'brief_summary', 'one_liner',
                'elevator_pitch', 'profile_tagline', 'professional_tagline', 'summary', 'intro'
            ],
            
            'title': [
                'title', 'job_title', 'position', 'role', 'designation', 'job_position', 'current_title',
                'professional_title', 'work_title', 'employment_title', 'position_title', 'job_role',
                'current_position', 'current_role', 'occupation', 'function', 'post', 'rank'
            ],
            
            'designation': [
                'designation', 'job_designation', 'position_title', 'rank', 'level', 'grade', 'position_level',
                'job_level', 'seniority', 'hierarchy', 'job_grade', 'position_rank'
            ],
            
            'about': [
                'about', 'bio', 'biography', 'profile_summary', 'personal_summary', 'description',
                'profile_description', 'about_me', 'personal_bio', 'background', 'profile',
                'summary', 'overview', 'introduction', 'personal_info', 'details', 'info'
            ],
            
            'skills': [
                'skills', 'skill_set', 'competencies', 'expertise', 'abilities', 'capabilities',
                'technical_skills', 'professional_skills', 'core_skills', 'key_skills',
                'specializations', 'proficiencies', 'talents', 'strengths', 'qualifications'
            ],
            
            # Location fields - comprehensive variations
            'contact_city': [
                'contact_city', 'city', 'location_city', 'person_city', 'current_city', 'residence_city',
                'home_city', 'living_city', 'based_in', 'located_in', 'town', 'municipality',
                'urban_area', 'locality', 'place', 'location'
            ],
            
            'contact_state': [
                'contact_state', 'state', 'location_state', 'person_state', 'current_state', 'residence_state',
                'home_state', 'province', 'region', 'territory', 'area', 'district'
            ],
            
            'contact_country': [
                'contact_country', 'country', 'location_country', 'person_country', 'current_country',
                'residence_country', 'home_country', 'nation', 'nationality', 'country_code',
                'geographic_location', 'region_country'
            ],
            
            # Organization fields - extensive variations
            'organization_name': [
                'organization_name', 'company', 'company_name', 'employer', 'organization', 'org_name',
                'business_name', 'firm', 'corporation', 'enterprise', 'workplace', 'current_company',
                'current_employer', 'work_company', 'business', 'company_employer', 'org',
                'corporate_name', 'entity', 'institution', 'establishment'
            ],
            
            'organization_name_url': [
                'organization_name_url', 'company_url', 'org_url', 'organization_url', 'employer_url',
                'company_link', 'organization_link', 'business_url', 'corporate_url'
            ],
            
            'company_name_for_emails': [
                'company_name_for_emails', 'company_domain', 'email_company', 'email_domain',
                'organization_domain', 'business_domain', 'corporate_domain', 'work_domain'
            ],
            
            'website': [
                'website', 'company_website', 'web_site', 'url', 'domain', 'homepage', 'web_address',
                'site', 'web_url', 'company_site', 'business_website', 'corporate_website',
                'organization_website', 'web_page', 'online_presence', 'www'
            ],
            
            'organization_linkedin_url': [
                'organization_linkedin_url', 'company_linkedin', 'org_linkedin', 'business_linkedin',
                'corporate_linkedin', 'organization_linkedin', 'company_linkedin_url',
                'employer_linkedin', 'workplace_linkedin'
            ],
            
            'facebook_url': [
                'facebook_url', 'facebook', 'fb_url', 'facebook_page', 'fb_page', 'facebook_profile',
                'facebook_link', 'fb_link', 'social_facebook', 'facebook_account'
            ],
            
            'twitter_url': [
                'twitter_url', 'twitter', 'twitter_handle', 'twitter_profile', 'twitter_account',
                'twitter_username', 'twitter_link', 'social_twitter', 'tweet_handle', 'x_url', 'x_handle'
            ],
            
            # Business fields - comprehensive variations
            'industries': [
                'industries', 'industry', 'sector', 'business_type', 'vertical', 'market',
                'business_sector', 'industry_type', 'field', 'domain', 'category',
                'business_category', 'market_sector', 'industry_vertical'
            ],
            
            'technologies': [
                'technologies', 'tech_stack', 'technology', 'tools', 'software', 'platforms',
                'technical_tools', 'tech_tools', 'systems', 'applications', 'programming_languages',
                'frameworks', 'development_tools', 'tech_skills'
            ],
            
            'keywords': [
                'keywords', 'tags', 'key_words', 'search_terms', 'labels', 'categories',
                'topics', 'subjects', 'themes', 'descriptors', 'identifiers'
            ],
            
            'employees': [
                'employees', 'employee_count', 'company_size', 'staff_count', 'workforce',
                'headcount', 'team_size', 'personnel_count', 'staff_size', 'number_of_employees',
                'employee_size', 'organization_size', 'manpower'
            ],
            
            'headquarters_location': [
                'headquarters_location', 'headquarters', 'hq_location', 'main_office', 'head_office',
                'corporate_headquarters', 'hq', 'primary_location', 'main_location',
                'corporate_office', 'home_office'
            ],
            
            # Address fields - extensive variations
            'organization_street_address': [
                'organization_street_address', 'street_address', 'address', 'office_address',
                'business_address', 'company_address', 'corporate_address', 'work_address',
                'physical_address', 'mailing_address', 'street', 'addr', 'location_address'
            ],
            
            'organization_city': [
                'organization_city', 'company_city', 'office_city', 'org_city', 'business_city',
                'corporate_city', 'work_city', 'headquarters_city'
            ],
            
            'organization_state': [
                'organization_state', 'company_state', 'office_state', 'org_state', 'business_state',
                'corporate_state', 'work_state', 'headquarters_state'
            ],
            
            'organization_country': [
                'organization_country', 'company_country', 'office_country', 'org_country',
                'business_country', 'corporate_country', 'work_country', 'headquarters_country'
            ],
            
            'organization_postal_code': [
                'organization_postal_code', 'postal_code', 'zip_code', 'zipcode', 'zip',
                'company_zip', 'office_zip', 'business_zip', 'postcode', 'postal'
            ],
            
            'company_phone': [
                'company_phone', 'office_phone', 'business_phone', 'org_phone', 'corporate_phone',
                'work_phone', 'organization_phone', 'headquarters_phone', 'main_phone'
            ],
            
            # Timeline and details - comprehensive variations
            'job_time_period': [
                'job_time_period', 'employment_period', 'tenure', 'work_period', 'duration',
                'employment_duration', 'job_duration', 'time_at_company', 'years_of_service',
                'service_period', 'work_tenure', 'employment_span'
            ],
            
            'founded_year': [
                'founded_year', 'founded', 'establishment_year', 'year_founded', 'established',
                'incorporation_year', 'startup_year', 'creation_year', 'launch_year',
                'founding_date', 'established_date', 'inception_year'
            ],
            
            'description': [
                'description', 'job_description', 'role_description', 'summary', 'details',
                'job_summary', 'position_summary', 'role_summary', 'responsibilities',
                'job_details', 'work_description', 'duties'
            ],
            
            'full_description': [
                'full_description', 'detailed_description', 'complete_description',
                'comprehensive_description', 'long_description', 'extended_description'
            ],
            
            'account_owner': [
                'account_owner', 'owner', 'account_manager', 'assigned_to', 'responsible_person',
                'contact_owner', 'lead_owner', 'sales_owner', 'account_rep', 'rep'
            ],
            
            'cb_rank_company': [
                'cb_rank_company', 'company_rank', 'cb_rank', 'crunchbase_rank',
                'startup_rank', 'business_rank', 'market_rank'
            ],
            
            'estimated_revenue_range': [
                'estimated_revenue_range', 'revenue', 'revenue_range', 'annual_revenue',
                'yearly_revenue', 'sales', 'turnover', 'income', 'earnings',
                'financial_size', 'revenue_size', 'business_size'
            ]
        }
        
        self.custom_mappings = {}
        
    def normalize_header(self, header: str) -> str:
        """Normalize header by removing special characters and converting to lowercase"""
        return re.sub(r'[^a-zA-Z0-9]', '_', str(header).lower().strip())
    
    def find_best_match(self, header: str, threshold: int = 80) -> Tuple[str, int]:
        """Find the best matching standard header using fuzzy matching"""
        normalized_header = self.normalize_header(header)
        
        # Check custom mappings first
        if normalized_header in self.custom_mappings:
            return self.custom_mappings[normalized_header], 100
            
        best_match = None
        best_score = 0
        best_standard = None
        
        # Check exact matches first
        for standard_header in self.required_headers:
            if normalized_header == self.normalize_header(standard_header):
                return standard_header, 100
        
        # Check pattern matches
        for standard_header, variations in self.header_mapping_patterns.items():
            for variation in variations:
                score = fuzz.ratio(normalized_header, self.normalize_header(variation))
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = variation
                    best_standard = standard_header
                    
        # If no good match found, return None to indicate unmapped header
        return best_standard if best_match else None, best_score
    
    def map_headers(self, headers: List[str]) -> Dict[str, str]:
        """Map a list of headers to standardized versions"""
        mapping = {}
        for header in headers:
            standard_header, _ = self.find_best_match(header)
            mapping[header] = standard_header
            
        return mapping
    
    def add_custom_mapping(self, original: str, standard: str):
        """Add a custom header mapping"""
        normalized = self.normalize_header(original)
        self.custom_mappings[normalized] = standard
        
    def get_mapping_suggestions(self, headers: List[str]) -> Dict[str, List[Tuple[str, int]]]:
        """Get top 3 suggestions for each header"""
        suggestions = {}
        
        for header in headers:
            normalized_header = self.normalize_header(header)
            candidates = []
            
            # Check against all required headers and their patterns
            for standard_header in self.required_headers:
                # Direct match with standard header
                score = fuzz.ratio(normalized_header, self.normalize_header(standard_header))
                candidates.append((standard_header, score))
                
                # Match with variations if they exist
                if standard_header in self.header_mapping_patterns:
                    for variation in self.header_mapping_patterns[standard_header]:
                        score = fuzz.ratio(normalized_header, self.normalize_header(variation))
                        candidates.append((standard_header, score))
                    
            # Sort by score, remove duplicates, and get top 5
            candidates = list(set(candidates))  # Remove duplicates
            candidates.sort(key=lambda x: x[1], reverse=True)
            suggestions[header] = candidates[:5]  # Show top 5 matches
            
        return suggestions
    
    def get_required_headers(self) -> List[str]:
        """Return the list of required headers"""
        return self.required_headers.copy()