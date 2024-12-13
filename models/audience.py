from typing import Optional, List, Any
from pydantic import BaseModel

class AudienceResponse(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    name: Optional[str] = None
    linkedin_url: Optional[str] = None
    title: Optional[str] = None
    email_status: Optional[str] = None
    photo_url: Optional[str] = None
    twitter_url: Optional[str] = None
    github_url: Optional[str] = None
    facebook_url: Optional[str] = None
    extrapolated_email_confidence: Optional[float] = 0.0
    headline: Optional[str] = None
    email: Optional[str] = None
    employment_history: Any= None
    state: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    is_likely_to_engage: Optional[bool] = None
    departments: Optional[List[str]] = None
    subdepartments: Optional[List[str]] = None
    seniority: Optional[str] = None
    functions: Optional[List[str]] = None
    phone_numbers: Optional[List] = None
    intent_strength: Optional[str] = None
    show_intent: Optional[bool] = None
    revealed_for_current_team: Optional[bool] = None
    funding_info: Optional[dict] = None
    company_linkedin_url: Optional[str] = None
    company_website_url: Optional[str] = None
    company_description: Optional[Any] = None
    company:Optional[str]=None
    technologies:Optional[str]=None


class AudienceRequest(BaseModel):
    user_id:Optional[str]=None
    q_organization_domains: Optional[str] = None
    page: Optional[int] = 1
    per_page: Optional[int] = 5
    organization_locations: Optional[list[str]] = None
    person_seniorities: Optional[list[str]] = None
    organization_num_employees_ranges: Optional[list[str]] = None
    person_titles: Optional[list[str]] = None
    organization_industry_tag_ids: Optional[list[str]] = None
    contact_email_status: list[str] = ["verified"]
    organization_latest_funding_stage_cd: Optional[list[str]] = None
    currently_using_any_of_technology_uids: Optional[list[str]] = None
    revenue_range: Optional[dict[str, str]] = None
    organization_job_locations: Optional[dict[str, str]] = None
    q_organization_keyword_tags: Optional[list[str]] = None
    q_organization_job_titles: Optional[List[str]] = None

    def to_req(self):
        request_dict = self.model_dump()
        if request_dict['q_organization_domains'] == None:
            del request_dict['q_organization_domains']
        if request_dict['organization_latest_funding_stage_cd'] == None:
            del request_dict['organization_latest_funding_stage_cd']
        if request_dict['currently_using_any_of_technology_uids'] == None:
            del request_dict['currently_using_any_of_technology_uids']
        if request_dict['organization_job_locations'] == None:
            del request_dict['organization_job_locations']
        if request_dict['q_organization_job_titles'] == None:
            del request_dict['q_organization_job_titles']
        return request_dict